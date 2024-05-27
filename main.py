import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src import config
from src.admin import app as admin_app
from src.handlers import register_routes
# from src.handlers.keyboards import view_button
# from src.middlewares.config import ConfigMiddleware
from worker import is_work

router = Router()

logger = logging.getLogger(__name__)


WEBHOOK_PATH = f"/bot/{config.TOKEN}"
WEBHOOK_URL = config.WEBHOOK_URL + WEBHOOK_PATH

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
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

print(config.WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


async def test():
    await bot.send_message(5290603408, "ishladi")
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    # uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)
app.mount("/", admin_app)
