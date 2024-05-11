# Your models for the app
import enum

from sqlalchemy import Column, Enum, Integer, String

from src.models.base import BaseModel


class UserLangEnum(enum.Enum):
    en = "en"
    ru = "ru"
    uz = "uz"


class Author(BaseModel):
    __tablename__ = 'authors'

    firstname = Column(String(63))

    phone_number = Column(String(15))
    tg_user_id = Column(String(15))
    lang = Column(Enum(UserLangEnum), default=UserLangEnum.uz)
