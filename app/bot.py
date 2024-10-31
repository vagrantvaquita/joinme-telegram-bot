from aiogram import Bot, Dispatcher

from app.commands.delete import delete_command
from app.commands.start import start_command
from app.configs import CONFIG_BOT, TOKEN

dp = Dispatcher()
dp.include_routers(start_command, delete_command)
bot = Bot(token=TOKEN, default=CONFIG_BOT)
