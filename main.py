from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.baskets import router as baskets_router
from app.routes.products import router as products_router
from app.routes.users import router as users_router

origins = ["http://localhost:8000"]
app = FastAPI()

app.include_router(users_router)
app.include_router(products_router)
app.include_router(baskets_router)
app.add_middleware(CORSMiddleware, allow_origins=origins)
