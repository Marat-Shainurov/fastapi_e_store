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
#  1. Registration/email verification


def append_products(db: Session, products_to_append: list, basket_id: int):
    basket = db.query(Basket).filter_by().filter_by(id=basket_id).one_or_none()
    if basket:
        for p in products_to_append:
            product = db.query(Product).filter_by(id=p).one_or_none()
            if product:
                basket.products.append(product)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product {p} not found")
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Basket {basket_id} not found")
    return db.query(Basket).filter_by(id=basket_id).one()


def delete_products_from_basket(db: Session, basket_id: int, products_to_remove: list[int]):
    basket = db.query(Basket).filter_by(id=basket_id).one_or_none()
    if basket:
        for p in products_to_remove:
            product = db.query(Product).filter_by(id=p).one_or_none()
            if not product:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product {p} not found")
            if product and product in basket.products:
                basket.products.remove(product)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Product {p} is not in the basket")
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Basket {basket_id} not found")
    return db.query(Basket).filter_by(id=basket_id).one()


def get_basket(db: Session, basket_id: int) -> Type[Basket]:
    basket = db.query(Basket).filter_by(id=basket_id).one_or_none()
    if basket is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Basket {basket_id} not found"
        )
    return basket


def get_baskets(db: Session, offset: int, limit: int):
    baskets = db.query(Basket).offset(offset).limit(limit).all()
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
