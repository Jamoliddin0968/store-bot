
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.applications import Starlette
from starlette.requests import Request
from wtforms import FileField, Form, StringField, validators

from src.database import engine
from src.models import Category, Products, SubCategory, Type
from src.utils import save_image

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


class ProductAdmin(ModelView, model=Products):
    column_list = ["name",]
    #


class TypeAdmin(ModelView, model=Type):
    icon = "fa-solid fa-category"
    column_list = ["name",]
    page_size = 25


class CategoryAdmin(ModelView, model=Category):
    icon = "fa-solid fa-category"
    column_list = ["name",]
    page_size = 25


class SubCategoryAdmin(ModelView, model=SubCategory):
    icon = "fa-solid fa-category"
    column_list = ["category", "name"]
    page_size = 25


admin.add_view(CategoryAdmin)
admin.add_view(SubCategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(TypeAdmin)
