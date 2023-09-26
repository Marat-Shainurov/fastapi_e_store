from pydantic import BaseModel, Field

from app.schemas import ProductInBasket


class UserBase(BaseModel):
    name: str = Field(..., title="User name")
    last_name: str = Field(..., title="User last name")
    username: str = Field(..., title="User username")
    email: str = Field(..., title="User email")
    phone: str = Field(
        ...,
        title="Must start with '+7' and followed by 10 numbers",
        pattern="^\+7[0-9]{10}$"
    )
    is_active: bool = Field(default=True, title="User is_active status")


class UserCreate(UserBase):
    password: str = Field(
        ...,
        pattern="^[A-Z$%&!:].{7,}$",
        title="Must be longer than 8 symbols (latin letters, at least one uppercase, at least one symbol from $%&!:)."
    )


class UserInDB(UserBase):
    hashed_password: str
    id: int = Field(..., title="User id")
    products: list[ProductInBasket] = Field(default=[], title="User's products")

    class Config:
        from_attributes = True


class UserBaseUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    is_active: bool | None = None
