"""
Custom exceptions module.
"""


class InvalidAgeError(
    Exception
):
    """Raised when age is invalid."""


def validate_age(
    age: int
) -> None:
    """Validate age."""

    if age < 0:
        raise InvalidAgeError(
            "Age cannot be negative."
        )