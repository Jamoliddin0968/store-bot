# Your models for the app
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey('category.id'))

    parent = relationship("Category", remote_side=[id])
    children = relationship("Category")
