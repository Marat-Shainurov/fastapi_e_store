from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.config import SessionLocal
from app.schemas import UserCreate, UserInDB
from app.services.crud_users import add_user
from app.services.tokens import get_token_header, get_password_hashed
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
