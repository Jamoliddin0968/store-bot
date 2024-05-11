# Your models for the app
from sqlalchemy import Column, Integer, String

from src.models.base import BaseModel


class Products(BaseModel):
    __tablename__ = 'authors'

    name = Column(String(255))
    image = Column(String(255))
