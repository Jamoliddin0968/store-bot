import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from src.services import UsersService

from .keyboards import contact_share_markup, language_markup

users_service = UsersService()

router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(F.text == "Biz bilan bo'g'lanish")
async def start_handler(message: types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.first_name}")
    description = "Assalomu alaykum ! YotiqTut onlayn magazinga xush kelibsiz.\n"
    description += "Привет! Добро пожаловать в интернет-журнал YatiqTut.\n"
    description += "Hello! Welcome to the YatiqTut online store\n"
    await message.answer(description)
    await message.answer(
        f"Iltimos telefon raqamingizni yuboring !", reply_markup=contact_share_markup
    )
