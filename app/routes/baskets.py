from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import UserInDB, BasketBase
from app.services import create_basket_with_products
from app.services import get_current_active_user

router = APIRouter(
    prefix="/baskets",
    tags=["baskets"]
)


@router.post("/", response_model=BasketBase, status_code=status.HTTP_201_CREATED)
async def create_basket(products: list[int] = Query(..., description='Products to add'),
                        db: Session = Depends(get_db),
                        current_user: UserInDB = Depends(get_current_active_user)):
    return create_basket_with_products(db=db, products_to_add=products)
