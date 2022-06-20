import requests
from scripts.constants import Constants
import json


def get_access_token(username, password, base_url='http://localhost:8000'):
    auth_url = f"{base_url}/api/v1/users/login/"
    auth_response = requests.post(auth_url, json={'username': username, 'password': password})
    access_token = auth_response.json().get('access')
    # refresh_token = auth_response.json().get('refresh')
    return access_token


def update_data(method, url_extension, access_token, headers, payload, base_url='http://localhost:8000', files=[]):
    headers['Authorization'] = f'Bearer {access_token}'
    url = f'{base_url}{url_extension}'
    response = requests.request(method, url, headers=headers, data=payload)
    return response


def get_data(url_extension, access_token=None, headers={}, payload={}, files=None, base_url='http://localhost:8000'):
    if files is None:
        files = []
    if access_token is not None:
        headers['Authorization'] = f'Bearer {access_token}'
    url = f'{base_url}{url_extension}'
    response = requests.request('GET', url, headers=headers, data=payload, files=files)
    return response


class RestCalls:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.access_token = get_access_token(username, password, base_url)
        self.headers = {}
        self.payload = {}
        self.files = []
        self.retries = 1

    def verify_update_access_token(self):
        verify_url = f"{self.base_url}/api/v1/users/token-verify/"
        response = requests.request("POST", verify_url, json={'token': self.access_token})
        if response.status_code == 200:
            return {'status': Constants.SUCCESS}
        elif response.status_code == 401 and self.retries > 0:
            self.retries -= 1
            self.access_token = get_access_token(self.username, self.password, self.base_url)
            self.verify_update_access_token()
        else:
            return {
                'status': Constants.FAILURE,
                'error_msg': response.text,
                'response': response
            }


class ProductRestCalls(RestCalls):
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)
        self.products = None
        self.get_products_url_ext = '/api/v1/product/'
        self.add_product_url_ext = '/api/v1/product/'

    def update_headers_with_token(self, token):
        self.headers['Authorization'] = f"Bearer {token}"

    def get_products(self):
        token_validation = self.verify_update_access_token()
        if token_validation.get('status') == Constants.SUCCESS:
            products_response = get_data(self.get_products_url_ext,
                                         self.access_token,
                                         self.headers,
                                         self.payload,
                                         self.files,
                                         self.base_url)
            if products_response.status_code == 200:
                self.products = products_response.json().get('results')
                return {
                    'status': Constants.SUCCESS,
                    'data': self.products
                }
            return {
                'status': Constants.FAILURE,
                'data': products_response
            }
        return {
            'status': Constants.FAILURE,
        }

    def add_product(self, data):
        self.verify_update_access_token()
        self.payload = data
        self.update_headers_with_token(self.access_token)
        endpoint = self.base_url + self.add_product_url_ext
        response = requests.post(endpoint, json=data, headers=self.headers)
        return response

    def update_product(self, product_id, data):
        self.verify_update_access_token()
        self.payload = data
        product_update_url = f'{self.add_product_url_ext}{product_id}/'
        endpoint = self.base_url + product_update_url
        self.update_headers_with_token(self.access_token)
        response = requests.request("PATCH", endpoint, headers=self.headers, json=data)
        return response
