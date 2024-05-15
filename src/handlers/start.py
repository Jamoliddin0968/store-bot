import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from src.repositories import UsersRepo

from .keyboards import contact_share_markup, language_markup, menu_markup
from .states import Registration

users_repo = UsersRepo()

router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    print(message)
    await message.answer(f"Assalomu alaykum {message.from_user.first_name}")
    description = "Assalomu alaykum ! YotiqTut onlayn magazinga xush kelibsiz.\n\n"
    description += "Привет! Добро пожаловать в интернет-журнал YatiqTut.\n\n"
    description += "Hello! Welcome to the YatiqTut online store\n"
    await message.answer(description)
    telegram_id = message.from_user.id
    if await users_repo.is_exists(tg_user_id=telegram_id):
        await message.answer(text="Bosh menyu", reply_markup=menu_markup)
    else:
        await message.answer(
            f"Iltimos telefon raqamingizni yuboring !", reply_markup=contact_share_markup
        )
        await state.clear()
        await state.set_state(Registration.phone_number)


@router.message(Registration.phone_number)
async def get_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    if phone_number[0] == "+":
        phone_number = phone_number
    else:
        phone_number = f"+{phone_number}"
    await state.set_state(Registration.language)
    await state.set_data(phone_number=phone_number)
    await message.answer("Tilni tanlang", reply_markup=language_markup)


@router.message(Registration.language)
async def callbacks_num(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = ""
    if message.text == "🇺🇿 Uz":
        lang = "uz"
    elif message.text == "🇷🇺 Ru":
        lang = "ru"
    elif message.text == "🇺🇸 En":
        lang = "en"
    else:
        await message.answer("Tilni tanlang", reply_markup=language_markup)
        return None
    data = await state.get_data()
    await users_repo.create({
        "tg_user_id": telegram_id,
        "lang": lang,
        "phone_number": data.get("phone_number")
    })
    await state.clear()
    await message.answer(text="Bosh menyu", reply_markup=menu_markup)
