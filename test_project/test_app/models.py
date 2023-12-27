"""Models for test_app."""
from django.db import models

from great_django_family import GetOrNew


# Create your models here.
class TestGetOrNew(GetOrNew):
    """Implemntation of a model using GetOrNew."""

    name = models.CharField(max_length=100)

    class Meta:
        """Meta class for TestGetOrNew."""

        app_label = "test_app"
