import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import BufferedInputFile, FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto

from src.config import GROUP_ID
from src.handlers.states import OrderState
from src.repositories import CategoryRepo, ProductRepo, SubCategoryRepo
from test_bot import bot

from .keyboards import (create_inline_buttons, create_product_buttons,
                        menu_markup)

category_repo = CategoryRepo()
product_repo = ProductRepo()
router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(F.text == "🛒 Buyurtma berish")
async def start_handler(message: types.Message):
    """
        Buyurtma berish
    """
    categories = await category_repo.get_all()
    if len(categories) == 0:
        await message.answer("Categoriyalar mavjud emas", reply_markup=menu_markup)
    else:
        await message.answer(text="Categoriyani tanlang", reply_markup=create_inline_buttons(prefix="category_", data=categories))

sub_category_repo = SubCategoryRepo()


@router.callback_query(F.data.startswith("category_"))
async def get_subcategories(callback: CallbackQuery):
    """
        sub category ni olish
    """
    category_id = callback.data.split("category_")[-1]
    subcategories = await sub_category_repo.filter(category_id=category_id)
    if len(subcategories) == 0:
        await callback.message.answer("SubCategoriyalar mavjud emas", reply_markup=menu_markup)
    else:
        await callback.message.answer(text="Categoriyani tanlang", reply_markup=create_inline_buttons(prefix="subcategory_", data=subcategories))


@router.callback_query(F.data.startswith("subcategory_"))
async def get_subcategories(callback: CallbackQuery):
    """
        productni olish
    """
    subcategory_id = callback.data.split("subcategory_")[-1]
    subcategories = await product_repo.filter(subcategory_id=subcategory_id)
    if len(subcategories) == 0:
        await callback.message.answer("Mahsulot mavjud emas", reply_markup=menu_markup)
    else:
        lst = [InputMediaPhoto(media=FSInputFile(item.image))
               for item in subcategories]
        await callback.message.answer_media_group(media=lst)
        await callback.message.answer(text="Mahsulotni tanlang", reply_markup=create_inline_buttons(prefix="product_", data=subcategories))


@router.callback_query(F.data.startswith("product_"))
async def get_subcategories(callback: CallbackQuery, state: FSMContext):
    """
        productni olish
    """
    product_id = callback.data.split("product_")[-1]
    product = await product_repo.filter_one(id=product_id)
    if not product:
        await callback.message.answer("Mahsulot mavjud emas", reply_markup=menu_markup)
    elif product.types:
        await state.update_data(product_id=product.id)
        await callback.message.answer("Tanlang", reply_markup=create_product_buttons(prefix="item_", data=product.types))
        await state.set_state(OrderState.type)
    else:
        await state.update_data(product_id=product.id)
        await callback.message.answer(text="Mahsulot o'lchamini kiriting:")
        await state.set_state(OrderState.size)


@router.message(OrderState.type)
async def select_state(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer(text="Mahsulot o'lchamini kiriting:")
    await state.set_state(OrderState.size)


@router.message(OrderState.size)
async def select_state(message: Message, state: FSMContext):
    data = await state.get_data()
    size = message.text
    product = await product_repo.get(id=data.product_id)
    await message.answer("Buyurtma qabul qilindi", reply_markup=menu_markup)
    await bot.send_message(chat_id=GROUP_ID, text=f"{product.name}")
    await state.clear()
