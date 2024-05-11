
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from src.database import get_db
from src.services.subcategory import SubCategoryService


from src.schemas.subcategory import SubCategoryCreate, SubCategoryInfo, SubCategoryUpdate
router = APIRouter(prefix='/subcategories', tags=["subcategory"],)
# Routes


@router.post("/", response_model=SubCategoryInfo)
def create_new_subcategory(data: SubCategoryCreate, db: Session = Depends(get_db)):
    return SubCategoryService.create_subcategory(db=db, data=data)


@router.get("/", response_model=list[SubCategoryInfo])
def get_all_subcategories(db: Session = Depends(get_db)):
    return SubCategoryService.get_all_subcategories(db=db)


@router.get("/{subcategory_id}", response_model=SubCategoryInfo)
def get_subcategory_by_id(subcategory_id: int, db: Session = Depends(get_db)):
    return SubCategoryService.get_subcategory_by_id(db=db, subcategory_id=subcategory_id)


@router.put("/{subcategory_id}", response_model=SubCategoryInfo)
def update_subcategory_by_id(subcategory_id: int, data: SubCategoryUpdate, db: Session = Depends(get_db)):
    return SubCategoryService.update_subcategory(db=db, subcategory_id=subcategory_id, data=data)


@router.delete("/{subcategory_id}")
def delete_subcategory_by_id(subcategory_id: int, db: Session = Depends(get_db)):
    return SubCategoryService.delete_subcategory(db=db, subcategory_id=subcategory_id)
