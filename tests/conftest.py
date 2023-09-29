import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.database.config import Base
from main import app

TEST_DATABASE_URL = "postgresql://postgres:Benzokolon1@localhost:5432/tests_fastapi_store"

engine = create_engine(TEST_DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        transaction.rollback()
        session.close()
        connection.close()
