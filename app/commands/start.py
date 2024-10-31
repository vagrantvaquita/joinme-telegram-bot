from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from app.webapp import CREATE_EVENT_URL, LIST_EVENTS_URL, LIST_MYEVENTS_URL

start_command = Router()


@start_command.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=(
            "Ready to connect with awesome people and discover fun events? You've got two options:\n\n"
            "<b>1️⃣ Create an Event</b>: Got something in mind? Start your own event, share the details, and invite others to join in the fun!\n"
            "<b>2️⃣ Find an Event</b>: Looking for something to do? Browse upcoming events and find the perfect one to join. Meet new people, make memories!\n\n"
            "Choose an option below 👇 and let's get started!"
        ),
        reply_markup=InlineKeyboardMarkup(
            resize_keyboard=True,
            is_persistent=False,
            one_time_keyboard=False,
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Create event", web_app=WebAppInfo(url=CREATE_EVENT_URL)
                    ),
                    InlineKeyboardButton(
                        text="📌 Find event", web_app=WebAppInfo(url=LIST_EVENTS_URL)
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="✏️ See my events",
                        web_app=WebAppInfo(url=LIST_MYEVENTS_URL),
                    ),
                ],
            ],
        ),
    )
