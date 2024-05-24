# Your models for the app
from sqlalchemy import Column, ForeignKey, Integer, String

from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey('category.id'))

    def __str__(self):
        return f"{self.name}"
