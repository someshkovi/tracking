import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracking.settings')

django.setup()

from behave import fixture, use_fixture
from django.contrib.auth.models import User
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
from products.models import Product


class BaseTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        User.objects.create_superuser(username='admin', password='admin', email='admin@admin.com')

        User.objects.create(username='elon', password='roadster@123', email='elon@tesla.com',
                            first_name='elon', last_name='musk', is_active=True, is_staff=True)
        Product.objects.create(name="Roadster", price=1235)
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        User.objects.filter().delete()
        super(BaseTestCase, cls).tearDownClass()


@fixture
def django_test_case(context):
    context.test_case = BaseTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    context.selenium.quit()
    del context.test_case


def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)
