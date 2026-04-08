"""This module contains core functions for working with the Projects endpoints
of the DistillerSR API.
"""

import pandas as pd

from pystiller._utils import _checks, _requests


def _get_projects(distiller_instance_url, distiller_token, timeout=1800):
    """Get the list of the Distiller projects associated to the user.

    This internal function queries the DistillerSR API to retrieve the list of
    projects accessible to the authenticated user. The result is a data frame
    listing available projects.

    Args:
        distiller_instance_url (str): The URL of the DistillerSR instance.
        distiller_token (str): The Distiller authentication token.
        timeout (int, optional): The maximum number of seconds to wait for the
            service response. Defaults to 1800 seconds (30 minutes).

    Returns:
        pd.DataFrame: A data frame with four columns:
            - id: The project ID.
            - name: The project name.
            - de_project_id.
            - is_hidden.
    """

    _checks._require_type(value=distiller_instance_url, expected_type=str)
    _checks._require_type(value=distiller_token, expected_type=str)
    _checks._require_type(value=timeout, expected_type=int)

    projects_url_ = f"{distiller_instance_url}/projects"

    service_response_ = _requests._perform_service_request(
        service_url=projects_url_,
        distiller_token=distiller_token,
        timeout=timeout)

    _requests._handle_http_errors(
        response=service_response_,
        error_message="Unable to retrieve projects")

    response_data_ = _requests._parse_json_response(
        response=service_response_,
        error_message="Failed to parse projects service response")

    response_data_ = pd.DataFrame(response_data_)

    return response_data_
