from sqlalchemy.orm import Session

from app.models import User
from app.services.tokens import get_password_hashed
from app.schemas import UserCreate


def add_user(db: Session, user: UserCreate):
    hashed_pwd = get_password_hashed(plain_password=user.password)
    new_user = User(
        name=user.name, last_name=user.last_name, username=user.username, email=user.email, phone=user.phone,
        hashed_password=hashed_pwd, is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user():
    pass


def get_users():
    pass


def update_user():
    pass


def delete_user():
    pass
