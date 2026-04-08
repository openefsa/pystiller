import unittest

from pystiller._utils._data import _flatten


class TestData(unittest.TestCase):

    ##############
    # _flatten() #
    ##############

    def test__flatten_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _flatten, nested_data=123)

    def test__flatten_empty(self):
        """Test the behaviour for empty data."""
        self.assertTrue(_flatten(nested_data=list()).empty)
        self.assertTrue(_flatten(nested_data=dict()).empty)

    def test__flatten_sep(self):
        flattened_ = _flatten(nested_data={'a': {'b': 1}})
        self.assertEqual(flattened_.keys()[0], "a_b")
        flattened_ = _flatten(nested_data={'a': {'b': 1}}, separator='.')
        self.assertEqual(flattened_.keys()[0], "a.b")

    def test__flatten_dict1(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                '1': 4,
                '2': 5
            }
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', 'b', 'c', "d_1", "d_2"]
        )

    def test__flatten_dict2(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                '1': 4,
                '2': {
                    '3': 5
                }
            }
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', 'b', 'c', "d_1", "d_2_3"]
        )

    def test__flatten_dict3(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6}
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', "b_x", "b_y", "b_z"]
        )

    def test__flatten_dict4(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6},
                "some text"
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', "b_x", "b_y", "b_z", 'b']
        )

    def test__flatten_list_of_dicts(self):
        """Test the behaviour for flattening a list of dictionaries."""
        flattened_ = _flatten(nested_data=[
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6}
        ])
        self.assertEqual(list(flattened_.keys()), ['a', 'b', 'c'])

    def test__flatten_dict_of_lists1(self):
        """Test the behaviour for flattening a dictionary of lists."""
        flattened_ = _flatten(nested_data={
            'a': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6}
            ],
            'b': [
                {'x': 7, 'y': 8, 'z': 9},
                {'x': 10, 'y': 11, 'z': 12}
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ["parent_key", 'x', 'y', 'z']
        )

    def test__flatten_dict_of_lists2(self):
        """Test the behaviour for flattening a dictionary of lists."""
        flattened_ = _flatten(nested_data={
            'a': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6}
            ],
            'b': [
                {'x': 7, 'y': 8, 'z': 9},
                "some text"
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ["parent_key", 'x', 'y', 'z', "atomic_value"]
        )
