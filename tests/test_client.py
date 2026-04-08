import os
import unittest
from unittest.mock import patch
import pandas as pd
from dotenv import load_dotenv

from pystiller.client import Client

load_dotenv()

class TestClient(unittest.TestCase):

    ##############
    # __init__() #
    ##############

    def test___init___types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, Client, distiller_key=123,
                          distiller_instance_url="https://example.org")
        self.assertRaises(ValueError, Client, distiller_key='',
                          distiller_instance_url="https://example.org")
        self.assertRaises(TypeError, Client, distiller_key="DISTILLER_API_KEY",
                          distiller_instance_url=123)
        self.assertRaises(ValueError, Client,
                          distiller_key="DISTILLER_API_KEY",
                          distiller_instance_url='')

    @patch("pystiller.client._env._read_environment_variable")
    @patch("pystiller.client._authentication._get_authentication_token")
    def test___init__1(self, mock_get_auth_token, mock_read_env_var):
        """Test the correct creation of the object."""
        mock_read_env_var.return_value = "test"
        mock_get_auth_token.return_value = "test"
        with patch.dict(os.environ, {
            "DISTILLER_API_KEY": "test",
            "DISTILLER_INSTANCE_URL": "test",
        }, clear=True):
            self._client = Client()
            self.assertIsInstance(self._client, Client)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test___init__1_online(self):
        """Test the correct creation of the object."""
        self._client = Client()
        self.assertIsInstance(self._client, Client)

    @patch("pystiller.client._authentication._get_authentication_token")
    def test___init__2(self, mock_get_auth_token):
        """Test the correct creation of the object."""
        mock_get_auth_token.return_value = "test"
        self.assertIsInstance(Client(
            distiller_key="DISTILLER_API_KEY",
            distiller_instance_url="DISTILLER_INSTANCE_URL"
        ), Client)

    @patch("pystiller.client._authentication._get_authentication_token")
    def test___init___instance_url_trailing_slash(self, mock_get_auth_token):
        """Test the behaviour for trailing slash in instance URLs."""
        mock_get_auth_token.return_value = "test"
        client_ = Client(
            distiller_key="DISTILLER_API_KEY",
            distiller_instance_url="https://example.org/")
        self.assertEqual(
            client_._distiller_instance_url,
            "https://example.org")

    ##################
    # get_projects() #
    ##################

    @patch("pystiller.client._authentication._get_authentication_token")
    @patch("pystiller.client._projects._get_projects")
    def test_get_projects(self, mock_get_projects, mock_get_auth):
        mock_get_projects.return_value = pd.DataFrame()
        mock_get_auth.return_value = "test_token"
        client_ = Client(distiller_key="DISTILLER_API_KEY",
                         distiller_instance_url="https://example.org",
                         automatic_token_refresh=True)
        projects_ = client_.get_projects()
        self.assertIsInstance(projects_, pd.DataFrame)

    # This test requires the DISTILLER_API_KEY and DISTILLER_INSTANCE_URL
    # environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_get_projects_online(self):
        client_ = Client()
        projects_ = client_.get_projects()
        self.assertIsInstance(projects_, pd.DataFrame)

    #################
    # get_reports() #
    #################

    @patch("pystiller.client._authentication._get_authentication_token")
    @patch("pystiller.client._datarama._get_reports")
    def test_get_reports(self, mock_get_reports, mock_get_auth):
        mock_get_reports.return_value = pd.DataFrame()
        mock_get_auth.return_value = "test_token"
        client_ = Client(distiller_key="DISTILLER_API_KEY",
                         distiller_instance_url="https://example.org",
                         automatic_token_refresh=True)
        reports_ = client_.get_reports(project_id=123)
        self.assertIsInstance(reports_, pd.DataFrame)

    # This test requires the DISTILLER_API_KEY, DISTILLER_INSTANCE_URL, and
    # DISTILLER_PROJECT_ID_TEST environment variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_get_reports_online(self):
        client_ = Client()
        reports_ = client_.get_reports(
            project_id=int(os.getenv("DISTILLER_PROJECT_ID_TEST")))
        self.assertIsInstance(reports_, pd.DataFrame)
        self.assertIsInstance(reports_, pd.DataFrame)

    ################
    # get_report() #
    ################

    @patch("pystiller.client._authentication._get_authentication_token")
    @patch("pystiller.client._datarama._get_report")
    def test_get_report(self, mock_get_report, mock_get_auth):
        mock_get_report.return_value = pd.DataFrame()
        mock_get_auth.return_value = "test_token"
        client_ = Client(distiller_key="DISTILLER_API_KEY",
                         distiller_instance_url="https://example.org",
                         automatic_token_refresh=True)
        report_ = client_.get_report(project_id=123, report_id=456)
        self.assertIsInstance(report_, pd.DataFrame)

    # This test requires the DISTILLER_API_KEY, DISTILLER_INSTANCE_URL,
    # DISTILLER_PROJECT_ID_TEST, and DISTILLER_REPORT_ID_TEST environment
    # variables to be set.
    # This test performs real requests to the DistillerSR API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_get_report_online(self):
        client_ = Client()
        report_ = client_.get_report(
            project_id=int(os.getenv("DISTILLER_PROJECT_ID_TEST")),
            report_id=int(os.getenv("DISTILLER_REPORT_ID_TEST")))
        self.assertIsInstance(report_, pd.DataFrame)
        self.assertIsInstance(report_, pd.DataFrame)
