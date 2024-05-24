from typing import Dict

from pydantic import BaseModel

from src.database import get_db
from src.models import Category, Products, SubCategory, Users, Words


class CRUDRepository:
    model = None  # This should be set by the child class

    async def create(self, obj_in: Dict) -> BaseModel:
        with get_db() as session:
            new_obj = self.model(**obj_in)
            session.add(new_obj)
            session.commit()
            session.refresh(new_obj)
            return new_obj

    async def get(self, instance_id: int) -> BaseModel:
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

    async def get_all(self):
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


class CategoryRepo(CRUDRepository):
    model = Category


class SubCategoryRepo(CRUDRepository):
    model = SubCategory


class ProductRepo(CRUDRepository):
    model = Products


class WordsRepo(CRUDRepository):
    model = Words

    def get_by_word(self, word):
        with get_db() as session:
            return session.query(self.model).filter_by(value=word).first()
