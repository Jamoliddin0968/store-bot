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


class OrderProcessState(StatesGroup):
    selecting_product = State()
    entering_quantity = State()


@router.message(F.text == "🛒 Mahsulotlar")
async def start_handler(message: types.Message):
    await show_products(message, page=0)


async def show_products(message: types.Message, page: int, existing_message_id: int = None):
    offset = page * ITEMS_PER_PAGE
    with get_db() as session:  # Use synchronous session
        products_stmt = select(Products).offset(offset).limit(ITEMS_PER_PAGE)
        products = session.execute(products_stmt)
        products = products.scalars().all()

    lst = []
    tlist = []
    for product in products:
        button = InlineKeyboardButton(
            text=f"{product.name} - {product.price}",
            callback_data=f"product_{product.id}"
        )
        tlist.append(button)
        if len(tlist) == 2:
            lst.append(tlist)
            tlist = []
    if tlist:
        lst.append(tlist)
        tlist = []

    # Adding pagination buttons
    if page > 0:
        tlist.append(InlineKeyboardButton(
            text="Previous", callback_data=f"page_{page-1}"))
    if len(products) == ITEMS_PER_PAGE:
        tlist.append(InlineKeyboardButton(
            text="Next", callback_data=f"page_{page+1}"))
    if tlist:
        lst.append(tlist)
    keyboard = InlineKeyboardMarkup(inline_keyboard=lst)
    # keyboard.

    if existing_message_id:
        await message.edit_text("Mahsulotni tanlang:", reply_markup=keyboard)
    else:
        await message.answer("Mahsulotni tanlang:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("page_"))
async def paginate_products(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    await show_products(callback_query.message, page=page, existing_message_id=callback_query.message.message_id)
    await callback_query.answer()


@router.callback_query(F.data.startswith("product_"))
async def add_to_order(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = int(callback_query.data.split("_")[1])
    with get_db() as session:
        product_stmt = select(Products).where(Products.id == product_id)
        product = session.execute(product_stmt).scalars().first()

    if product:
        await callback_query.message.answer(f"{product.name} qancha miqdorda buyurtma qilasiz?")
        await state.update_data(product_id=product_id)
        await state.set_state(OrderProcessState.entering_quantity)

    await callback_query.answer()


@router.message(OrderProcessState.entering_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = float(message.text)
    except ValueError:
        await message.answer("Iltimos osn kiriting ( 5, 4.5 , 3.1 ).")
        return

    data = await state.get_data()
    product_id = data.get('product_id')
    user_id = message.from_user.id

    with get_db() as session:
        product_stmt = select(Products).where(Products.id == product_id)
        product = session.execute(product_stmt).scalars().first()

        if product:
            # Retrieve or create order
            order_stmt = select(Order).where(
                Order.user_id == user_id, Order.status == OrderStatus.PENDING)
            order = session.execute(order_stmt).scalars().first()

            if not order:
                order = Order(user_id=user_id)
                session.add(order)
                session.commit()
                session.refresh(order)

            # Create or update order item
            order_item = OrderItems(
                order_id=order.id,
                product_id=product_id,
                count=quantity
            )
            session.add(order_item)
            session.commit()

            await message.answer(f"{product.name} ({quantity} kg) savatchaga qo'shildi!")
        else:
            await message.answer("Product topilmadi")

    await state.clear()


@router.message(F.text == "🛒 Savatcha")
async def show_order(message: types.Message):
    user_id = message.from_user.id
    with get_db() as session:
        # Retrieve the user's order
        order_stmt = select(Order).where(
            Order.user_id == user_id, Order.status == OrderStatus.PENDING)
        order = session.execute(order_stmt).scalars().first()

        if order:
            order_items_stmt = select(OrderItems).where(
                OrderItems.order_id == order.id).options(joinedload(OrderItems.product))
            order_items = session.execute(order_items_stmt).scalars().all()

            if order_items:
                # Format the order summary as a numbered list
                order_summary = "\n".join(
                    [f"{i+1}. {item.product.name} - {item.count} kg" for i,
                        item in enumerate(order_items)]
                )
            else:
                order_summary = "No items in your order."

            # Add action buttons for sending or canceling the order
            action_buttons = [
                InlineKeyboardButton(
                    text="Yuborish", callback_data="send_order"),
                InlineKeyboardButton(text="Bekor qilish",
                                     callback_data="cancel_order")
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[action_buttons])

            await message.answer(f"Faol buyurtmangiz:\n{order_summary}", reply_markup=keyboard)
        else:
            await message.answer("Sizda faol buyurtmalar yo'q")
    return None

    # await callback_query.answer()


@router.callback_query(F.data == "send_order")
async def send_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    with get_db() as session:
        # Retrieve the user's order
        order_stmt = select(Order).where(
            Order.user_id == user_id, Order.status == OrderStatus.PENDING)
        order = session.execute(order_stmt).scalars().first()

        if order:
            order_items_stmt = select(OrderItems).where(
                OrderItems.order_id == order.id)
            order_items = session.execute(order_items_stmt).scalars().all()

            if order_items:
                order.status = OrderStatus.ACTIVE
                session.add(order)
                session.commit()
                await callback_query.message.answer("Buyurta yuborildi!")

            else:
                await callback_query.message.answer("Buyurtma bo'sh.")
        else:
            await callback_query.message.answer("buyurtma topilmadi.")

    # Hide the inline keyboard after action
    await callback_query.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    with get_db() as session:
        # Retrieve and delete the user's order
        order_stmt = select(Order).where(
            Order.user_id == user_id, Order.status == OrderStatus.PENDING)
        order = session.execute(order_stmt).scalars().first()

        if order:
            session.delete(order)
            session.commit()

            await callback_query.message.answer("Your order has been canceled.")
        else:
            await callback_query.message.answer("No order found to cancel.")

    # Hide the inline keyboard after action
    await callback_query.message.edit_reply_markup(reply_markup=None)
