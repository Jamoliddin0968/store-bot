
from sqlalchemy import Column, String

from src.models.base import BaseModel


class Book(BaseModel):
    __tablename__ = "books"
    name = Column(String(127))
    description = Column(String(255))
