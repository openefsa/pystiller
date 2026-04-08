"""This module contains core functions for working with the Datarama endpoints
of the DistillerSR API.
"""
import time
import pandas as pd
from enum import StrEnum

from pystiller._utils import _checks, _requests


class ReportFormat(StrEnum):
    """The supported report formats."""
    CSV = "csv",
    EXCEL = "excel"


def _get_reports(project_id, distiller_instance_url, distiller_token,
                 timeout=1800):
    """Get the list of the Distiller reports associated to a project.

    This internal function queries the DistillerSR API to retrieve the list of
    reports associated with a project. The result is a data frame listing
    available reports.

    Args:
        project_id (int): The ID of the project as provided by DistillerSR.
        distiller_instance_url (str): The URL of the DistillerSR instance.
        distiller_token (str): The Distiller authentication token.
        timeout (int, optional): The maximum number of seconds to wait for the
            service response. Defaults to 1800 seconds (30 minutes).

    Returns:
        pd.DataFrame: A data frame with four columns:
            - id: The project ID.
            - name: The project name.
            - date: The creation date of the report.
            - view: The format of the report (e.g., html, csv, excel).
    """

    _checks._require_type(value=project_id, expected_type=int)
    _checks._require_type(value=distiller_instance_url, expected_type=str)
    _checks._require_type(value=distiller_token, expected_type=str)
    _checks._require_type(value=timeout, expected_type=int)

    reports_url_ = (f"{distiller_instance_url}/projects/{project_id}" +
                     "/reports/datarama")

    service_response_ = _requests._perform_service_request(
        service_url=reports_url_,
        distiller_token=distiller_token,
        timeout=timeout)

    _requests._handle_http_errors(
        response=service_response_,
        error_message="Unable to retrieve reports")

    response_data_ = _requests._parse_json_response(
        response=service_response_,
        error_message="Failed to parse reports service response")

    response_data_ = pd.DataFrame(response_data_)

    return response_data_


def _get_report(project_id, report_id, distiller_instance_url, distiller_token,
                report_format = ReportFormat.CSV, timeout=1800, attempts=1,
                retry_each=600, verbose=True):
    """Get a Distiller report associated to a project.

    This internal function queries the DistillerSR API to retrieve a saved
    report associated with a project. The result is a data frame containing
    metadata about the saved report.

    Args:
        project_id (int): The ID of the project as provided by DistillerSR.
        report_id (int): The ID of the report as provided by DistillerSR.
        distiller_instance_url (str): The URL of the DistillerSR instance.
        distiller_token (str): The Distiller authentication token.
        report_format (ReportFormat, optional): The desired format of the
            document. Defaults to CSV (Comma Separated Values).
        timeout (int, optional): The maximum number of seconds to wait for the
            service response. Defaults to 1800 seconds (30 minutes).
        attempts (int, optional): The maximum number of attempts. Defaults to 1
            attempt.
        retry_each (int, optional): The delay between attempts. Defaults to
            600 seconds (10 minutes).
        verbose (bool, optional): A flag to specify whether to make the
            function verbose or not. Defaults to True.

    Returns:
        pd.DataFrame: A data frame containing the Distiller report as designed
            within DistillerSR.
    """

    _checks._require_type(value=project_id, expected_type=int)
    _checks._require_type(value=report_id, expected_type=int)
    _checks._require_type(value=distiller_instance_url, expected_type=str)
    _checks._require_type(value=distiller_token, expected_type=str)
    _checks._require_type(value=report_format, expected_type=ReportFormat)
    _checks._require_type(value=timeout, expected_type=int)
    _checks._require_type(value=attempts, expected_type=int)
    _checks._require_minimum(value=attempts, minimum=1)
    _checks._require_type(value=retry_each, expected_type=int)
    _checks._require_minimum(value=retry_each, minimum=0)

    report_url_ = f"{distiller_instance_url}/datarama/query"

    request_body_ = {
        "project_id": project_id,
        "saved_report_id": report_id,
        "use_saved_format": True
    }

    for attempt_ in range(attempts):
        if verbose and attempts > 1:
            print(f"Starting attempt {attempt_ + 1}...")
        try:
            service_response_ = _requests._perform_service_request(
                service_url=report_url_,
                distiller_token=distiller_token,
                body=request_body_,
                timeout=timeout)

            _requests._handle_http_errors(
                response=service_response_,
                error_message=f"Unable to retrieve report {report_id}")

            if report_format == ReportFormat.CSV:
                response_data_ = _requests._parse_csv_response(
                    response=service_response_,
                    error_message="Failed to parse CSV for report " +
                                  f"{report_id}")
            else:
                response_data_ = _requests._parse_xlsx_response(
                    response=service_response_,
                    error_message="Failed to parse XLSX for report " +
                                  f"{report_id}")

            response_data_ = pd.DataFrame(response_data_)

            return response_data_

        except Exception as e_:
            if verbose:
                print(f"Attempt failed with reason:\n{e_}")

            if attempt_ < attempts:
                if verbose:
                    print(f"Sleeping for {retry_each} seconds...")
                time.sleep(retry_each)

    raise RuntimeError(f"Unable to retrieve report {report_id}\nAll " +
                       "attempts to retrieve the report failed")
