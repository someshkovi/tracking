from rest_framework.test import APIClient

from products.models import Product
from products.tests import base_test


class ProductCreateTestCase(base_test.NewUserTestCase):
    """
    Product create api test case
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/login/', {'username': self.username,
                                                                        'password': self.password},
                                               format='json')
        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_product_create_api(self):
        self.create_product = self.client.post('/api/v1/product/',
                                               {
                                                   'name': 'Test product',
                                                   'price': 1010
                                               })
        self.assertEquals(self.create_product.status_code, 201)
        self.assertTrue('Test product' in self.create_product.json()['data']['name'])
        self.assertEquals(1010, self.create_product.json()['data']['price'])

    def tearDown(self) -> None:
        self.client.logout()
        Product.objects.filter().delete()
        super().tearDown()


class ProductListingTestCase(base_test.NewUserTestCase):
    """
    Product list api test case
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/login/', {'username': self.username,
                                                                        'password': self.password},
                                               format='json')
        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create a new product
        self.product = Product.objects.create(name='Test product',
                                              price=2020)

    def test_product_listing_api(self):
        self.list_products = self.client.get('/api/v1/product/', format='json')
        self.assertEquals(self.list_products.status_code, 200)
        self.assertTrue(self.list_products.json()['status'])
        self.assertTrue('Test product' in self.list_products.json()['data'][0]['name'])

    def tearDown(self) -> None:
        self.client.logout()
        Product.objects.filter().delete()
        super().tearDown()


class ProductTestReadByIdCase(base_test.NewUserTestCase):
    """
    Product Read API by Id Test Case
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.product = Product.objects.create(name='Test Product', price=2021)

    def test_organization_read_by_id_api(self):
        self.read_product_by_id = self.client.get(f'/api/v1/product/{self.product.id}/', format='json')

        self.assertEquals(self.read_product_by_id.status_code, 200)
        self.assertTrue('Test Product' in self.read_product_by_id.json()['name'])
        self.assertEquals(2021, self.read_product_by_id.json()['price'])

    def tearDown(self):
        self.client.logout()
        self.product.delete()
        super().tearDown()
