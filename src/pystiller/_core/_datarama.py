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

            if attempts > 1 and attempt_ < attempts:
                if verbose:
                    print(f"Sleeping for {retry_each} seconds...")
                time.sleep(retry_each)

    raise RuntimeError(f"Unable to retrieve report {report_id}\nAll " +
                       "attempts to retrieve the report failed")


def _get_report_async(project_id, report_id, distiller_instance_url,
                      distiller_async_instance_url, distiller_token,
                      timeout=1800):
    """Submit an asynchronous job to retrieve a Distiller report.

    This helper function submits an asynchronous job to DistillerSR to retrieve
    a saved report associated with a given project ID. It requires user
    authentication and a valid asynchronous API endpoint URL. The result is a
    dataframe containing metadata about the submitted job.

    Args:
        project_id (int): The ID of the project as provided by DistillerSR.
        report_id (int): The ID of the report as provided by DistillerSR.
        distiller_instance_url (str): The URL of the DistillerSR instance.
        distiller_async_instance_url (str): The URL of the asynchronous
            DistillerSR instance.
        distiller_token (str): The Distiller authentication token.
        timeout (int, optional): The maximum number of seconds to wait for the
            service response. Defaults to 1800 seconds (30 minutes).

    Returns:
        pd.DataFrame: A data frame containing metadata about the submitted job.
    """

    _checks._require_type(value=project_id, expected_type=int)
    _checks._require_type(value=report_id, expected_type=int)
    _checks._require_type(value=distiller_instance_url, expected_type=str)
    _checks._require_type(value=distiller_async_instance_url,
                          expected_type=str)
    _checks._require_type(value=distiller_token, expected_type=str)
    _checks._require_type(value=timeout, expected_type=int)

    service_url_ = f"{distiller_async_instance_url}/jobs"
    report_url_ = f"{distiller_instance_url}/datarama/query"

    request_body_ = {
        "endpoint": report_url_,
        "method": "POST",
        "headers": {
            "Authorization": f"Bearer {distiller_token}",
            "Content-Type": "application/json"
        },
        "body": {
            "project_id": f"{project_id}",
            "saved_report_id": f"{report_id}",
            "use_saved_format": "true"
        }
    }

    service_response_ = _requests._perform_service_request(
        service_url=service_url_,
        body=request_body_,
        timeout=timeout)

    _requests._handle_http_errors(
        response=service_response_,
        allowed_status_code=202,
        error_message=f"Unable to submit job for report {report_id}")

    response_data_ = _requests._parse_json_response(
        response=service_response_,
        error_message="Failed to parse job submission response")

    response_data_ = pd.DataFrame([response_data_])

    return response_data_


def _get_async_report_status(job_token, distiller_async_instance_url,
                             timeout=1800):
    """Get the status of an asynchronous job to retrieve a Distiller report.

    This helper function gets the status of a successfully submitted Distiller
    asynchronous job to retrieve a saved report. It requires a valid
    asynchronous job token. The result is a dataframe containing metadata about
    the job status.

    Args:
        job_token (str): The token associated to the submitted asynchronous
            job.
        distiller_async_instance_url (str): The URL of the asynchronous
            DistillerSR instance.
        timeout (int, optional): The maximum number of seconds to wait for the
            service response. Defaults to 1800 seconds (30 minutes).

    Returns:
        pd.DataFrame: A data frame containing metadata about the job status.
    """

    _checks._require_type(value=job_token, expected_type=str)
    _checks._require_type(value=distiller_async_instance_url,
                          expected_type=str)
    _checks._require_type(value=timeout, expected_type=int)

    service_url_ = f"{distiller_async_instance_url}/jobs/{job_token}"

    service_response_ = _requests._perform_service_request(
        service_url=service_url_,
        timeout=timeout)

    _requests._handle_http_errors(
        response=service_response_,
        error_message=f"Unable to get job status")

    response_data_ = _requests._parse_json_response(
        response=service_response_,
        error_message="Failed to parse job status response")

    response_data_ = pd.DataFrame([response_data_])

    return response_data_


def _get_async_report_result(job_token, distiller_async_instance_url,
                             report_format=ReportFormat.CSV, timeout=1800):
    """Get the result of an asynchronous job to retrieve a Distiller report.

    This helper function gets the result of a successful Distiller asynchronous
    job to retrieve a saved report associated with a given project ID. It
    requires a valid asynchronous job token. The result is a dataframe
    containing metadata about the saved report.

    Args:
        job_token (str): The token associated to the submitted asynchronous
            job.
        report_format (ReportFormat, optional): The desired format of the
            document. Defaults to CSV (Comma Separated Values).
        distiller_async_instance_url (str): The URL of the asynchronous
            DistillerSR instance.
        timeout (int, optional): The maximum number of seconds to wait for the
            service response. Defaults to 1800 seconds (30 minutes).

    Returns:
        pd.DataFrame: A data frame containing the Distiller report as designed
            within DistillerSR.
    """

    _checks._require_type(value=job_token, expected_type=str)
    _checks._require_type(value=distiller_async_instance_url,
                          expected_type=str)
    _checks._require_type(value=report_format, expected_type=ReportFormat)
    _checks._require_type(value=timeout, expected_type=int)

    service_url_ = f"{distiller_async_instance_url}/jobs/{job_token}/result"

    service_response_ = _requests._perform_service_request(
        service_url=service_url_,
        timeout=timeout)

    _requests._handle_http_errors(
        response=service_response_,
        error_message=f"Unable to get job result")

    if report_format == ReportFormat.CSV:
        response_data_ = _requests._parse_csv_response(
            response=service_response_,
            error_message="Failed to parse the requested report as CSV")
    else:
        response_data_ = _requests._parse_xlsx_response(
            response=service_response_,
            error_message="Failed to parse the requested report as XLSX")

    response_data_ = pd.DataFrame(response_data_)

    return response_data_
