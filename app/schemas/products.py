from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """A schema for creating new products, with 2 compulsory fields."""
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")


class ProductBase(ProductCreate):
    """A base schema for products."""
    created_at: datetime = Field(..., title="Creation date")
    updated_at: datetime = Field(..., title="Last update")
    owner_id: int | None = Field(..., title="Product owner id")
    is_active: bool = Field(default=True, title="Product status")


class ProductInBasket(BaseModel):
    """A schema for short representation of the products related to a specific basket."""
    id: int = Field(..., title="Product id")
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")


class BasketInDB(BaseModel):
    """A base schema for baskets."""
    id: int
    products: List[ProductInBasket]

    class ConfigDict:
        from_attributes = True


class ProductInDb(ProductBase):
    """A broader full version of the products' schema."""
    id: int = Field(..., title="Product id")
    baskets: list[BasketInDB] = Field(default=[], title="Baskets the product in")

    class ConfigDict:
        from_attributes = True


class ProductBaseUpdate(BaseModel):
    """A schema for the patch method. Allows to set some of the fields to update."""
    name: str | None = None
    price: float | None = None
    owner_id: int | None = None
    is_active: bool | None = None


class ProductBasePut(BaseModel):
    """A schema for the put method. Requires all the fields set in the schema."""
    name: str
    price: float
    owner_id: int
    is_active: bool
