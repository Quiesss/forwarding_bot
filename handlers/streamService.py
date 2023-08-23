import json
import os
import sqlite3
import uuid

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from conf import bot
from db.db import DB
from processing.Partners import get_partner_params
from treatment import parse_conf

router = Router()


class AddOffer(StatesGroup):
    add_main_info = State()
    add_json = State()


@router.message(Command("get"))
async def get_stream(message: Message, command: CommandObject):
    query = command.args
    if not query:
        return await message.reply(
            'Чтобы получить информацию о потоке, отправьте команду \n\n '
            '<code>/get partner offer_name country keitaro</code>'
        )

    query = query.strip().split()
    db = DB()
    streams_from_db = db.get_offer(query)

    if len(streams_from_db) == 0:
        return await message.answer('Не нашел потоки по этому запросу')
    if len(streams_from_db) > 6:
        return await message.answer(
            f'В ответе слишком много потоков ({len(streams_from_db)}), уточните запрос, чтобы сократить ответ'
        )

    for stream in streams_from_db:

        stream_data = json.loads(stream[4])
        stream_id = stream[0]
        partner = stream[1]
        offer_name = stream[2]
        country = stream[3]
        json_stream_data = ''
        for k in stream_data:
            json_stream_data += f' ➖ <b>{k}: </b> {stream_data.get(k)}\n'
        keitaro = stream[5]
        image_path = './processing/product/img/' + stream[6] if stream[6] else ''

        msg = f'<b>#:</b> {stream_id}\n' \
              f'<b>ПП:</b> {partner}\n' \
              f'<b>Название оффера:</b> {offer_name}\n' \
              f'<b>Страна:</b> {country}\n' \
              f'<b>Данные потока:</b> \n' \
              f'{json_stream_data} \n' \
              f'<b>Кейтаро:</b> {keitaro}'
        if image_path and os.path.isfile(image_path):
            offer_image = FSInputFile(image_path, filename='product.png')
            if offer_image:
                await message.answer_document(offer_image, caption=msg)
        else:
            await message.answer(msg)


@router.message(Command("add"))
async def add_stream(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if not command.args:
        return await message.answer(
            'Чтобы добавить поток, нужно отправить \n\n <code>/add</code> partner offer_name country keitaro'
        )
    offer_data = command.args.split()
    if len(offer_data) != 4:
        return await message.answer(
            'Чтобы добавить поток, нужно отправить \n\n <code>/add</code> partner offer_name country keitaro'
        )

    partner_param = get_partner_params(offer_data[0].lower().strip())
    if not partner_param:
        return await message.answer('Нет такой ппшки')
    await state.set_state(AddOffer.add_main_info)
    await state.set_data({
        'partner': offer_data[0].strip(),
        'offer_name': offer_data[1].replace('_', ' '),
        'country': offer_data[2].strip(),
        'keitaro': offer_data[3].strip()
    })
    partner_param = ': \n'.join(partner_param)

    await message.answer(
        f'<b>partner:</b> {offer_data[0]}\n'
        f'<b>offer_name:</b> {offer_data[1]}\n'
        f'<b>country:</b> {offer_data[2]}\n'
        f'<b>keitaro:</b> {offer_data[3]} \n\n'
        f'<b>Теперь пришлите фото оффера в формате .png вместе с данными для потока в формате:</b> \n\n'
        f'<code>{partner_param}:\nprice: </code>'
    )


@router.message(Command(commands=['del']))
async def delete_stream_command(message: Message, command: CommandObject):
    stream_id = command.args
    if not stream_id:
        return await message.answer('Не понял команды, для удаления потока напишите \n\n <code>/del stream_id</code>')
    try:
        db = DB()
        delete_stream = db.del_stream(stream_id)
        if delete_stream:
            return await message.answer('✅Успешно удалил поток #' + stream_id)
        else:
            return await message.answer('❌ Не смог удалить поток, возможно его не существует')
    except sqlite3.Error as error:
        await message.answer('Ошибка: ' + error)


@router.message(AddOffer.add_main_info)
async def add_data_to_stream(message: Message, state: FSMContext):
    offer_data = await state.get_data()
    db = DB()

    if message.document:
        json_data = json.dumps(parse_conf(message.caption))
        image = await bot.get_file(message.document.file_id)
        image_path = image.file_path
        new_name = str(uuid.uuid4()) + '.png'
        await bot.download_file(image_path, './processing/product/img/' + new_name)
    else:
        json_data = json.dumps(parse_conf(message.text))
        new_name = None

    is_add = db.add_offer(
        partner=offer_data.get('partner'),
        offer_name=offer_data.get('offer_name'),
        country=offer_data.get('country'),
        data=json_data,
        keitaro=offer_data.get('keitaro'),
        image=new_name
    )

    if is_add:
        answer = f'✅Добавил поток: \n\n' \
                 f'<b>partner:</b> {offer_data.get("partner")}\n' \
                 f'<b>offer_name:</b> {offer_data.get("offer_name")}\n' \
                 f'<b>country:</b> {offer_data.get("country")}\n' \
                 f'<b>keitaro:</b> {offer_data.get("keitaro")} \n'
        if message.document:
            answer += '<b>✅Добавил фото оффера</b>'
        await message.answer(answer)
    else:
        await message.answer(f'Что-то пошло не так: {is_add}')
        await state.clear()
