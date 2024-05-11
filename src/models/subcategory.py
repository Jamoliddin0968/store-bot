# Your models for the app
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class SubCategory(BaseModel):
    __tablename__ = "subcategory"
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey(
        'category.id', ondelete="CASCADE"), nullable=False)

    category = relationship("Category")
