import asyncio
import logging

from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message

API_TOKEN = '5889492973:AAHI1vdaIXv3H1lmPacgnHQThO49vHLBfDo'

bot = Bot(API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
router = Router()


@router.message(Command(commands=['start']))
async def start_msg(message: Message):
    await message.answer('Отправляйте сюда свое тз в строго следующем формате: \n\n'
                         '<b>Гео: \n'
                         'Название ПП и Email каба: \n'
                         'Поток из ПП:\n'
                         'Ваш порядковый номер: \n'
                         'Комментарии: \n'
                         'Домонетка: </b>\n')


@router.message()
async def forward_message(message: Message):
    await message.forward('-1001895213515')
    await message.reply('Отправил, ожидайте')


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
