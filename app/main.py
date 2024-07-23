import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.create_event import create_router
from handlers.find_event import find_router
from handlers.start import start_router

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CONFIG = DefaultBotProperties(parse_mode=ParseMode.HTML)


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(start_router, create_router, find_router)
    bot = Bot(token=TOKEN, default=CONFIG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
