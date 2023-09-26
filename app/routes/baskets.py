from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import UserInDB, BasketInDB
from app.services import create_basket_with_products, remove_products_from_basket, destroy_basket, get_basket, \
    get_baskets
from app.services import get_current_active_user

router = APIRouter(
    prefix="/baskets",
    tags=["baskets"]
)


@router.post("/", response_model=BasketInDB, status_code=status.HTTP_201_CREATED)
async def create_basket(products: list[int] = Query(..., description='Products to add'),
                        db: Session = Depends(get_db),
                        current_user: UserInDB = Depends(get_current_active_user)):
    return create_basket_with_products(db=db, products_to_add=products)


@router.patch("{basket_id}/remove-products", response_model=BasketInDB)
async def remove_products(basket_id: int, products: list[int] = Query(..., description='Products to remove'),
                          db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    return remove_products_from_basket(db=db, products_to_remove=products, basket_id=basket_id)


@router.get("/{basket_id}", response_model=BasketInDB, status_code=status.HTTP_200_OK)
async def read_basket(basket_id: int, db: Session = Depends(get_db),
                      current_user: UserInDB = Depends(get_current_active_user)):
    return get_basket(db=db, basket_id=basket_id)


@router.get("/", response_model=list[BasketInDB], status_code=status.HTTP_200_OK, description="Baskets list")
async def read_baskets(db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    return get_baskets(db=db)


@router.delete("/{basket_id}", status_code=status.HTTP_204_NO_CONTENT, description="Basket id")
async def delete_basket(basket_id: int, db: Session = Depends(get_db),
                        current_user: UserInDB = Depends(get_current_active_user)):
    return destroy_basket(db=db, basket_id=basket_id)
