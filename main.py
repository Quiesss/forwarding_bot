import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union

from aiogram.fsm.storage.memory import MemoryStorage

from conf import DEFAULT_DELAY, bot
from handlers import common, autotune, streamService

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import (
    Message,
    TelegramObject
)


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


async def send():
    await bot.send('460956316', 'bot is stopped')


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(MediaGroupMiddleware())

    dp.include_router(streamService.router)
    dp.include_router(autotune.router)
    dp.include_router(common.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
