from typing import Dict, Type, Union

from pydantic import BaseModel

from src.database import get_db


class CreateMixin:
    async def create(self, obj_in: Dict):
        with get_db() as session:
            new_obj = self.model(**obj_in)
            session.add(new_obj)
            session.commit()
            session.refresh(new_obj)
            return new_obj


class RetrieveMixin:
    async def get(self, instance_id: int) -> BaseModel:
        with get_db() as session:
            return session.query(self.model).filter_by(id=instance_id).first()

    async def get_multi(self, skip: int = 0, limit: int = 100):
        with get_db() as session:
            return session.query(self.model).offset(skip).limit(limit).all()


class UpdateMixin:
    async def update(self, instance_id: int, obj_in: Dict) -> BaseModel:
        with get_db() as session:

            obj_data = obj_in

            session.query(self.model).filter_by(
                id=instance_id).update(obj_data)
            session.commit()
            return session.query(self.model).filter_by(id=instance_id).first()


class DeleteMixin:
    async def delete(self, instance_id: int) -> None:
        with get_db() as session:
            session.query(self.model).filter_by(id=instance_id).delete()
            session.commit()

    async def delete_multi(self, **kwargs) -> None:
        with get_db() as session:
            session.query(self.model).filter_by(**kwargs).delete()
            session.commit()


class ExistsMixin:
    async def is_exists(self, **filter_kwargs) -> bool:
        with get_db() as session:
            query = session.query(self.model).filter_by(
                **filter_kwargs).exists()
            result = session.query(query).scalar()
            return result


class FilterMixin:
    async def filter_one(self, **filter_kwargs) -> bool:
        with get_db() as session:
            instance = session.query(self.model).filter_by(
                **filter_kwargs).first()
            return instance

    async def filter(self, **filter_kwargs) -> bool:
        with get_db() as session:
            instance_list = session.query(self.model).filter_by(
                **filter_kwargs).all()
            return instance_list


class GetAllMixin:
    async def get_all(self):
        with get_db() as session:
            return session.query(self.model).all()


class CRUDRepoBase(CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin, ExistsMixin, GetAllMixin, FilterMixin):
    model = None
