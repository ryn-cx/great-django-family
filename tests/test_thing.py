"""Test great-django-family."""

from __future__ import annotations

import datetime
from io import StringIO

import pytest
from django.core.management import call_command
from django.db import models

from src.great_django_family import auto_unique
from test_project.test_app.models import (
    ImplementedGetOrNew,
    ImplementedModelWithTimestamps,
)

CURRENT_TIMESTAMP = datetime.datetime.now().astimezone()
PAST_TIMESTAMP = CURRENT_TIMESTAMP - datetime.timedelta(days=1)
FUTURE_TIMESTAMP = CURRENT_TIMESTAMP + datetime.timedelta(days=1)
OPTIONS: list[datetime.datetime | None] = [
    None,
    PAST_TIMESTAMP,
    CURRENT_TIMESTAMP,
    FUTURE_TIMESTAMP,
]
TIMESTAMP_COMBINATIONS: list[
    tuple[datetime.datetime | None, datetime.datetime | None]
] = [(a, b) for a in OPTIONS for b in OPTIONS]


# Based on code from: https://stackoverflow.com/a/73588607 It's easier to test
# an actual implementation of an abstract model than it is to test the abstract
# model itself. One problem is that you could modify the abstract model and
# those changes will not be reflected in the implemented model until after
# migrations are made, to avoid this always check if any migrations are missing
# before running the tests.
class TestForMigrations:
    @pytest.mark.django_db
    def test_for_missing_migrations(self) -> None:
        output = StringIO()
        call_command("makemigrations", no_input=True, dry_run=True, stdout=output)
        assert output.getvalue().strip() == "No changes detected"


class TestAutoUnique:
    def test_auto_unique(self) -> None:
        # Auto unique dynamically gets the class name when executed so it needs
        # to be tested in a nested class that is the same as a real one that
        # would be used in a Django project. The class is used implicitly so the
        # error needs to be ignored.
        class ModelName:  # type: ignore[reportUnusedClass]
            class Meta:
                assert auto_unique("field1", "field2") == models.UniqueConstraint(
                    fields=("field1", "field2"),
                    name="UQ_ModelName_field1-field2",
                )


@pytest.mark.django_db
class TestGetOrNew:
    def test_get_or_new_new_object(self) -> None:
        instance, missing = ImplementedGetOrNew.objects.get_or_new(name="test")
        assert missing is True
        assert instance.name == ImplementedGetOrNew(name="test").name

    def test_get_or_new_existing_object(self) -> None:
        instance, _missing = ImplementedGetOrNew.objects.get_or_new(name="test")
        instance.save()
        obj2, missing = ImplementedGetOrNew.objects.get_or_new(name="test")
        assert missing is False
        assert obj2.id == instance.id


@pytest.mark.django_db
class TestModelWithTimestamps:
    def test_no_entry_up_to_date(self) -> None:
        instance = ImplementedModelWithTimestamps(name="test")
        for info_timestamp, modified_timestamp in TIMESTAMP_COMBINATIONS:
            assert instance.is_up_to_date(info_timestamp, modified_timestamp) is False
            assert instance.is_outdated(info_timestamp, modified_timestamp) is True

    def test_existing_entry_up_to_date(self) -> None:
        instance = ImplementedModelWithTimestamps(name="test")
        instance.add_timestamps_and_save(CURRENT_TIMESTAMP)

        for info_timestamp, modified_timestamp in TIMESTAMP_COMBINATIONS:
            is_up_to_date = FUTURE_TIMESTAMP not in (info_timestamp, modified_timestamp)
            output = instance.is_up_to_date(info_timestamp, modified_timestamp)
            assert output is is_up_to_date

            is_outdated = FUTURE_TIMESTAMP in (info_timestamp, modified_timestamp)
            output = instance.is_outdated(info_timestamp, modified_timestamp)
            assert output is is_outdated
