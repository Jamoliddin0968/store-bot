from fastapi import HTTPException
from sqlalchemy.orm import Session
# from sqlalchemy import func
# from src.models.subcategory import SubCategory

from src.models.category import Category
from src.schemas.category import (CategoryCreate,  CategoryUpdate)


class CategoryService:

    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        new_category = Category(**category.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def get_category_by_id(db: Session, category_id: int):
        category = db.query(Category).filter(
            Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    @staticmethod
    def get_all_categories(db: Session):
        return db.query(Category).all()

    @staticmethod
    def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
        category = CategoryService.get_category_by_id(
            db=db, category_id=category_id)
        for key, value in category_data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: int):
        category = CategoryService.get_category_by_id(
            db=db, category_id=category_id)
        db.delete(category)
        db.commit()
        return {"message": "Category deleted successfully"}
