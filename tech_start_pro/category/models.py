from django.db import models

from core.models import AbstractBaseModel


class Category(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name
