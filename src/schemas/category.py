from typing import List

from pydantic import BaseModel

from src.schemas.subcategory import SubCategoryInfo


class CategoryBase(BaseModel):
    name: str
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInfo(CategoryBase):
    id: int
    subcategories: List[SubCategoryInfo]
    subcategory_count: int = 0
    book_count: int = 0

    class ConfigDict:
        from_attributes = True
