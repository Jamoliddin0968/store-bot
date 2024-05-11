from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    phone_number = State()
    language = State()


class OrderState(StatesGroup):
    category = State()
    subcategory = State()
