"""GetOrNewModel and supporting classes."""
from __future__ import annotations

from typing import ClassVar, Self, TypeVar

from django.db import models

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

        abstract = True
