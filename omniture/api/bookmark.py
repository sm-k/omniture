from collections import OrderedDict
from json import loads, dumps
from typing import Optional, Iterable

import omniture as omniture_
from omniture.data import BookmarkFolder, GetReportDescriptionResponse, Dashboard


class Bookmark:
    """
    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/c-methods-bookmark
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture

    def get_bookmarks(
        self,
        folder_limit=None,  # type: Optional[int]
        folder_offset=None  # type: Optional[int]
    ):
        # type: (...) -> Iterable[BookmarkFolder]
        """
        Retrieves a list of bookmarks for the authenticated user.
        Parameters folder_limit and folder_offset are optional, and only necessary if the total bookmark count
        exceeds 500,  which is the limit. Use them to select a certain range of folders out of the entire set.

        :param folder_limit:

            (optional) Limit the retrieval to the specified number of bookmarks.

        :param folder_offset:

            (optional) Start the bookmark retrieval at the specified offset.

        :return:

            Bookmark folders and the bookmarks that are contained in each folder.
        """
        data = OrderedDict()
        if folder_limit is not None:
            data['folder_limit'] = folder_limit
        if folder_offset is not None:
            data['folder_offset'] = folder_offset
        response = self.omniture.request(
            'Bookmark.GetBookmarks',
            data=dumps(data)
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        for bf in data['folders']:
            yield BookmarkFolder(bf)

    def get_dashboards(
        self,
        dashboard_limit=None,  # type: Optional[int]
        dashboard_offset=None  # type: Optional[int]
    ):
        # type: (...) -> Iterable[Dashboard]
        """
        Retrieves a list of dashboards for the authenticated user.
        Parameters `dashboard_limit` and `dashboard_offset` are optional, and only necessary if the total dashboard
        count exceeds 500,  which is the limit. Use them to select a certain range of dashboards out of the entire set.

        :param dashboard_limit:

            (optional) Limit the retrieval to the specified number of dashboards.

        :param dashboard_offset:

            (optional) Start the dashboard retrieval at the specified offset.

        :return:

            Bookmark folders and the bookmarks that are contained in each folder.
        """
        data = OrderedDict()
        if dashboard_limit is not None:
            data['dashboard_limit'] = dashboard_limit
        if dashboard_offset is not None:
            data['dashboard_offset'] = dashboard_offset
        response = self.omniture.request(
            'Bookmark.GetDashboards',
            data=dumps(data)
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        for d in data['dashboards']:
            yield Dashboard(d)

    def get_report_description(
        self,
        bookmark_id  # type: int
    ):
        # type: (...) -> GetReportDescriptionResponse
        """
        Retrieves the name, associated report type, and report description for the supplied bookmark ID.
        This report description can then be used to retrieve report data via the Report API.
        An error is returned for unsupported bookmark types.

        :param bookmark_id:

            (required) The ID of the bookmark for which you want to retrieve the report description.

        :return:

            An instance of `ReportDescription` suitable for use in the Report API.
        """
        response = self.omniture.request(
            'Bookmark.GetReportDescription',
            data=dumps({'bookmark_id': bookmark_id})
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        return GetReportDescriptionResponse(data)
