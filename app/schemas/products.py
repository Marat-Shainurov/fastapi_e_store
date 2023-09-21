from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")


class ProductInDb(ProductBase):
    id: int = Field(..., title="Product id")
    created_at: datetime = Field(..., title="Creation date")
    updated_at: datetime = Field(..., title="Last update")
    owner_id: int = Field(..., title="Product owner id")
    is_active: bool = Field(default=True, title="Product status")
