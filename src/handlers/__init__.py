from aiogram import Dispatcher

from .order import router as order_routes
from .start import router as start_routes


def register_routes(dp: Dispatcher):
    dp.include_router(start_routes)
    dp.include_router(order_routes)
