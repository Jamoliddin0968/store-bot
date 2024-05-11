import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from src.services import UsersService

from .keyboards import contact_share_markup, language_markup, menu_markup
from .states import Registration

users_service = UsersService()

router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum {message.from_user.first_name}")
    description = "Assalomu alaykum ! YotiqTut onlayn magazinga xush kelibsiz.\n\n"
    description += "Привет! Добро пожаловать в интернет-журнал YatiqTut.\n\n"
    description += "Hello! Welcome to the YatiqTut online store\n"
    await message.answer(description)
    telegram_id = message.from_user.id
    if await users_service.is_exists(tg_user_id=telegram_id):
        message.answer(text="Bosh menyu", reply_markup=menu_markup)
    else:
        await message.answer(
            f"Iltimos telefon raqamingizni yuboring !", reply_markup=contact_share_markup
        )
        await state.set_state(Registration.phone_number)


@router.message(Registration.phone_number, F.contact)
async def get_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    if phone_number[0] == "+":
        phone_number = phone_number
    else:
        phone_number = f"+{phone_number}"
    await state.set_state(Registration.language)
    telegram_id = message.from_user.id
    user = await users_service.get_or_create(tg_user_id=telegram_id)
    await users_service.update(user.id, {"phone_number": phone_number})
    await message.answer("Tilni tanlang", reply_markup=language_markup)


@router.message(Registration.language)
async def callbacks_num(message: Message):
    telegram_id = message.from_user.id
    if message.text == "Uz":
        pass
    elif message.text == "Ru":
        pass
