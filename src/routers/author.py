from src.schemas.author import AuthorInfo, AuthorCreate
from src.services.author import AuthorService
from fastapi import APIRouter, Depends
from src.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix='/author', tags=["author",])


@router.post("/create/", response_model=AuthorInfo)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    return AuthorService.create(data=data, db=db)


@router.delete('/delete/{author_id}/')
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return AuthorService.delete(db=db, author_id=author_id)
