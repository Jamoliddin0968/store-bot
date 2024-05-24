from typing import Any, Dict, Optional

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18n, I18nMiddleware

from src.repositories import UsersRepo

# dp.update.middleware(ConfigMiddleware(config))
i18n = I18n(path="locales", default_locale="en", domain="messages")

user_repo = UsersRepo()


class MyI18nMiddleware(I18nMiddleware):
    """
    This middleware stores locale in the FSM storage
    """

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        tg_user = data.get('event_from_user')

        user = await user_repo.filter_one(tg_user_id=tg_user.id)
        if not user:
            return None
        elif not user.lang:
            return "uz"
        return user.lang.value


lang_middleware = MyI18nMiddleware(i18n=i18n)
