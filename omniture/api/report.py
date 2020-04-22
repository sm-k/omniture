from collections import OrderedDict
from json import loads, dumps
from typing import Optional, Sequence, Iterable

import omniture as omniture_
from omniture.data import ReportDescription, ReportResponse, ReportQueueItem, ReportMetric, ReportElement


class Report:
    """
    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/methods-1
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture

    def queue(self, report_description):
        # type: (ReportDescription) -> int
        """
        Queue a report to run.

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-queue

        :param report_description:

            An instance of `ReportDescription` detailing parameters of the report.

        :return:
            The ID of the report. Pass this ID to `Report.get` to retrieve the report.

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-queue
        """
        response = self.omniture.request(
            'Report.Queue',
            data=dumps({
                'reportDescription': report_description.data
            })
        )
        return loads(str(response.read(), 'utf-8'))['reportID']

    def cancel(self, report_id):
        # type: (int) -> bool
        """
        Cancels a previously submitted report request, and removes it from the processing queue.

        :param report_id:

            A report ID returned by `Report.queue`.

        :return:


        """
        response = self.omniture.request(
            'Report.Cancel',
            data=dumps({
                'reportID': report_id
            })
        )
        return loads(str(response.read(), 'utf-8'))

    def get(self, report_id):
        # type: (int) -> ReportResponse
        r"""
        Retrieves a report queued using `Report.queue`.

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-get

        :param report_id:

            A report ID returned by `Report.queue`.

        :return:

            The report is returned if it is ready, otherwise an HTTP error 400 is returned

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-get
        """
        response = self.omniture.request(
            'Report.Get',
            data=dumps({
                'reportID': report_id
            })
        )
        return ReportResponse(response.read())

    def get_queue(self):
        # type: () -> Iterable[ReportQueueItem]
        """
        Returns a list of reports in a company's report queue.

        :return:

            A list of the company's currently queued report requests.
            The company is determined by the authentication credentials provided with the request.

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-getqueue-2
        """
        response = self.omniture.request(
            'Report.GetQueue'
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        for rqi in data:
            yield ReportQueueItem(rqi)

    def run(self, report_description):
        # type: (ReportDescription) -> ReportResponse
        """
        Run a real-time report immediately without using the queue.
        For all other report types, use `Report.queue`.

        :param report_description:

            An instance of `ReportDescription` detailing parameters of the report.

        :return:

            The report is returned if it is ready, otherwise an HTTP error 400 is returned

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-run
        """
        response = self.omniture.request(
            'Report.Run',
            data=dumps({
                'reportDescription': report_description.data
            })
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        return ReportResponse(data['reportResponse'])

    def get_metrics(
        self,
        rsid,  # type: str,
        existing_elements=None,  # type: Optional[Sequence[str]]
        existing_metrics=None,  # type: Optional[Sequence[str]]
        report_type=None  # type: Optional[str]
    ):
        # type: (...) -> Iterable[ReportMetric]
        """
        Retrieves a list of possible valid metrics for a report.

        :param rsid:

            The Analytics report suite you want to use to generate the report.

        :param existing_elements:

            (optional) Include a list of elements already present in the
            `ReportDescription` to get compatible metrics.

        :param existing_metrics:

            (optional) Include a list of metrics already present in the
            `ReportDescription` to get compatible metrics.

        :param report_type:

            (optional) Include the report type (any, ranked, trended, pathing, fallout, realtime)
            to get compatible metrics.

        :return:

            Metrics available for the suite, optionally based on the elements, metrics,
            and report types specified.
        """
        request_data = {}
        for k, v in (
            ('reportSuiteID', rsid),
            ('existingElements', existing_elements),
            ('existingMetrics', existing_metrics),
            ('reportType', report_type)
        ):
            if v is not None:
                request_data[k] = v
        response = self.omniture.request(
            'Report.GetMetrics',
            data=dumps(request_data)
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        for d in data:
            yield ReportMetric(d)

    def get_elements(
        self,
        rsid,  # type: str,
        existing_elements=None,  # type: Optional[Sequence[str]]
        existing_metrics=None,  # type: Optional[Sequence[str]]
        report_type=None  # type: Optional[str]
    ):
        # type: (...) -> Iterable[ReportMetric]
        """
        Retrieves a list of possible valid elements for a report.

        :param rsid:

            The Analytics report suite you want to use to generate the report.

        :param existing_elements:

            (optional) Include a list of elements already present in the
            `ReportDescription` to get compatible metrics.

        :param existing_metrics:

            (optional) Include a list of metrics already present in the
            `ReportDescription` to get compatible metrics.

        :param report_type:

            (optional) Include the report type (any, ranked, trended, pathing, fallout, realtime)
            to get compatible metrics.

        :return:

            Elements available for the suite, optionally based on the elements, metrics,
            and report types specified.
        """
        request_data = {}
        for k, v in (
            ('reportSuiteID', rsid),
            ('existingElements', existing_elements),
            ('existingMetrics', existing_metrics),
            ('reportType', report_type)
        ):
            if v is not None:
                request_data[k] = v
        response = self.omniture.request(
            'Report.GetElements',
            data=dumps(request_data)
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        for d in data:
            yield ReportElement(d)

    def validate(self, report_description):
        # type: (ReportDescription) -> bool
        """
        Determines if a report description is valid without running the report. If the report is not valid,
        an error will be returned detailing the problem.

        :param report_description:

            The report structure that you want to validate.

        :return:

            Returns `True` if the operation is successful.
        """
        response = self.omniture.request(
            'Report.Validate',
            data=dumps({
                'reportDescription': report_description
            })
        )
        return loads(str(response.read(), 'utf-8'))
