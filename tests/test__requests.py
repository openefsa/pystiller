import io
import json
import os
import unittest
from json import JSONDecodeError
from unittest.mock import patch
import pandas as pd
import requests
from dotenv import load_dotenv
from requests import Response, HTTPError

from pystiller._utils._requests import (_perform_authentication_request,
                                        _perform_service_request,
                                        _handle_http_errors,
                                        _parse_json_response,
                                        _parse_csv_response,
                                        _parse_xlsx_response)

load_dotenv()


class TestRequests(unittest.TestCase):

    #####################################
    # _perform_authentication_request() #
    #####################################

    def test__perform_authentication_request_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _perform_authentication_request,
                          distiller_instance_url=123, distiller_key="")
        self.assertRaises(TypeError, _perform_authentication_request,
                          distiller_instance_url="", distiller_key=123)
        self.assertRaises(TypeError, _perform_authentication_request,
                          distiller_instance_url="", distiller_key="",
                          timeout="")

    @patch("pystiller._utils._requests.requests.post")
    def test__perform_authentication_request_bad_url(self, mock_post):
        """Test the behaviour for bad instance URLs."""
        mock_post.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _perform_authentication_request,
                          distiller_instance_url="https://invalid-domain",
                          distiller_key="DISTILLER_API_KEY")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_authentication_request_bad_url_online(self):
        """Test the behaviour for bad instance URLs."""
        self.assertRaises(Exception, _perform_authentication_request,
                          distiller_instance_url="https://invalid-domain",
                          distiller_key="DISTILLER_API_KEY")

    @patch("pystiller._utils._requests.requests.post")
    def test__perform_authentication_request_output(self, mock_post):
        """Test the output type of the request."""
        mock_post.return_value = Response()
        response_ = _perform_authentication_request(
            distiller_instance_url="https://example.org",
            distiller_key="DISTILLER_API_KEY"
        )
        self.assertIsInstance(response_, Response)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_authentication_request_output_online(self):
        """Test the output type of the request."""
        response_ = _perform_authentication_request(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        self.assertIsInstance(response_, Response)

    ##############################
    # _perform_service_request() #
    ##############################

    def test__perform_service_request_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _perform_service_request, service_url=123,
                          distiller_token="")
        self.assertRaises(TypeError, _perform_service_request, service_url="",
                          distiller_token=123)
        self.assertRaises(TypeError, _perform_service_request, service_url="",
                          distiller_token="", body=123)
        self.assertRaises(TypeError, _perform_service_request, service_url="",
                          distiller_token="", body={}, timeout="")

    @patch("pystiller._utils._requests.requests.get")
    def test__perform_service_request_get_bad_url(self, mock_get):
        """Test the behaviour for bad instance URLs in GET requests."""
        mock_get.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _perform_service_request,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_API_TOKEN")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_service_request_get_bad_url_online(self):
        """Test the behaviour for bad instance URLs in GET requests."""
        self.assertRaises(Exception, _perform_service_request,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_API_TOKEN")

    @patch("pystiller._utils._requests.requests.get")
    def test__perform_service_request_get_output(self, mock_get):
        """Test the output type of GET requests."""
        mock_get.return_value = Response()
        response_ = _perform_service_request(
            service_url="https://example.org/projects",
            distiller_token="DISTILLER_API_TOKEN"
        )
        self.assertIsInstance(response_, Response)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_service_request_get_output_online(self):
        """Test the output type of GET requests."""
        auth_response_ = _perform_authentication_request(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        token_ = auth_response_.json()["token"]

        response_ = _perform_service_request(
            service_url=f"{os.getenv('DISTILLER_INSTANCE_URL')}/projects",
            distiller_token=token_
        )
        self.assertIsInstance(response_, Response)

    @patch("pystiller._utils._requests.requests.post")
    def test__perform_service_request_post_bad_url(self, mock_post):
        """Test the behaviour for bad instance URLs in POST requests."""
        mock_post.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _perform_service_request,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN", body={'a': 1})

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_service_request_post_bad_url_online(self):
        """Test the behaviour for bad instance URLs in POST requests."""
        self.assertRaises(Exception, _perform_service_request,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN", body={'a': 1})

    @patch("pystiller._utils._requests.requests.post")
    def test__perform_service_request_post_output(self, mock_post):
        """Test the output type of the POST request."""
        mock_post.return_value = Response()
        response_ = _perform_service_request(
            service_url="https://example.org/datarama/query",
            distiller_token="DISTILLER_TOKEN", body={'a': 1}
        )
        self.assertIsInstance(response_, Response)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_service_request_post_output_online(self):
        """Test the output type of the POST request."""
        auth_response_ = _perform_authentication_request(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        token_ = auth_response_.json()["token"]

        response_ = _perform_service_request(
            service_url=f"{os.getenv('DISTILLER_INSTANCE_URL')}/datarama/query",
            distiller_token=token_,
            body={
                "project_id": 42483,
                "saved_report_id": 155,
                "use_saved_format": True
            }
        )
        self.assertIsInstance(response_, Response)

    #########################
    # _handle_http_errors() #
    #########################

    def test__handle_http_errors_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _handle_http_errors, response=123)
        self.assertRaises(TypeError, _handle_http_errors,
                          response=requests.Response(), error_message=123)

    def test__handle_http_errors_valid(self):
        """Test the behaviour for status code 200."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"data": "Custom data"})
                              .encode("utf-8"))
        self.assertIsNone(_handle_http_errors(response=response_))

    def test__handle_http_errors_invalid(self):
        """Test the behaviour for bad status codes."""
        response_ = Response()
        response_.status_code = 502
        response_.url = "https://example.org"
        response_.method = "GET"
        self.assertRaises(HTTPError, _handle_http_errors, response=response_)

    ##########################
    # _parse_json_response() #
    ##########################

    def test__parse_json_response_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _parse_json_response, response=123)
        self.assertRaises(TypeError, _parse_json_response,
                          response=requests.Response(), error_message=123)

    def test__parse_json_response_valid(self):
        """Test the behaviour for valid parameters and data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"data": "Custom data"})
                              .encode("utf-8"))
        self.assertIsInstance(
            _parse_json_response(response=response_),
            dict
        )

    def test__parse_json_response_valid_flatten(self):
        """Test the behaviour for valid parameters and data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"data": "Custom data"})
                              .encode("utf-8"))
        self.assertIsInstance(
            _parse_json_response(response=response_, flatten=True),
            pd.DataFrame
        )

    def test__parse_json_response_invalid(self):
        """Test the behaviour for invalid body data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = "text/html"
        response_._content = "<html>content</html>".encode("utf-8")
        self.assertRaises(
            JSONDecodeError,
            _parse_json_response,
            response=response_
        )

    #########################
    # _parse_csv_response() #
    #########################

    def test__parse_csv_response_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _parse_csv_response, response=123)
        self.assertRaises(TypeError, _parse_csv_response,
                          response=requests.Response(), error_message=123)

    def test__parse_csv_response_valid(self):
        """Test the behaviour for valid parameters and data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = "text/csv"
        response_._content = "a,b\n1,2".encode("utf-8")
        self.assertIsInstance(
            _parse_csv_response(response=response_),
            pd.DataFrame
        )

    def test__parse_csv_response_invalid(self):
        """Test the behaviour for invalid body data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = "text/csv"
        response_._content = "a,b\n1,2\n3\n4,5,6".encode("utf-8")
        self.assertRaises(
            Exception,
            _parse_csv_response,
            response=response_
        )

    ##########################
    # _parse_xlsx_response() #
    ##########################

    def test__parse_xlsx_response_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _parse_xlsx_response, response=123)
        self.assertRaises(TypeError, _parse_xlsx_response,
                          response=requests.Response(), error_message=123)

    def test__parse_xlsx_response_valid(self):
        """Test the behaviour for valid parameters and data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = (
            "application/vnd.openxmlformats-officedocuments." +
            "spreadsheetml.sheet"
        )
        dataframe_ = pd.DataFrame({
            'a': [1, 2],
            'b': [3, 4]
        })
        buffer_ = io.BytesIO()
        dataframe_.to_excel(buffer_, index=True) # type: ignore[arg-type]
        buffer_.seek(0)
        response_._content = buffer_.getvalue()
        self.assertIsInstance(
            _parse_xlsx_response(response=response_),
            pd.DataFrame
        )

    def test__parse_xlsx_response_invalid(self):
        """Test the behaviour for invalid body data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "POST"
        response_.headers["Content-Type"] = (
            "application/vnd.openxmlformats-officedocuments." +
            "spreadsheetml.sheet"
        )
        response_._content = b"Not an XLSX content"
        self.assertRaises(
            Exception,
            _parse_xlsx_response,
            response=response_
        )
