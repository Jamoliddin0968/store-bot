import enum
from datetime import datetime, timedelta

import pytz
from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                        String, func)
from sqlalchemy.orm import backref, relationship

from src.models.base import BaseModel

# from datetime import timezone


def get_current_datetime_tashkent():
    tz_tashkent = pytz.timezone('Asia/Tashkent')
    return datetime.now(tz_tashkent)


class OrderStatus(enum.Enum):
    PENDING = 'pending'
    # sREJECTED = 'rejected'
    ACCEPTED = 'accepted'


class Order(BaseModel):
    __tablename__ = 'orders'

    user_id = Column(Integer,  nullable=False)

    datetime = Column(DateTime, default=get_current_datetime_tashkent)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    items = relationship("OrderItems", viewonly=True)

    def __str__(self):
        return f"{self.dmtt} - {self.id}"


class OrderItems(BaseModel):
    __tablename__ = "order_items"
    order_id = Column(ForeignKey(
        "orders.id", ondelete="CASCADE"), nullable=False)
    # product_name = Column(String(127), nullable=False)
    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=True)
    count = Column(Float, nullable=False)

    order = relationship("Order")

    # def __str__(self) -> str:
    #     return f"{self.product_name} {self.count}"
