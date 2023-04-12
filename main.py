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


# def update_zip(zip_name, filename, data):
#     # generate a temp file
#     tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zip_name))
#     os.close(tmpfd)
#
#     # create a temp copy of the archive without filename
#     with zipfile.ZipFile(zip_name, 'r') as zin:
#
#         with zipfile.ZipFile(tmpname, 'w') as zout:
#             zout.comment = zin.comment  # preserve the comment
#             for item in zin.infolist():
#                 print(item.filename)
#                 if item.filename.split('/')[-1] not in ['index.php', 'index.html']:
#                     zout.writestr(item, zin.read(item.filename))
#                 else:
#                     index_path = item.filename
#
#     # replace with the temp archive
#     os.remove(zip_name)
#     os.rename(tmpname, zip_name)
#     if 'index_path' in locals():
#         # now add filename with its new data
#         with zipfile.ZipFile(zip_name, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
#             zf.writestr(index_path, data)
#     else:
#
#
# @dp.message(F.document)
# async def test(message: Message):
#     file = await bot.get_file(message.document.file_id)
#     file_name = message.document.file_name
#     name_split = message.document.file_name.split('.')
#     original_name = name_split[0] if len(name_split) == 2 else ''
#     uniq_name = str(uuid.uuid4()) + '.zip'
#     await bot.download_file(file.file_path, file_name)
#
#     update_zip(file_name, 'index.php', 'test')
#
#     new_file = FSInputFile(file_name, file_name)
#     await message.answer_document(new_file)

    # exit()
    # with zipfile.ZipFile(uniq_name, 'a') as archive:
    #     # archive.write('order.php', original_name + '/order.php')
    #     count = len(list(zipfile.Path(uniq_name).iterdir()))
    #     if count <= 3:
    #         path_php = archive.filelist[0].filename + 'index.php'
    #         path_html = archive.filelist[0].filename + 'index.html'
    #     else:
    #         path_php = 'index.php'
    #         path_html = 'index.html'
    #     try:
    #         index_file = archive.read(path_php)
    #         path = path_php
    #     except KeyError:
    #         index_file = archive.read(path_html)
    #         path = path_html
    #
    #     soup = BeautifulSoup(index_file, 'html.parser')
    #     soup.head.append('TEST APPEND HEAD')
    #
    #     new_file = FSInputFile(uniq_name, uniq_name)
    #     await message.answer_document(new_file)
    #
    # os.remove(uniq_name)

@dp.message(F.reply_to_message & ~F.chat.type.in_({"private"}))
async def from_chat_to_user(message: Message):
    print(message.chat.id)
    if message.reply_to_message:
        if message.reply_to_message.forward_from:
            to_user = message.reply_to_message.forward_from.id
        elif '|' in message.reply_to_message.text:
            to_user = message.reply_to_message.text.split('|')[1].strip()
        else:
            to_user = CHAT_ID_TO_SEND
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
                               'Название ПП: \n'
                               'Метка: \n'
                               'Оффер: \n'
                               'Комментарии: \n'
                               'КТ:</b>')
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
    await bot.send_message(
        CHAT_ID_TO_SEND,
        text=f'Сообщение от @{username} ({message.from_user.full_name}) | {message.from_user.id}', parse_mode=None
    )
    return await bot.send_media_group(CHAT_ID_TO_SEND, media=group_elements)


@dp.message(F.chat.type.in_({"private"}), ~F.content_type.in_({'pinned_message'}))
async def handle_text(message: Message):
    await message.reply('Отправил, ожидайте')
    return await message.forward(CHAT_ID_TO_SEND)


if __name__ == "__main__":
    dp.message.middleware(MediaGroupMiddleware())
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
