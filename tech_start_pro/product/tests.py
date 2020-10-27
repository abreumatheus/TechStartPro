from django.apps import apps
from django.test import TestCase

from product.apps import ProductConfig


class TestProductAppConfig(TestCase):
    def test_apps(self):
        self.assertEqual(ProductConfig.name, 'product')
        self.assertEqual(apps.get_app_config('product').name, 'product')
