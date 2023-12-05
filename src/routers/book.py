
from fastapi import APIRouter

router = APIRouter(prefix='book')


@router.get("/all")
def get_all_book():
    return {"hello": "world"}

