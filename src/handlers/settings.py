
from aiogram import Dispatcher, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.repositories import UsersRepo
from src.translate import lang_middleware

from .filters import IsPrivateFilter
from .keyboards import get_menu_markup, get_settings_markup, language_markup
from .states import SeetingsState

router = Router()
router.message.filter(IsPrivateFilter())

users_repo = UsersRepo()


@router.message(F.text == __("⚙️ Sozlamalar"))
async def start_handler(message: types.Message):
    await message.answer(_("""⚙️ Sozlamalar\n"""), reply_markup=get_settings_markup())


@router.callback_query(F.data == "settings_lang")
async def set_lang(callback: CallbackQuery, state: FSMContext):
    """
        productni olish
    """
    await callback.message.answer(_("Tilni tanlang"), reply_markup=language_markup)
    await state.set_state(SeetingsState.lang)


@router.message(SeetingsState.lang)
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
        await message.answer(_("Tilni tanlang"), reply_markup=language_markup)
        return None
    user = await users_repo.filter_one(tg_user_id=telegram_id)
    if user:
        await users_repo.update(user.id, {
            "lang": lang
        })
        await lang_middleware.set_locale(state=state, locale=lang)
    await state.set_state(state=None)
    await message.answer(_("""⚙️ Sozlamalar\n"""), reply_markup=get_settings_markup())


@router.callback_query(F.data == "settings_phone")
async def set_phone(callback: CallbackQuery, state: FSMContext):
    """
        settings phone
    """
    await callback.message.answer(_("Telelfon raqamingizni yuboring (12 xonali)"))
    await state.set_state(SeetingsState.phone)


def validate_uzbek_phone_number(phone_number: str):
    cleaned_number = ''.join(filter(str.isdigit, phone_number))
    if not cleaned_number.startswith('998'):
        return False
    cleaned_number = cleaned_number[3:]
    valid_prefixes = ["90", "91", "93", "94",
                      "95", "97", "98", "99", "88", "33", "55"]
    if cleaned_number.startswith(tuple(valid_prefixes)) and len(cleaned_number) == 9:
        return True
    else:
        return False


@router.message(SeetingsState.phone)
async def callbacks_num(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not validate_uzbek_phone_number(message.text):
        await message.answer(_("Telelfon raqamingizni yuboring (12 xonali)\n+998 XX XXX XX XX"))
    else:
        user = await users_repo.filter_one(tg_user_id=telegram_id)
        if user:
            await users_repo.update(user.id, {
                "phone_number": message.text
            })

        await state.set_state(state=None)
        await message.answer(reply_markup=ReplyKeyboardRemove())
        await message.answer(_("""⚙️ Sozlamalar\n"""), reply_markup=get_settings_markup())


@router.callback_query(F.data == "settings_home")
async def set_lang(callback: CallbackQuery):
    """
        settings phone
    """
    await callback.message.answer(text=_("Bosh menyu"), reply_markup=get_menu_markup())
