import uuid
from fastapi.exceptions import HTTPException
import os
from src.models.book import Book
from src.services.author import AuthorService
from src.services.subcategory import SubCategoryService
from datetime import datetime

from src.config import UPLOAD_DIRECTORY


class BookService:

    @staticmethod
    def create_book(db, data):
        AuthorService.get_or_404(db=db, author_id=data.author_id)
        SubCategoryService.get_or_404(
            db=db, subcategory_id=data.subcategory_id)
        db_book = Book(**data.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_or_404(db, book_id):
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(detail="Book not found", status_code=404)
        return book

    @staticmethod
    def update_book(db, data, book_id):
        db_book = BookService.get_or_404(db, book_id)
        for field, value in data.dict().items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book(db, book_id):
        db_book = get_book(db, book_id)
        db.delete(db_book)
        db.commit()
        return {"messgae": "ok"}
