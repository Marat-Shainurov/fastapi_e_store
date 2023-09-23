from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import UserInDB, ProductBase, ProductCreate, ProductInDb, ProductBaseUpdate
from app.services import (get_current_active_user, add_product, get_products, get_product, put_product, patch_product,
                          destroy_product)

router = APIRouter(
    prefix='/products',
    tags=['products'],
)


@router.post("/", response_model=ProductInDb, status_code=status.HTTP_201_CREATED)
async def create_product(
        product: ProductCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)
):
    return add_product(db=db, product=product, current_user=current_user)


@router.get("/")
async def read_products(current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return get_products(db=db)


@router.get("/{product_id}")
async def retrieve_product(product_id: int, current_user: UserInDB = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    return get_product(db=db, product_id=product_id)


@router.put("/{product_id}", response_model=ProductBase)
async def update_product(product: ProductBase, product_id: int,
                         current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return put_product(product=product, product_id=product_id, db=db)


@router.patch("/{product_id}", response_model=ProductBase)
async def partial_update_product(
        product: ProductBaseUpdate, product_id: int, current_user: UserInDB = Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    return patch_product(product_id=product_id, product=product, db=db)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db),
                         current_user: UserInDB = Depends(get_current_active_user)):
    return destroy_product(product_id=product_id, db=db)
