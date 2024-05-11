from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

contact_share_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞  Telefon raqamni yuborish',
                        request_contact=True)],
    ],
    resize_keyboard=True,
)


language_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Uz')],
        [KeyboardButton(text='Ru')],
        [KeyboardButton(text='En')],
    ],
    resize_keyboard=True,
)
