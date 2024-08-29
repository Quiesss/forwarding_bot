import os
import tempfile
import traceback
import uuid
import zipfile
from typing import List

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from conf import bot
from processing.Partners import get_partner_params
from processing.product.Product import product_img_names
from treatment import parse_conf, IndexParse, make_order_file

router = Router()


@router.message(F.text.in_(get_partner_params()))
async def get_partner_ta(message: Message):
    params = ': \n'.join(get_partner_params(message.text))
    await message.answer(
        f'''
<b>Шаблон тз для {message.text}</b> \n
<code>partner: {message.text}
cobeklo: 
{params}: 
sub2: 
success: 
product: 
lang: 
op/minfobiz: 
</code>
        ''')


@router.message(F.text == 'ta')
async def get_ta(message: Message):
    return message.answer(
        '''
<b>Вот что можно указать в тз:</b> \n
<code>cobeklo:</code> d3f3ed212 (without brackets)\n
<code>mask:</code> +8 999 8934234 (маска номера телефона)\n
<code>anchor:</code> #form (Селектор (#form, .toscroll и тд, к которому нужно проскролить)\n 
<code>anti_d:</code> 1 (антидубль, по кукам)\n
<code>country:</code> ES\n 
<code>op:</code> 9M (домонетка OneProfit, писать цифру + первую букву)\n
<code>minfobiz:</code> ES (писать гео, 2 буквы)\n 
<code>a:</code> {offer} (на что поменять ссылки в тегах "a", можно не указывать, тогда просто очистит)\n
<code>Шаблон:</code> 
<code>
cobeklo: 
anti_d
anchor: #form
validator
</code>
        ''')


async def update_zip(zip_name, filename, conf: dict):
    msg = []
    # product_name = 'product.png'
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zip_name))
    os.close(tmpfd)
    # create a temp copy of the archive without filename
    with zipfile.ZipFile(zip_name, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment  # preserve the comment
            for item in zin.infolist():
                curr_file = item.filename.split('/')[-1]
                # if curr_file.split('.')[0] in product_img_names:
                #     product_name = curr_file
                #     continue
                try:
                    c_filename = item.filename.encode('cp437').decode('utf-8')
                except UnicodeDecodeError:
                    c_filename = item.filename
                if curr_file == 'order.php':
                    continue
                if curr_file not in ['index.php', 'index.html', 'order.php']:
                    zout.writestr(c_filename, zin.read(item.filename))
                else:
                    index_path = c_filename
                    try:
                        new_index = IndexParse(zin.read(item.filename), conf, msg).tuning()
                    except Exception as e:
                        msg.append(('Ошибка: ' + str(e)))
                        print(traceback.format_exc())  # debugging line
                        return msg
    os.remove(zip_name)
    os.rename(tmpname, zip_name)
    if 'index_path' in locals():
        # now add a filename with its new data
        with zipfile.ZipFile(zip_name, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
            path = index_path.split('/')
            if len(path) > 1:
                main_folder = '/'.join(path[:-1]) + '/'
            else:
                main_folder = ''
            # if conf.get('partner'):
            #     zf.writestr(main_folder + 'order.php', make_order_file(conf, msg))
            #     msg.append('✅Настройка ордер файла')
            # else:
            #     msg.append('❌Ордер файл не настроен, не нашел в тз параметр partner')

            # if conf.get('product'):
            #     prod = conf.get('product') + '.png'
            # if os.path.isfile(f'./processing/product/img/{prod}'):
            # zf.write(f'./processing/product/img/{prod}', main_folder + product_name)
            # msg.append('✅Добавил изображение оффера')
            # else:
            #     msg.append('❌Не нашел изображения для этого оффера или подходящего файла')

            zf.writestr(index_path, str(new_index))
            return msg
    else:
        return False


@router.message(F.document | F.media_group_id, F.from_user.id.in_({460956316, 5215165553}))
async def update_index(message: Message, album: List[Message] = None):
    if not message.caption and not album and not message.document.file_id:
        return await message.answer('Не понял что нужно сделать, пришлите ТЗ')
    if album is not None:
        conf = parse_conf(album[-1].caption)
        caption = []
        file_names = []

        for element in album:
            if element.document:
                curr_file = await bot.get_file(element.document.file_id)
                curr_name = element.document.file_name
                file_names.append(str(uuid.uuid4()) + '.zip')
                await bot.download_file(curr_file.file_path, file_names[-1])
                result_msg = await update_zip(file_names[-1], 'index.php', conf)
                caption.append('\n'.join(result_msg))
                # caption_kwargs = {"caption": '\n'.join(res)}
                new_file = FSInputFile(file_names[-1], curr_name)
                # If sending lends in one message
                # input_media = InputMediaDocument(media=new_file, parse_mode=None)
                # group_elements.append(input_media)
                await message.answer_document(new_file, caption='\n'.join(result_msg))

        # res_capture = '\n\n'.join(caption)
        # if len(caption) > 200:
        #     await message.answer(res_capture)
        # else:
        #     group_elements[0].caption = res_capture
        # await message.answer_media_group(media=group_elements)
        for path in file_names:
            os.remove(path)
        return

    conf = parse_conf(message.caption)
    file = await bot.get_file(message.document.file_id)
    file_name = message.document.file_name
    uniq_name = str(uuid.uuid4()) + '.zip'
    await bot.download_file(file.file_path, uniq_name)
    res = await update_zip(uniq_name, 'index.php', conf)
    new_file = FSInputFile(uniq_name, file_name)
    await message.answer_document(new_file, caption='\n'.join(res))
    os.remove(uniq_name)
