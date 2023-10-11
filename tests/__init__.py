from tests.tests_users import test_create_user, test_create_user_verify_email, test_get_users, test_get_user, \
    test_update_user, test_partial_update, test_delete_user
from tests.tests_products import test_create_product, test_retrieve_product, test_get_products, test_update_product, \
    test_partial_update_product, test_delete_product
from tests.tests_baskets import test_create_basket, test_get_basket, test_get_baskets, test_add_products_to_basket, \
    test_remove_products_from_basket, test_delete_basket

__all__ = [
    'test_create_user', 'test_create_user_verify_email', 'test_get_users', 'test_get_user', 'test_update_user',
    'test_partial_update', 'test_delete_user',
    'test_create_product', 'test_retrieve_product', 'test_get_products', 'test_update_product',
    'test_partial_update_product', 'test_delete_product',
    'test_create_basket', 'test_get_basket', 'test_get_baskets', 'test_add_products_to_basket',
    'test_remove_products_from_basket', 'test_delete_basket',
]
