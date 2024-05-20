from aiogram.fsm.state import StatesGroup, State


class NextStep(StatesGroup):
    password = State()


class Session(StatesGroup):
    session_id = State()
