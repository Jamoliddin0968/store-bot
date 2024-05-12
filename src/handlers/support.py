import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile

from .keyboards import contact_share_markup, language_markup, menu_markup

router = Router()
# router.message.filter(IsPrivateFilter())
dp = Dispatcher()


@router.message(F.text == "📞 Biz bilan bo'g'lanish")
async def start_handler(message: types.Message):
    await message.answer("""Biz bilan bog'lanish\n📱 +998902720884\n📱 +998997600884""", reply_markup=menu_markup)
