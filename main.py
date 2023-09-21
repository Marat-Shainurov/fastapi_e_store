from fastapi import FastAPI

from app.database.config import SessionLocal
from app.routes.users import router as users_router
from app.routes.products import router as products_router

app = FastAPI()

app.include_router(users_router)
app.include_router(products_router)