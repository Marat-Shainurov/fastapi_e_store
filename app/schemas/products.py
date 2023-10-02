from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")


class ProductBase(ProductCreate):
    created_at: datetime = Field(..., title="Creation date")
    updated_at: datetime = Field(..., title="Last update")
    owner_id: int | None = Field(..., title="Product owner id")
    is_active: bool = Field(default=True, title="Product status")


class ProductInBasket(BaseModel):
    id: int = Field(..., title="Product id")
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")


class BasketInDB(BaseModel):
    id: int
    products: List[ProductInBasket]

    class ConfigDict:
        from_attributes = True


class ProductInDb(ProductBase):
    id: int = Field(..., title="Product id")
    baskets: list[BasketInDB] = Field(default=[], title="Baskets the product in")

    class ConfigDict:
        from_attributes = True


class ProductBaseUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    owner_id: int | None = None
    is_active: bool | None = None


class ProductBasePut(BaseModel):
    name: str
    price: float
    owner_id: int
    is_active: bool
