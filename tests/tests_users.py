from fastapi import status

from tests.conftest import client


def test_create_user(db_session):
    data = {
        "name": "Name",
        "last_name": "Surname",
        "username": "n_surname",
        "email": "n_surname@gmail.com",
        "phone": "+74157650847",
        "password": "QWE123qwe123!"
    }
    response = client.post("/users/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['email'] == 'n_surname@gmail.com'
    assert response.json()['is_active'] is False
    assert response.json()['phone'] == '+74157650847'
    assert isinstance(response.json()['hashed_password'], str) is True
    assert isinstance(response.json()['verification_code'], str) is True
    assert response.json()['username'] == 'n_surname'
    assert response.json()['products'] == []
