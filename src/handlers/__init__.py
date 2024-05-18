from aiogram import Dispatcher
from aiogram.utils.i18n import ConstI18nMiddleware, I18n
from aiogram.utils.i18n.middleware import ConstI18nMiddleware

from .common import router as home_router
from .order import router as order_routes
from .settings import router as settings_router
from .start import router as start_routes
from .support import router as support_router

i18n = I18n(path="locales", default_locale="en", domain="messages")

support_router.message.middleware(ConstI18nMiddleware(locale='en', i18n=i18n))
settings_router.message.middleware(ConstI18nMiddleware(locale='en', i18n=i18n))
home_router.message.middleware(ConstI18nMiddleware(locale='en', i18n=i18n))
start_routes.message.middleware(ConstI18nMiddleware(locale='en', i18n=i18n))
order_routes.message.middleware(ConstI18nMiddleware(locale='en', i18n=i18n))


def register_routes(dp: Dispatcher):
    dp.include_router(support_router)
    dp.include_router(settings_router)
    dp.include_router(home_router)
    dp.include_router(start_routes)
    dp.include_router(order_routes)
