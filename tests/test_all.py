# """Test great-django-family."""

# from __future__ import annotations

# import datetime
# from io import StringIO

# import pytest
# from django.core.management import call_command
# from django.db import models

# from src.great_django_family import auto_unique
# from test_project.test_project import settings
# settings.configure()
# from test_project.test_app.models import (
#     ImplementedGetOrNew,
#     ImplementedModelWithTimestamps,
# )


# CURRENT_TIMESTAMP = datetime.datetime.now().astimezone()
# PAST_TIMESTAMP = CURRENT_TIMESTAMP - datetime.timedelta(days=1)
# FUTURE_TIMESTAMP = CURRENT_TIMESTAMP + datetime.timedelta(days=1)


# # Based on code from: https://stackoverflow.com/a/73588607 It's easier to test
# # an actual implementation of an abstract model than it is to test the abstract
# # model itself. One problem is that you could modify the abstract model and
# # those changes will not be reflected in the implemented model until after
# # migrations are made, to avoid this always check if any migrations are missing
# # before running the tests.
# @pytest.mark.django_db
# def test_for_missing_migrations() -> None:
#     """Test that there are no missing migrations."""
#     output = StringIO()
#     call_command("makemigrations", no_input=True, dry_run=True, stdout=output)
#     assert output.getvalue().strip() == "No changes detected"


# class TestAutoUnique:
#     """Test model for testing."""

#     def test_auto_unique(self) -> None:
#         """Test that auto_test works."""

#         # These nested classes are reuqired for the test to represent how they would be used in an actual project
#         class ModelName:  # type: ignore  # noqa: PGH003 - This model is accessed implicitly in the test
#             class Meta:
#                 assert auto_unique("field1", "field2") == models.UniqueConstraint(
#                     fields=("field1", "field2"),
#                     name="UQ_ModelName_field1-field2",
#                 )


# @pytest.mark.django_db
# class TestGetOrNew:
#     """Test GetOrNew."""

#     def test_get_or_new(self) -> None:
#         """Test that get_or_new works."""
#         # Test for an object that does not exist
#         obj, missing = ImplementedGetOrNew.objects.get_or_new(name="test")
#         assert missing is True
#         assert obj.name == ImplementedGetOrNew(name="test").name

#         # Save object for ne
#         obj.save()

#         # Get the same object

#         obj2, missing = ImplementedGetOrNew.objects.get_or_new(name="test")
#         assert missing is False
#         assert obj2.id == obj.id


# @pytest.mark.django_db
# class TestModelWithTimestamps:
#     """Test ModelWithTimestamps."""

#     def setup_method(self) -> None:
#         """Configure the test."""
#         self.obj = ImplementedModelWithTimestamps(name="test")
#         self.timestamp = datetime.datetime.now().astimezone()
#         self.past_timestamp = self.timestamp - datetime.timedelta(days=1)
#         self.future_timestamp = self.timestamp + datetime.timedelta(days=1)

#     @pytest.mark.parametrize(
#         ("info_timestamp", "modified_timestamp"),
#         [
#             (None, None),
#             (None, PAST_TIMESTAMP),
#             (None, CURRENT_TIMESTAMP),
#             (None, FUTURE_TIMESTAMP),
#             (CURRENT_TIMESTAMP, None),
#             (CURRENT_TIMESTAMP, PAST_TIMESTAMP),
#             (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
#             (CURRENT_TIMESTAMP, FUTURE_TIMESTAMP),
#             (PAST_TIMESTAMP, None),
#             (PAST_TIMESTAMP, PAST_TIMESTAMP),
#             (PAST_TIMESTAMP, CURRENT_TIMESTAMP),
#             (PAST_TIMESTAMP, FUTURE_TIMESTAMP),
#             (FUTURE_TIMESTAMP, None),
#             (FUTURE_TIMESTAMP, PAST_TIMESTAMP),
#             (FUTURE_TIMESTAMP, CURRENT_TIMESTAMP),
#             (FUTURE_TIMESTAMP, FUTURE_TIMESTAMP),
#         ],
#     )
#     def test_no_entry(
#         self,
#         info_timestamp: datetime.datetime | None,
#         modified_timestamp: datetime.datetime,
#     ) -> None:
#         """Test that is_up_to_date works when the object has no entry in the database."""
#         assert self.obj.is_up_to_date(info_timestamp, modified_timestamp) is False
#         assert self.obj.is_outdated(info_timestamp, modified_timestamp) is True

#     @pytest.mark.parametrize(
#         ("info_timestamp", "modified_timestamp"),
#         [
#             (None, None),
#             (None, PAST_TIMESTAMP),
#             (None, CURRENT_TIMESTAMP),
#             (None, FUTURE_TIMESTAMP),
#             (CURRENT_TIMESTAMP, None),
#             (CURRENT_TIMESTAMP, PAST_TIMESTAMP),
#             (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
#             (CURRENT_TIMESTAMP, FUTURE_TIMESTAMP),
#             (PAST_TIMESTAMP, None),
#             (PAST_TIMESTAMP, PAST_TIMESTAMP),
#             (PAST_TIMESTAMP, CURRENT_TIMESTAMP),
#             (PAST_TIMESTAMP, FUTURE_TIMESTAMP),
#             (FUTURE_TIMESTAMP, None),
#             (FUTURE_TIMESTAMP, PAST_TIMESTAMP),
#             (FUTURE_TIMESTAMP, CURRENT_TIMESTAMP),
#             (FUTURE_TIMESTAMP, FUTURE_TIMESTAMP),
#         ],
#     )
#     def test_existing_entry(
#         self,
#         info_timestamp: datetime.datetime | None,
#         modified_timestamp: datetime.datetime,
#     ) -> None:
#         """Test that is_up_to_date works when the object has an entry in the database."""
#         self.obj.info_timestamp = CURRENT_TIMESTAMP
#         self.obj.info_modified_timestamp = CURRENT_TIMESTAMP
#         self.obj.save()

#         outdated = FUTURE_TIMESTAMP in (info_timestamp, modified_timestamp)
#         assert (
#             self.obj.is_up_to_date(info_timestamp, modified_timestamp) is not outdated
#         )
#         assert self.obj.is_outdated(info_timestamp, modified_timestamp) is outdated
