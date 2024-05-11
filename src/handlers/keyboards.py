from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.i18n import gettext as _

contact_share_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞  Telefon raqamni yuborish',
                        request_contact=True)],
    ],
    resize_keyboard=True,
)


language_markup = InlineKeyboardMarkup(
    keyboard=[
        [InlineKeyboardButton(text='Uz', callback_data="uz"),
         InlineKeyboardButton(text='Ru', callback_data="ru"),
         InlineKeyboardButton(text='En', callback_data="en")],
    ],
    resize_keyboard=True,
)
