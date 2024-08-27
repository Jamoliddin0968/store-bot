# Your models for the app
import enum

from sqlalchemy import Column, Enum, Integer, String

from src.models.base import BaseModel


class UserLangEnum(enum.Enum):
    en = "en"
    ru = "ru"
    uz = "uz"


class TgUsers(BaseModel):
    __tablename__ = 'tg_users'

    firstname = Column(String(63), nullable=True)
    lastname = Column(String(63), nullable=True)
    username = Column(String(63), nullable=True)
    phone_number = Column(String(15), nullable=True)
    tg_user_id = Column(String(15), nullable=True)


class Users(BaseModel):
    __tablename__ = 'users'

    firstname = Column(String(63), nullable=True)
    lastname = Column(String(63), nullable=True)
    username = Column(String(63), nullable=True)
    password = Column(String(63), nullable=True)
    phone_number = Column(String(15), nullable=True)
    tg_user_id = Column(String(15), nullable=True)
