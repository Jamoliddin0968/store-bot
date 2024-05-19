from aiogram import Dispatcher

from src.translate import lang_middleware

from .common import router as home_router
from .order import router as order_routes
from .settings import router as settings_router
from .start import router as start_routes
from .support import router as support_router

support_router.message.outer_middleware(lang_middleware)
settings_router.message.outer_middleware(lang_middleware)
home_router.message.outer_middleware(lang_middleware)
start_routes.message.outer_middleware(lang_middleware)
order_routes.message.outer_middleware(lang_middleware)


support_router.callback_query.outer_middleware(lang_middleware)
settings_router.callback_query.outer_middleware(lang_middleware)
home_router.callback_query.outer_middleware(lang_middleware)
start_routes.callback_query.outer_middleware(lang_middleware)
order_routes.callback_query.outer_middleware(lang_middleware)


def register_routes(dp: Dispatcher):
    dp.include_router(support_router)
    dp.include_router(settings_router)
    dp.include_router(home_router)
    dp.include_router(start_routes)
    dp.include_router(order_routes)
