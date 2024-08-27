from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from src.repositories import (order_items_repo, order_repo, product_repo,
                              user_repo)


# Define your states
class OrderDialogSG(StatesGroup):
    select_product = State()
    select_quantity = State()

# Start order dialog


async def start_order(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(OrderDialogSG.select_product)

# Fetch available products and create a product selection menu


async def get_products(dialog_manager: DialogManager, **kwargs):
    products = await product_repo.get_all()  # Fetch all products from your repo
    return {
        "products": [(product.id, product.name) for product in products]
    }


async def on_product_selected(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    product_id = button.widget_id
    dialog_manager.dialog_data["selected_product_id"] = product_id
    await dialog_manager.switch_to(OrderDialogSG.select_quantity)


async def on_quantity_selected(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    quantity = float(c.message.text)
    product_id = dialog_manager.dialog_data["selected_product_id"]

    # Create order and order item
    order = await order_repo.create({"user_id": c.from_user.id, "status": "pending"})
    await order_items_repo.create({"order_id": order.id, "product_id": product_id, "count": quantity})

    await c.message.answer(f"Order created! Product ID: {product_id}, Quantity: {quantity}")
    await dialog_manager.done()

# Dialog to select a product
product_selection_dialog = Dialog(
    Window(
        Const("Please select a product:"),
        Button(Format("{item[1]}"), id=Format(
            "{item[0]}"), on_click=on_product_selected),
        Cancel(Const("Cancel")),
        getter=get_products,
        state=OrderDialogSG.select_product,
    ),
    Window(
        Const("Please enter the quantity (as a float):"),
        Button(Const("Confirm"), id="confirm", on_click=on_quantity_selected),
        Cancel(Const("Cancel")),
        state=OrderDialogSG.select_quantity,
    )
)
