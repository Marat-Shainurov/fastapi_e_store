from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import UserCreate, UserInDB, Token, UserBase
from app.services import add_user, get_current_active_user, get_users, update_user, destroy_user, create_access_token, \
    authenticate_user
from app.services.tokens import ACCESS_TOKEN_EXPIRES_MINUTES

router = APIRouter(
    prefix='/users',
    tags=['users'],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


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


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_users(
        user: UserCreate, current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    new_user = add_user(db=db, user=user)
    return new_user


@router.get("/", response_model=list[UserInDB], status_code=status.HTTP_200_OK)
async def read_users(current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return get_users(db=db)


@router.get("/current-user", status_code=status.HTTP_200_OK)
async def read_request_user(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user


@router.put("/{username}", response_model=UserInDB, status_code=status.HTTP_200_OK)
async def put_user(username: str, user_to_update: UserBase, current_user: UserInDB = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    return update_user(db=db, username=username, user_to_update=user_to_update)


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str, current_user: UserInDB = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):
    return destroy_user(db=db, username=username)
