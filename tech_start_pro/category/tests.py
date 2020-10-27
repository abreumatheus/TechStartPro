from django.apps import apps
from django.test import TestCase

from .apps import CategoryConfig


class TestCategoryAppConfig(TestCase):
    def test_apps(self):
        self.assertEqual(CategoryConfig.name, 'category')
        self.assertEqual(apps.get_app_config('category').name, 'category')
