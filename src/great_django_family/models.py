"""Abstract models for Django."""

from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Self, TypeVar

from django.db import models


class ModelWithId(models.Model):
    """Abstract Model with the id explicitly defined for type checking."""

    id: models.AutoField

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        """Required to make the model abstract."""

        abstract = True  # Required to be able to subclass models.Model


class ModelWithTimestamps(models.Model):
    """Abstract model with timestamps.

    This includes an info_timestamp, info_modified_timestamp
    """

    info_timestamp = models.DateTimeField()
    """Timestamp representing when the information was obtained."""

    # If I modify information by hand I do not want the timestamp to auto-update
    # Therefore automatically updating timestamps is not appropriate and it must be
    # updated manually.
    info_modified_timestamp = models.DateTimeField()
    """Timestamp representing when the information in the database was last modified."""

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        """Required to make the model abstract."""

        abstract = True  # Required to be able to subclass models.Model


class ModelWithTimestampsAndFunctions(ModelWithTimestamps):
    """Abstract model with timestamps and functions.

    This includes info_timestamp, info_modified_timestamp and timestamp related
    functions.
    """

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        """Required to make the model abstract."""

        abstract = True  # Required to be able to subclass models.Model

    def is_up_to_date(
        self,
        minimum_info_timestamp: datetime | None = None,
        minimum_modified_timestamp: datetime | None = None,
    ) -> bool:
        """Check if the information in the database is up to date.

        Args:
            minimum_info_timestamp: The minimum info_timestamp required for the data to
                be considered up to date.
            minimum_modified_timestamp: The minimum info_modified_timestamp that is
                required for the data to be considered up to date.

        Returns:
            True if the information is up to date, False otherwise.
        """
        # If no timestamp is present the information has to be outdated
        if not self.info_timestamp or not self.info_modified_timestamp:
            return False

        # Check that minimum_info_timestamp is up to date
        if minimum_info_timestamp and minimum_info_timestamp > self.info_timestamp:
            return False

        # Check that minimum_modified_timestamp is up to date
        return not (
            minimum_modified_timestamp
            and minimum_modified_timestamp > self.info_modified_timestamp
        )

    def is_outdated(
        self,
        minimum_info_timestamp: datetime | None = None,
        minimum_modified_timestamp: datetime | None = None,
    ) -> bool:
        """Check if the information in the database is up to date.\

        Args:
            minimum_info_timestamp: The minimum info_timestamp required for the data to
                be considered outdated.
            minimum_modified_timestamp: The minimum info_modified_timestamp that is
            required for the data to be considered outdated.

        Returns:
            True if the information is outdated, False otherwise.
        """
        return not self.is_up_to_date(
            minimum_info_timestamp,
            minimum_modified_timestamp,
        )

    def add_timestamps_and_save(self, info_timestamp: datetime) -> None:
        """Add timestamps to the model and save it.

        Args:
            info_timestamp: The timestamp to add to the model.

        Returns:
            None
        """
        self.add_timestamps(info_timestamp)
        self.save()

    def add_timestamps(self, info_timestamp: datetime) -> None:
        """Add timestamps to the model.

        Args:
            info_timestamp: The timestamp to add to the model.

        Returns:
            None
        """
        self.info_timestamp = info_timestamp
        self.info_modified_timestamp = datetime.now().astimezone()


class ModelWithTimestampsAndUpdateAt(ModelWithTimestamps):
    """Abstract model with timestamps and update_at.

    This includes info_timestamp, info_modified_timestamp, update_at and
    timestamp related functions.
    """

    updated_at = models.DateTimeField()
    """Timestamp representing when the information need to be updated."""

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        """Required to make the model abstract."""

        abstract = True  # Required to be able to subclass models.Model


_T = TypeVar("_T", bound=models.Model)


class _GetOrNewManager(models.Manager[_T]):
    def get_or_new(self, **values: str | int | models.Model) -> tuple[_T, bool]:
        """Get an object if it exist, otherwise create it.

        This is similar to get_or_create but with some small differences. get_or_create
        will immediatly attempt to create and save an object even if it doesn't have all
        the required information for the object to be saved, get_or_new will not save
        the object on initialization, and instead must be saved manually when all of the
        information has been added to the object.

        This is useful for when creating a new object but not all of the information is
        easily avaialble at the time of object initialization.

        Args:
            values: The values to use to get or create the object, the keys are the
            field names and the values are the values to use for the fields.

        Returns:
            A tuple containing the object and a boolean representing if the object was
            created or not, if the object was created the boolean will be True, if the
            object was fetched the boolean will be False

        """
        try:
            return (self.get(**values), False)
        except self.model.DoesNotExist:
            return (self.model(**values), True)


class ModelWithGetOrNew(models.Model):
    """Model template with a get_or_new function."""

    # The types here don't exactly match up, but this implementation is as close
    # as possible to Django's official example on how to implement something
    # similar. See: https://docs.djangoproject.com/en/5.0/topics/db/managers/
    objects: ClassVar[_GetOrNewManager[Self]] = _GetOrNewManager()

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        """Required to make the model abstract."""

        abstract = True  # Required to be able to subclass models.Model
