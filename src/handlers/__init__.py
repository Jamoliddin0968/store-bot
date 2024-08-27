from aiogram import Dispatcher

from .common import router as home_router
from .order import router as order_routes
from .start import router as start_routes


def register_routes(dp: Dispatcher):
    dp.include_router(home_router)
    dp.include_router(start_routes)
    dp.include_router(order_routes)
