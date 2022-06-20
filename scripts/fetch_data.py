import json

from scripts.constants import Constants
from scripts.amazon import get_amazon_product_info, get_amazon_results_by_search
from scripts.flipkart import get_flipkart_product_info


def store_update_price(product_url, service='amazon.in', limit=10_00_00_000):
    if 'amazon.in' in product_url:
        response = get_amazon_product_info(product_url)
    elif 'flipkart.com' in product_url:
        response = get_flipkart_product_info(product_url)
    else:
        response = {
            'status': Constants.ERROR
        }
    if response.get('status') == Constants.SUCCESS:
        title = response['data'].get('name')
        price = response['data'].get('price')
        availability = response['data'].get('availability')
        availability_message = response['data'].get('availability_message')
        is_url_valid = True
    else:
        title, price, availability, availability_message, is_url_valid = None, None, None, None, False
    # if title is not None and price < limit and available:
    #     # message = f'Price below limit : \n {title} \n Price: {price} \n {product_url} \n\n'
    json_response = json.dumps({
        'title': title,
        'price': price,
        'product_url': product_url,
        'availability': availability,
        'availability_message': availability_message,
        'is_url_valid': is_url_valid
    })
    return json_response
