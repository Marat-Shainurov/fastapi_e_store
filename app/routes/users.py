from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.config import SessionLocal
from app.schemas import UserCreate, UserInDB, Token
from app.services.authentication import authenticate_user
from app.services.crud_users import add_user, oauth2_scheme, get_current_active_user
from app.services.tokens import create_access_token, get_password_hashed, ACCESS_TOKEN_EXPIRES_MINUTES
from app.database.db import get_db

router = APIRouter(
    prefix='/users',
    tags=['users'],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_users(user: UserCreate, db: Session = Depends(get_db)):
    new_user = add_user(db=db, user=user)
    return new_user


@router.get("/read/request-user")
async def read_request_user(request_user: UserInDB = Depends(get_current_active_user)):
    return request_user


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
