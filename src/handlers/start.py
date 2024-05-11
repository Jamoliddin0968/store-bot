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


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.first_name}")
    description = "Assalomu alaykum ! YotiqTut onlayn magazinga xush kelibsiz.\n"
    description += "Привет! Добро пожаловать в интернет-журнал YatiqTut.\n"
    description += "Hello! Welcome to the YatiqTut online store\n"
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
    telegram_id = message.from_user.id
    user = await users_service.get_or_create(tg_user_id=telegram_id)
    await users_service.update(user.id, {"phone_number": phone_number})
    await message.answer("Tilni tanlang", reply_markup=language_markup)


@router.callback_query(F.text.startswith("language_"))
async def callbacks_num(callback: types.CallbackQuery):
    telegram_id = callback.message.from_user.id
    lang = callback.data.split("_")[1]
    user = await users_service.get_or_create(tg_user_id=telegram_id)
    await users_service.update(user.id, {"lang": lang})
    await callback.message.answer(f"Tilni tanlang {lang}")
