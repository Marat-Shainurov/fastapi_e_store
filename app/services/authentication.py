from typing import Type

from sqlalchemy.orm import Session

from app.models import User
from app.services import get_user, verify_password


def authenticate_user(db: Session, username: str, password: str) -> Type[User] | bool:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    else:
        return user
