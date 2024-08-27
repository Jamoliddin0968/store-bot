from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    phone_number = State()
    language = State()


class OrderState(StatesGroup):
    product_id = State()
    type = State()
    size = State()


class UserOrderState(StatesGroup):
    start = State()
    product = State()
