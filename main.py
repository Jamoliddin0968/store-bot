import json
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI, Request

from src import config
from src.handlers import register_routes

# from src.handlers.keyboards import view_button
# from src.middlewares.config import ConfigMiddleware

router = Router()

logger = logging.getLogger(__name__)


WEBHOOK_PATH = f"/bot/{config.tg.token}"
WEBHOOK_URL = config.WEBHOOK_URL + WEBHOOK_PATH

storage = MemoryStorage()

bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.delete_webhook()
    await bot.set_webhook(url=WEBHOOK_URL)
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)

# Register middlewares
# dp.update.middleware(ConfigMiddleware(config))

# Register routes
register_routes(dp)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):

    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int


@app.post('/send-message/')
async def bot_webhook(msg: str, user_id: str, order_id: int):

    await bot.send_message(user_id, msg)
    # await state.set_state("dwadaw")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    # uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)
