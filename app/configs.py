import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("TELEGRAM_WEBAPP_URL")
CONFIG_BOT = DefaultBotProperties(parse_mode=ParseMode.HTML)
