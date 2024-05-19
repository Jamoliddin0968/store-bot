import io

from aiogram import F, Router, types
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from .filters import IsPrivateFilter
from .keyboards import get_menu_markup

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(F.text == __("📞 Biz bilan bo'g'lanish"))
async def start_handler(message: types.Message):
    await message.answer(_("Biz bilan bog'lanish\n📱 +998902720884\n📱 +998997600884"), reply_markup=get_menu_markup())
