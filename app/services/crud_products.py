from datetime import datetime
from typing import Type

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductBase, UserInDB, ProductCreate, ProductBaseUpdate


def add_product(db: Session, product: ProductCreate, current_user: UserInDB) -> Product:
    current_date = datetime.utcnow()
    new_product_schema = ProductBase(
        **product.model_dump(), created_at=current_date, updated_at=current_date, owner_id=current_user.id
    )
    new_product = Product(
        name=new_product_schema.name, price=new_product_schema.price, created_at=new_product_schema.created_at,
        updated_at=new_product_schema.updated_at, owner_id=new_product_schema.owner_id,
        is_active=new_product_schema.is_active
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_products(db: Session) -> list[Type[Product]]:
    return db.query(Product).all()


def get_product(db: Session, product_id: int) -> Type[Product]:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No product found"
    )


def put_product(product: ProductBase, product_id: int, db: Session) -> Type[Product]:
    product_to_update = db.query(Product).filter(Product.id == product_id)
    if product_to_update.first():
        product_to_update.update(values={**product.model_dump()})
        db.commit()
        db.refresh(product_to_update.first())
        return product_to_update.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No product found"
        )


def patch_product(product_id: int, product: ProductBaseUpdate, db: Session):
    stored_product = db.query(Product).filter_by(id=product_id).one_or_none()
    if stored_product is not None:
        stored_data_schema = ProductBase(**stored_product.__dict__)
    else:
        stored_data_schema = ProductBase()
    update_data = product.model_dump(exclude_unset=True)
    updated_product_schema = stored_data_schema.model_copy(update=update_data)
    product_to_update_db = db.query(Product).filter_by(id=product_id)
    product_to_update_db.update(values={**updated_product_schema.model_dump()})
    db.commit()
    db.refresh(product_to_update_db.one_or_none())
    return db.query(Product).filter_by(id=product_id).one_or_none()


def destroy_product(product_id: int, db: Session):
    db.query(Product).filter(Product.id == product_id).delete(synchronize_session=False)
    db.commit()
