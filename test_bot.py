import asyncio
import json
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src import config
from src.admin import app as admin_app
from src.handlers import register_routes

# from src.handlers.keyboards import view_button
# from src.middlewares.config import ConfigMiddleware
# from worker import is_work

router = Router()

logger = logging.getLogger(__name__)


storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=storage)


# Register middlewares
# dp.update.middleware(ConfigMiddleware(config))

# Register routes
register_routes(dp)


async def main():
    await bot.set_my_commands(
        [BotCommand(command="start", description="ishga tushirish"),
         ], BotCommandScopeDefault()
    )
    dp.bot
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    asyncio.run(main())
    # uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)
