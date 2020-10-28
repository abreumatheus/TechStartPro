import time

from decouple import config
from django.test import TestCase
from selenium import webdriver

from core.models import AbstractBaseModel


class TestAbstractBaseModel(TestCase):
    def setUp(self):
        self.base_model = AbstractBaseModel()

    def test_abstract_base_model_should_be_instantiated_correctly(self):
        self.assertIsInstance(self.base_model, AbstractBaseModel)
        self.assertIsNotNone(self.base_model.id)
        self.assertIsNone(self.base_model.created_at)
        self.assertIsNone(self.base_model.updated_at)


class TestDocumentationFunctional(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(config("APP_DOCS_URL", default='http://127.0.0.1:8000/'))

    def tearDown(self):
        self.driver.quit()

    def test_tech_start_pro_api_in_page_title(self):
        self.assertIn("TechStartPro API", self.driver.title)

    def test_page_displays_correct_email_address(self):
        time.sleep(3)
        self.assertTrue(self.driver.find_elements_by_link_text('abreumatheus@icloud.com'))

    def test_page_displays_correct_license_type(self):
        time.sleep(3)
        self.assertTrue(self.driver.find_elements_by_link_text('MIT License'))

    def test_all_operations_listed(self):
        time.sleep(3)
        category_operations = ['category_list', 'category_create', 'category_read', 'category_update',
                               'category_partial_update', 'category_delete']
        product_operations = ['product_list', 'product_create', 'product_read', 'product_update',
                              'product_partial_update', 'product_delete']

        all_operations = [*category_operations, *product_operations]

        main_div = self.driver.find_element_by_class_name('api-content')

        self.assertTrue(all(main_div.find_element_by_id(f'operation/{name}') for name in all_operations))
