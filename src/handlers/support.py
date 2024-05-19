import io

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from .filters import IsPrivateFilter
from .keyboards import contact_share_markup, get_menu_markup, language_markup

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(F.text == __("📞 Biz bilan bo'g'lanish"))
async def start_handler(message: types.Message):
    await message.answer(_("Biz bilan bog'lanish\n📱 +998902720884\n📱 +998997600884"), reply_markup=get_menu_markup())
