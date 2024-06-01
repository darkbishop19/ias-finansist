from aiogram.fsm.state import StatesGroup, State


class NextStep(StatesGroup):
    password = State()


class Session(StatesGroup):
    session_id = State()


class Admin(StatesGroup):
    telegram_user_id = State()
