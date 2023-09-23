from typing import Type

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.database.db import get_db
from app.models import User
from app.schemas import UserCreate, TokenData, UserInDB, UserBase, UserBaseUpdate
from app.services.tokens import get_password_hashed, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


def get_user(db: Session, username: str) -> Type[User]:
    user = db.query(models.User).filter(User.username == username).first()
    if user:
        return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Type[User]:
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


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def add_user(db: Session, user: UserCreate) -> User:
    hashed_pwd = get_password_hashed(plain_password=user.password)
    new_user = User(
        name=user.name, last_name=user.last_name, username=user.username, email=user.email, phone=user.phone,
        hashed_password=hashed_pwd, is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session) -> list[Type[User]]:
    return db.query(User).all()


def put_user(db: Session, username: str, user_to_update: UserBase) -> Type[User]:
    user = db.query(User).filter(User.username == username)
    if user:
        user.update(values={**user_to_update.model_dump()})
        updated_user = db.query(User).filter(User.username == username).first()
        db.commit()
        db.refresh(updated_user)
        return updated_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No user found"
    )


def patch_user(db: Session, username, user_to_update: UserBaseUpdate) -> Type[User]:
    stored_user = db.query(User).filter_by(username=username).one_or_none()
    if stored_user:
        stored_data_schema = UserBase(**stored_user.__dict__)
    else:
        stored_data_schema = UserBase()
    update_data = user_to_update.model_dump(exclude_unset=True)
    updated_user_schema = stored_data_schema.model_copy(update=update_data)
    user_to_update_db = db.query(User).filter_by(username=username)
    user_to_update_db.update(values={**updated_user_schema.model_dump()})
    db.commit()
    db.refresh(user_to_update_db.one_or_none())
    return db.query(User).filter_by(username=username).one_or_none()


def destroy_user(db: Session, username: str) -> None:
    db.query(User).filter(User.username == username).delete(synchronize_session=False)
    db.commit()
