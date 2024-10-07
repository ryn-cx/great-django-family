"""Functions for Django models."""

from __future__ import annotations

import inspect

from django.db import models


class StackInspectionError(Exception):
    """Error raised when the stack is invalid."""


def auto_unique(*fields: str) -> models.UniqueConstraint:
    """Automatically generate a unique constraint for the given fields.

    When using models.UniqueConstraint one of the required parameters is the
    name of the constraint. It is simpler to have this name automatically
    generated to decrease the possibility of accidently making two constraints
    with the same name.

    Args:
        *fields: The fields to create a unique constraint for.

    Returns:
        The generated unique constraint.

    Raises:
        `StackInspectionError`: If the function is not called from within the
        `Meta` class of a model.
    """
    # This function may not be reliable because it relies on undocumented
    # behavior of the inspect module
    # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    # The first frame will be the Meta class, the second one will be the actual
    # class.
    for i, frame_info in enumerate(inspect.stack()):
        if frame_info.function == "Meta":
            model_name = inspect.stack()[i + 1].function
            return models.UniqueConstraint(
                fields=fields,
                name=f"UQ_{model_name}_{'-'.join(fields)}",
            )

    msg = (
        "auto_unique failed because the Meta class was not found, "
        "auto_unique may have been called incorrectly."
    )
    raise StackInspectionError(msg)
