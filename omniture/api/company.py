from collections import OrderedDict
from json import loads, dumps
from typing import Optional, Sequence, Iterable

import omniture as omniture_
from omniture.data import CompanyReportSuite, TrackingServerData


class Company:
    """
    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-methods-company
    """

    def __init__(self, omniture, name=None):
        # type: (omniture_.Omniture, Optional[str]) -> None
        self.omniture = omniture
        self.name = name

    def get_end_point(self, company) -> str:
        # type: (Optional[str]) -> str
        """
        Retrieves the endpoint for the specified company where API calls should be made.

        :param company:

            The company name, can also be passed in query string or WSSE header.

        :return:

            The company endpoint.
        """
        data = None
        if company is None:
            company = self.name
        if company is not None:
            data = dumps({
                "company": company
            })
        response = self.omniture.request(
            'Company.GetEndpoint',
            data=data
        )
        return loads(str(response.read(), 'utf-8'))

    def get_login_key(
        self,
        company=None,  # type: Optional[str]
        login=None,  # type: Optional[str]
        password=None  # type: Optional[str]
    ):
        # type: (...) -> str
        """
        Returns the api key when called with the correct username and password.

        :param company:

            Login company.

        :param login:

            Account name.

        :param password:

            Account password.

        :return:

            The API key.
        """
        response = self.omniture.request(
            'Company.GetLoginKey',
            data=dumps(OrderedDict([
                ('company', company or self.name),
                ('login', login),
                ('password', password),
            ]))
        )
        return loads(str(response.read(), 'utf-8'))

    def get_report_suites(
        self,
        types=('standard', 'rollup'),  # type: Optional[Sequence[str]]
        search=None  # type: Optional[str]
    ):
        # type: (...) -> Iterable[CompanyReportSuite]
        """
        Retrieves all report suites associated with the requesting company.

        :param types:

            A list of report suite types that you want to include in the report suite list.
            Supported types include: "standard" and "rollup".

        :param search:

            A search filter to apply in retrieving report suites.

        :return:


        """
        data = OrderedDict([
            ('types', types)
        ])
        if search is not None:
            data['search'] = search
        response = self.omniture.request(
            'Company.GetReportSuites',
            data=dumps(data)
        )
        for rs in loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)['report_suites']:
            yield CompanyReportSuite(rs)

    def get_tracking_server(self, rsid):
        # type: (str) -> TrackingServerData
        """
        Returns the tracking server and namespace for the specified report suite.

        :param rsid:

            The tracking server information for the specified report suite.

        :return:

            An instance of `ReportDescription` suitable for use in the Report API.
        """
        response = self.omniture.request(
            'Company.GetTrackingServer',
            data=dumps({'rsid': rsid})
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        return TrackingServerData(data)

    def get_version_access(self):
        # type: () -> Iterable[CompanyReportSuite]
        """
        Retrieves version access for the company of the authenticated user.

        :return:

            A list of Analytics interfaces to which the company has access.
        """
        response = self.omniture.request(
            'Company.GetVersionAccess'
        )
        for va in loads(str(response.read(), 'utf-8')):
            yield va
