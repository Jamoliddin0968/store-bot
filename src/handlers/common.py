import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from src.services import UsersService

from .keyboards import menu_markup

users_service = UsersService()

router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(F.text == "Bosh menyu")
async def start_handler(message: types.Message):
    await message.answer("""Bosh menyu""", reply_markup=menu_markup)
