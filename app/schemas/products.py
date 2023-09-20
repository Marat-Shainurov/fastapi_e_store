from datetime import datetime

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(..., title="Product id")
    name: str = Field(..., title="Product name")
    price: float = Field(..., title="Product price")
    created_at: datetime = Field(..., title="Creation date")
    updated_at: datetime = Field(..., title="Last update")
    is_active: bool = Field(default=True, title="Product status")
    owner_id: int = Field(..., title="Product owner id")
