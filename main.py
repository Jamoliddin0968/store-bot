from fastapi import FastAPI

from src.admin import app as a_router

app = FastAPI()

app.mount("/", a_router)
