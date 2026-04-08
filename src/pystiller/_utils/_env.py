"""This module contains internal functions for working with environment
variables."""

import os
from dotenv import load_dotenv

from pystiller._utils import _checks


def _read_environment_variable(name):
    """Reads an environment variable.

    Args:
        name: The name of the environment variable to read.

    Raises:
        ValueError: If the value is not set.

    Returns:
        str: The value of the environment variable.
    """

    _checks._require_type(value=name, expected_type=str)

    load_dotenv()

    environment_variable_ = os.getenv(name)

    if environment_variable_ is None:
        raise ValueError(f"The {name} environment variable is not set")

    return environment_variable_
