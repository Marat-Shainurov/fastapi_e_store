from fastapi import FastAPI

from app.database.config import SessionLocal
from app.routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
