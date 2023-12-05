from src.models.author import Author
from fastapi.exceptions import HTTPException


class AuthorService:

    @staticmethod
    def create(db, data):
        author = Author(**data.model_dump())
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    @staticmethod
    def get_or_404(db, author_id):
        author = db.query(Author).filter(Author.id == author_id).first()

        if not author:
            raise HTTPException(detail="Author not found", status_code=404)
        return author

    @staticmethod
    def delete(db, author_id):
        author = AuthorService.get_or_404(db=db, author_id=author_id)
        db.delete(author)
        db.commit()
        return {"message": "ok"}
