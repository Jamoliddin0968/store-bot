import io

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.repositories import UsersRepo

from .filters import IsPrivateFilter
from .keyboards import get_contact_share_markup, menu_markup
from .states import Registration

users_repo = UsersRepo()

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    description = "Assalomu alaykum !"""
    # print(message)
    await message.answer(description)
    telegram_id = message.from_user.id
    if await users_repo.is_exists(tg_user_id=telegram_id):
        await message.answer(text=("Bosh menyu"), reply_markup=menu_markup)
    else:
        await message.answer(
            (f"Iltimos telefon raqamingizni yuboring !"), reply_markup=get_contact_share_markup()
        )
        await state.set_state(state=None)
        await state.set_state(Registration.phone_number)


@router.message(Registration.phone_number)
async def get_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    if phone_number[0] == "+":
        phone_number = phone_number
    else:
        phone_number = f"+{phone_number}"
    await state.set_state(Registration.language)
    await state.update_data(phone_number=phone_number)
    telegram_id = message.from_user.id
    data = await state.get_data()
    await users_repo.create({
        "tg_user_id": telegram_id,
        "phone_number": data.get("phone_number")
    })

    await state.set_state(state=None)
    await message.answer(text=("Bosh menyu"), reply_markup=menu_markup)
