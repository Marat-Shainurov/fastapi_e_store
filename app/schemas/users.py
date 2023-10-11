from enum import Enum

from pydantic import BaseModel, Field

from app.schemas import ProductInBasket


class UserBase(BaseModel):
    """A base schema for users representation."""
    name: str = Field(..., title="User name")
    last_name: str = Field(..., title="User last name")
    username: str = Field(..., title="User username")
    email: str = Field(..., title="User email")
    phone: str = Field(
        ...,
        title="Must start with '+7' and followed by 10 numbers",
        pattern="^\+7[0-9]{10}$"
    )


class UserCreate(UserBase):
    """A schema for users creating. Extends the UserBase schema with the password field."""
    password: str = Field(
        ...,
        pattern="^[A-Z$%&!:].{7,}$",
        title="Must be longer than 8 symbols (latin letters, at least one uppercase, at least one symbol from $%&!:)."
    )


class UserBasePut(BaseModel):
    """A schema for the put method. Requires all the fields set in the schema."""
    name: str
    last_name: str
    username: str
    email: str
    phone: str = Field(
        ...,
        title="Must start with '+7' and followed by 10 numbers",
        pattern="^\+7[0-9]{10}$"
    )
    is_active: bool


class UserBaseUpdate(BaseModel):
    """A schema for the patch method. Allows to set some of the fields to update."""
    name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None
    phone: str | None = Field(
        default=None,
        title="Must start with '+7' and followed by 10 numbers",
        pattern="^\+7[0-9]{10}$"
    )
    is_active: bool | None = None


class UserOutput(BaseModel):
    """A schema for the response_model option in the users' routes."""
    id: int
    name: str
    last_name: str
    username: str
    email: str
    phone: str
    is_active: bool
    products: list[ProductInBasket]


class UserInDB(UserBase):
    """A broader full version of the users' schema."""
    hashed_password: str
    id: int = Field(..., title="User id")
    products: list[ProductInBasket] = Field(default=[], title="User's products")
    verification_code: str | None = Field(default=None, title="Verification code")
    is_active: bool = Field(default=False, title="User is_active status")

    class ConfigDict:
        from_attributes = True


class GetUserBy(Enum):
    """An Unum class for the get_user_by query list. Sets the field to get a user by."""
    username = 'username'
    email = 'email'
    phone = 'phone'

