"""This module contains internal functions for performing type and data checks.
"""


def _require_type(value, expected_type):
    """Check that a value is of the expected type.

    Args:
        value: The value to check.
        expected_type: The expected type.

    Raises:
        TypeError: If the value is not of the expected type.

    Returns:
        None: The function returns nothing if the check passes.
    """

    if not isinstance(value, expected_type):
        raise TypeError(f"Expected type {expected_type}, got {type(value)}")


def _require_string_not_empty(value):
    """Check that a string is not empty.

    Args:
        value: The string to check.

    Raises:
        ValueError: If the string is empty.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=value, expected_type=str)

    if not value.strip():
        raise ValueError("Expected non-empty string, got empty string")


def _require_minimum(value, minimum):
    """Check that a value is not less than the given minimum.

    Args:
        value: The value to check.
        minimum: The minimum value.

    Raises:
        ValueError: If the value is not less than the given minimum.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=value, expected_type=int)
    _require_type(value=minimum, expected_type=int)

    if value < minimum:
        raise ValueError(f"Expected value >= {minimum}, got {value}")
