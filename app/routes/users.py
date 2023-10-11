from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.db import get_db
from app.schemas import UserCreate, UserInDB, Token, UserBase, UserBaseUpdate, UserBasePut, UserOutput
from app.schemas.users import GetUserBy
from app.services import add_user, get_current_active_user, get_users, put_user, destroy_user, create_access_token, \
    authenticate_user, patch_user, verify_email, get_user
from app.services.tokens import ACCESS_TOKEN_EXPIRES_MINUTES

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_users(user: UserCreate, db: Session = Depends(get_db)):
    new_user = await add_user(db=db, user=user)
    return new_user


@router.post("/{username}/verify-email")
def verify_user_email(username: str, code: str, db: Session = Depends(get_db)):
    result = verify_email(db=db, username=username, verification_code=code)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result})


@router.get("/", response_model=list[UserOutput], status_code=status.HTTP_200_OK)
def read_users(offset: int = 0, limit: int = 100,
               current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return get_users(db=db, offset=offset, limit=limit)


@router.get("/current-user", status_code=status.HTTP_200_OK)
def read_request_user(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user


@router.get("/{get_by_value}", response_model=UserOutput, status_code=status.HTTP_200_OK)
def retrieve_user(get_user_by: GetUserBy, get_by_value: str,
                  current_user: UserInDB = Depends(get_current_active_user),
                  db: Session = Depends(get_db)):
    return get_user(db=db, get_by=get_user_by.value, get_by_value=get_by_value)


@router.put("/{username}", response_model=UserOutput, status_code=status.HTTP_200_OK)
def update_user(username: str, user: UserBasePut, current_user: UserInDB = Depends(get_current_active_user),
                db: Session = Depends(get_db)):
    return put_user(db=db, username=username, user_to_update=user)


@router.patch("/{username}", response_model=UserOutput, status_code=status.HTTP_200_OK)
def partial_update_user(username: str, user: UserBaseUpdate, db: Session = Depends(get_db),
                        current_user: UserInDB = Depends(get_current_active_user), ):
    return patch_user(db=db, user_to_update=user, username=username)


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, current_user: UserInDB = Depends(get_current_active_user),
                db: Session = Depends(get_db)):
    return destroy_user(db=db, username=username)
