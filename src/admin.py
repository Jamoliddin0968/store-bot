from typing import List

from fastadmin import register
# from fastadmin import register
from fastadmin.api.frameworks.fastapi.app import app as admin_app
from fastadmin.models.orms.sqlalchemy import SqlAlchemyModelAdmin
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database import get_db
from src.models import Products, TgUsers, Users
from src.repositories import user_repo

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    # Set to True to log SQL queries
)

# Create a configured "Session" class
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@register(Users, sqlalchemy_sessionmaker=async_session)
class UserAdmin(SqlAlchemyModelAdmin):
    exclude = ("hash_password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    async def authenticate(self, username: str, password: str) -> int | None:
        user = await user_repo.filter_one(username=username)
        if not user:
            return None
        if not password_context.verify(password, user.password):
            return None
        return user.id


@register(Products, sqlalchemy_sessionmaker=async_session)
class ProductAdmin(SqlAlchemyModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("id", "name")
    list_filter = ("id", "name", "price")
    search_fields = ("name",)
