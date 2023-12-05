from sqlalchemy.orm import Session
from src.models.subcategory import SubCategory
from fastapi import HTTPException
from src.schemas.subcategory import SubCategoryCreate,  SubCategoryUpdate
from src.services.category import CategoryService


class SubCategoryService:

    @staticmethod
    def create_subcategory(db: Session, data: SubCategoryCreate):
        _category = CategoryService.get_category_by_id(
            db=db, category_id=data.category_id)
        new_category = SubCategory(**data.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def get_subcategory_by_id(db: Session, subcategory_id: int):
        category = db.query(SubCategory).filter(
            SubCategory.id == subcategory_id).first()
        if not category:
            raise HTTPException(
                status_code=404, detail="SubCategory not found")
        return category

    @staticmethod
    def get_all_subcategories(db: Session):
        return db.query(SubCategory).all()

    @staticmethod
    def update_subcategory(db: Session, subcategory_id: int, data: SubCategoryUpdate):
        subcategory = SubCategoryService.get_subcategory_by_id(
            db=db, subcategory_id=subcategory_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(subcategory, key, value)
        db.commit()
        db.refresh(subcategory)
        return subcategory

    @staticmethod
    def delete_subcategory(db: Session, subcategory_id: int):
        subcategory = SubCategoryService.get_subcategory_by_id(
            db=db, subcategory_id=subcategory_id)
        db.delete(subcategory)
        db.commit()
        return {"message": "SubCategory deleted successfully"}
