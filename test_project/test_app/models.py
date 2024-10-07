"""Models for test_app."""

from django.db import models

from src.great_django_family import (
    ModelWithGetOrNew,
    ModelWithId,
    ModelWithTimestampsAndFunctions,
)


# Create your models here.
class ImplementedGetOrNew(ModelWithId, ModelWithGetOrNew):
    """Implemntation of a model using GetOrNew."""

    name = models.CharField(max_length=100)

    # This is defined just to clear up some false positives from Pylance
    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta class for TestGetOrNew."""


class ImplementedModelWithTimestamps(ModelWithId, ModelWithTimestampsAndFunctions):
    """Implemntation of a model using GetOrNew."""

    name = models.CharField(max_length=100)

    # This is defined just to clear up some false positives from Pylance
    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta class for TestGetOrNew."""
