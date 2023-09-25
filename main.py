from fastapi import FastAPI

from app.routes.baskets import router as baskets_router
from app.routes.products import router as products_router
from app.routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(products_router)
app.include_router(baskets_router)
