"""This module contains core functions for working with the Authentication
endpoint of the DistillerSR API.
"""

from pystiller._utils import _checks, _requests


def _get_authentication_token(distiller_instance_url, distiller_key,
                              timeout=1800):
    """Authenticate to a DistillerSR session.

    This helper function authenticates a user to a DistillerSR instance
    using the personal access key. The function sets a valid
    authentication token that can be used to access protected DistillerSR
    API endpoints and records the exact date and time the token was issued,
    which can be used to manage future refresh operations.

    Args:
        distiller_instance_url (str): The URL of the DistillerSR instance.
        distiller_key (str): The personal access key generated in DistillerSR.
        timeout (int, optional): The maximum number of seconds to wait for the
            authentication response. Defaults to 1800 seconds (30 minutes).

    Returns:
        str: The obtained DistillerSR authentication token.
    """

    _checks._require_type(value=distiller_instance_url, expected_type=str)
    _checks._require_type(value=distiller_key, expected_type=str)
    _checks._require_type(value=timeout, expected_type=int)

    authentication_response_ = _requests._perform_authentication_request(
        distiller_instance_url=distiller_instance_url,
        distiller_key=distiller_key,
        timeout=timeout)

    _requests._handle_http_errors(authentication_response_)

    response_data_ = _requests._parse_json_response(
        authentication_response_)

    return response_data_["token"]
