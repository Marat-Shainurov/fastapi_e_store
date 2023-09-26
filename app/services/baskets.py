from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
from typing import Type

from app.models import Basket, Product


def create_basket_with_products(db: Session, products_to_add: list[int]) -> Basket:
    new_basket = Basket()
    db.add(new_basket)
    for product_id in products_to_add:
        product = db.query(Product).filter_by(id=product_id).one_or_none()
        if product:
            new_basket.products.append(product)
            db.commit()
            db.refresh(new_basket)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with {product_id} id not found"
            )
    return new_basket


# todo:
#  1. check and configure the user-product deleting process
#  2. Registration/email verification


def remove_products_from_basket(db: Session, basket_id: int, products_to_remove: list[int]):
    basket = db.query(Basket).filter_by(id=basket_id).one_or_none()
    if basket:
        for p in products_to_remove:
            product = db.query(Product).filter_by(id=p).one_or_none()
            if product:
                basket.products.remove(product)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with {p} id not found")
    db.commit()
    return db.query(Basket).filter_by(id=basket_id).one()


def get_basket(db: Session, basket_id: int) -> Type[Basket]:
    basket = db.query(Basket).filter_by(id=basket_id).one_or_none()
    if basket is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Basket {basket_id} not found"
        )
    return basket


def get_baskets(db: Session):
    baskets = db.query(Basket).all()
    return baskets if baskets else []


def destroy_basket(db: Session, basket_id: int) -> None:
    basket = db.query(Basket).filter_by(id=basket_id).one_or_none()
    if basket:
        db.delete(basket)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Basket {basket_id} not found"
        )
