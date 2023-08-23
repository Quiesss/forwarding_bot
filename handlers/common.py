from typing import List

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio

from conf import bot, CHAT_ID_TO_SEND

router = Router()


@router.message(F.reply_to_message & ~F.chat.type.in_({"private"}))
async def from_chat_to_user(message: Message):
    if message.reply_to_message:
        if message.reply_to_message.forward_from:
            to_user = message.reply_to_message.forward_from.id
        elif '|' in message.reply_to_message.text:
            to_user = message.reply_to_message.text.split('|')[1].strip()
        else:
            return message.answer('Не могу отправить пользователю личное сообщение. Либо он скрыт,'
                                  ' либо вы ответили не на то сообщение')
        if message.text == 'я':
            await bot.send_message(
                to_user,
                f'Ваше тз принял в работу @{message.from_user.username}'
            )
        else:
            await bot.send_message(
                to_user,
                message.text
            )


@router.message(F.media_group_id)
async def handle_albums(message: Message, album: List[Message]):
    """This handler will receive a complete album of any type."""
    group_elements = []
    for element in album:
        caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}
        if element.photo:
            input_media = InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs, parse_mode=None)
        elif element.video:
            input_media = InputMediaVideo(media=element.video.file_id, **caption_kwargs, parse_mode=None)
        elif element.document:
            input_media = InputMediaDocument(media=element.document.file_id, **caption_kwargs, parse_mode=None)
        elif element.audio:
            input_media = InputMediaAudio(media=element.audio.file_id, **caption_kwargs)
        else:
            return message.answer("This media type isn't supported!")

        group_elements.append(input_media)
    username = message.from_user.username if message.from_user.username else 'unknown'
    await message.reply('Отправил, ожидайте')
    await bot.send_message(
        CHAT_ID_TO_SEND,
        text=f'Сообщение от @{username} ({message.from_user.full_name}) | {message.from_user.id}', parse_mode=None
    )
    return await bot.send_media_group(CHAT_ID_TO_SEND, media=group_elements)


@router.message(Command(commands=['help']))
async def cmd_start(message: Message):
    return message.answer(
        '<b>Команды по работе с потоками:</b> \n\n'
        '<code>/get partner offer_name country keitaro</code> \n\n'
        '<code>/add partner offer_name country keitaro </code>\n\n'
        '<code>/del stream_id </code>\n\n'
        'Для автонастройки, напишите маленькими буквами требуемую ПП (напр. shakes, everad), '
        'далее заполните полученный шаблон и отправьте файлы вместе с ТЗ'
    )


@router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    pin = await message.answer('‼️Отправляйте сюда свое тз в строго следующем формате: \n\n'
                               '<b>Гео</b> - 2 буквенный формат (ES, FR, PT)\n'
                               '<b>Метка</b> - Цифра + 1 буква имени/гео/оффер (14K/ES/W-loss) \n'
                               '<b>Оффер</b> - полное название оффера или ссылка на оффер \n'
                               '<b>Код доступа</b> - ваш личный код cobeklo или прочерк, '
                               'если нужно настроить на льющиеся ссылки \n\n'
                               '<b>Гео: \n'
                               'Название ПП: \n'
                               'Метка: \n'
                               'Код доступа: \n'
                               'Оффер: \n'
                               'Комментарии: \n'
                               'КТ: \n'
                               'Тематика: </b>'
                               )
    await bot.unpin_all_chat_messages(chat_id=message.chat.id)
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=pin.message_id)


@router.message(F.chat.type.in_({"private"}), ~F.content_type.in_({'pinned_message'}))
async def handle_text(message: Message):
    await message.reply('Отправил, ожидайте')
    return await message.forward(CHAT_ID_TO_SEND)
