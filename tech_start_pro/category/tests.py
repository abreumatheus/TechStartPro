from unittest.mock import patch, call

from django.apps import apps
from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
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


class TestImportCommand(TestCase):
    @patch('builtins.print', return_value='Finished!')
    def test_command_should_output_finished(self, mock_print):
        call_command('import_categories', 'category/test_dummy_data/import-test.csv')
        mock_print.assert_called_with('Finished!')

    def test_command_with_invalid_filetype_should_raise_exception(self):
        with self.assertRaises(Exception) as context:
            call_command('import_categories', 'category/test_dummy_data/__init__.py')

        self.assertEqual(context.exception.__str__(), 'Unexpected file format. Try it with a valid csv file.')

    @patch('builtins.print', return_value='Finished!')
    def test_command_should_save_categories_to_database(self, _):
        call_command('import_categories', 'category/test_dummy_data/import-test.csv')

        saved_categories = []

        for category in Category.objects.all():
            saved_categories.append(str(category))

        self.assertEqual(3, len(saved_categories))
        self.assertIn('Toys', saved_categories)
        self.assertIn('Notebooks', saved_categories)
        self.assertIn('Cellphones', saved_categories)

    @patch('builtins.print',
           side_effect=['The category "Toys" is likely already in the database. Skipping.', 'Finished!'])
    def test_command_should_warn_category_already_on_database(self, mock_print):
        call_command('import_categories', 'category/test_dummy_data/import-duplicate-test.csv')

        expected = [call('The category "Toys" is likely already in the database. Skipping.'), call('Finished!')]
        self.assertEqual(expected, mock_print.mock_calls)
