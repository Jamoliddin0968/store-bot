from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.author import AuthorCreate, AuthorInfo, AuthorUpdate
from src.services.author import AuthorService

router = APIRouter(prefix='/authors', tags=["author",])


@router.post("/", response_model=AuthorInfo)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    return AuthorService.create(data=data, db=db)


@router.post("/upload-image/{author_id}")
async def upload_author_image(author_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return AuthorService.upload_image(db=db, author_id=author_id, file=file)


@router.get("/{author_id}", response_model=AuthorInfo)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return AuthorService.get_or_404(db=db, author_id=author_id)


@router.get("/")
def get_all_author(db: Session = Depends(get_db)):
    return AuthorService.get_all_authors(db=db)


@router.put("/{author_id}")
def update(author_id: int, data: AuthorUpdate, db: Session = Depends(get_db)):
    return AuthorService.update(db=db, author_id=author_id, data=data)


@router.delete('/{author_id}')
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return AuthorService.delete(db=db, author_id=author_id)
