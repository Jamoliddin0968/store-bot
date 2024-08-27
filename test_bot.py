import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from src import config
from src.handlers import register_routes

router = Router()

logger = logging.getLogger(__name__)


storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=storage)


# Register middlewares

register_routes(dp)


async def main():
    await bot.set_my_commands(
        [BotCommand(command="start", description="ishga tushirish"),
         ], BotCommandScopeDefault()
    )
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    asyncio.run(main())
    # uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)
