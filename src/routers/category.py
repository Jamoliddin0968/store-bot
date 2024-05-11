
from sqlalchemy import select, func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.category import Category
from src.schemas.category import CategoryCreate, CategoryInfo, CategoryUpdate
from src.services.category import CategoryService
from fastapi.responses import UJSONResponse
from sqlalchemy.orm import joinedload
from src.models.subcategory import SubCategory
router = APIRouter(prefix='/categories', tags=["category",])
# Routes


@router.post("/", response_model=CategoryInfo)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryService.create_category(db, category)


@router.get("/", response_model=List[CategoryInfo])
def get_all_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories(db)


@router.get("/{category_id}/", response_model=CategoryInfo)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.get_category_by_id(db=db, category_id=category_id)


@router.put("/{category_id}", response_model=CategoryInfo)
def update_category_by_id(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return CategoryService.update_category(db, category_id, category)


@router.delete("/{category_id}")
def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.delete_category(db, category_id)


@router.get("/test/", response_model=List[CategoryInfo])
def test(db: Session = Depends(get_db)):
    categories = db.query(Category).options(
        joinedload(Category.subcategories)).all()

    data = [
        {
            "id": category.id,
            "name": category.name,
            "is_active": category.is_active,
            "subcategories": category.subcategories,
            "subcategory_count": len(category.subcategories)
        }
        for category in categories
    ]

    return data
