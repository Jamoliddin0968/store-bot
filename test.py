import asyncio

from fastapi import FastAPI

from src.admin import app as admin_app
from src.repositories import ProductRepo

app = FastAPI()


async def get_():
    return await ProductRepo().get_all()
app.mount("/", admin_app)
