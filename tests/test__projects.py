import json
import os
import unittest
from unittest.mock import patch
import pandas as pd
import requests
from dotenv import load_dotenv
from pystiller._core import _authentication
from requests import Response

from pystiller._core._projects import _get_projects

load_dotenv()


class TestProjects(unittest.TestCase):

    ###################
    # _get_projects() #
    ###################

    def test__get_projects_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _get_projects,
                          distiller_instance_url=123, distiller_token="")
        self.assertRaises(TypeError, _get_projects,
                          distiller_instance_url="", distiller_token=123)
        self.assertRaises(TypeError, _get_projects,
                          distiller_instance_url="", distiller_token="",
                          timeout="")

    @patch("pystiller._core._projects._requests._perform_service_request")
    def test__get_projects_bad_url(self, mock_serv_req):
        """Test the behaviour for bad instance URLs."""
        mock_serv_req.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _get_projects,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_projects_bad_url_online(self):
        """Test the behaviour for bad instance URLs."""
        self.assertRaises(Exception, _get_projects,
                          distiller_instance_url="https://invalid-domain",
                          distiller_token="DISTILLER_TOKEN")

    @patch("pystiller._core._projects._requests._perform_service_request")
    def test__get_projects_output(self, mock_serv_req):
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
        response_ = _get_projects(
            distiller_instance_url="https://example.org",
            distiller_token="DISTILLER_TOKEN"
        )
        self.assertIsInstance(response_, pd.DataFrame)
        self.assertEqual(len(response_.columns), 4)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__get_projects_output_online(self):
        """Test the output type of the request."""
        token_ = _authentication._get_authentication_token(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_key=os.getenv("DISTILLER_API_KEY")
        )
        response_ = _get_projects(
            distiller_instance_url=os.getenv("DISTILLER_INSTANCE_URL"),
            distiller_token=token_
        )
        self.assertIsInstance(response_, pd.DataFrame)
        self.assertEqual(len(response_.columns), 4)
