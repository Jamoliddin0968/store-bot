import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from src.repositories import CategoryRepo

from .keyboards import create_inline_buttons

category_repo = CategoryRepo()
router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(F.text == "🛒 Buyurtma berish")
async def start_handler(message: types.Message):
    categories = await category_repo.get_all()

    await message.answer(text="Categoritani tanlang", reply_markup=create_inline_buttons(prefix="category_", data=categories))
