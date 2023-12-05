
from sqlalchemy.orm import Session
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryInfo
from fastapi import APIRouter, Depends
from src.database import get_db
from src.services.category import CategoryService
router = APIRouter(prefix='/category', tags=["category"])
# Routes


@router.post("/create/", response_model=CategoryInfo)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryService.create_category(db, category)


@router.get("/all/")
def get_all_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories(db)


@router.get("/detail/{category_id}/", response_model=CategoryInfo)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.get_category_by_id(db=db, category_id=category_id)


@router.put("/update/{category_id}/", response_model=CategoryInfo)
def update_category_by_id(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return CategoryService.update_category(db, category_id, category)


@router.delete("/delete/{category_id}/")
def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.delete_category(db, category_id)
