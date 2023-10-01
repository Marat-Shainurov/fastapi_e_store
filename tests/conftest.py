import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.database.config import TESTING, SessionLocal
from app.models import User
from main import app

user_data = {
    "name": "Name",
    "last_name": "Surname",
    "username": "n_surname",
    "email": "n_surname@gmail.com",
    "phone": "+74157650846",
    "password": "QWE123qwe123!"
}


@pytest.fixture(scope="function")
def db_session():
    if TESTING:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


@pytest.fixture(scope='function')
def user_fixture(db_session):
    client = TestClient(app)
    data = user_data
    response_create = client.post("/users/", json=data)
    assert response_create.status_code == status.HTTP_201_CREATED
    assert response_create.json()['username'] == data['username']
    assert response_create.json()['email'] == data['email']
    user = db_session.query(User).filter_by(username=data['username']).one()
    yield user

    db_session.delete(user)
    db_session.commit()
