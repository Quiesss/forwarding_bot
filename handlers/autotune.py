import os
import tempfile
import uuid
import zipfile
import unicodedata
from typing import List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile

from conf import bot
from treatment import parse_conf, IndexParse, make_order_file

router = Router()

UTF8_FLAG = 0x800  # bit 11

def _raw_name_bytes_from_zipinfo(item: zipfile.ZipInfo) -> bytes:
    if (item.flag_bits & UTF8_FLAG) != 0:
        return item.filename.encode('utf-8')
    return item.filename.encode('cp437')

def _decode_zip_name(item: zipfile.ZipInfo) -> str:
    raw = _raw_name_bytes_from_zipinfo(item)
    try:
        return unicodedata.normalize("NFC", raw.decode('utf-8'))
    except UnicodeDecodeError:
        pass
    for enc in ('cp866', 'cp1251'):
        try:
            cand = raw.decode(enc)
            return unicodedata.normalize("NFC", cand)
        except UnicodeDecodeError:
            continue
    return item.filename



async def update_zip(zip_name, filename, conf: dict):
    msg = []
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zip_name))
    os.close(tmpfd)

    decoded_index_path = None

    with zipfile.ZipFile(zip_name, 'r') as zin, \
        zipfile.ZipFile(tmpname, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zout:

        zout.comment = zin.comment
        decoded_index_path = None
        new_index_bytes = None

        for item in zin.infolist():
            data = zin.read(item.filename)
            name_u = _decode_zip_name(item)
            base = name_u.split('/')[-1]

            if base == 'order.php':
                continue

            if base in ('index.php', 'index.html'):
                decoded_index_path = name_u
                try:
                    new_index_bytes = bytes(str(IndexParse(data, conf, msg).tuning()), 'utf-8')
                except Exception as e:
                    msg.append('Ошибка: ' + str(e))
                    return msg
                continue

            zi = zipfile.ZipInfo(filename=name_u, date_time=item.date_time)
            # перетащим важные метаданные
            zi.compress_type  = item.compress_type
            zi.comment        = item.comment
            zi.extra          = item.extra
            zi.internal_attr  = item.internal_attr
            zi.external_attr  = item.external_attr
            zi.create_system  = item.create_system
            zi.create_version = item.create_version
            zi.extract_version= item.extract_version
            # КРИТИЧНО: проставить UTF-8 флаг (zipfile обычно сам поставит для non-ASCII, но явно — надёжней)
            zi.flag_bits = (item.flag_bits | UTF8_FLAG)
            zout.writestr(zi, data)

    # затем дописываем новый index как UTF-8:
    with zipfile.ZipFile(zip_name, 'a', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        out_path = decoded_index_path.replace('.html', '.php')
        zi = zipfile.ZipInfo(filename=out_path)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.flag_bits = UTF8_FLAG
        zf.writestr(zi, new_index_bytes)

                    
    os.remove(zip_name)
    os.rename(tmpname, zip_name)

    if decoded_index_path is not None and new_index_bytes is not None:
        with zipfile.ZipFile(zip_name, mode='a', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
            out_path = decoded_index_path.replace('.html', '.php')
            zi = zipfile.ZipInfo(filename=out_path)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.flag_bits = UTF8_FLAG
            zf.writestr(zi, new_index_bytes)
        msg.append('✅ Заменён index.* и унифицирована кодировка имён (UTF-8)')
        return msg

    return False


# @router.message(F.document | F.media_group_id, F.from_user.id.in_({460956316, 5215165553}))
@router.message(Command(commands=["preland"]), F.document | F.media_group_id)
async def update_index(message: Message, album: List[Message] = None):
    if not message.caption and not album and not message.document.file_id:
        return await message.answer('Не понял что нужно сделать, пришлите ТЗ')
    if album is not None:
        # conf = parse_conf(album[-1].caption)
        params = album[0].caption.split(" ")
        if len(params) != 2:
            return await message.answer(
                '''Невалидный формат команды, укажите в следующем формат \n\n /preland <b>param=code</b>'''
            )
        params = params[1].strip().split("=")
        caption = []
        file_names = []
        await message.answer("Начал обработку " + str(len(album)) + " прелендингов, ожидайте")
        for element in album:
            if element.document:
                curr_file = await bot.get_file(element.document.file_id)
                curr_name = element.document.file_name
                file_names.append(str(uuid.uuid4()) + '.zip')
                await bot.download_file(curr_file.file_path, file_names[-1])
                result_msg = await update_zip(file_names[-1], 'index.php', params)
                caption.append('\n'.join(result_msg))
                # caption_kwargs = {"caption": '\n'.join(res)}
                new_file = FSInputFile(file_names[-1], curr_name)
                # If sending lends in one message
                # input_media = InputMediaDocument(media=new_file, parse_mode=None)
                # group_elements.append(input_media)
                await message.answer_document(new_file, caption='\n'.join(result_msg))
        for path in file_names:
            os.remove(path)
        return

    params = message.caption.split(" ")
    if len(params) != 2:
        return await message.answer(
            "Невалидный формат команды, укажите в следующем формате \n\n <b>/preland param=code</b>"
                                    )
    await message.answer("Начал обработку прелендинга, ожидайте")
    params = params[1].strip().split("=")
    try:
        file = await bot.get_file(message.document.file_id)
    except TelegramBadRequest:
        return await message.answer(
            "‼️Архив слишком большой"
        )
    file_name = message.document.file_name
    uniq_name = str(uuid.uuid4()) + '.zip'
    await bot.download_file(file.file_path, uniq_name)
    res = await update_zip(uniq_name, 'index.php', params)
    with open(uniq_name, 'rb') as f:
        data = f.read()
    safe_name = unicodedata.normalize("NFC", file_name)
    doc = BufferedInputFile(data, filename=safe_name)
    await message.answer_document(doc, caption='\n'.join(res))
    # new_file = FSInputFile(uniq_name, safe_name)
    # await message.answer_document(new_file, caption='\n'.join(res))
    os.remove(uniq_name)
