"""Models for test_app."""

from django.db import models

from great_django_family import ModelWithGetOrNew, ModelWithId


# Create your models here.
class ImplementedGetOrNew(ModelWithId, ModelWithGetOrNew):
    """Implemntation of a model using GetOrNew."""

    name = models.CharField(max_length=100)

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta class for TestGetOrNew."""

        app_label = "test_app"
