from asyncio import run
from typing import List

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from src.repositories import product_repo


def get_contact_share_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=("📞 Telefon raqamni yuborish"), request_contact=True
                )
            ],
        ],
        resize_keyboard=True,
    )


menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=("🛒 Buyurtma berish")),
         KeyboardButton(text=("🛒 Mening buyurtmalarim"))],
        [
            KeyboardButton(text=("📞 Biz bilan bo'g'lanish")),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def get_settings_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=("🏠 Bosh menyu"), callback_data="settings_home"
                )
            ],
        ],
        resize_keyboard=True,
    )
    return markup


async def create_product_button_list():
    products = await product_repo.get_all()
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=item.name)
                for item in products[i: i + 2]
            ]
            for i in range(0, len(products), 2)
        ],
        resize_keyboard=True,
    )


def create_inline_buttons(prefix: str, data: List, return_prefix="", language="uz"):
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
            InlineKeyboardButton(text=("🔙 Orqaga"),
                                 callback_data=return_prefix),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)


def create_product_buttons(prefix: str, data: List, language="uz"):
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
