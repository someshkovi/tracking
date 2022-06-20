from typing import List, Union

import requests

from scripts.flipkart import get_flipkart_product_info
from scripts.amazon import get_amazon_product_info
from scripts.rest_calls import update_data, ProductRestCalls
from scripts.constants import Constants


def fetch_single_product_data(product):
    url = product.get('url')
    if 'amazon.in' in url:
        fetch_data = get_amazon_product_info('url')

    if 'flipkart.com' in url:
        fetch_data = get_flipkart_product_info('url')

    for param in ['price', 'rating', 'ratings_count', 'reviews_count', 'availability_message', 'availability']:
        product[param] = fetch_data.get(param, product.get(param))

    if (product.get('name') is None) and (fetch_data.get('name') is not None):
        product['name'] = fetch_data['name']


def add_product(data):
    add_response = ProductRestCalls('http://localhost:8000', 's', 's').add_product(data)
    return add_response


def update_product_data(product_id, data):
    update_response = ProductRestCalls('http://localhost:8000', 's', 's').update_product(product_id, data)
    return update_response


def get_products() -> dict:
    get_response = ProductRestCalls('http://localhost:8000', 's', 's').get_products()
    if get_response['status'] == Constants.SUCCESS:
        products = get_response['data']
        return {
            'status': Constants.SUCCESS,
            'data': products
        }
    else:
        return {
            'status': Constants.FAILURE,
            'data': response
        }


def test():
    response = get_products()
    if response['status'] == Constants.SUCCESS:
        products = response['data']
        print(products)

    response = add_product({'name': 'another product', 'price': 101})
    print(response.json())

    response = update_product_data(response.json()['data']['id'], {'name': 'modified_product'})
    print(response.json())


if __name__ == '__main__':
    test()
