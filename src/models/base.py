from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from src.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
