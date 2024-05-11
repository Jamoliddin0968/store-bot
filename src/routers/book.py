from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.book import Book as DBBook
from src.schemas.book import BookCreate, BookUpdate, BookResponse
from src.services.book import BookService


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    return BookService.create_book(db=db, data=data)


@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return BookService.get_or_404(db=db, book_id=book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    return BookService.update_book(book_id=book_id, data=data, db=db)


@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return BookService
