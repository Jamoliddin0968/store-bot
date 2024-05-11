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
    await message.answer(
        f"Iltimos telefon raqamingizni yuboring !", reply_markup=contact_share_markup
    )
