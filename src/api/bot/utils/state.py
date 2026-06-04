from aiogram.fsm.state import StatesGroup, State


class AuthState(StatesGroup):
    waiting_for_email = State()
    waiting_for_code = State()
