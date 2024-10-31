from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.callbacks import EventAction
from app.clients import DynamoDB

delete_command = Router()


@delete_command.callback_query(EventAction.filter(F.action == "delete"))
async def callback_delete_event(query: CallbackQuery, callback_data: EventAction):
    await query.answer(text="Message received", cache_time=6)
    with DynamoDB("joinme-prod-events") as table:
        table.delete(
            {"user_id": callback_data.user_id, "timestamp": callback_data.timestamp}
        )
    await query.message.delete()
    await query.message.answer(text="Your event was deleted...")
