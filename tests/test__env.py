import os
import unittest

from pystiller._utils._env import _read_environment_variable


class TestEnv(unittest.TestCase):

    ####################################
    # _read_environment_variable() #
    ####################################

    def test__read_environment_variable_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _read_environment_variable, name=123)

    def test__read_environment_variable_not_set(self):
        """Test the behaviour for unset environment variables."""
        if "TEST_VAR" in os.environ:
            del os.environ["TEST_VAR"]
        self.assertRaises(ValueError, _read_environment_variable,
                          name="TEST_VAR")

    def test__read_environment_variable_output(self):
        """Test the behaviour for valid data."""
        os.environ["TEST_VAR"] = "some value"
        self.assertIsInstance(_read_environment_variable(name="TEST_VAR"), str)
        del os.environ["TEST_VAR"]
