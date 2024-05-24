
import uuid

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.applications import Starlette
from starlette.datastructures import UploadFile
from starlette.requests import Request

from src.database import engine
from src.models import Category, Products, SubCategory, Type, Words

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

    def on_model_change(self, data: dict, model, is_created: bool, request: Request):
        image: UploadFile = data.get('image')
        if image:
            filename = "tmp"+"/"+str(uuid.uuid4())+"." + \
                image.filename.split('.')[-1]
            saved_image = UploadFile(
                image.file,  filename=filename)
            with open(filename, "wb") as f:
                f.write(image.file.read())
            image.file.seek(0)
            data['image'] = saved_image
        return super().on_model_change(data, model, is_created, request)


class TranslatesAdmin(ModelView, model=Words):
    icon = "fa-solid fa-translate"
    column_list = ["value", "value_uz", "value_ru", "value_en"]
    page_size = 25


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
admin.add_view(TranslatesAdmin)
