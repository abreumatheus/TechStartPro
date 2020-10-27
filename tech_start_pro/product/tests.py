from django.apps import apps
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

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


class TestProductEndpoints(APITestCase):
    def setUp(self):
        self.sample_product = Product.objects.create(name='iPhone', price=399.99, description='Test')
        self.sample_category = self.sample_product.categories.create(name='Cell')

        product2 = Product.objects.create(name='LG Notebook', price=2999.99, description='Test')
        product2.categories.create(name='Notebook')

        product3 = Product.objects.create(name='Samsung TV', price=499.99, description='Test')
        product3.categories.create(name='TVs')

    def test_post_request_should_create_new_product(self):
        payload = {'name': 'S20', 'description': 'Test', 'price': 399.99, 'categories': [self.sample_category.id]}
        response = self.client.post('/api/product/', payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request_should_return_all_three_products(self):
        response = self.client.get('/api/product/')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)

    def test_get_request_w_id_should_return_matching_product(self):
        response = self.client.get(f'/api/product/{self.sample_product.id}/')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['id'], str(self.sample_product.id))
        self.assertEqual(data['name'], self.sample_product.name)

    def test_get_request_w_name_param_should_return_matching_products(self):
        name = self.sample_product.name
        response = self.client.get(f'/api/product/?name={name}')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['name'], name)

    def test_get_request_w_category_param_should_return_matching_products(self):
        category = self.sample_product.categories.get().id
        response = self.client.get(f'/api/product/?categories={category}')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['categories'][0], category)

    def test_get_request_w_price_param_should_return_matching_products(self):
        price = self.sample_product.price
        response = self.client.get(f'/api/product/?price={price}')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['price'], price)

    def test_get_request_w_description_param_should_return_matching_products(self):
        description = self.sample_product.description
        response = self.client.get(f'/api/product/?description={description}')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertEqual(data['results'][0]['description'], description)
        self.assertEqual(data['results'][1]['description'], description)
        self.assertEqual(data['results'][2]['description'], description)

    def test_get_request_w_multi_params_should_return_matching_products(self):
        category = self.sample_product.categories.get().id
        description = self.sample_product.description
        response = self.client.get(f'/api/product/?categories={category}&description={description}')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['description'], description)
        self.assertEqual(data['results'][0]['categories'][0], category)

    def test_patch_request_should_partially_update_and_return_updated_product(self):
        old_object = self.client.get(f'/api/product/{self.sample_product.id}/')
        old_object_data = old_object.data

        payload = {'name': 'Samsung Phone'}
        response = self.client.patch(f'/api/product/{self.sample_product.id}/', payload)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], payload['name'])
        self.assertNotEqual(data['updated_at'], old_object_data['updated_at'])

    def test_put_request_should_update_and_return_updated_product(self):
        old_object = self.client.get(f'/api/product/{self.sample_product.id}/')
        old_object_data = old_object.data

        payload = {'name': 'Switch', 'description': 'Test', 'price': 299.99, 'categories': [self.sample_category.id]}
        response = self.client.put(f'/api/product/{self.sample_product.id}/', payload)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], payload['name'])
        self.assertNotEqual(data['updated_at'], old_object_data['updated_at'])

    def test_delete_request_should_return_http_status_204_and_delete_product(self):
        delete_response = self.client.delete(f'/api/product/{self.sample_product.id}/')
        get_response = self.client.get('/api/product/')
        data = get_response.data

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(data['count'], 2)
        self.assertTrue(all(product['id'] != self.sample_product.id for product in data['results']))
