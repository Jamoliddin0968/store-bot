from typing import List

from fastadmin import register
# from fastadmin import register
from fastadmin.api.frameworks.fastapi.app import app as admin_app
from fastadmin.models.orms.sqlalchemy import SqlAlchemyModelAdmin
from passlib.context import CryptContext

from src.database import get_db
from src.models import Products, TgUsers, Users
from src.repositories import user_repo

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@register(Users, sqlalchemy_sessionmaker=get_db)
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


@register(Products)
class ProductAdmin(SqlAlchemyModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("id", "name")
    list_filter = ("id", "name", "price")
    search_fields = ("name",)
