"""Abstract models for Django."""
from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Self, TypeVar

from django.db import models


class ModelWithId(models.Model):
    """Abstract Model with the id explicitly defined for type checking."""

    id: models.AutoField  # noqa: A003 - This value exists no matter what, this just documents it

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta information for ModelWithIdAndTimestamp."""

        abstract = True  # Required to be able to subclass models.Model


class ModelWithTimestamps(models.Model):
    """Abstract model with an info_timestamp, info_modified_timestamp and timestamp related functions."""

    info_timestamp = models.DateTimeField()
    """Timestamp representing when the information was obtained."""

    # If I modify information by hand I do not want the timestamp to auto-update
    # Therefore automatically updating timestamps is not appropriate and it must be updated manually
    info_modified_timestamp = models.DateTimeField()
    """Timestamp representing when the information in the database was last modified."""

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta information for ModelWithIdAndTimestamp."""

        abstract = True  # Required to be able to subclass models.Model

    def is_up_to_date(
        self,
        minimum_info_timestamp: datetime | None = None,
        minimum_modified_timestamp: datetime | None = None,
    ) -> bool:
        """Check if the information in the database is up to date."""
        # If no timestamp is present the information has to be outdated
        if not self.info_timestamp or not self.info_modified_timestamp:
            return False

        # Check that minimum_info_timestamp is up to date
        if minimum_info_timestamp and minimum_info_timestamp > self.info_timestamp:
            return False

        # Check that minimum_modified_timestamp is up to date
        if minimum_modified_timestamp and minimum_modified_timestamp > self.info_modified_timestamp:
            return False

        # If other tests passed information is up to date
        return True

    def is_outdated(
        self,
        minimum_info_timestamp: datetime | None = None,
        minimum_modified_timestamp: datetime | None = None,
    ) -> bool:
        """Check if the information in the database is outdated."""
        return not self.is_up_to_date(minimum_info_timestamp, minimum_modified_timestamp)

    def add_timestamps_and_save(self, info_timestamp: datetime) -> None:
        """Add timestamps to the model and save it."""
        self.add_timestamps(info_timestamp)
        self.save()

    def add_timestamps(self, info_timestamp: datetime) -> None:
        """Add timestamps to the model."""
        self.info_timestamp = info_timestamp
        self.info_modified_timestamp = datetime.now().astimezone()


_T = TypeVar("_T", bound=models.Model)


class _GetOrNewManager(models.Manager[_T]):
    """Temp docstring."""

    def get_or_new(self, **values: str | int | models.Model) -> tuple[_T, bool]:
        """Get an object if it exist, otherwise create it.

        This is similar to get_or_create but with some small differences. get_or_create will immediatly attempt to
        create and save an object even if it doesn't have all the required information for the object to be saved,
        get_or_new will not save the object on initialization, and instead must be saved manually when all of the
        information has been added to the object.

        This is useful for when creating a new object but not all of the information is easily avaialble at the time of
        object initialization.

        Args:
        ----
        values: The values to use to get or create the object, the keys are the field names and the values are the
        values to use for the fields.

        Returns:
        -------
        A tuple containing the object and a boolean representing if the object was created or not, if the object was
        created the boolean will be True, if the object was fetched the boolean will be False
        """
        try:
            return (self.get(**values), False)
        except self.model.DoesNotExist:
            return (self.model(**values), True)


class ModelWithGetOrNew(models.Model):
    """Model template with a get_or_new function in the model manager."""

    # The types here don't exactly match up, but this implementation is as close as possible to Django's official
    # example on how to implement something similar. See: https://docs.djangoproject.com/en/5.0/topics/db/managers/
    # Also, this is labeled as a ClassVar because the original implementation has a type hint for ClassVar.
    objects: ClassVar[_GetOrNewManager[Self]] = _GetOrNewManager()

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta information for the GetOrNewModel."""

        abstract = True  # Required to be able to subclass models.Model


# THis SHOULD be redundant, but for some reason if you try to create ModelWithIdAndTimestampAndGetOrNew all in a single
# class it will have a type error so this itermidiate class is required.
class ModelWithIdAndTimestamp(ModelWithId, ModelWithTimestamps):
    """Abstract model with an id and timestamps."""

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta information for ModelWithIdAndTimestamp."""

        abstract = True  # Required to be able to subclass models.Model


# THis SHOULD be redundant, but for some reason if you try to create ModelWithIdAndTimestampAndGetOrNew all in a single
# class it will have a type error so make this class in advance to make it easier to use all of the abstract classes at
# once.
class ModelWithIdTimestampAndGetOrNew(ModelWithIdAndTimestamp, ModelWithGetOrNew):
    """Abstract model with an id, timestamps and a get_or_new function."""

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta information for ModelWithIdAndTimestampAndGetOrNew."""

        abstract = True  # Required to be able to subclass models.Model
