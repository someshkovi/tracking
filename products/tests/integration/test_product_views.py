from django.test import TestCase, Client
from django.urls import reverse

from products.models import Product
from accounts.models import User


class ProductCreateTestCase(TestCase):

    def setUp(self):
        self.username = 'tester'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        # self.client.post('/login/', {'username': self.username, 'password': self.password})
        self.p1 = Product.objects.create(
            name='tp1',
            price=100,
            url='https://www.amazon.in/Sony-WH-1000XM4-Cancelling-Headphones-Bluetooth/dp/B0863FR3S9/ref=sr_1_3'
                '?keywords=sony%2Bmx1000m4&qid=1652684397&sprefix=sony%2Bmx%2Caps%2C629&sr=8-3&th=1',
            user=self.user)

    def test_ProductsListView(self):
        response = self.client.get('/products/all/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['product_list']), 1)
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_ProductDetailView(self):
        response = self.client.get(reverse('products:product-detail', kwargs={'pk': self.p1.id}))
        self.assertEqual(response.status_code, 200)
        get_product = response.context_data['product']
        self.assertEqual(get_product.name, 'tp1')
        self.assertEquals(get_product.price, response.context_data['product'].min_price, 100)
        self.assertEqual(get_product.availability, False)
        self.assertEqual(get_product.is_url_valid, False)

    def test_ProductUpdateView(self):
        response = self.client.post(
            reverse('products:product-update', kwargs={'pk': self.p1.id}),
            {
                # 'name': 'tp1',
                # 'category':
                # 'price': 250,
                # 'url': 'test_url',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.price, 250)
