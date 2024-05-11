from aiogram import Dispatcher

from .order import router as order_routes
from .settings import router as settings_router
from .start import router as start_routes
from .support import router as support_router


def register_routes(dp: Dispatcher):
    dp.include_router(start_routes)
    dp.include_router(order_routes)
    dp.include_router(support_router)
    dp.include_router(settings_router)
