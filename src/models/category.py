# Your models for the app
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"
    name = Column(String(255))
    is_active = Column(Boolean(), default=True)

    subcategories = relationship("SubCategory", back_populates="category")
    # books = relationship("books")
