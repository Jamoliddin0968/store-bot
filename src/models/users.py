# Your models for the app
import enum

from sqlalchemy import Column, Enum, Integer, String

from src.models.base import BaseModel


class UserLangEnum(enum.Enum):
    en = "en"
    ru = "ru"
    uz = "uz"


class Users(BaseModel):
    __tablename__ = 'users'

    firstname = Column(String(63), nullable=True)

    phone_number = Column(String(15), nullable=True)
    tg_user_id = Column(String(15), nullable=True)
    lang = Column(Enum(UserLangEnum), default=UserLangEnum.uz)
