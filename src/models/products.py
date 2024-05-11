from sqlalchemy import Column, ForeignKey, Integer, String

from src.models.base import BaseModel


class Products(BaseModel):
    __tablename__ = 'products'
    subcategory_id = Column(Integer, ForeignKey(
        "subcategory.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255))
    image = Column(String(25), nullable=True)
    tg_message_id = Column(String(25), nullable=True)
