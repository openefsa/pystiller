import os
import json
import unittest
from unittest.mock import patch
import requests
from dotenv import load_dotenv
from requests import Response

from pystiller._core._authentication import _get_authentication_token

load_dotenv()


class TestAuthentication(unittest.TestCase):

    ###############################
    # _get_authentication_token() #
    ###############################

    def test__get_authentication_token_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _get_authentication_token,
                          distiller_instance_url=123, distiller_key="")
        self.assertRaises(TypeError, _get_authentication_token,
                          distiller_instance_url="", distiller_key=123)
        self.assertRaises(TypeError, _get_authentication_token,
                          distiller_instance_url="", distiller_key="",
                          timeout="")

    @patch("pystiller._core._authentication._requests." +
           "_perform_authentication_request")
    def test__get_authentication_token_bad_url(self, mock_auth_req):
        """Test the behaviour for bad instance URLs."""
        mock_auth_req.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _get_authentication_token,
                          distiller_instance_url="https://invalid-domain",
                          distiller_key="DISTILLER_API_KEY")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_authentication_token_bad_url_online(self):
        """Test the behaviour for bad instance URLs."""
        self.assertRaises(Exception, _get_authentication_token,
                          distiller_instance_url="https://invalid-domain",
                          distiller_key="DISTILLER_API_KEY")

    @patch("pystiller._core._authentication._requests." +
           "_perform_authentication_request")
    def test__get_authentication_token_output(self, mock_auth_req):
        """Test the output type of the request."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://example.org"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"token": "DISTILLER_TOKEN"})
                              .encode("utf-8"))
        mock_auth_req.return_value = response_
        token_ = _get_authentication_token(
            distiller_instance_url="https://example.org",
            distiller_key="DISTILLER_API_KEY"
        )
        self.assertIsInstance(token_, str)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_authentication_token_output_online(self):
        """Test the output type of the request."""
        token_ = _get_authentication_token(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        self.assertIsInstance(token_, str)
