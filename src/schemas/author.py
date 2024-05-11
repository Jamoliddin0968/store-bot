from pydantic import BaseModel


class AuthorBase(BaseModel):
    firstname: str
    lastname: str
    birthdate: int
    country: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorInfo(AuthorBase):
    id: int
