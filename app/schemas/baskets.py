from pydantic import BaseModel, Field


class BasketBase(BaseModel):
    id: int = Field()
    products: list | None = Field(default=None, title="Products in the basket")
