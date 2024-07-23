from typing import Optional

from aiogram.filters.callback_data import CallbackData
from pydantic import Field


class StartQuery(CallbackData, prefix="&"):
    action: str


class EventTypeQuery(CallbackData, prefix="&"):
    desc: str


class EventTypeQuery(CallbackData, prefix="&"):
    answer: str
