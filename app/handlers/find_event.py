from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.keyboards import inline_categories_keyboard
from app.models.texts import EVENT_SUMMARY
from app.storage import events

find_router = Router()


def keyboard_from_events(event_type, events):
    keyboard_builder = InlineKeyboardBuilder()
    for event in events:
        keyboard_builder.button(
            text=f"{event}",
            callback_data=f"&pick:{event_type}:{event}",
        )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


@find_router.callback_query(F.data.startswith("&event_type:"))
async def list_registered_events(callback_query: CallbackQuery) -> None:
    await callback_query.answer(text="Message received")

    _, event_type = callback_query.data.split(":")

    if len(events[event_type]) > 0:
        await callback_query.message.edit_text(
            text="This are current events",
            reply_markup=keyboard_from_events(event_type, events[event_type]),
        )
    else:
        await callback_query.message.answer(
            text=f"No events listed for {event_type} category"
        )


@find_router.callback_query(F.data.startswith("&pick:"))
async def pick_one_event(callback_query: CallbackQuery) -> None:
    await callback_query.answer(text="Message received")

    _, event_type, event_name = callback_query.data.split(":")

    data = events[event_type][event_name]

    await callback_query.message.edit_text(
        text=EVENT_SUMMARY.format(**data),
        reply_markup=inline_categories_keyboard.as_markup(),
    )
