from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

from app.models.keyboards import (
    categories_keyboard,
    event_creation_confirmation_keyboard,
)
from app.models.stages import Event
from app.models.texts import EVENT_SUMMARY, NO, YES
from app.storage import events

create_router = Router()


@create_router.message(Event.Title)
async def update_event_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(Event.Category)
    await message.answer(
        text="Choose an event type",
        reply_markup=categories_keyboard.as_markup(),
    )


@create_router.message(Event.Category)
async def update_event_category(message: Message, state: FSMContext) -> None:
    if message.text.startswith("🍑"):
        await message.answer(
            text="Vicky, what you are looking for is in another app 😜, go back to /start",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    await state.update_data(category=message.text)
    await state.set_state(Event.Description)
    await message.answer(
        text="Write a description for your event",
        reply_markup=ReplyKeyboardRemove(),
    )


@create_router.message(Event.Description)
async def update_event_desc(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Event.DateTime)
    await message.answer(text="Choose date time")


@create_router.message(Event.DateTime)
async def update_event_datetime(message: Message, state: FSMContext) -> None:
    await state.update_data(datetime=message.text)
    await state.set_state(Event.Location)
    await message.answer(text="Mention place of event")


@create_router.message(Event.Location)
async def update_event_location(message: Message, state: FSMContext) -> None:
    await state.update_data(location=message.text)
    await state.set_state(Event.URL)
    await message.answer(
        text="Create and provide link for telegram channel - Here you and other people can get to known each other and start convo"
    )


@create_router.message(Event.URL)
async def update_event_url(message: Message, state: FSMContext) -> None:
    data = await state.update_data(url=message.text)
    await state.set_state(Event.Confirmation)
    await message.answer(
        text=EVENT_SUMMARY.format(**data),
        reply_markup=event_creation_confirmation_keyboard.as_markup(),
    )


@create_router.callback_query(Event.Confirmation, F.data == YES)
async def save_created_event(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    data = await state.get_data()
    await state.clear()
    await events.add_event(state.key.user_id, data)
    await callback_query.message.answer(
        text=f"Event Created! You can return to /start now."
    )


@create_router.callback_query(Event.Confirmation, F.data == NO)
async def delete_created_event(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer(text=f"Event deleted")
