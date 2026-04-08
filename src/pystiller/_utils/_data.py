"""This module contains internal functions for processing API response data."""

import pandas as pd


def _flatten(nested_data, separator='_'):
    """Flattens nested JSON structures into a pandas DataFrame.

    This helper function automatically expands lists into multiple rows and
    flattens nested dictionaries.

    Args:
        nested_data: The dictionary or list of dictionaries to flatten.
        separator (str): The separator to use for nested columns names.
            Defaults to '_'.

    Raises:
        TypeError: If data is not a dictionary or a list of dictionaries. Data
            can be empty.

    Returns:
        pandas.DataFrame: A flattened DataFrame, where:
            - Lists are expanded into multiple rows.
            - Nested dictionaries become columns with separator-notation.
            - Parent-level fields are repeated for each child row.
    """

    def _flatten_dictionary(dictionary, sep, parent_key=''):
        """Flatten a nested dictionary without expanding lists.

        This helper function recursively traverses a dictionary and creates
        flat key-value pairs for nested keys, using the specified separator.
        Lists are kept as-is and not expanded by this function.

        Args:
            dictionary (dict): The dictionary to flatten.
            sep (str): The separator to use between parent and child keys.
            parent_key (str, optional): The parent key for the flattened
                dictionary. It is the prefix to prepend to keys (used in
                recursion). Defaults to ''.

        Returns:
            dict: A flattened dictionary with sep-notated keys for nested
                structures.
        """

        dictionary_items_ = []

        for key_, value_ in dictionary.items():
            new_key_ = f"{parent_key}{sep}{key_}" if parent_key else key_
            if isinstance(value_, dict):
                dictionary_items_.extend(
                    _flatten_dictionary(dictionary=value_, sep=sep,
                                        parent_key=new_key_).items())
            else:
                dictionary_items_.append((new_key_, value_))

        return dict(dictionary_items_)


    def _is_dictionary_of_lists(dictionary):
        """Check if a dictionary contains only lists as values.

        This helper function identifies the special case where the top-level
        dictionary keys represent categories amd all values are lists.

        Args:
            dictionary (dict): The dictionary to check.

        Returns:
            bool: True if all values in the dictionary are lists, False
                otherwise.
        """

        return all(isinstance(value_, list) for value_ in dictionary.values())


    def _expand_dictionary_of_lists(dictionary, sep):
        """Expand a dictionary where all values are lists.

        This helper function handles the special case where each top-level key
        maps to a list of items. It creates a "key" column to preserve the
        original dictionary key and expands each list item into a separate row.

        Args:
            dictionary (dict): The dictionary where all values are lists.
            sep (str): The separator for flattening nested dictionaries within
                list items.

        Returns:
            pandas.DataFrame: DataFrame with a "key" column containing the
                original dictionary key and additional columns from the list
                items.
        """

        expanded_rows_ = []

        for key_, value_ in dictionary.items():
            for item_ in value_:
                if isinstance(item_, dict):
                    row_ = {"parent_key": key_}
                    flat_item_ = _flatten_dictionary(dictionary=item_, sep=sep)
                    row_.update(flat_item_)
                    expanded_rows_.append(row_)
                else:
                    expanded_rows_.append({"parent_key": key_,
                                           "atomic_value": item_})

        return pd.DataFrame(expanded_rows_)


    def _find_list_columns(dictionary):
        """Finds dictionary keys that contain lists of dictionaries.

        This helper function identifies columns that need to be expanded into
        multiple rows. It only considers lists that contain at least one
        dictionary.

        Args:
            dictionary (dict): The dictionary to check.

        Returns:
            list: The list of keys whose values are lists of dictionaries.
        """

        list_keys_ = []

        for key_, value_ in dictionary.items():
            if (isinstance(value_, list) and value_
                    and any(isinstance(item_, dict) for item_ in value_)):
                list_keys_.append(key_)

        return list_keys_


    def _expand_lists(dictionary, sep):
        """Recursively expand lists in a dictionary into DataFrame rows.

        This helper is the main recursive function that handles the expansion
        logic. It detects different types of structures and applies the
        appropriate expansion strategy. It processes one list level at a time
        and recurses for additional nested lists.

        Args:
            dictionary (dict): The dictionary to process.
            sep (str): The separator for nested column names.

        Returns:
            pandas.DataFrame: A DataFrame with all lists expanded into rows and
                nested dictionaries flattened.
        """

        if _is_dictionary_of_lists(dictionary=dictionary):
            return _expand_dictionary_of_lists(dictionary=dictionary, sep=sep)

        list_keys_ = _find_list_columns(dictionary=dictionary)

        if not list_keys_:
            flat_ = _flatten_dictionary(dictionary=dictionary, sep=sep)
            return pd.DataFrame([flat_])

        list_key_ = list_keys_[0]
        list_data_ = dictionary[list_key_]

        base_data_ = {key_: value_ for key_, value_ in dictionary.items()
                      if key_ != list_key_}

        expanded_rows_ = []

        for item_ in list_data_:
            row_data_ = base_data_.copy()

            if isinstance(item_, dict):
                for key_, value_ in item_.items():
                    row_data_[f"{list_key_}{sep}{key_}"] = value_
            else:
                row_data_[list_key_] = item_

            expanded_rows_.append(_expand_lists(dictionary=row_data_, sep=sep))

        return pd.concat(expanded_rows_, ignore_index=True)

    if not nested_data:
        return pd.DataFrame()

    elif (isinstance(nested_data, list)
          and all(isinstance(item_, dict) for item_ in nested_data)):
        dataframes_ = [_expand_lists(dictionary=item_, sep=separator)
                       for item_ in nested_data]
        return pd.concat(dataframes_, ignore_index=True)

    elif isinstance(nested_data, dict):
        return _expand_lists(dictionary=nested_data, sep=separator)

    raise TypeError("Data must empty, a dictionary or a list of dictionaries")
