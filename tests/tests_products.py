from dateutil.parser import parse
from fastapi import status
from fastapi.testclient import TestClient

from app.models import Product
from main import app
from tests.conftest import user_data, product_data
from tests.testing_services import get_auth_header_for_tests, delete_object_for_tests

client = TestClient(app)


def test_create_product(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response = client.post("/products", headers=header, json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == product_data['name']
    assert response.json()['price'] == product_data['price']
    assert response.json()['owner_id'] == user_fixture.id
    assert response.json()['baskets'] == []
    assert response.json()['created_at'] == response.json()['updated_at']
    assert response.json()['is_active'] is True
    product = db_session.query(Product).filter_by(name=response.json()['name']).first()
    delete_object_for_tests(obj=product, db_session=db_session)


def test_retrieve_product(db_session, user_fixture, product_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response = client.get(f"/products/{product_fixture.id}", headers=header)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict) is True
    assert response.json()['id'] == product_fixture.id
    assert response.json()['name'] == product_data['name']
    assert response.json()['price'] == product_data['price']
    assert response.json()['owner_id'] == user_fixture.id
    assert response.json()['baskets'] == []


def test_get_products(db_session, user_fixture, product_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response_product_2 = client.post("/products", json={'name': 'Test 2', 'price': 2000}, headers=header)
    product_2 = db_session.query(Product).filter_by(name=response_product_2.json()['name']).first()
    response_products = client.get("/products", headers=header)
    assert len(response_products.json()) == 2
    assert isinstance(response_products.json(), list) is True
    assert response_products.json()[1]['name'] == response_product_2.json()['name']
    assert response_products.json()[0]['name'] == product_data['name']
    delete_object_for_tests(obj=product_2, db_session=db_session)


def test_update_product(db_session, user_fixture, product_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    data_to_update = {
        "name": "Updated",
        "price": 1500,
        "owner_id": user_fixture.id,
        "is_active": True
    }
    response_update = client.put(f"/products/{product_fixture.id}", headers=header, json=data_to_update)
    assert response_update.status_code == status.HTTP_200_OK
    assert response_update.json()['name'] == data_to_update['name']
    assert response_update.json()['price'] == data_to_update['price']
    assert parse(response_update.json()['created_at']) == product_fixture.created_at
    assert parse(response_update.json()['updated_at']) > product_fixture.updated_at


def test_partial_update_product(db_session, user_fixture, product_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    data_to_update = {
        "name": "Updated partly",
        "price": 20000
    }
    response_update = client.patch(f"/products/{product_fixture.id}", headers=header, json=data_to_update)
    assert response_update.status_code == status.HTTP_200_OK
    assert response_update.json()['name'] == data_to_update['name']
    assert response_update.json()['price'] == data_to_update['price']
    assert parse(response_update.json()['created_at']) == product_fixture.created_at
    assert parse(response_update.json()['updated_at']) > product_fixture.updated_at


def test_delete_product(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response_create = client.post("/products", headers=header, json=product_data)
    response_delete = client.delete(f"/products/{response_create.json()['id']}", headers=header)
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    assert db_session.query(Product).all() == []
