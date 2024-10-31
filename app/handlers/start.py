from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.models.keyboards import inline_categories_keyboard, start_keyboard
from app.models.stages import Event

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Do you want to create and event or join and existing one?",
        reply_markup=start_keyboard.as_markup(),
    )


@start_router.message(Command("createEvent"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Event.Title)
    await message.answer(text="Name your event")


@start_router.callback_query(F.data == "&event:create")
async def command_start_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer(text="Message received", cache_time=6)
    await state.set_state(Event.Title)
    await callback_query.message.edit_text(text="Name your event")


@start_router.callback_query(F.data == "&event:find")
async def command_start_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer(text="Message received", cache_time=6)
    await callback_query.message.edit_text(
        text="Choose category", reply_markup=inline_categories_keyboard.as_markup()
    )
