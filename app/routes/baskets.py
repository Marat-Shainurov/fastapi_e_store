from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import UserInDB, BasketInDB
from app.services import create_basket_with_products, delete_products_from_basket, destroy_basket, get_basket, \
    get_baskets, append_products, get_current_active_user, get_basket_and_sum

router = APIRouter(
    prefix="/baskets",
    tags=["baskets"]
)


@router.post("/", response_model=BasketInDB, status_code=status.HTTP_201_CREATED)
def create_basket(products: list[int] = Query(..., description='Products to add'),
                  db: Session = Depends(get_db),
                  current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint creates a **new basket**.
    - **Authorization** required.
    """
    return create_basket_with_products(db=db, products_to_add=products)


@router.patch("/{basket_id}/add-products", response_model=BasketInDB, status_code=status.HTTP_200_OK)
def add_products_to_basket(basket_id: int, db: Session = Depends(get_db),
                           products: list[int] = Query(..., description="Products to add to the basket"),
                           current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint **adds products to a basket** by the basket's id.
    - **Authorization** required.
    """
    return append_products(db=db, products_to_append=products, basket_id=basket_id)


@router.patch("/{basket_id}/remove-products", response_model=BasketInDB, status_code=status.HTTP_200_OK)
def remove_products_from_basket(
        basket_id: int, products: list[int] = Query(..., description='Products to remove from the basket'),
        db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint **removes products from a basket** by the basket's id.
    - **Authorization** required.
    """
    return delete_products_from_basket(db=db, products_to_remove=products, basket_id=basket_id)


@router.get("/{basket_id}", response_model=BasketInDB, status_code=status.HTTP_200_OK)
def read_basket(basket_id: int, db: Session = Depends(get_db),
                current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint returns a stored ** basket by the basket's id**.
    - **Authorization** required.
    """
    return get_basket(db=db, basket_id=basket_id)


@router.get("/{basket_id}/total-sum", status_code=status.HTTP_200_OK)
def read_basket_with_total_sum(basket_id: int, db: Session = Depends(get_db),
                               current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint returns a stored ** basket by the basket's id** and its **total_sum**.
    - **Authorization** required.
    """
    return get_basket_and_sum(db=db, basket_id=basket_id)


@router.get("/", response_model=list[BasketInDB], status_code=status.HTTP_200_OK, description="Baskets list")
def read_baskets(offset: int = 0, limit: int = 100,
                 db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint returns  **a list of stored baskets**.
    - **Authorization** required.
    """
    return get_baskets(db=db, offset=offset, limit=limit)


@router.delete("/{basket_id}", status_code=status.HTTP_204_NO_CONTENT, description="Basket id")
def delete_basket(basket_id: int, db: Session = Depends(get_db),
                  current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint **deletes a basket by the basket's id**.
    - **Authorization** required.
    """
    return destroy_basket(db=db, basket_id=basket_id)
