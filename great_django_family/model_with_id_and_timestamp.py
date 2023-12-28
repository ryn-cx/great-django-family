"""Model that includes an auto incrmented id, info_timestamp, and info_modified_timestamp and some functions."""

from __future__ import annotations

from datetime import datetime

from django.db import models
from paved_path import PavedPath


class ModelWithTimestamps(models.Model):
    """Model tempalte with an info_timestamp, info_modified_timestamp and some functions."""

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

    def add_timestamps_and_save(self, info_timestamp: PavedPath | datetime) -> None:
        """Add timestamps to the model and save it."""
        self.add_timestamps(info_timestamp)
        self.save()

    def add_timestamps(self, info_timestamp: PavedPath | datetime) -> None:
        """Add timestamps to the model."""
        if isinstance(info_timestamp, PavedPath):
            self.info_timestamp = info_timestamp.aware_mtime()
        else:
            self.info_timestamp = info_timestamp.astimezone()

        self.info_modified_timestamp = datetime.now().astimezone()


class ModelWithId(models.Model):
    """Model tempalte with the id explicitly defined for type checking."""

    id: models.AutoField  # noqa: A003 - This value exists no matter what, this just documents it

    class Meta:  # type: ignore  # noqa: PGH003 - Meta has false positives
        """Meta information for ModelWithIdAndTimestamp."""

        abstract = True  # Required to be able to subclass models.Model
