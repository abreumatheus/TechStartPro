from django.apps import apps
from django.test import TestCase

from product.apps import ProductConfig
from product.models import Product


class TestProductAppConfig(TestCase):
    def test_apps(self):
        self.assertEqual(ProductConfig.name, 'product')
        self.assertEqual(apps.get_app_config('product').name, 'product')


class TestProductModels(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='iPhone', price=399.99, description='Test')
        self.product.categories.create(name='Cell')

    def test_product_model_should_be_instantiated_correctly(self):
        self.assertIsInstance(self.product, Product)
        self.assertIsNotNone(self.product.id)
        self.assertIsNotNone(self.product.created_at)
        self.assertIsNotNone(self.product.updated_at)
        self.assertEqual('iPhone', self.product.name)

    def test_product_model_should_have_correct_str_representation(self):
        self.assertEqual("iPhone - ['Cell']", str(self.product))
