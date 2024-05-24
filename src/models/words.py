# Your models for the app
from sqlalchemy import Column, ForeignKey, Integer, String

from src.models.base import BaseModel


class Words(BaseModel):
    __tablename__ = "words"
    value = Column(String(255), unique=True)
    value_uz = Column(String(255))
    value_ru = Column(String(255))
    value_en = Column(String(255))

    def __str__(self):
        return f"{self.value}"
