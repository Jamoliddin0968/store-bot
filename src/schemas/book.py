from pydantic import BaseModel as PydanticBase


class BookBase(PydanticBase):
    name: str
    description: str
    author_id: int
    subcategory_id: int
    file: str = None
    audio_file: str = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
