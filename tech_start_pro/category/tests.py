from django.apps import apps
from django.test import TestCase
from rest_framework.test import APITestCase

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


class TestCategoryEndpoints(APITestCase):
    def setUp(self):
        self.sample_category = Category.objects.create(name='Furniture')

        Category.objects.create(name='Toys')

        Category.objects.create(name='Cellphones')

    def test_post_request_should_create_new_category(self):
        payload = {'name': 'Decoration'}
        response = self.client.post('/api/category/', payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request_should_return_all_three_categories(self):
        response = self.client.get('/api/category/')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)

    def test_get_request_w_id_should_return_matching_category(self):
        response = self.client.get(f'/api/category/{self.sample_category.id}/')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['id'], str(self.sample_category.id))
        self.assertEqual(data['name'], self.sample_category.name)

    def test_get_request_w_search_param_should_return_matching_categories(self):
        response = self.client.get(f'/api/category/?search={self.sample_category.name}')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['name'], self.sample_category.name)

    def test_patch_request_should_partially_update_and_return_updated_category(self):
        old_object = self.client.get(f'/api/category/{self.sample_category.id}/')
        old_object_data = old_object.data

        payload = {'name': 'Computers'}
        response = self.client.patch(f'/api/category/{self.sample_category.id}/', payload)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], payload['name'])
        self.assertNotEqual(data['updated_at'], old_object_data['updated_at'])

    def test_put_request_should_update_and_return_updated_category(self):
        old_object = self.client.get(f'/api/category/{self.sample_category.id}/')
        old_object_data = old_object.data

        payload = {'name': 'Notebooks'}
        response = self.client.put(f'/api/category/{self.sample_category.id}/', payload)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], payload['name'])
        self.assertNotEqual(data['updated_at'], old_object_data['updated_at'])

    def test_delete_request_should_return_http_status_204_and_delete_category(self):
        delete_response = self.client.delete(f'/api/category/{self.sample_category.id}/')
        get_response = self.client.get('/api/category/')
        data = get_response.data

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(data['count'], 2)
        self.assertTrue(all(category['id'] != self.sample_category.id for category in data['results']))
