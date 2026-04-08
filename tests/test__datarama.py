import io
import json
import os
import unittest
from unittest.mock import patch
from requests.exceptions import HTTPError
import pandas as pd
import requests
from dotenv import load_dotenv
from pystiller._core import _authentication
from requests import Response

from pystiller._core._datarama import _get_reports, _get_report, ReportFormat

load_dotenv()


class TestDatarama(unittest.TestCase):

    ##################
    # _get_reports() #
    ##################

    def test__get_reports_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _get_reports, project_id='',
                          distiller_instance_url=123, distiller_token="")
        self.assertRaises(TypeError, _get_reports, project_id=123,
                          distiller_instance_url=123, distiller_token="")
        self.assertRaises(TypeError, _get_reports, project_id=123,
                          distiller_instance_url="", distiller_token=123)
        self.assertRaises(TypeError, _get_reports, project_id=123,
                          distiller_instance_url="", distiller_token="",
                          timeout="")

    @patch("pystiller._core._datarama._requests._perform_service_request")
    def test__get_reports_bad_url(self, mock_serv_req):
        """Test the behaviour for bad instance URLs."""
        mock_serv_req.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _get_reports, project_id=123,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_reports_bad_url_online(self):
        """Test the behaviour for bad instance URLs."""
        self.assertRaises(Exception, _get_reports, project_id=123,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN")

    @patch("pystiller._core._datarama._requests._perform_service_request")
    def test__get_reports_output(self, mock_serv_req):
        """Test the output type of the request."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = json.dumps({
            "a": [1], "b": [2], "c": [3], "d": [4]
        }).encode("utf-8")
        mock_serv_req.return_value = response_
        response_ = _get_reports(
            project_id=123,
            distiller_instance_url="https://example.org",
            distiller_token="DISTILLER_TOKEN"
        )
        self.assertIsInstance(response_, pd.DataFrame)
        self.assertEqual(len(response_.columns), 4)

    # This test requires the DISTILLER_API_KEY, DISTILLER_INSTANCE_URL, and
    # DISTILLER_PROJECT_ID_TEST environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_reports_output_online(self):
        """Test the output type of the request."""
        token_ = _authentication._get_authentication_token(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        response_ = _get_reports(
            project_id=int(os.getenv("DISTILLER_PROJECT_ID_TEST")),
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_token=token_
        )
        self.assertIsInstance(response_, pd.DataFrame)
        self.assertEqual(len(response_.columns), 4)

    #################
    # _get_report() #
    #################

    def test__get_report_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _get_report, project_id="", report_id=456,
                          distiller_instance_url="", distiller_token="")
        self.assertRaises(TypeError, _get_report, project_id=123, report_id="",
                          distiller_instance_url="", distiller_token="")
        self.assertRaises(TypeError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url=123,
                          distiller_token="")
        self.assertRaises(TypeError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token=123)
        self.assertRaises(TypeError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token="", report_format=123)
        self.assertRaises(TypeError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token="", report_format=ReportFormat.CSV,
                          timeout="")
        self.assertRaises(TypeError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token="", report_format=ReportFormat.CSV,
                          timeout=1, attempts="")
        self.assertRaises(TypeError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token="", report_format=ReportFormat.CSV,
                          timeout=1, attempts=1, retry_each="")
        self.assertRaises(ValueError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token="", report_format=ReportFormat.CSV,
                          timeout=1, attempts=0, retry_each=1)
        self.assertRaises(ValueError, _get_report, project_id=123,
                          report_id=456, distiller_instance_url="",
                          distiller_token="", report_format=ReportFormat.CSV,
                          timeout=1, attempts=1, retry_each=-1)

    @patch("pystiller._core._datarama._requests._perform_service_request")
    def test__get_report_bad_url(self, mock_serv_req):
        """Test the behaviour for bad instance URLs."""
        mock_serv_req.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _get_report, project_id=123,
                          report_id=456, attempts=1, retry_each=1,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_report_bad_url_online(self):
        """Test the behaviour for bad instance URLs."""
        self.assertRaises(Exception, _get_report, project_id=123,
                          report_id=456, attempts=1, retry_each=1,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN")

    @patch("pystiller._core._datarama._requests._perform_service_request")
    def test__get_report_output_xlsx(self, mock_serv_req):
        """Test the output type of the request."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = (
                "application/vnd.openxmlformats-officedocuments." +
                "spreadsheetml.sheet"
        )
        dataframe_ = pd.DataFrame({
            'a': [1], 'b': [2], 'c': [3], 'd': [4]
        })
        buffer_ = io.BytesIO()
        dataframe_.to_excel(buffer_, index=True)  # type: ignore[arg-type]
        buffer_.seek(0)
        response_._content = buffer_.getvalue()
        mock_serv_req.return_value = response_
        response_ = _get_report(
            project_id=123, report_id=456, report_format=ReportFormat.EXCEL,
            distiller_instance_url="https://example.org", attempts=1,
            distiller_token="DISTILLER_TOKEN"
        )
        self.assertIsInstance(response_, pd.DataFrame)

    # This test requires the DISTILLER_API_KEY, DISTILLER_INSTANCE_URL,
    # DISTILLER_PROJECT_ID_TEST, and DISTILLER_REPORT_ID_TEST environment
    # variables to be set. This test performs real requests to the DistillerSR
    # API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_report_output_xlsx_online(self):
        """Test the output type of the request."""
        token_ = _authentication._get_authentication_token(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        response_ = _get_report(
            project_id=int(os.getenv("DISTILLER_PROJECT_ID_TEST")),
            report_id=int(os.getenv("DISTILLER_REPORT_ID_TEST")),
            report_format=ReportFormat.EXCEL,
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_token=token_, attempts=1
        )
        self.assertIsInstance(response_, pd.DataFrame)

    @patch("pystiller._core._datarama._requests._perform_service_request")
    def test__get_report_output_csv(self, mock_serv_req):
        """Test the output type of the request."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = "text/csv"
        response_._content = "a,b\n1,2".encode("utf-8")
        mock_serv_req.return_value = response_
        response_ = _get_report(
            project_id=123, report_id=456, report_format=ReportFormat.CSV,
            distiller_instance_url="https://example.org",
            distiller_token="DISTILLER_TOKEN", attempts=1
        )
        self.assertIsInstance(response_, pd.DataFrame)

    @patch("pystiller._core._datarama._requests._perform_service_request")
    @patch("pystiller._core._datarama.time.sleep")
    def test__get_report_delay(self, mock_sleep, mock_serv_req):
        """Test the output type of the request."""
        sleep_called_ = False
        def _mark_sleep(*args, **kwargs):
            nonlocal sleep_called_
            sleep_called_ = True
        mock_sleep.side_effect = _mark_sleep
        mock_serv_req.side_effect = HTTPError
        self.assertRaises(RuntimeError, _get_report, project_id=123,
                          report_id=456, report_format=ReportFormat.CSV,
                          distiller_instance_url="https://example.org",
                          distiller_token="DISTILLER_TOKEN", attempts=2,
                          retry_each=1, verbose=False)
        self.assertTrue(sleep_called_)

    @patch("pystiller._core._datarama._requests._perform_service_request")
    def test__get_report_verbose(self, mock_serv_req):
        """Test the output type of the request."""
        mock_serv_req.side_effect = HTTPError
        self.assertRaises(RuntimeError, _get_report, project_id=123,
                          report_id=456, report_format=ReportFormat.CSV,
                          distiller_instance_url="https://example.org",
                          distiller_token="DISTILLER_TOKEN", attempts=2,
                          retry_each=1)
