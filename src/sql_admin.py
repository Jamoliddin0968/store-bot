
from typing import Any, Coroutine

from fastapi import Request
from sqladmin import Admin, BaseView, ModelView, expose
from sqladmin.authentication import AuthenticationBackend
from sqladmin.pagination import Pagination
from sqlalchemy.orm import joinedload, selectinload
from starlette.applications import Starlette
from starlette.requests import Request

from src.database import engine, get_db
from src.models import Products, Users

app = Starlette()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        try:
            username, password = form["username"], form["password"]
            if (username == "admin" and password == "123"):
                acces_token = "token_data.get(access_token)"
                request.session.update({"Bearer token": acces_token})
                return True
        except Exception as e:
            print(e.args, e)
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("Bearer token")
        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key="...")
admin = Admin(app=app, engine=engine,
              authentication_backend=authentication_backend)


# class OrderAdmin(ModelView, model=Order):
#     column_list = ["id", "dmtt", "company",]
#     page_size = 25
#     can_create = False
#     column_sortable_list = [Order.id]
#     column_default_sort = ("id", True)


# class OrderItemAdmin(ModelView, model=OrderItems):
#     column_list = ["product_name", "count"]
#     page_size = 25
#     # column_exclude_list = ["order_id",]


class ProductAdmin(ModelView, model=Products):
    column_list = ["name"]
    page_size = 25


class UserAdmin(ModelView, model=Users):
    page_size = 25
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = [Users.firstname, Users.lastname,]

    form_widget_args = {
        "password": {
            "readonly": True,
        },
    }

    # async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
    #     new_pass = data.get("new_password")
    #     if new_pass:
    #         data["password"] = self._token_service.get_hashed_password(
    #             new_pass)
    #         data["new_password"] = None
    #     return await super().on_model_change(data, model, is_created, request)


admin.add_view(UserAdmin)

admin.add_view(ProductAdmin)
# admin.add_view(OrderAdmin)
# admin.add_view(OrderItemAdmin)

# admin.add_view(TestLimitAdmin)
