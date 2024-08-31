from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.models import Order
from src.models.order import OrderItems, OrderStatus
from src.models.products import Products

from .keyboards import menu_markup

router = Router()

# Pagination settings
ITEMS_PER_PAGE = 5


def get_orders_by_status(session, status):
    """
    Retrieve all orders with a specific status.
    :param session: SQLAlchemy session object
    :param status: Status to filter orders by (OrderStatus Enum)
    :return: List of orders with the specified status
    """
    orders_stmt = select(Order).where(Order.status == status)
    orders = session.execute(orders_stmt).scalars().all()
    return orders


class OrderProcessState(StatesGroup):
    selecting_product = State()
    entering_quantity = State()

# Handler for "🛒 Yangi buyurtmalar" (New Orders)


@router.message(F.text == "🛒 Yangi buyurtmalar")
async def show_new_orders(message: types.Message):
    orders = get_orders_by_status(OrderStatus.PENDING)
    if orders:
        for order in orders:
            await message.answer(f"Buyurtma #{order.id}: {order.datetime}\nStatus: {order.status.name}")
    else:
        await message.answer("Yangi buyurtmalar mavjud emas.")

# Handler for "🛒 Tasdiqlangan buyurtmalar" (Accepted Orders)


@router.message(F.text == "🛒 Tasdiqlangan buyurtmalar")
async def show_accepted_orders(message: types.Message):
    orders = get_orders_by_status(OrderStatus.ACCEPTED)
    if orders:
        for order in orders:
            await message.answer(f"Buyurtma #{order.id}: {order.datetime}\nStatus: {order.status.name}")
    else:
        await message.answer("Tasdiqlangan buyurtmalar mavjud emas.")
