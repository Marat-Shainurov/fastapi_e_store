from fastapi import status
from fastapi.testclient import TestClient

from app.models import User
from main import app
from tests.conftest import user_data
from tests.testing_services import verify_email_for_tests, get_auth_header_for_tests, delete_object_for_tests

client = TestClient(app)


def test_create_user(db_session):
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['email'] == user_data['email']
    assert response.json()['is_active'] is False
    assert response.json()['phone'] == user_data['phone']
    assert isinstance(response.json()['hashed_password'], str) is True
    assert isinstance(response.json()['verification_code'], str) is True
    assert response.json()['username'] == user_data['username']
    assert response.json()['products'] == []
    user = db_session.query(User).filter_by(username=response.json()['username']).one()
    delete_object_for_tests(obj=user, db_session=db_session)


def test_create_user_verify_email(db_session):
    response = client.post("/users/", json=user_data)
    username = response.json()["username"]
    verification_code = response.json()["verification_code"]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["is_active"] is False
    assert response.json()["username"] == "n_surname"

    user = db_session.query(User).filter_by(username=username).first()
    assert user.username == "n_surname"
    response_verification = client.post(f"/users/{username}/verify-email?code={verification_code}")
    assert response_verification.json()["message"] == "You email is verified! Thank you!"
    db_session.commit()

    user = db_session.query(User).filter_by(username=username).first()
    assert user.is_active is True
    delete_object_for_tests(obj=user, db_session=db_session)


def test_get_users(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response_users = client.get("/users", headers=header)
    assert response_users.status_code == status.HTTP_200_OK
    assert response_users.json() == [
        {'id': response_users.json()[0]['id'], 'name': user_data['name'], 'last_name': user_data['last_name'],
         'username': user_data['username'], 'email': user_data['email'], 'phone': user_data['phone'], 'is_active': True,
         'products': []}]


def test_get_user(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response_get_by_username = client.get(f"/users/{user_fixture.username}?get_user_by=username", headers=header)
    response_get_by_email = client.get(f"/users/{user_fixture.email}?get_user_by=email", headers=header)
    response_get_by_phone = client.get(f"/users/{user_fixture.phone}?get_user_by=phone", headers=header)

    assert response_get_by_username.status_code == status.HTTP_200_OK
    assert response_get_by_username.json()['username'] == user_data['username']
    assert response_get_by_email.status_code == status.HTTP_200_OK
    assert response_get_by_email.json()['username'] == user_data['username']
    assert response_get_by_phone.json()['username'] == user_data['username']
    assert response_get_by_phone.status_code == status.HTTP_200_OK


def test_update_user(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    data_to_update: dict = user_data.copy()
    del data_to_update['password']
    data_to_update['is_active'] = True
    data_to_update['name'] = 'updated'
    data_to_update['last_name'] = 'updated last_name'
    response_update = client.put(f"/users/{user_fixture.username}", headers=header, json=data_to_update)
    data_to_update.update({'id': user_fixture.id, 'products': []})
    assert response_update.json() == data_to_update


def test_partial_update(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response_partial_update = client.patch(f"/users/{user_fixture.username}", headers=header, json={'name': 'updated'})
    updated_data: dict = user_data.copy()
    updated_data['name'] = 'updated'
    updated_data['is_active'] = True
    del updated_data['password']
    updated_data.update({'id': user_fixture.id, 'products': []})
    assert response_partial_update.json() == updated_data
    assert response_partial_update.status_code == status.HTTP_200_OK


def test_delete_user(db_session):
    response_create = client.post("/users/", json=user_data)
    verify_email_for_tests(client=client, username=response_create.json()['username'],
                           verification_code=response_create.json()['verification_code'])
    header = get_auth_header_for_tests(
        client=client, password=user_data['password'], username=response_create.json()['username'])

    users = db_session.query(User).all()
    assert users[0].username == response_create.json()['username']

    response_delete = client.delete(f"/users/{response_create.json()['username']}", headers=header)
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    users = db_session.query(User).all()
    assert users == []
