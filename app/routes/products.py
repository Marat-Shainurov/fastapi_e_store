from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import UserInDB, ProductCreate, ProductInDb, ProductBaseUpdate, ProductBasePut
from app.services import (get_current_active_user, add_product, get_products, get_product, put_product, patch_product,
                          destroy_product)

router = APIRouter(
    prefix='/products',
    tags=['products'],
)


@router.post("/", response_model=ProductInDb, status_code=status.HTTP_201_CREATED)
def create_product(
        product: ProductCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Endpoint creates a **new product**:
    - **_name_**: each product must have its name.
    - **_price_**: each product must have its price.
    - **Authorization** required.
    """
    return add_product(db=db, product=product, current_user=current_user)


@router.get("/", response_model=list[ProductInDb], status_code=status.HTTP_200_OK)
def read_products(offset: int = 0, limit: int = 100, current_user: UserInDB = Depends(get_current_active_user),
                  db: Session = Depends(get_db)):
    """
    - Endpoint returns **a list of stored products**.
    - **Authorization** required.
    """
    return get_products(db=db, offset=offset, limit=limit)


@router.get("/{product_id}", response_model=ProductInDb)
def retrieve_product(product_id: int, current_user: UserInDB = Depends(get_current_active_user),
                     db: Session = Depends(get_db)):
    """
    - Endpoint returns a **product** by its _product_id_.
    - **Authorization** required.
    """
    return get_product(db=db, product_id=product_id)


@router.put("/{product_id}", response_model=ProductInDb, status_code=status.HTTP_200_OK)
def update_product(product: ProductBasePut, product_id: int,
                   current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    - Endpoint updates a **product** by its _product_id_.
    - **ProductBasePut** schema is used to pass a products to update.
    Fields to update (all required):
    {
      "name": "string",
      "price": 0,
      "owner_id": 0,
      "is_active": true
    }
    - Authorization required.
    """
    return put_product(product=product, product_id=product_id, db=db)


@router.patch("/{product_id}", response_model=ProductInDb, status_code=status.HTTP_200_OK)
def partial_update_product(
        product: ProductBaseUpdate, product_id: int, current_user: UserInDB = Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    """
    - Endpoint partially updates a **product** by its _product_id_.
    - **ProductBaseUpdate** schema is used to pass a products to update.
    Available fields to update:
    {
      "name": "string",
      "price": 0,
      "owner_id": 0,
      "is_active": true
    }
    - Authorization required.
    """
    return patch_product(product_id=product_id, product=product, db=db)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db),
                   current_user: UserInDB = Depends(get_current_active_user)):
    """
    - Endpoint deletes a **product** by its _product_id_.
    **Authorization** required.
    """
    return destroy_product(product_id=product_id, db=db)
