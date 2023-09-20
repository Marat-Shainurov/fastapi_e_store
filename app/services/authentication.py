from sqlalchemy.orm import Session

from app.schemas import UserInDB
from app.services import get_user
from app.services.tokens import verify_password


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | bool:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    else:
        return user
