from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from models.texts import NO, YES

start_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="Create event", callback_data="&event:create"),
            InlineKeyboardButton(text="Find event", callback_data="&event:find"),
        ]
    ]
)

inline_categories_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="⚽ Sports", callback_data="&event_type:⚽ Sports"),
            InlineKeyboardButton(text="✈️ Travel", callback_data="&event_type:✈️ Travel"),
            InlineKeyboardButton(text="🎤 Concerts", callback_data="&event_type:🎤 Concerts"),
        ],
        [
            InlineKeyboardButton(text="🍛 Food/Drink", callback_data="&event_type:🍛 Food/Drink"),
            InlineKeyboardButton(
                text="🎥 Cinema/Theatre", callback_data="&event_type:🎥 Cinema/Theatre"
            ),
            InlineKeyboardButton(text="🎨 Art", callback_data="&event_type:🎨 Art"),
            InlineKeyboardButton(text="🏃 Health", callback_data="&event_type:🏃 Health"),
            InlineKeyboardButton(text="😜 Fun", callback_data="&event_type:😜 Fun"),
        ],
        [
            InlineKeyboardButton(text="✨ Tech/Business", callback_data="&event_type:✨ Tech/Business"),
            InlineKeyboardButton(text="🍑 Horny?", callback_data="&event_type:🍑 Horny?"),
            InlineKeyboardButton(text="Other", callback_data="&event_type:Other"),
        ],
    ],
)

categories_keyboard = ReplyKeyboardBuilder(
    markup=[
        [
            KeyboardButton(text="⚽ Sports"),
            KeyboardButton(text="✈️ Travel"),
            KeyboardButton(text="🎤 Concerts"),
        ],
        [
            KeyboardButton(text="🍛 Food/Drink"),
            KeyboardButton(text="🎥 Cinema/Theatre"),
            KeyboardButton(text="🎨 Art"),
            KeyboardButton(text="🏃 Health"),
            KeyboardButton(text="😜 Fun"),
        ],
        [
            KeyboardButton(text="✨ Tech/Business"),
            KeyboardButton(text="🍑 Horny?"),
            KeyboardButton(text="Other"),
        ],
    ],
)

event_creation_confirmation_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text=YES, callback_data=YES),
            InlineKeyboardButton(text=NO, callback_data=NO),
        ]
    ]
)
