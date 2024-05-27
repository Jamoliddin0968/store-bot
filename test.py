import asyncio

from fastapi import FastAPI

from src.admin import app as admin_app
from src.repositories import ProductRepo

app = FastAPI()


app.mount("/", admin_app)
