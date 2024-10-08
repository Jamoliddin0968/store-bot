from typing import Dict, Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Order, OrderItems, Products, Users

# Create a type variable that can be any subclass of the base model
ModelType = TypeVar('ModelType', bound=declarative_base())


class CRUDRepository:
    model: Type[ModelType] = None  # This should be set by the child class

    async def create(self, obj_in: Dict) -> ModelType:
        with get_db() as session:
            new_obj = self.model(**obj_in)
            session.add(new_obj)
            session.commit()
            session.refresh(new_obj)
            return new_obj

    async def get(self, instance_id: int) -> ModelType:
        with get_db() as session:
            return session.query(self.model).filter_by(id=instance_id).first()

    async def get_multi(self, skip: int = 0, limit: int = 100):
        with get_db() as session:
            return session.query(self.model).offset(skip).limit(limit).all()

    async def update(self, instance_id: int, obj_in: Dict) -> BaseModel:
        with get_db() as session:
            obj_data = obj_in
            session.query(self.model).filter_by(
                id=instance_id).update(obj_data)
            session.commit()
            return session.query(self.model).filter_by(id=instance_id).first()

    async def delete(self, instance_id: int) -> None:
        with get_db() as session:
            session.query(self.model).filter_by(id=instance_id).delete()
            session.commit()

    async def delete_multi(self, **kwargs) -> None:
        with get_db() as session:
            session.query(self.model).filter_by(**kwargs).delete()
            session.commit()

    async def is_exists(self, **filter_kwargs) -> bool:
        with get_db() as session:
            query = session.query(self.model).filter_by(
                **filter_kwargs).exists()
            result = session.query(query).scalar()
            return result

    async def filter_one(self, **filter_kwargs) -> BaseModel:
        with get_db() as session:
            return session.query(self.model).filter_by(**filter_kwargs).first()

    async def filter(self, **filter_kwargs):
        with get_db() as session:
            return session.query(self.model).filter_by(**filter_kwargs).all()

    async def get_all(self) -> List[ModelType]:
        with get_db() as session:
            return session.query(self.model).all()


class UsersRepo(CRUDRepository):
    model = Users

    async def get_user_language(self, tg_user_id):
        language = "uz"
        user: Users = await self.filter_one(tg_user_id=tg_user_id)
        if user:
            return user.lang
        return language


class ProductRepo(CRUDRepository):
    model = Products


class OrderRepo(CRUDRepository):
    model = Order


class OrderItemsRepo(CRUDRepository):
    model = OrderItems


order_items_repo = OrderItemsRepo()
order_repo = OrderRepo()
user_repo = UsersRepo()
product_repo = ProductRepo()
