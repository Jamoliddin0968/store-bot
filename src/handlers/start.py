import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from .keyboards import contact_share_markup

router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.first_name}")
    description = "Assalomu alaykum ! YotiqTut onlayn magazinga xush kelibsiz."
    description += "Привет! Добро пожаловать в интернет-журнал YatiqTut."
    description += "Hello! Welcome to the YatiqTut online store"
    await message.answer(description)
    await message.answer(
        f"Iltimos telefon raqamingizni yuboring !", reply_markup=contact_share_markup
    )


@router.message(F.contact)
async def get_contact(message: Message):
    phone_number = message.contact.phone_number
    if phone_number[0] == "+":
        phone_number = phone_number
    else:
        phone_number = f"+{phone_number}"
    telegram_id = str(message.from_user.id)
    await message.answer("yaxshi")
