from django.apps import apps
from django.test import TestCase

from .apps import CategoryConfig
from .models import Category


class TestCategoryAppConfig(TestCase):
    def test_apps(self):
        self.assertEqual(CategoryConfig.name, 'category')
        self.assertEqual(apps.get_app_config('category').name, 'category')


class TestCategoryModels(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Toys')

    def test_category_model_should_be_instantiated_correctly(self):
        self.assertIsInstance(self.category, Category)
        self.assertIsNotNone(self.category.id)
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)
        self.assertEqual('Toys', self.category.name)

    def test_category_model_should_have_correct_str_representation(self):
        self.assertEqual('Toys', str(self.category))
