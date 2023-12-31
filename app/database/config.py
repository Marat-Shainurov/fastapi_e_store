import os

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = \
    f"postgresql://postgres:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:5432/{os.getenv('DB_NAME')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

association_table = Table(
    "association_baskets_products",
    Base.metadata,
    Column("baskets_id", ForeignKey("baskets.id"), primary_key=True),
    Column("products_id", ForeignKey("products.id"), primary_key=True),
)
