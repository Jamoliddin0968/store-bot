import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from src.repositories import CategoryRepo, SubCategoryRepo

from .keyboards import create_inline_buttons, menu_markup

category_repo = CategoryRepo()
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
