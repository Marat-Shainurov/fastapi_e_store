from sqlalchemy.orm import Session

from app import models
from app.models import User
from app.schemas import UserInDB
from app.services.tokens import verify_password


def get_user_schema(db: Session, username: str) -> UserInDB | None:
    user = db.query(models.User).filter(User.username == username).first()
    if user:
        return UserInDB(**user.__dict__)
    return


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | bool:
    user = get_user_schema(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    else:
        return user
