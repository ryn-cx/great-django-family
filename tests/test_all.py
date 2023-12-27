"""Test great-django-family."""
from __future__ import annotations

import pytest
from django.db import models

from great_django_family import auto_unique
from test_project.test_app.models import TestGetOrNew


class TestAutoUnique:
    """Test model for testing."""

    def test_auto_unique(self) -> None:
        """Test that auto_test works."""

        # These nested classes are reuqired for the test to represent how they would be used in an actual project
        class ModelName:  # type: ignore  # noqa: PGH003 - This model is used implicitly in the test
            class Meta:
                assert auto_unique("field1", "field2") == models.UniqueConstraint(
                    fields=("field1", "field2"),
                    name="ModelName_field1,field2",
                )


class TestIt:
    """Test the GetOrNew mixin."""

    @pytest.mark.django_db()
    def test_get_or_new(self) -> None:
        """Test that get_or_new works."""
        # Test for an object that does not exist
        obj, missing = TestGetOrNew().get_or_new(name="test")
        assert missing is True
        assert obj.name == TestGetOrNew(name="test").name

        # Save object for next test
        obj.save()

        # Test for an object that already exists
        obj2, missing = TestGetOrNew().get_or_new(name="test")
        assert missing is False
        assert obj2.pk == obj.pk
