"""A mixin that adds a get_or_new method to a model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from typing import Self


class GetOrNew(models.Model):
    """A mixin that adds a get_or_new method to a model."""

    class Meta:
        """Meta information for GetOrNew."""

        abstract = True

    def get_or_new(self, **values: str | int | models.Model) -> tuple[Self, bool]:
        """Inspired by get_or_create, but with some differences.

        get_or_create will immediatly attempt to create an object even if it doesn't have all the required information,
        get_or_new will not save the object, and instead must be saved manually when all of the information has been
        added to the object

        This is useful for when creating a new object but not all of the information is easily avaialble at the time of
        object initialization

        Args:
        ----
        values: The values to use to get or create the object, the keys are the field names and the values are the
        values to use for the fields

        Returns:
        -------
        A tuple containing the object and a boolean representing if the object was created or not, if the object was
        created the boolean will be True, if the object was fetched the boolean will be False
        """
        try:
            return (self.__class__.objects.get(**values), False)
        except self.DoesNotExist:
            return (self.__class__(**values), True)
