from typing import List

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


def get_contact_share_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_("📞 Telefon raqamni yuborish"), request_contact=True
                )
            ],
        ],
        resize_keyboard=True,
    )


language_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 Uz"),
            KeyboardButton(text="🇷🇺 Ru"),
            KeyboardButton(text="🇺🇸 En"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def get_menu_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("🛒 Buyurtma berish"))],
            [
                KeyboardButton(text=_("⚙️ Sozlamalar")),
                KeyboardButton(text=_("📞 Biz bilan bo'g'lanish")),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


def get_settings_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("⚙️ Tilni o'zgartirish"), callback_data="settings_lang"
                ),
                InlineKeyboardButton(
                    text=_("⚙️ Telefon raqamni o'zgartirish"),
                    callback_data="settings_phone",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("🏠 Bosh menyu"), callback_data="settings_home"
                )
            ],
        ],
        resize_keyboard=True,
    )
    return markup


def create_inline_buttons(prefix: str, data: List, return_prefix=""):
    buttons = [
        [
            InlineKeyboardButton(
                text=item.name, callback_data=f"{prefix}{item.id}")
            for item in data[i: i + 2]
        ]
        for i in range(0, len(data), 2)
    ]
    buttons.append(
        [
            InlineKeyboardButton(text=_("🔙 Orqaga"),
                                 callback_data=return_prefix),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)


def create_product_buttons(prefix: str, data: List):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=item.name, callback_data=f"{prefix}{item.id}")
                for item in data[i: i + 2]
            ]
            for i in range(0, len(data), 2)
        ],
        resize_keyboard=True,
    )
