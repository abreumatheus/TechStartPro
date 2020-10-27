from django.db import models

from category.models import Category
from core.models import AbstractBaseModel


class Product(AbstractBaseModel):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        categories = self.categories.order_by('name')
        return f'{self.name} - {[category.name for category in categories]}'
