from pydantic import BaseModel
from src.schemas.subcategory import SubCategoryInfo
from typing import List


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
