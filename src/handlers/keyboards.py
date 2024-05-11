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
    inline_keyboard=[
        [InlineKeyboardButton(text='Uz', callback_data="language_uz"),
         InlineKeyboardButton(text='Ru', callback_data="language_ru"),
         InlineKeyboardButton(text='En', callback_data="language_en")],
    ],
    resize_keyboard=True,
)


menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Buyurtma berish')],
        [KeyboardButton(text="Sozlamalar"),
         KeyboardButton(text="Biz bilan bo'g'lanish")]
    ], resize_keyboard=True
)
