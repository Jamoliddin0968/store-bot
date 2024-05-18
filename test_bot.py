import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.utils.i18n import ConstI18nMiddleware, I18n, middleware
from aiogram.utils.i18n.middleware import ConstI18nMiddleware

from src import config
from src.handlers import register_routes

router = Router()

logger = logging.getLogger(__name__)


storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=storage)


# Register middlewares
# dp.update.middleware(ConfigMiddleware(config))
i18n = I18n(path="locales", default_locale="en", domain="messages")

# Register routes
register_routes(dp)


async def main():
    await bot.set_my_commands(
        [BotCommand(command="start", description="ishga tushirish"),
         ], BotCommandScopeDefault()
    )
    await bot.delete_webhook()
    dp.message.middleware(ConstI18nMiddleware(locale='en', i18n=i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    asyncio.run(main())
    # uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)
