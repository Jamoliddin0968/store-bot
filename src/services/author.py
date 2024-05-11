import uuid
from fastapi.exceptions import HTTPException
import os
from src.models.author import Author

from datetime import datetime

from src.config import UPLOAD_DIRECTORY


class AuthorService:

    @staticmethod
    def create(db, data):
        author = Author(**data.model_dump())
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    @staticmethod
    def upload_image(db, author_id, file):
        author = AuthorService.get_or_404(author_id=author_id, db=db)
        current_datetime = datetime.now()
        current_unix_timestamp = int(current_datetime.timestamp())
        unique_id = str(uuid.uuid4())
        if author.image:

            if os.path.exists(author.image):
                os.remove(author.image)
        file_extension = file.filename.split(".")[-1]
        new_filename = f"{unique_id}{current_unix_timestamp}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIRECTORY, new_filename)

        with open(file_path, "wb") as image_file:
            image_file.write(file.file.read())
            author.image = file_path
            db.commit()
        return file_path

    @staticmethod
    def get_or_404(db, author_id):
        author = db.query(Author).filter(Author.id == author_id).first()

        if not author:
            raise HTTPException(detail="Author not found", status_code=404)
        return author

    @staticmethod
    def get_all_authors(db):
        return db.query(Author).all()

    @staticmethod
    def update(db, author_id, data):
        author = AuthorService.get_or_404(db=db, author_id=author_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(author, key, value)
        db.commit()
        db.refresh(author)
        return author

    @staticmethod
    def delete(db, author_id):
        author = AuthorService.get_or_404(db=db, author_id=author_id)
        db.delete(author)
        db.commit()
        return {"message": "ok"}
