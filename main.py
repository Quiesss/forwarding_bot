import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union

from aiogram import BaseMiddleware, Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
    TelegramObject,
)

DEFAULT_DELAY = 0.6
CHAT_ID_TO_SEND = '-1001895213515'

bot = Bot("5889492973:AAHI1vdaIXv3H1lmPacgnHQThO49vHLBfDo", parse_mode="HTML")
dp = Dispatcher()


class MediaGroupMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return  # Don't propagate the event
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)


@dp.message(F.reply_to_message)
async def test(message: Message):
    if message.reply_to_message:
        to_user = message.reply_to_message.forward_from.id if message.reply_to_message.forward_from else \
        message.reply_to_message.text.split('|')[1].strip()
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


@dp.message(Command(commands=['start']))
async def cmd_start(message: Message):
    pin = await message.answer('‼️Отправляйте сюда свое тз в строго следующем формате: \n\n'
                               '<b>Гео: \n'
                               'Название ПП и Email каба: \n'
                               'Поток из ПП: \n'
                               'Ваш порядковый номер: \n'
                               'Комментарии: \n'
                               'Домонетка:</b>')
    await bot.unpin_all_chat_messages(chat_id=message.chat.id)
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=pin.message_id)


@dp.message(F.media_group_id)
async def handle_albums(message: Message, album: List[Message]):
    """This handler will receive a complete album of any type."""
    group_elements = []
    for element in album:
        print(element.caption)
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
    await bot.send_message(CHAT_ID_TO_SEND, text=f'Сообщение от @{username}', parse_mode=None)
    return await bot.send_media_group(CHAT_ID_TO_SEND, media=group_elements)


@dp.message(F.chat.type.in_({"private"}), ~F.content_type.in_({'pinned_message'}))
async def handle_text(message: Message):
    await message.reply('Отправил, ожидайте')
    return await message.forward(CHAT_ID_TO_SEND)


if __name__ == "__main__":
    dp.message.middleware(MediaGroupMiddleware())
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
