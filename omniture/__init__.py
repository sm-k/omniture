import functools
import ssl
import time
from base64 import b64encode
from hashlib import sha1
from http.cookiejar import CookieJar
from json import loads
from numbers import Number
from typing import Dict, Optional, Union
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPSHandler
from uuid import uuid4

from omniture.api.bookmark import Bookmark
from omniture.api.calculated_metrics import CalculatedMetrics
from omniture.api.company import Company
from omniture.api.data_feed import DataFeed
from omniture.api.data_sources import DataSources
from omniture.api.permissions import Permissions
from omniture.api.report import Report
from omniture.api.report_suite import ReportSuite
from omniture.api.scheduling import Scheduling
from omniture.api.segments import Segments
from omniture.api.social import Social
from omniture.data import CreateReportSuiteResponse
from omniture.data import JSONObject, JSONArray, ReportDescription, ReportDescriptionMetric, \
    ReportDescriptionElement, CompanyReportSuite, BookmarkFolder, GetReportDescriptionResponse, Dashboard, \
    TrackingServerData, ReportResponse, ReportQueueItem, ReportMetric, ReportElement
from omniture.errors import ReportNotReadyError, BadRequest, AuthenticationError, InvalidReportID, \
    BookmarkNotSupportedError


class Omniture:
    """https://marketing.adobe.com/developer/documentation"""

    def __init__(
        self,
        company=None,  # type: Optional[str]
        user=None,  # type: Optional[str]
        password=None,  # type: Optional[str]
        version=None,  # type: Optional[str]
        host=None  # type: Optional[str]
    ):
        # type: (...) -> None
        r"""
        This class interfaces with Omniture's REST Web Service.

        :param user:

            This is your *API* User-Name (not the same as the user-name you log-in with on the website). It can
            be found on your Account Information page, under "Web Service". If you do not have a "Web Service" section
            on your Account Information page, you need to contact your administrator.

        :param password:

            Your "Shared Secret", which can be found under "Web Service" on your Account Information page.

        :param version:

            This is the version number of the REST interface your wish to use. Only version 1.4 is supported
            at this time.

        :param host:

            This is the URL of your data center. If not provided, it will be inferred automatically by attempting to
            connect to each data center sequentially.
                - api.omniture.com' # San Jose
                - api2.omniture.com # Dallas
                - api3.omniture.com # London
                - api4.omniture.com # Singapore
                - api5.omniture.com # Pacific NW
        """
        self._version = None
        self.version = version or '1.4'
        if company is not None:
            self.company.name = company
        self.user = user
        self.password = password
        if host is None:
            for i in range(6):
                self.host = 'api%s.omniture.com' % ('' if i == 0 else str(i))
                self.cookie_jar = CookieJar()
                self.opener = build_opener(
                    HTTPCookieProcessor(self.cookie_jar),
                    HTTPSHandler(context=ssl._create_unverified_context())
                )
                try:
                    end_point = self.company.get_end_point(company=self.company.name)
                    host = end_point.split('//')[-1].split('/')[0]
                    if host != self.host:
                        self.host = host
                        self.cookie_jar = CookieJar()
                        self.opener = build_opener(
                            HTTPCookieProcessor(self.cookie_jar),
                            HTTPSHandler(context=ssl._create_unverified_context())
                        )
                    break
                except URLError as e:
                    if i == 5:
                        raise e
        else:
            self.host = host
            self.cookie_jar = CookieJar()
            self.opener = build_opener(
                HTTPCookieProcessor(self.cookie_jar),
                HTTPSHandler(context=ssl._create_unverified_context())
            )

    @property
    def origin(self):
        return 'https://%s' % self.host

    @property
    def end_point(self):
        return (
            '%s/admin/%s/rest/' % (
                self.origin,
                self.version
            )
        )

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, v):
        # type: (Union[str, Number]) -> None
        if isinstance(v, Number):
            v = str(v)
        elif isinstance(v, str):
            v = v.strip()
        else:
            raise ValueError('Omniture.version requires a string or numeric version.')
        self._version = v

    def request(
        self,
        method=None,  # type: Optional[str]
        data=None,  # type: Optional[Union[Dict, str, bytes]]
        headers=None,  # type: Optional[Dict]
        timeout=None,  # type: Optional[int]
        echo=False  # type: bool
    ):
        # type: (...) -> HTTPResponse
        kw = {}
        if data is not None:
            if isinstance(data, (JSONObject, JSONArray)):
                data = str(data)
            if isinstance(data, str):
                data = bytes(data, 'utf-8')
            elif hasattr(data, 'items'):
                data = bytes(urlencode(data), 'utf-8')
            else:
                data = data
            kw['data'] = data
        if method:
            url = '%s?method=%s' % (self.end_point, method)
        else:
            url = self.end_point
        request = Request(
            url,
            **kw
        )
        if self.user and self.password and method != 'Company.GetLoginKey':
            nonce = str(uuid4())
            b64_nonce = str(
                b64encode(bytes(nonce, 'utf-8')),
                'utf-8'
            )
            created = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            password_digest = str(
                b64encode(sha1(
                    bytes(nonce + created + self.password, 'utf-8')
                ).digest()),
                'utf-8'
            )
            user = self.user
            if self.company.name is not None:
                user += ':' + self.company.name
            hs = {
                'X-WSSE': (
                    'UsernameToken ' +
                    'Username = "%s", ' % user +
                    'PasswordDigest = "%s", ' % password_digest +
                    'Nonce = "%s", ' % b64_nonce +
                    'Created = "%s"' % created
                )
            }
        else:
            hs = {}
        if headers is not None:
            hs.update(**headers)
        for k, v in hs.items():
            request.add_header(k, v)
        kw = {}
        if timeout is not None:
            kw['timeout'] = timeout

        def request_text():
            return (
                ('\n%s: %s\n' % (request.get_method(), url)) +
                '\n'.join(
                    '%s: %s' % (k, v)
                    for k, v in request.header_items()
                ) + (
                    ('\n' + str(request.data, encoding='utf-8'))
                    if request.data is not None
                    else ''
                )
            )
        if echo:
            print(request_text())
        try:
            response = self.opener.open(request, **kw)
        except HTTPError as e:
            response = str(e.file.read(), 'utf-8')
            e.msg = (
                'Request:\n' +
                request_text() +
                '\n\nResponse:\n' +
                response +
                '\n\n' +
                e.msg
            )
            if response:
                response_data = loads(response)
                if response_data['error'] == 'report_not_ready':
                    raise ReportNotReadyError(response_data)
                elif response_data['error'] == 5021:
                    raise InvalidReportID(response_data)
                elif response_data['error'] == 'Bad Request':
                    if 'authentication' in response_data['error_description']:
                        authentication_error = AuthenticationError(response_data)
                        if method != 'Company.GetLoginKey':
                            # If the user is attempting to use their account login, lookup
                            # their API "shared secret".
                            try:
                                self.password = self.company.get_login_key(
                                    company=self.company.name,
                                    login=self.user,
                                    password=self.password
                                )
                            except BadRequest:
                                raise authentication_error
                            return self.request(
                                method=method,
                                data=data,
                                headers=headers,
                                timeout=timeout,
                                echo=echo
                            )
                        raise authentication_error
                    elif response_data['error_description'] == 'This bookmark is not supported':
                        raise BookmarkNotSupportedError(response_data)
                    else:
                        raise BadRequest(response_data)
            raise e
        return response

    @property
    @functools.lru_cache(maxsize=1)
    def bookmark(self):
        return Bookmark(self)

    @property
    @functools.lru_cache(maxsize=1)
    def calculated_metrics(self):
        return CalculatedMetrics(self)

    @property
    @functools.lru_cache(maxsize=1)
    def company(self):
        return Company(self)

    @property
    @functools.lru_cache(maxsize=1)
    def data_feed(self):
        return DataFeed(self)

    @property
    @functools.lru_cache(maxsize=1)
    def data_sources(self):
        return DataSources(self)

    @property
    @functools.lru_cache(maxsize=1)
    def permissions(self):
        return Permissions(self)

    @property
    @functools.lru_cache(maxsize=1)
    def report(self):
        return Report(self)

    @property
    @functools.lru_cache(maxsize=1)
    def report_suite(self):
        return ReportSuite(self)

    @property
    @functools.lru_cache(maxsize=1)
    def scheduling(self):
        return Scheduling(self)

    @property
    @functools.lru_cache(maxsize=1)
    def segments(self):
        return Segments(self)

    @property
    @functools.lru_cache(maxsize=1)
    def social(self):
        return Social(self)


@functools.lru_cache()
def connect(
    company: str=None,
    user: str=None,
    password: str=None,
    version: Optional[str]=None,
    host: Optional[str]=None
) -> Omniture:
    return Omniture(
        company=company,
        user=user,
        password=password,
        version=version,
        host=host
    )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
