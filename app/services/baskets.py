from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status

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
#  1. delete_products_from_basket.
#  2. check and configure the user-product deleting process
#  3. Registration/email verification


def delete_products_from_basket(db: Session, products_to_add: list[int]):
    pass
