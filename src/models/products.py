
from sqlalchemy import Column, Integer, String

# from fastapi_storages.
from src.models.base import BaseModel

# from sqlalchemy.orm import relationship


class Products(BaseModel):
    __tablename__ = 'products'
    name = Column(String(255))
    price = Column(Integer(),)

    def __str__(self):
        return self.name
