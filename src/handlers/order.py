from aiogram import Dispatcher, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, FSInputFile, Message,
                           ReplyKeyboardRemove)
from aiogram.types.input_file import FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.config import GROUP_ID
from src.handlers.states import OrderState
from src.repositories import (CategoryRepo, ProductRepo, SubCategoryRepo,
                              UsersRepo)

from .filters import IsPrivateFilter
from .keyboards import (create_inline_buttons, create_product_buttons,
                        get_menu_markup)

user_repo = UsersRepo()
category_repo = CategoryRepo()
product_repo = ProductRepo()

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(F.text == __("🛒 Buyurtma berish"))
async def start_handler(message: types.Message):
    """
    Buyurtma berish
    """
    language = await user_repo.get_user_language(message.from_user.id)
    categories = await category_repo.get_all()
    if len(categories) == 0:
        await message.answer(
            _("Categoriyalar mavjud emas"), reply_markup=get_menu_markup()
        )
    else:
        await message.answer(
            text=_("Categoriyani tanlang"),
            reply_markup=create_inline_buttons(
                prefix="category_", data=categories, return_prefix="home_page_order", language=language
            ),
        )


sub_category_repo = SubCategoryRepo()


@router.callback_query(F.data.startswith("category_"))
async def get_subcategories(callback: CallbackQuery):
    """
    sub category ni olish
    """
    language = await user_repo.get_user_language(callback.from_user.id)
    category_id = callback.data.split("category_")[-1]
    subcategories = await sub_category_repo.filter(category_id=category_id)
    if len(subcategories) == 0:
        await callback.message.answer(
            _("SubCategoriyalar mavjud emas"), reply_markup=get_menu_markup()
        )
    else:
        await callback.message.edit_text(
            text=_("Categoriyani tanlang"),
            reply_markup=create_inline_buttons(
                prefix="subcategory_",
                data=subcategories,
                return_prefix=f"return_to_order",
                language=language
            ),
        )


@router.callback_query(F.data == "home_page_order")
async def get_subcategories(callback: CallbackQuery):
    """
    catogirydan orqaga
    """
    await callback.message.delete()
    await callback.message.answer(_("Bosh menyu"), reply_markup=get_menu_markup())
    # callback.message.


@router.callback_query(F.data == "return_to_order")
async def get_subcategories(callback: CallbackQuery):
    """
    catogirydan orqaga
    """
    language = await user_repo.get_user_language(callback.from_user.id)
    categories = await category_repo.get_all()
    await callback.message.edit_text(
        text=_("Categoriyani tanlang"),
        reply_markup=create_inline_buttons(
            prefix="category_", data=categories, return_prefix="home_page_order", language=language
        ),
    )

    # callback.message.


@router.callback_query(F.data.startswith("subcategory_"))
async def get_subcategories(callback: CallbackQuery):
    """
    productni olish
    """
    language = await user_repo.get_user_language(callback.from_user.id)
    subcategory_id = callback.data.split("subcategory_")[-1]
    subcategories = await product_repo.filter(subcategory_id=subcategory_id)
    if len(subcategories) == 0:
        await callback.message.answer(
            _("Mahsulot mavjud emas"), reply_markup=get_menu_markup()
        )
    else:

        category_id = subcategories[0].subcategory_id
        category = await sub_category_repo.get(category_id)
        category_id = category.category_id
        lst = [InputMediaPhoto(media=FSInputFile(item.image))
               for item in subcategories]
        await callback.message.answer_media_group(media=lst)
        await callback.message.answer(
            text=_("Mahsulotni tanlang"),
            reply_markup=create_inline_buttons(
                prefix="product_",
                data=subcategories,
                return_prefix=f"category_{category_id}",
                language=language
            ),
        )
        await callback.message.delete()


@router.callback_query(F.data.startswith("product_"))
async def get_subcategories(callback: CallbackQuery, state: FSMContext):
    """
    productni olish
    """
    language = await user_repo.get_user_language(callback.from_user.id)
    product_id = callback.data.split("product_")[-1]
    product = await product_repo.filter_one(id=product_id)
    if not product:
        await callback.message.answer(
            _("Mahsulot mavjud emas"), reply_markup=get_menu_markup()
        )
    elif product.types:
        await state.update_data(product_id=product.id)
        await callback.message.answer(
            _("Tanlang"),
            reply_markup=create_product_buttons(
                prefix="item_", data=product.types, language=language),
        )
        await state.set_state(OrderState.type)
    else:
        await state.update_data(product_id=product.id)
        await callback.message.answer(
            text=_("Mahsulot o'lchamini kiriting:"), reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(OrderState.size)


@router.message(OrderState.type)
async def select_state(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer(
        text=_("Mahsulot o'lchamini kiriting:"), reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderState.size)


@router.message(OrderState.size)
async def select_state(message: Message, state: FSMContext):
    data = await state.get_data()
    size = message.text
    product = await product_repo.get(data["product_id"])
    await message.answer(_("Buyurtma qabul qilindi"), reply_markup=get_menu_markup())
    new_img = FSInputFile(product.image)
    description = f"Buyurtma qoldirildi\n"
    description += f"Nomi: {product.name}\n"
    if "type" in data:
        description += f"Turi: {data['type']}\n"
    description += f"O'lchami: {size}\n"
    user = await user_repo.filter_one(tg_user_id=message.from_user.id)
    description += f"Mijoz: {message.from_user.first_name}\n"
    if user:
        description += f"Mijoz raqami: {user.phone_number}\n"
    await message.bot.send_photo(chat_id=GROUP_ID, photo=new_img, caption=description)
    await state.set_state(state=None)
