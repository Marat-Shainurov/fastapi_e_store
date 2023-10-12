from pydantic import BaseModel


class Token(BaseModel):
    """A base token schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """A schema to store data for tokens encoding/decoding."""
    username: str | None = None
