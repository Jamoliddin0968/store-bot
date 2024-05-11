# Your models for the app
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType, ImageType
from sqlalchemy import Column, Integer, String

from src.models.base import BaseModel


class Products(BaseModel):
    __tablename__ = 'authors'

    name = Column(String(255))
    image = Column(ImageType(storage=FileSystemStorage(path="/tmp")))
