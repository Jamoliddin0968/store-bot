
from typing import Any

from fastapi import Request
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.applications import Starlette
from starlette.requests import Request

from src.database import engine
from src.models import Category

# from src.infrastructure.services.token_service import TokenService

app = Starlette()


# class AdminAuth(AuthenticationBackend):
#     async def login(self, request: Request) -> bool:
#         form = await request.form()
#         try:
#             username, password = form["username"], form["password"]
#             if (username == "admin" and password == "123"):
#                 acces_token = "token_data.get(access_token)"
#                 request.session.update({"Bearer token": acces_token})
#                 return True
#         except Exception as e:
#             print(e.args, e)
#         return False

#     async def logout(self, request: Request) -> bool:
#         request.session.clear()
#         return True

#     async def authenticate(self, request: Request) -> bool:
#         token = request.session.get("Bearer token")
#         if not token:
#             return False
#         return True


# authentication_backend = AdminAuth(secret_key="...")
admin = Admin(app=app, engine=engine)


# class DmttAdmin(ModelView, model=Dmtt):
#     icon = "fa-solid fa-school"
#     column_list = ["name", "user"]
#     page_size = 25


# class ContractAdmin(ModelView, model=Contract):
#     icon = "fa-solid fa-file-excel"
#     column_list = ["dmtt", "company"]
#     page_size = 25


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


# class ProductAdmin(ModelView, model=Product):
#     column_list = ["name"]
#     page_size = 25


# class UserAdmin(ModelView, model=User):
#     page_size = 25
#     name = "User"
#     name_plural = "Users"
#     icon = "fa-solid fa-user"
#     column_list = [User.first_name, User.last_name, User.role]
#     _token_service = TokenService()

#     form_widget_args = {
#         "password": {
#             "readonly": True,
#         },
#     }

#     async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
#         new_pass = data.get("new_password")
#         if new_pass:
#             data["password"] = self._token_service.get_hashed_password(
#                 new_pass)
#             data["new_password"] = None
#         return await super().on_model_change(data, model, is_created, request)


class CategoryAdmin(ModelView, model=Category):
    icon = "fa-solid fa-category"
    column_list = "__all__"
    page_size = 25


admin.add_view(CategoryAdmin)
