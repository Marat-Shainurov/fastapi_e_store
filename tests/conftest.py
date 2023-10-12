import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.database.config import TESTING, SessionLocal
from app.models import User, Product, Basket
from main import app
from tests.testing_services import verify_email_for_tests, get_auth_header_for_tests, delete_object_for_tests

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
    verify_email_for_tests(
        client=client, username=response_create.json()['username'],
        verification_code=response_create.json()['verification_code'])
    user = db_session.query(User).filter_by(username=data['username']).one()
    yield user
    db_session.delete(user)
    db_session.commit()


product_data = {
    "name": "Test",
    "price": 1000
}


@pytest.fixture(scope='function')
def product_fixture(db_session, user_fixture):
    client = TestClient(app)
    header = get_auth_header_for_tests(client=client, password=user_data['password'], username=user_fixture.username)
    response = client.post("/products", headers=header, json=product_data)
    assert response.json()['name'] == product_data['name']
    assert response.json()['price'] == product_data['price']
    assert response.json()['owner_id'] == user_fixture.id
    product = db_session.query(Product).filter_by(name=response.json()['name']).first()
    yield product

    db_session.delete(product)
    db_session.commit()


@pytest.fixture(scope='function')
def basket_fixture(db_session, user_fixture):
    client = TestClient(app)
    header = get_auth_header_for_tests(client=client, username=user_fixture.username, password=user_data['password'])
    product_data_for_basket = {
        "name": "Product 1",
        "price": 1000
    }
    response_product_1 = client.post("/products", headers=header, json=product_data_for_basket)
    assert response_product_1.status_code == status.HTTP_201_CREATED

    product_data_2 = product_data_for_basket.copy()
    product_data_2['name'] = 'Product 2'
    response_product_2 = client.post("/products", headers=header, json=product_data_2)
    assert response_product_2.status_code == status.HTTP_201_CREATED

    product_1 = db_session.query(Product).filter_by(name=response_product_1.json()['name']).first()
    product_2 = db_session.query(Product).filter_by(name=response_product_2.json()['name']).first()

    response_basket = client.post(
        f"/baskets/?products={product_1.id}&products={product_2.id}", headers=header)
    basket = db_session.query(Basket).filter_by(id=response_basket.json()['id']).one_or_none()
    assert response_basket.status_code == status.HTTP_201_CREATED

    yield basket

    delete_object_for_tests(obj=product_1, db_session=db_session)
    delete_object_for_tests(obj=product_2, db_session=db_session)
    delete_object_for_tests(obj=basket, db_session=db_session)
