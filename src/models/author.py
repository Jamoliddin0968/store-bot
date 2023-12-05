# Your models for the app
from sqlalchemy import Column, Integer, String

from src.models.base import BaseModel


class Author(BaseModel):
    __tablename__ = 'authors'

    firstname = Column(String(63))
    lastname = Column(String(31))
    birthdate = Column(Integer)
    image = Column(String(255), nullable=True)
    country = Column(String(31))
