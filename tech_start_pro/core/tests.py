from django.test import TestCase

from core.models import AbstractBaseModel


class TestAbstractBaseModel(TestCase):
    def setUp(self):
        self.base_model = AbstractBaseModel()

    def test_abstract_base_model_should_be_instantiated_correctly(self):
        self.assertIsInstance(self.base_model, AbstractBaseModel)
        self.assertIsNotNone(self.base_model.id)
        self.assertIsNone(self.base_model.created_at)
        self.assertIsNone(self.base_model.updated_at)
