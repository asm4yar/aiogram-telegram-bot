import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import misc
from config import BOT_TOKEN
from handlers import routers
from handlers.error_handlers import global_error_handler


async def start_bot():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN,
        )
    )
    dp = Dispatcher()
    dp.errors.register(global_error_handler)

    dp.startup.register(misc.on_start)
    dp.shutdown.register(misc.on_shutdown)
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
