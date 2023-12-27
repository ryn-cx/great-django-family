from __future__ import annotations

from django.db import models

from great_django_family import auto_unique


class TestGreatDjangoFamily:
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
