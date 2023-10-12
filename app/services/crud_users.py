from typing import Type

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.database.db import get_db
from app.emails import get_verification_code, send_mail
from app.models import User
from app.schemas import UserCreate, TokenData, UserInDB, UserBaseUpdate, EmailSchema, UserBasePut
from app.services import get_password_hashed
from app.services.tokens import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


def get_user_by_username(db: Session, username: str) -> Type[User]:
    user = db.query(models.User).filter(User.username == username).one_or_none()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User '{username}' not found!"
    )


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter_by(email=email).one_or_none()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User with '{email}' email not found!"
    )


def get_user_by_phone(db: Session, phone: str):
    user = db.query(User).filter_by(phone=phone).one_or_none()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User with '{phone}' phone number not found!"
    )


def get_user(get_by: str, get_by_value: str, db: Session):
    if get_by == 'username':
        return get_user_by_username(db, get_by_value)
    elif get_by == 'email':
        return get_user_by_email(db, get_by_value)
    else:
        return get_user_by_phone(db, get_by_value)


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
    user = get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def verify_email(db: Session, username: str, verification_code: str):
    user = db.query(User).filter_by(username=username).one_or_none()
    if user:
        code_to_check_db = user.verification_code
        if code_to_check_db == verification_code:
            user.is_active = True
            db.commit()
            return 'You email is verified! Thank you!'
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid verification code!'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {username} not found!'
        )


async def add_user(db: Session, user: UserCreate):
    hashed_pwd = get_password_hashed(plain_password=user.password)
    code = get_verification_code()
    new_user = User(
        name=user.name, last_name=user.last_name, username=user.username, email=user.email, phone=user.phone,
        hashed_password=hashed_pwd, verification_code=code,
    )
    email_schema = EmailSchema(email=[user.email])
    await send_mail(email=email_schema, verification_code=code)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, offset: int, limit: int) -> list[Type[User]]:
    return db.query(User).offset(offset).limit(limit).all()


def put_user(db: Session, username: str, user_to_update: UserBasePut) -> Type[User]:
    user = db.query(User).filter(User.username == username)
    if user.one_or_none():
        user.update(values={**user_to_update.model_dump()})
        updated_user = db.query(User).filter_by(username=user_to_update.model_dump().get('username')).first()
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
        stored_data_schema = UserBaseUpdate(**stored_user.__dict__)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User {username} not found")
    update_data = user_to_update.model_dump(exclude_unset=True)
    updated_user_schema = stored_data_schema.model_copy(update=update_data)
    user_to_update_db = db.query(User).filter_by(username=username)
    user_to_update_db.update(values={**updated_user_schema.model_dump()})
    db.commit()
    db.refresh(user_to_update_db.one())
    return db.query(User).filter_by(username=updated_user_schema.model_dump().get('username')).one()


def destroy_user(db: Session, username: str) -> None:
    user = db.query(User).filter(User.username == username).one_or_none()
    if user:
        db.delete(user)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {username} not found"
        )
