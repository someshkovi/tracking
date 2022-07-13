from django.test import TestCase
from products.models import Product


class ProductCreateTestCase(TestCase):

    def setUp(self):
        Product.objects.create(name='tp1')
        Product.objects.create(name='test product 2', price=100)

    def test_products_price(self):
        p1 = Product.objects.get(name='tp1')
        self.assertIsNone(p1.url)
        self.assertFalse(p1.is_url_valid)
