from typing import Any, Dict

from aiogram.types import TelegramObject
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

# dp.update.middleware(ConfigMiddleware(config))
i18n = I18n(path="locales", default_locale="en", domain="messages")


lang_middleware = FSMI18nMiddleware(i18n=i18n)
