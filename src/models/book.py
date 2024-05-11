# Your models for the app
from bson import ObjectId
from mongoengine import Document, StringField
from sqlalchemy import Column, String

from src.models.base import BaseModel


class Book(BaseModel):
    __tablename__ = "books"
    name = Column(String(127))
    description = Column(String(255))


class BookMongo(Document):
    id = ObjectId()
    meta = {'collection': 'books'}
    name = StringField(max_length=127, required=True)
    description = StringField(max_length=255)
