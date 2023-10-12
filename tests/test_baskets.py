from fastapi import status
from fastapi.testclient import TestClient

from app.models import Product, Basket
from main import app
from tests.conftest import user_data
from tests.testing_services import get_auth_header_for_tests, delete_object_for_tests

client = TestClient(app)


def test_create_basket(db_session, user_fixture):
    header = get_auth_header_for_tests(client=client, username=user_fixture.username, password=user_data['password'])
    product_data_for_basket = {
        "name": "Product 1",
        "price": 1000
    }
    response_product_1 = client.post("/products", headers=header, json=product_data_for_basket)
    assert response_product_1.status_code == status.HTTP_201_CREATED
    assert response_product_1.json()['name'] == product_data_for_basket['name']

    product_data_2 = product_data_for_basket.copy()
    product_data_2['name'] = 'Product 2'
    response_product_2 = client.post("/products", headers=header, json=product_data_2)
    assert response_product_2.status_code == status.HTTP_201_CREATED
    assert response_product_2.json()['name'] == product_data_2['name']

    product_1 = db_session.query(Product).filter_by(name=response_product_1.json()['name']).first()
    product_2 = db_session.query(Product).filter_by(name=response_product_2.json()['name']).first()

    response_basket = client.post(
        f"/baskets/?products={product_1.id}&products={product_2.id}", headers=header)
    basket = db_session.query(Basket).filter_by(id=response_basket.json()['id']).one_or_none()
    assert response_basket.status_code == status.HTTP_201_CREATED
    assert response_basket.json()['id'] == basket.id
    assert len(response_basket.json()['products']) == 2
    assert response_basket.json()['products'][0]['id'] == product_1.id
    assert response_basket.json()['products'][1]['id'] == product_2.id

    delete_object_for_tests(obj=product_1, db_session=db_session)
    delete_object_for_tests(obj=product_2, db_session=db_session)
    delete_object_for_tests(obj=basket, db_session=db_session)


def test_get_basket(db_session, user_fixture, basket_fixture):
    header = get_auth_header_for_tests(client=client, username=user_fixture.username, password=user_data['password'])
    response = client.get(f"/baskets/{basket_fixture.id}", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == basket_fixture.id
    assert len(response.json()['products']) == 2


def test_get_baskets(db_session, user_fixture, basket_fixture):
    header = get_auth_header_for_tests(client=client, username=user_fixture.username, password=user_data['password'])
    response = client.get("/baskets", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == basket_fixture.id
    assert len(response.json()[0]['products']) == 2


def test_add_products_to_basket(db_session, user_fixture, basket_fixture, product_fixture):
    header = get_auth_header_for_tests(client=client, username=user_fixture.username, password=user_data['password'])
    assert len(basket_fixture.products) == 2
    response = client.patch(
        f"/baskets/{basket_fixture.id}/add-products?products={product_fixture.id}", headers=header)
    assert len(response.json()['products']) == 3
    assert product_fixture.id in [i['id'] for i in response.json()['products']]


def test_remove_products_from_basket(db_session, user_fixture, basket_fixture):
    header = get_auth_header_for_tests(client=client, username=user_fixture.username, password=user_data['password'])
    assert len(basket_fixture.products) == 2
    response = client.patch(
        f"/baskets/{basket_fixture.id}/remove-products?products={basket_fixture.products[0].id}", headers=header)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['products']) == 1


def test_delete_basket(db_session, user_fixture, product_fixture):
    header = get_auth_header_for_tests(client=client, password=user_data['password'],
                                       username=user_fixture.username)
    response_create_basket = client.post(
        f"/baskets/?products={product_fixture.id}", headers=header)
    assert response_create_basket.status_code == status.HTTP_201_CREATED
    response_delete_basket = client.delete(f"/baskets/{response_create_basket.json()['id']}", headers=header)
    assert response_delete_basket.status_code == status.HTTP_204_NO_CONTENT
    assert db_session.query(Basket).all() == []
