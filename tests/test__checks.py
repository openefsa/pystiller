import unittest

from pystiller._utils._checks import (_require_type, _require_string_not_empty,
                                      _require_minimum)


class TestChecks(unittest.TestCase):

    ###################
    # _require_type() #
    ###################

    def test__require_type_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _require_type, value=123,
                          expected_type=str)

    def test__require_type_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_require_type(value=123, expected_type=int))

    ###############################
    # _require_string_not_empty() #
    ###############################

    def test__require_string_not_empty_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _require_string_not_empty, value=123)

    def test__require_string_not_empty_empty(self):
        """Test the behaviour for empty strings."""
        self.assertRaises(ValueError, _require_string_not_empty, value="")

    def test__require_string_not_empty_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_require_string_not_empty(value="test"))

    ######################
    # _require_minimum() #
    ######################

    def test__require_minimum_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _require_minimum, value='', minimum=0)
        self.assertRaises(TypeError, _require_minimum, value=0, minimum='')

    def test__require_minimum_wrong(self):
        """Test the behaviour for empty strings."""
        self.assertRaises(ValueError, _require_minimum, value=0, minimum=1)

    def test__require_minimum_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_require_minimum(value=1, minimum=0))
