from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.future import select

from src.database import get_db
from src.models import Order
from src.models.order import OrderItems
from src.models.products import Products

router = Router()

# Pagination settings
ITEMS_PER_PAGE = 5


class OrderProcessState(StatesGroup):
    selecting_product = State()
    entering_quantity = State()


@router.message(Command('order'))
async def start_handler(message: types.Message):
    await show_products(message, page=0)


async def show_products(message: types.Message, page: int, existing_message_id: int = None):
    offset = page * ITEMS_PER_PAGE
    with get_db() as session:  # Use synchronous session
        products_stmt = select(Products).offset(offset).limit(ITEMS_PER_PAGE)
        products = session.execute(products_stmt)
        products = products.scalars().all()

    lst = []
    for product in products:
        button = InlineKeyboardButton(
            text=f"{product.name} - ${product.price}",
            callback_data=f"product_{product.id}"
        )
        lst.append(button)

    # Adding pagination buttons
    if page > 0:
        lst.append(InlineKeyboardButton(
            text="Previous", callback_data=f"page_{page-1}"))
    if len(products) == ITEMS_PER_PAGE:
        lst.append(InlineKeyboardButton(
            text="Next", callback_data=f"page_{page+1}"))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[lst])

    if existing_message_id:
        await message.edit_text("Select a product:", reply_markup=keyboard)
    else:
        await message.answer("Select a product:", reply_markup=keyboard)


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
        await callback_query.message.answer(f"How many of {product.name} would you like to order?")
        await state.update_data(product_id=product_id)
        await state.set_state(OrderProcessState.entering_quantity)

    await callback_query.answer()


@router.message(OrderProcessState.entering_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = float(message.text)
    except ValueError:
        await message.answer("Please enter a valid number.")
        return

    data = await state.get_data()
    product_id = data.get('product_id')
    user_id = message.from_user.id

    with get_db() as session:
        product_stmt = select(Products).where(Products.id == product_id)
        product = session.execute(product_stmt).scalars().first()

        if product:
            # Retrieve or create order
            order_stmt = select(Order).where(Order.user_id == user_id)
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

            await message.answer(f"Added {quantity} of {product.name} to your order!")
        else:
            await message.answer("Product not found.")

    await state.clear()
