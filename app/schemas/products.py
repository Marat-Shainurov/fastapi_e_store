from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")


class ProductBase(ProductCreate):
    created_at: datetime = Field(..., title="Creation date")
    updated_at: datetime = Field(..., title="Last update")
    owner_id: int = Field(..., title="Product owner id")
    is_active: bool = Field(default=True, title="Product status")


class ProductInDb(ProductBase):
    id: int = Field(..., title="Product id")


class ProductBaseUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    owner_id: int | None = None
    is_active: bool | None = None
