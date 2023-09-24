from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Benzokolon1@localhost:5432/fastapi_store"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

association_table = Table(
    "association_baskets_products",
    Base.metadata,
    Column("baskets_id", ForeignKey("baskets.id"), primary_key=True),
    Column("products_id", ForeignKey("products.id"), primary_key=True),
)
