from datetime import datetime, timedelta

from pystiller._core._datarama import ReportFormat
from pystiller._utils import _checks, _env
from pystiller._core import _authentication, _projects, _datarama


class Client:
    """Client class for working with the DistillerSR API.

    Attributes:
        _distiller_key (str): The API key used for authentication.
        _distiller_instance_url (str): The Distiller instance URL.
        _distiller_token (str): The Distiller authorization token.
        _automatic_token_refresh (bool): If True, automatic token refresh is
            performed when the token is going to expire.
        _distiller_token_last_update (datetime.datetime): The datetime of the
            last Distiller authentication token update (needed for refreshes).

    Methods:
        get_projects(): Gets the list of Distiller projects associated with the
            user.
        get_reports(project_id): Gets the list of Distiller reports associated
            to a project.
        get_report(project_id, report_id): Retrieves a specific Distiller
            report.
        _get_or_refresh_token(): Checks if the Distiller token is still valid.
            If not, it will request a new one. If the token is not set (e.g.,
            at client initialisation), it will request it.
    """

    def __init__(self, distiller_key=None, distiller_instance_url=None,
                 automatic_token_refresh=False):
        """Initialize the client.

        Args:
            distiller_key (str, optional): The API key used for authentication.
            distiller_instance_url (str, optional): The Distiller instance URL.
            automatic_token_refresh (bool, optional): If True, automatically
                refresh the Distiller token if it is going to expire. Defaults
                to False.

        Examples:
            >>> from pystiller import Client

            >>> # Create a client using the API key and the instance URL
            >>> # defined in the .env file.
            >>> client_with_default = Client()

            >>> # Create a client using manually specified API key and instance
            >>> # URL.
            >>> client_with_customs = Client(
            >>>     distiller_key="<your_distiller_api_key>",
            >>>     distiller_instance_url="<your_distiller_instance_url>"
            >>> )
        """

        if distiller_key is not None:
            self._distiller_key = distiller_key
        else:
            self._distiller_key = _env._read_environment_variable(
                name="DISTILLER_API_KEY")

        _checks._require_type(value=self._distiller_key, expected_type=str)
        _checks._require_string_not_empty(value=self._distiller_key)

        if distiller_instance_url is not None:
            self._distiller_instance_url = distiller_instance_url
        else:
            self._distiller_instance_url = _env._read_environment_variable(
                name="DISTILLER_INSTANCE_URL")

        _checks._require_type(value=self._distiller_instance_url,
                              expected_type=str)
        _checks._require_string_not_empty(value=self._distiller_instance_url)

        if self._distiller_instance_url.endswith('/'):
            self._distiller_instance_url = self._distiller_instance_url[:-1]

        self._automatic_token_refresh = automatic_token_refresh
        _checks._require_type(value=self._automatic_token_refresh,
                              expected_type=bool)

        self._distiller_token = None
        self._distiller_token_last_update = None

        self._get_or_refresh_token()


    def _get_or_refresh_token(self):
        """Get or refresh a Distiller token.

        This helper function checks if the Distiller token is still valid. If
        not, it will request a new one. If the token is not set (e.g., at
        client initialisation), it will request it. Checks are based on the
        last token update timestamp. The default duration for Distiller tokens
        is 60 minutes (1 hour). The refresh will happen if the token is older
        than 55 minutes.

        Returns:
            None: The functions returns nothing.
        """

        token_missing_ = not self._distiller_token

        now_ = datetime.now()

        token_expired_ = (
            self._distiller_token_last_update and
            now_ - self._distiller_token_last_update >= timedelta(minutes=55)
        )

        if token_missing_ or token_expired_:
            self._distiller_token = _authentication._get_authentication_token(
                distiller_instance_url=self._distiller_instance_url,
                distiller_key=self._distiller_key)
            self._distiller_token_last_update = now_


    def get_projects(self, timeout=1800):
        """Get the list of the Distiller projects associated to the user.

        This function queries the DistillerSR API to retrieve the list of
        projects accessible to the authenticated user. The result is a data
        frame listing available projects.

        Args:
            timeout (int, optional): The maximum number of seconds to wait for
                the response. Defaults to 1800 seconds (30 minutes).

        Returns:
            pd.DataFrame: A data frame with four columns:
                - id: The project ID.
                - name: The project name.
                - de_project_id.
                - is_hidden.

        Examples:
            >>> from pystiller import Client

            >>> client = Client()

            >>> # Get the list of available projects.
            >>> projects = client.get_projects()
        """

        if self._automatic_token_refresh:
            self._get_or_refresh_token()

        return _projects._get_projects(
            distiller_instance_url=self._distiller_instance_url,
            distiller_token=self._distiller_token,
            timeout=timeout)


    def get_reports(self, project_id, timeout=1800):
        """Get the list of the Distiller reports associated to a project.

        This function queries the DistillerSR API to retrieve the list of
        reports associated with a project. The result is a data frame listing
        available reports.

        Args:
            project_id (int): The ID of the project as provided by DistillerSR.
            timeout (int, optional): The maximum number of seconds to wait for
                the service response. Defaults to 1800 seconds (30 minutes).

        Returns:
            pd.DataFrame: A data frame with four columns:
                - id: The project ID.
                - name: The project name.
                - date: The creation date of the report.
                - view: The format of the report (e.g., html, csv, excel).

        Examples:
            >>> from pystiller import Client

            >>> client = Client()

            >>> # Get the list of available reports.
            >>> reports = client.get_reports(project_id=123)
        """

        if self._automatic_token_refresh:
            self._get_or_refresh_token()

        return _datarama._get_reports(
            project_id=project_id,
            distiller_instance_url=self._distiller_instance_url,
            distiller_token=self._distiller_token,
            timeout=timeout)


    def get_report(self, project_id, report_id,
                   report_format = ReportFormat.CSV, timeout=1800, attempts=1,
                   retry_each=600, verbose=True):
        """Get a Distiller report associated to a project.

        This function queries the DistillerSR API to retrieve a saved report
        associated with a project. The result is a data frame containing
        metadata about the saved report.

        Args:
            project_id (int): The ID of the project as provided by DistillerSR.
            report_id (int): The ID of the report as provided by DistillerSR.
            report_format (ReportFormat, optional): The desired format of the
                document. Defaults to CSV (Comma Separated Values).
            timeout (int, optional): The maximum number of seconds to wait for
                the service response. Defaults to 1800 seconds (30 minutes).
            attempts (int, optional): The maximum number of attempts. Defaults
                to 1 attempt.
            retry_each (int, optional): The delay between attempts. Defaults to
                600 seconds (10 minutes).
            verbose (bool, optional): A flag to specify whether to make the
                function verbose or not. Defaults to True.

        Returns:
            pd.DataFrame: A data frame containing the Distiller report as
                designed within DistillerSR.

        Examples:
            >>> from pystiller import Client, ReportFormat

            >>> client = Client()

            >>> # Get a specific report.
            >>> report = client.get_report(project_id=123, report_id=456)
        """

        if self._automatic_token_refresh:
            self._get_or_refresh_token()

        return _datarama._get_report(
            project_id=project_id,
            report_id=report_id,
            distiller_instance_url=self._distiller_instance_url,
            distiller_token=self._distiller_token,
            report_format=report_format,
            timeout=timeout,
            attempts=attempts,
            retry_each=retry_each,
            verbose=verbose)
