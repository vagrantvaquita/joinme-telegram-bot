from aiogram.fsm.state import State, StatesGroup


class Event(StatesGroup):
    Title = State()
    Category = State()
    Description = State()
    DateTime = State()
    Location = State()
    URL = State()
    Confirmation = State()
