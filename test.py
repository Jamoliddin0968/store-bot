from fastapi import FastAPI

from src.admin import app as admin_app

app = FastAPI()
app.mount("/", admin_app)
