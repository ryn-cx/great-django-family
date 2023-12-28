from __future__ import annotations

from io import StringIO

import pytest
from django.core.management import call_command
from django.db import models

from great_django_family import auto_unique
from test_project.test_app.models import ImplementedGetOrNew


# Based on code from: https://stackoverflow.com/a/73588607
# It's easier to test an actual implementation of an abstract model than it is to test the abstract model itself. One
# problem is that you could modify the abstract model and those changes will not be reflected in the implemented model
# until after migrations are made, to avoid this always check if any migrations are missing before running the tests.
@pytest.mark.django_db()
def test_for_missing_migrations() -> None:
    """Test that there are no missing migrations."""
    output = StringIO()
    call_command("makemigrations", no_input=True, dry_run=True, stdout=output)
    assert output.getvalue().strip() == "No changes detected"


class TestAutoUnique:
    """Test model for testing."""

    def test_auto_unique(self) -> None:
        """Test that auto_test works."""

        # These nested classes are reuqired for the test to represent how they would be used in an actual project
        class ModelName:  # type: ignore  # noqa: PGH003 - This model is accessed implicitly in the test
            class Meta:
                assert auto_unique("field1", "field2") == models.UniqueConstraint(
                    fields=("field1", "field2"),
                    name="ModelName_field1,field2",
                )


class TestModels:
    """Test the Models."""

    @pytest.mark.django_db()
    def test_get_or_new(self) -> None:
        """Test that get_or_new works."""
        # Test for an object that does not exist
        obj, missing = ImplementedGetOrNew.objects.get_or_new(name="test")
        assert missing is True
        assert obj.name == ImplementedGetOrNew(name="test").name

        # Save object for ne
        obj.save()

        # Get the same object

        obj2, missing = ImplementedGetOrNew.objects.get_or_new(name="test")
        assert missing is False
        assert obj2.id == obj.id
