from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.database.db import get_db
from app.models import User
from app.schemas import UserCreate, TokenData, UserInDB
from app.services.tokens import get_password_hashed, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


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


def get_user(db: Session, username: str) -> UserInDB | None:
    user = db.query(models.User).filter(User.username == username).first()
    if user:
        return UserInDB(**user.__dict__)
    return


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_users():
    pass


def update_user():
    pass


def delete_user():
    pass
