import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI

from src import config
from src.admin import admin_app as fast_admin_app
from src.admin_handlers import register_routes as admin_register_routes
from src.handlers import register_routes
from worker import start_periodic_requests

router = Router()

logger = logging.getLogger(__name__)

# Webhook paths for client and admin bots
WEBHOOK_PATH = f"/bot/{config.TOKEN}"
ADMIN_WEBHOOK_PATH = f"/bot/{config.ADMIN_TOKEN}"

# Full webhook URLs
WEBHOOK_URL = f"{config.WEBHOOK_URL}{WEBHOOK_PATH}"
ADMIN_WEBHOOK_URL = f"{config.WEBHOOK_URL}{ADMIN_WEBHOOK_PATH}"

# Storage setup
storage = MemoryStorage()

# Bots and dispatchers
bot = Bot(token=config.TOKEN)
admin_bot = Bot(token=config.ADMIN_TOKEN)

dp = Dispatcher(storage=storage)
admin_dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_periodic_requests()

    # Set webhooks for both client and admin bots
    await bot.delete_webhook()
    await bot.set_webhook(url=WEBHOOK_URL)
    await admin_bot.delete_webhook()
    await admin_bot.set_webhook(url=ADMIN_WEBHOOK_URL)

    yield

    # Cleanup: delete webhooks
    await bot.delete_webhook()
    await admin_bot.delete_webhook()

# FastAPI application setup
app = FastAPI(lifespan=lifespan)
app.mount("/admin/", fast_admin_app)

# Register routes
register_routes(dp)
admin_register_routes(admin_dp)

# Webhook handlers for client and admin bots


@app.post(WEBHOOK_PATH)
async def client_bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


@app.post(ADMIN_WEBHOOK_PATH)
async def admin_bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await admin_dp.feed_webhook_update(bot=admin_bot, update=telegram_update)

# For testing purposes


async def test():
    await bot.send_message(5290603408, "ishladi")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
