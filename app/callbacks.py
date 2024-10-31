from aiogram.filters.callback_data import CallbackData


class EventAction(CallbackData, prefix="&event"):
    action: str
    user_id: str
    timestamp: int
