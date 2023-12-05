from pydantic import BaseModel


class SubCategoryBase(BaseModel):
    category_id: int
    name: str
    is_active: bool = True


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(SubCategoryBase):
    pass


class SubCategoryInfo(SubCategoryBase):
    id: int
