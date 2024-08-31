

from aiogram import F, Router, types

from .filters import IsPrivateFilter
from .keyboards import menu_markup

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(F.text == ("Bosh menyu"))
async def start_handler(message: types.Message):
    await message.answer(("Bosh menyu"), reply_markup=menu_markup)
