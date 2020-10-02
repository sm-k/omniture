"""
This module describes JSON data types used in Omniture's REST API:

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/datatypes
"""

from collections import OrderedDict
from datetime import datetime, date
from json import loads, dumps
from typing import Union, Optional, Dict, Sequence, Iterable, AnyStr
import re


def str2date(s: str):
    dt = datetime.strptime(s, '%Y-%m-%d')
    return date(dt.year, dt.month, dt.day)


def str2datetime(s: str):
    errors = []
    for f in (
        '%Y-%m-%dT%H:%M:%S',  # ISO datetime
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S%Z',
        '%Y-%m-%dT%H:%M:%S%Z%z',
        '%Y-%m-%d %H:%M:%S',  # python datetime
        '%Y-%m-%d %H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S%Z',
        '%Y-%m-%d %H:%M:%S%Z%z'
    ):
        try:
            return datetime.strptime(s, f)
        except ValueError as e:
            errors.append(e)
    raise ValueError(
        '\n'.join(str(e) for e in errors)
    )


class JSONArray(list):
    """
    This is a base class for building JSON arrays to be used in Omniture requests and responses.
    """

    def __init__(self, *args):
        """
        In child classes, initialization should accept arguments matching the JSON object's
        properties, and should assign these values *explicitly* to attributes of the same name.
        """
        super().__init__(*args)

    @property
    def data(self):
        # type: ()-> list
        """
        :return: A list of values campatible with JSON serialization.
        """
        l = []
        for v in self:
            if v is None:
                continue
            if isinstance(v, (JSONArray, JSONObject)):
                v = v.data
            elif isinstance(v, Sequence) and not isinstance(v, (str, bytes)):
                v = JSONArray(v).data
            #elif isinstance(v, Dict) and not isinstance(v, (str, bytes)):
            #    v = JSONObject(v).data
            elif isinstance(v, date):
                v = v.strftime('%Y-%m-%d')
            elif isinstance(v, datetime):
                v = v.strftime('%Y-%m-%dT%H:%M:%S%z')
            l.append(v)
        return l

    def __str__(self):
        # type: () -> str
        """
        :return: A JSON representation of this array.
        """
        return dumps(self.data)

    def __repr__(self):
        # type: () -> str
        """
        :return: A text representation of this array suitable for evaluating in Python.
        """
        r = '[%s]' % (
            '\n    ' + ',\n    '.join(
                (
                    '\n\t'.join(repr(v).split('\n')) if isinstance(v, JSONObject)
                    else re.sub(
                        r'(\r?\n)\s*',
                        r'',
                        re.sub(
                            r'(,\r?\n)\s*',
                            r', ',
                            repr(v)
                        )
                    )
                )
                for v in self
            ) + '\n'
            if self
            else ''
        )
        cn = self.__class__.__name__.split('.')[-1]
        if cn != 'JSONArray':
            r = '%s(%s)' % (cn, r)
        return r

    def __eq__(self, other):
        # type: (object) -> bool
        if isinstance(other, self.__class__) and self.data == other.data:
            return True
        else:
            return False

    def __ne__(self, other):
        # type: (object) -> bool
        if self == other:
            return False
        else:
            return True


class JSONObject:
    """
    This is a base class for building JSON objects to be used in Omniture requests and responses.
    """

    _keys_attributes = OrderedDict()  # type: Dict

    def __init__(self):
        # type: () -> None
        """
        In child classes, initialization should accept arguments matching the JSON object's properties, and should
        assign these explicitly to attributes of the same name.
        """
        pass

    @property
    def data(self):
        # type: () -> Dict
        """
        :return:

            An ordered dictionary of the data represented by this object, in formats suitable for
            JSON serialization.
        """
        d = OrderedDict()
        for k, v in self.items():
            if v is None:
                continue
            if isinstance(v, (JSONArray, JSONObject)):
                v = v.data
            elif isinstance(v, Sequence) and not isinstance(v, (str, bytes)):
                v = JSONArray(v).data
            #elif isinstance(v, Dict) and not isinstance(v, (str, bytes)):
            #    v = JSONObject(v).data
            elif isinstance(v, date):
                v = v.strftime('%Y-%m-%d')
            elif isinstance(v, datetime):
                v = v.strftime('%Y-%m-%dT%H:%M:%S%z')
            d[k] = v
        return d

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: str
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Dict
        for k, v in data.items():
            if (v is None) or v == '':
                continue
            a = self._keys_attributes[k]  # type: str
            setattr(self, a, v)

    def items(self):
        # type: () -> Iterable[Tuple[str]]
        """
        Iterates through the key/value pairs of the corresponding JSON object.

        :return:

            An iterable of 2-item tuples representing JSON key/value pairs.
        """
        for k, a in self._keys_attributes.items():
            v = getattr(self, a)
            if v is not None:
                yield k, v

    def keys(self):
        """
        :return: The keys from the JSON object represented.
        """
        # type: () -> Iterable[str]
        for k, v in self.items():
            yield k

    def values(self):
        # type: () -> Iterable[str]
        """
        :return: The values from the JSON object represented.
        """
        for k, v in self.items():
            yield v

    def __str__(self):
        # type: () -> str
        """
        :return: A JSON representation of this object.
        """
        d = OrderedDict()
        for k, v in self.data.items():
            if v is not None:
                d[k] = v
        return dumps(d)

    def __repr__(self):
        # type: () -> str
        """
        :return: A text representation of this object suitable for evaluating in Python.
        """
        items = tuple(self.items())
        return '%s(%s)' % (
            self.__class__.__name__.split('.')[-1],
            (
                '\n    ' + ',\n    '.join(
                    (
                        self._keys_attributes[k] + '=' + re.sub(
                            r'(\r?\n)\s*',
                            r'',
                            re.sub(
                                r'(,\r?\n)\s*',
                                r', ',
                                repr(v)
                            )
                        )
                    )
                    for k, v in items
                    if v is not None
                ) + '\n'
                if items
                else ''
            )
        )

    def __eq__(self, other):
        # type: (object) -> bool
        if isinstance(other, self.__class__) and self.data == other.data:
            return True
        else:
            return False

    def __ne__(self, other):
        # type: (object) -> bool
        if self == other:
            return False
        else:
            return True


class DataWarehouseRequest(JSONObject):

    
    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('Contact_Name', 'contact_name'),
        ('Contact_Phone', 'contact_phone'),
        ('Email_To', 'email_to'),
        ('Email_Subject', 'email_subject'),
        ('Report_Name', 'report_name'),
        ('Report_Description', 'report_description'),
        ('File_Name', 'file_name'),
        ('Date_Type', 'date_type'),
        ('Date_Preset', 'date_preset'),
        ('Date_To', 'date_to'),
        ('Date_From', 'date_from'),
        ('Date_Granularity', 'date_granularity'),
        ('Segment_Id', 'segment_id'),
        ('Metric_List', 'metric_list'),
        ('Breakdown_List', 'breakdown_list'),
        ('FTP_Host', 'ftp_host'),
        ('FTP_Port', 'ftp_post'),
        ('FTP_Dir', 'ftp_dir'),
        ('FTP_UserName', 'ftp_username'),
        ('FTP_Password', 'ftp_password')
    ])
    

    def __init__(
        self,
        data=None,
        rsid=None,
        contact_name=None,
        contact_phone=None,
        email_to=None,
        email_subject=None,
        report_name=None,
        report_description=None,
        file_name=None,
        date_type=None,
        date_preset=None,
        date_to=None,
        date_from=None,
        date_granularity=None,
        segment_id=None,
        metric_list=None,
        breakdown_list=None,
        ftp_host=None,
        ftp_post=None,
        ftp_dir=None,
        ftp_username=None,
        ftp_password=None
    ):
        
        self.rsid = rsid
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.email_to = email_to
        self.email_subject = email_subject
        self.report_name = report_name
        self.report_description = report_description
        self.file_name = file_name
        self.date_type = date_type
        self.date_preset = date_preset
        self.date_to = date_to
        self.date_from = date_from
        self.date_granularity = date_granularity
        self.segment_id = segment_id
        self.metric_list = metric_list
        self.breakdown_list = breakdown_list
        self.ftp_host = ftp_host
        self.ftp_post = ftp_post
        self.ftp_dir = ftp_dir
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
        
        if data is not None:
            self.data = data
    

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            k = k.strip()
            print(k, v)
            if v is None:
                continue
            if k in ('date', 'dateFrom', 'dateTo'):
                v = str2date(v)
            a = self._keys_attributes[k]
            setattr(self, a, v)
        
        
class ReportDescriptionMetric(JSONObject):
    """
    A structure that identifies one metric used in a report.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescriptionmetric
    """

    _keys_attributes = OrderedDict([
        ('id', 'metric_id')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        metric_id=None,  #type: Optional[str]
    ):
        self.metric_id = metric_id
        if data is not None:
            self.data = data


class ReportDescriptionSearch(JSONObject):
    """
    A structure that defines a keyword search to use in the report definition.
    """

    _keys_attributes = OrderedDict([
        ('type', 'search_type'),
        ('keywords', 'keywords'),
        ('searches', 'searches')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        search_type=None,  # type: Optional[str],
        keywords=None,  # type: Optional[Sequence[str]],
        searches=None  # type: Optional[Union[Sequence[ReportDescriptionSearch],ReportDescriptionSearch]]
    ):
        """
        :param report_description_search_type:

            The type of search to use: "and", "or" or "not".

        :param keywords:

            A list of keywords to include or exclude from the search, based on the type.
            Keyword values can also leverage the following special characters to define advanced search criteria:

                * Wild Card (e.g. "page*.html")
                ^ Starts With (e.g. "^http://")
                $ Ends With (e.g. ".html$")

        :param searches:

            A list of subsearches. This allows you to build complex report searches.

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescriptionsearch
        """
        self.search_type = search_type
        self.keywords = keywords
        if isinstance(searches, ReportDescriptionSearch):
            searches = [ReportDescriptionSearch]
        self.searches = searches
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'searches':
                v = JSONArray([ReportDescriptionSearch(rds) for rds in v])
            setattr(self, a, v)


class ReportDescriptionSegment(JSONObject):
    """
    A structure that defines an inline segment to use in a `ReportDescription`.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescriptionsegment
    """

    _keys_attributes = OrderedDict([
        ('id', 'segment_id'),
        ('element', 'element'),
        ('search', 'search'),
        ('classification', 'classification'),
        ('selected', 'selected')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        segment_id=None,  # type: Optional[str]
        element=None,  # type: Optional[str]
        search=None,  # type: Optional[ReportDescriptionSearch]
        classification=None,  # type: Optional[str]
        selected=None  # type: Optional[Sequence[str]]
    ):
        """
        :param segment_id:

            (depracated) Specifies the existing saved segment ID that you want to apply to a search.

        :param element:

            Specifies the element (dimension) on which you want to segment.

        :param search:

            (Optional, provide either a selected value, or a classification and a search value).

        :param classification:

            (Optional, provide either a selected value, or a classification and a search value).
            Specifies how to integrate the include and an exclude segments.

        :param selected:

            ?

        Unsupported Elements:

            The following elements are not supported for inline segments.

             - pagedepth
             - visitnumber
             - mobilecarrier
             - hier*
             - *paths
             - *fallout
        """
        self.segment_id = segment_id
        self.element = element
        self.search = search
        self.classification = classification
        if isinstance(selected, str):
            selected = [selected]
        self.selected = selected
        if data is not None:
            self.data = data


class ReportDescriptionElement(JSONObject):
    """
    A structured data type that identifies one element used in a report.
    """

    _keys_attributes = OrderedDict([
        ('id', 'element_id'),
        ('classification', 'classification'),
        ('top', 'top'),
        ('startingWith', 'starting_with'),
        ('search', 'search'),
        ('selected', 'selected'),
        ('parentID', 'parent_id'),
        ('checkpoints', 'checkpoints'),
        ('pattern', 'pattern')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        element_id: Optional[str]=None,
        classification: Optional[str]=None,
        top: Optional[int]=None,
        starting_with: Optional[int]=None,
        search: Optional[int]=None,
        selected: Optional[int]=None,
        parent_id: Optional[int]=None,
        checkpoints: Optional[int]=None,
        pattern: Optional[Sequence[Sequence[str]]]=None
    ):
        """
        :param element_id:

            Specifies the name of the element to apply to the metrics report.

        :param classification:

            (Optional) Restricts the element results to only those that fall in the specified classification.
            For example you could set id = "trackingCode" and classification = "Campaigns" to get a report of
            all tracking codes for the Campaigns classification.

        :param top:

            (Optional) Specifies the number of rows in the report to return. Use with startingWith to generate paged
            reports. For example, top=5 returns five rows.

            The maximum number of top elements that can be requested is 50,000. Setting the "top" parameter to a number
            greater than 50000 will result in an element_top_invalid error.

        :param starting_with:

            (Optional) Specifies the first row in the report to return. Use with top to generate paged reports.
            For example, startingWith=20 returns report rows starting at row 20.

        :param search:

            (Optional) Applies a search to the element.

        :param selected:

            (Optional) Defines a specific list of items to request instead of using search, top, and startingWith to set
            the element parameters.

        :param parent_id:

            (Optional) Hierarchy report. To specify a specific level to report, add a level and parentID parameter. The
            parentID is returned in report data, making it available to request the next level of the hierarchy.

        :param checkpoints:

            Generates a pathing report.
            See https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/pathing

        :param pattern:

            Generates a fallout pathing report.
            See https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/pathing

        https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdescriptionelement
        """
        self.element_id = element_id
        self.classification = classification
        self.top = top
        self.starting_with = starting_with
        self.search = search
        self.selected = selected
        self.parent_id = parent_id
        self.checkpoints = checkpoints
        self.pattern = pattern
        if data is not None:
            self.data = data


class FTP(JSONObject):

    _keys_attributes = OrderedDict([
        ('host', 'host'),
        ('port', 'port'),
        ('directory', 'directory'),
        ('username', 'username'),
        ('password', 'password'),
        ('filename', 'filename')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        host: Optional[str]=None,
        port: Optional[int]=None,
        directory: Optional[str]=None,
        username: Optional[str]=None,
        password: Optional[str]=None,
        filename: Optional[str]=None,
    ):
        self.host = host
        self.port = port
        self.directory = directory
        self.username = username
        self.password = password
        self.filename = filename
        if data is not None:
            self.data = data

class RSMetric(JSONObject):

    _keys_attributes = OrderedDict([
        ('metric_name', 'metric_name'),
        ('display_name', 'display_name')
    ])
    
    def __init__(
        self,
        data=None,
        metric_name=None,
        display_name=None
    ):
        self.metric_name = metric_name 
        self.display_name = display_name 
        
        if data is not None:
            self.data = data
        
    @property
    def data(self):
        return super().data
        
class AvailableMetricsResponse(JSONObject):
    
    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('available_metrics', 'available_metrics')
    ])
    
    def __init__(
        self,
        data=None,
        rsid=None,
        site_title=None,
        available_metrics=None
    ):
        self.rsid = rsid
        self.site_title = site_title 
        self.available_metrics = available_metrics

        if data is not None:
            self.data = data
        
    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        data = data[0]
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            k = k.strip()
            if v is None:
                continue
            elif k == 'available_metrics':
                v = JSONArray([
                    RSMetric(metric_name=e['metric_name'], display_name=e['display_name'])
                    for e in v
                ])
            a = self._keys_attributes[k]
            setattr(self, a, v)
        
        
class RSElement(JSONObject):

    _keys_attributes = OrderedDict([
        ('element_name', 'element_name'),
        ('display_name', 'display_name')
    ])
    
    def __init__(
        self,
        data=None,
        element_name=None,
        display_name=None
    ):
        self.element_name = element_name 
        self.display_name = display_name 
        
        if data is not None:
            self.data = data
        
    @property
    def data(self):
        return super().data
        
class AvailableElementsResponse(JSONObject):
    
    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('available_elements', 'available_elements')
    ])
    
    def __init__(
        self,
        data=None,
        rsid=None,
        site_title=None,
        available_elements=None
    ):
        self.rsid = rsid
        self.site_title = site_title 
        self.available_elements = available_elements

        if data is not None:
            self.data = data
        
    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        data = data[0]
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            k = k.strip()
            if v is None:
                continue
            elif k == 'available_elements':
                v = JSONArray([
                    RSElement(element_name=e['element_name'], display_name=e['display_name'])
                    for e in v
                ])
            a = self._keys_attributes[k]
            setattr(self, a, v)
        
class ReportDescription(JSONObject):
    """
    A structure that contains information for creating a specific report.
    """

    _keys_attributes = OrderedDict([
        ('reportSuiteID', 'rsid'),
        ('date', 'date_from_to'),
        ('dateFrom', 'date_from'),
        ('dateTo', 'date_to'),
        ('dateGranularity', 'date_granularity'),
        ('source', 'source'),
        ('metrics', 'metrics'),
        ('elements', 'elements'),
        ('locale', 'locale'),
        ('sortMethod', 'sort_method'),
        ('sortBy', 'sort_by'),
        ('segments', 'segments'),
        ('anomalyDetection', 'anomaly_detection'),
        ('currentData', 'current_data'),
        ('expedite', 'expedite'),
        ('elementDataEncoding', 'element_data_encoding'),
        ('ftp', 'ftp'),
        ('segment_id', 'segment_id')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        rsid: Optional[str]=None,
        date_from_to: Optional[date]=None,
        date_from: Optional[date]=None,
        date_to: Optional[date]=None,
        date_granularity: Optional[str]=None,
        source: Optional[str]=None,
        metrics: Optional[Sequence[Union[str, ReportDescriptionMetric]]]=None,
        elements: Optional[Sequence[ReportDescriptionElement]]=None,
        locale: Optional[Sequence[str]]=None,
        sort_method: Optional[str]=None,
        sort_by: Optional[str]=None,
        segments: Optional[Union[Sequence[ReportDescriptionSegment], ReportDescriptionSegment]]=None,
        anomaly_detection: Optional[bool]=None,
        current_data: Optional[bool]=None,
        expedite: Optional[bool]=None,
        element_data_encoding: Optional[str]=None,
        ftp: Optional[FTP]=None,
        segment_id: Optional[str]=None
    ):
        """
        :param rsid:
            The id of the report suite in which this report should be run.

        :param date_from_to:
            The date on wich to report.
            The `date_from_to` argument should only be provided when `date_from` and `date_to` are *not* provided.

        :param date_from:
            The earliest date in the range being reported (must be on or after 2000-01-01).

        :param date_to:
            The latest date in the range being reported (must be on or before 2899-12-31).

        :param date_granularity:
            "minute", "hour", "day", "week", "month", "quarter", or "year".

        :param source:
            "standard" or "realtime".

        :param metrics:
            A list of `ReportDescriptionMetric` objects. At least one metric must be provided.

        :param elements:
            A list of elements (`ReportDescriptionElement` objects) that breaks down (organizes) the metrics
            data in the report.

        :param locale:
            A list of the locale codes to be reported. locale codes, including the following:
                - "en_US" for English (United States)
                - "de_DE" for German (Germany)
                - "es_ES" for Spanish (Spain)
                - "fr_FR" for French (France)
                - "jp_JP" for Japanese (Japan)
                - "pt_BR" for Portuguese (Brazil)
                - "ko_KR" for Korean (Korea)
                - "zh_CN" for Chinese (China)
                - "zh_TW" for Chinese (Taiwan)

        :param sort_method:
            "algorithm", "floorSensitivity", "firstRankPeriod", or "algorithmArgument".
            Only used when source = 'realtime'

        :param sort_by:
            The `ReportDescriptionMetric` ID to sort by.

        :param segments:
            A sequence of `ReportDescriptionSegment` objects.

        :param anomaly_detection:
            Return the upper bounds, lower bounds, and forecast data for anomaly detection.

        :param current_data:
            Include current data in the report. Defaults to `True` when available.

        :param expedite:
            Generates the report with a higher priority.

        :param element_data_encoding:
            "base64" or "utf8"

        :param ftp:

            ?
        """
        if metrics is not None:
            if isinstance(metrics, str):
                metrics = [metrics]
            metrics = JSONArray([
                m
                if isinstance(m, ReportDescriptionMetric)
                else ReportDescriptionMetric(metric_id=m)
                if isinstance(m, str)
                else ReportDescriptionMetric(m)
                for m in metrics
            ])
        if elements is not None:
            if isinstance(elements, str):
                elements = [elements]
            elements = JSONArray([
                e
                if isinstance(e, ReportDescriptionElement)
                else ReportDescriptionElement(element_id=e)
                for e in elements
            ])
        self.rsid = rsid
        self.date_from_to = date_from_to
        self.date_from = date_from
        self.date_to = date_to
        self.date_granularity = date_granularity
        self.source = source
        self.metrics = metrics
        self.elements = elements
        self.locale = locale
        self.sort_method = sort_method
        self.sort_by = sort_by
        if segments is not None:
            if isinstance(segments, ReportDescriptionSegment):
                segments = [segments]
            # segments = JSONArray(segments)
        self.segments = segments
        self.anomaly_detection = anomaly_detection
        self.current_data = current_data
        self.expedite = expedite
        self.element_data_encoding = element_data_encoding
        self.ftp = ftp
        self.segment_id = segment_id
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            k = k.strip()
            if v is None:
                continue
            if k in ('date', 'dateFrom', 'dateTo'):
                v = str2date(v)
            elif k == 'metrics':
                v = JSONArray([
                    ReportDescriptionMetric(metric)
                    for metric in v
                ])
            elif k == 'elements':
                v = JSONArray([
                    ReportDescriptionElement(element)
                    for element in v
                ])
            elif k == 'segments':
                v = JSONArray([
                    ReportDescriptionSegment(segment)
                    for segment in v
                ])
            elif k == 'ftp':
                v = FTP(v)
            a = self._keys_attributes[k]
            setattr(self, a, v)


class CompanyReportSuite(JSONObject):

    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('virtual', 'virtual')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        rsid: Optional[str]=None,
        site_title: Optional[str]=None,
        virtual: Optional[bool]=None
    ):
        self.rsid = rsid
        self.site_title = site_title
        self.virtual = virtual
        if data is not None:
            self.data = data


class ReportQueueItem(JSONObject):
    """
    A structure that contains queue data related to a requested report.
    """

    _keys_attributes = OrderedDict([
        ('reportSuiteID', 'rsid'),
        ('reportID', 'report_id'),
        ('type', 'report_type'),
        ('queueTime', 'queue_time'),
        ('status', 'status'),
        ('priority', 'priority'),
        ('estimate', 'estimate'),
        ('user', 'user')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        rsid: Optional[str]=None,
        report_id: Optional[int]=None,
        report_type: Optional[str]=None,
        queue_time: Optional[datetime]=None,
        status: Optional[str]=None,
        priority: Optional[int]=None,
        estimate: Optional[int]=None,
        user: Optional[str]=None
    ):
        r"""
        :param report_id:

            The request ID for the report.

        :param report_type:

            Report type being generated, one of the following values:
             - overtime
             - trended
             - trendedplus
             - ranked
             - universal

        :param queue_time:

            The time the report was requested (Pacific Time).

        :param status:

            The processing status of the report, one of the following values:
             - waiting
             - running

        :param priority:

            The priority in the queue.

        :param estimate:

            The estimate in seconds that the report will take to complete.

        :param user:

            The analytics user who requested the report.
        """
        self.rsid = rsid
        self.report_id = report_id
        self.report_type = report_type
        self.report_id = report_id
        self.queue_time = queue_time
        self.status = status
        self.priority = priority
        self.estimate = estimate
        self.user = user
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'queueTime' and isinstance(v, str):
                v = str2datetime(v)
            elif k in ('reportID', 'priority', 'estimate'):
                v = int(v)
            setattr(self, a, v)


class ReportMetric(JSONObject):

    _keys_attributes = OrderedDict([
        ('id', 'metric_id'),
        ('name', 'name'),
        ('type', 'metric_type'),
        ('decimals', 'decimals'),
        ('formula', 'formula'),
        ('latency', 'latency'),
        ('current', 'current')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        metric_id: Optional[str]=None,
        name: Optional[str]=None,
        metric_type: Optional[str]=None,
        decimals: Optional[int]=None,
        formula: Optional[str]=None,
        latency: Optional[int]=None,
        current: Optional[bool]=None
    ):
        self.metric_id = metric_id
        self.name = name
        self.metric_type = metric_type
        self.decimals = decimals
        self.formula = formula
        self.latency = latency
        self.current = current
        if data is not None:
            self.data = data


class ReportElement(JSONObject):
    """
    Defines an element appearing in a report.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportelement-1
    """

    _keys_attributes = OrderedDict([
        ('id', 'element_id'),
        ('name', 'name'),
        ('classification', 'classification'),
        ('top', 'top'),
        ('startingWith', 'starting_with'),
        ('correlation', 'correlation'),
        ('subrelation', 'subrelation'),
        ('hierarchy_levels', 'hierarchy_levels'),
        ('max_pathing_steps', 'max_pathing_steps')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        element_id: Optional[str]=None,
        name: Optional[str]=None,
        classification: Optional[str]=None,
        top: Optional[int]=None,
        starting_with: Optional[int]=None,
        correlation: Optional[bool]=None,
        subrelation: Optional[bool]=None,
        hierarchy_levels: Optional[int]=None,
        max_pathing_steps: Optional[int]=None
    ):
        """
        :param element_id:

            The element ID. This must match the element ID specified in the report description.

        :param name:

            The element name.

        :param classification:

            The name of the classification that was requested, if applicable.
        """
        self.element_id = element_id
        self.name = name
        self.classification = classification
        self.top = top
        self.starting_with = starting_with
        self.correlation = correlation
        self.subrelation = subrelation
        self.hierarchy_levels = hierarchy_levels
        self.max_pathing_steps = max_pathing_steps
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            k = k.strip()
            if v is None:
                continue
            if k in ('hierarchy_levels', 'max_pathing_steps'):
                v = int(v)
            a = self._keys_attributes[k]
            setattr(self, a, v)


class ReportSegment(JSONObject):
    """
    Identifies a segment that appears in a report.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportsegment
    """

    _keys_attributes = OrderedDict([
        ('id', 'segment_id'),
        ('name', 'name')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        segment_id: Optional[str]=None,
        name: Optional[str]=None
    ):
        """
        :param segment_id:

            The element ID. This must match the element ID specified in the report description.

        :param name:

            The element name.
        """
        self.segment_id = segment_id
        self.name = name
        if data is not None:
            self.data = data


class ReportDataPath(JSONObject):
    """
    Identifies a data path that appears in a report.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdatapath
    """

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('url', 'url')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        name: Optional[str]=None,
        url: Optional[str]=None
    ):
        """
        :param name:

            The data path name.

        :param url:

            The URL if the element is a page.
        """
        self.name = name
        self.url = url
        if data is not None:
            self.data = data


class ReportData(JSONObject):
    """
    Contains report data.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportdata-1
    """

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('url', 'url'),
        ('path', 'path'),
        ('parentID', 'parent_id'),
        ('year', 'year'),
        ('month', 'month'),
        ('day', 'day'),
        ('hour', 'hour'),
        ('minute', 'minute'),
        ('trend', 'trend'),
        ('counts', 'counts'),
        ('upperBounds', 'upper_bounds'),
        ('lowerBounds', 'lower_bounds'),
        ('forecasts', 'forecasts'),
        ('breakdownTotal', 'breakdown_total'),
        ('breakdown', 'breakdown')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        name: Optional[str]=None,
        url: Optional[str]=None,
        path: Optional[Sequence[ReportDataPath]]=None,
        parent_id: Optional[str]=None,
        year: Optional[int]=None,
        month: Optional[int]=None,
        day: Optional[int]=None,
        hour: Optional[int]=None,
        minute: Optional[int]=None,
        trend: Optional[float]=None,
        counts: Optional[Sequence[float]]=None,
        upper_bounds: Optional[Sequence[float]]=None,
        lower_bounds: Optional[Sequence[float]]=None,
        forecasts: Optional[Sequence[float]]=None,
        breakdown_total: Optional[Sequence[float]]=None,
        breakdown: Optional[Sequence['ReportData']]=None
    ):
        """
        :param name:

            This data item name.

        :param url:

            The data item URL, if applicable to the selected element.
            For example, pages and links have a URL, but products do not.

        :param path:

            The path for pathing reports.

        :param parent_id:

            Unique identifier for the element in a hierarchy report.
            Use in an instance of `ReportDescription` to request the next level of the hierarchy.

        :param year:

            The four-digit year for the item if the element is a date range for an Overtime or Trended report.

        :param month:

            The two-digit month for the item if the element is a date range for an Overtime or Trended report.

        :param day:

            The two-digit numeric day for the item if the element is a date range for an Overtime or Trended report.

        :param hour:

            The two-digit numeric hour for the item if the element is a date range for an Overtime or Trended report.

        :param minute:

            The two-digit numeric minute for the item if the element is a date range for a Real-Time report.

        :param trend:

            The slope of the trend line so you can determine the relative change between report intervals

        :param counts:

            A count of the number of occurrences of each metric in the report.

        :param upper_bounds:

            Upper level of the prediction interval. Values above this level are considered anomalous.
            Represents a 95% confidence that values will be below this level.

        :param lower_bounds:

            Lower level of the prediction interval. Values below this level are considered anomalous.
            Represents a 95% confidence that values will be above this level.

        :param forecasts:

            The predicted value based on the data analysis.
            This value is also the middle point between the upper and lower bounds.

        :param breakdown_total:

            The total metrics values for the breakdown.

        :param breakdown:

            This item's data, organized according to the next element.
            For example, a report of Browsers, broken down by page views, returns a report containing a
            listing of page views for each Browser type. This is only used in Ranked or Trended reports
            when multiple elements (Breakdowns) are specified. (recursive)

        """
        self.name = name
        self.url = url
        self.name = name
        self.path = path
        self.parent_id = parent_id
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.trend = trend
        self.counts = counts
        self.upper_bounds = upper_bounds
        self.lower_bounds = lower_bounds
        self.forecasts = forecasts
        self.breakdown_total = breakdown_total
        self.breakdown = breakdown
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if (v is None) or v == '':
                continue
            a = self._keys_attributes[k]
            if k == 'breakdown':
                v = JSONArray([
                    self.__class__(b)
                    for b in v
                ])
            elif k == 'path':
                v = JSONArray([
                    ReportDataPath(p)
                    for p in v
                ])
            elif k in ('year', 'month', 'day', 'hour', 'minute'):
                v = int(v)
            elif k in ('upperBounds', 'lowerBounds', 'counts', 'breakdownTotal'):
                v = JSONArray([
                    float(b) for b in v
                ])
            elif k == 'trend':
                v = float(v)
            setattr(self, a, v)


class ReportReportSuite(JSONObject):

    _keys_attributes = OrderedDict([
        ('id', 'suite_id'),
        ('name', 'name')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        suite_id: Optional[str]=None,
        name: Optional[str]=None
    ):
        self.suite_id = suite_id
        self.name = name
        if data is not None:
            self.data = data


class Report(JSONObject):

    _keys_attributes = OrderedDict([
        ('type', 'report_type'),
        ('reportSuite', 'report_suite'),
        ('period', 'period'),
        ('elements', 'elements'),
        ('metrics', 'metrics'),
        ('segments', 'segments'),
        ('data', 'report_data'),
        ('totals', 'totals'),
        ('version', 'version')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        report_type: Optional[str]=None,
        report_suite: Optional[ReportReportSuite]=None,
        period: Optional[str]=None,
        elements: Optional[Sequence[ReportElement]]=None,
        metrics: Optional[Sequence[ReportMetric]]=None,
        segments: Optional[Sequence[ReportSegment]]=None,
        report_data: Optional[Sequence[ReportData]]=None,
        totals: Optional[Sequence[float]]=None,
        version: Optional[str]=None
    ):
        self.report_type = report_type
        self.report_suite = report_suite
        self.period = period
        self.elements = elements
        self.metrics = metrics
        self.segments = segments
        self.report_data = report_data
        self.totals = totals
        self.version = version
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'reportSuite':
                v = ReportReportSuite(v)
            elif k == 'elements':
                v = JSONArray([
                    ReportElement(e)
                    for e in v
                ])
            elif k == 'metrics':
                v = JSONArray([
                    ReportMetric(m)
                    for m in v
                ])
            elif k == 'segments':
                v = JSONArray([
                    ReportSegment(s)
                    for s in v
                ])
            elif k == 'data':
                v = JSONArray([
                    ReportData(d)
                    for d in v
                ])
            setattr(self, a, v)


class ReportResponse(JSONObject):
    """
    The data returned in response to a report request.

    https://marketing.adobe.com/developer/documentation/analytics-reporting-1-4/r-reportresponse-1
    """

    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('waitSeconds', 'wait_seconds'),
        ('runSeconds', 'run_seconds'),
        ('report', 'report'),
        ('retryDelay', 'retry_delay')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]],
        rsid: Optional[str]=None,
        wait_seconds: Optional[float]=None,
        run_seconds: Optional[str]=None,
        report: Optional[Report]=None,
        retry_delay: Optional[float]=None
    ):
        self.rsid = rsid
        self.wait_seconds = wait_seconds
        self.run_seconds = run_seconds
        self.report = report
        self.retry_delay = retry_delay
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'report':
                v = Report(v)
            elif k == 'retryDelay':
                v = float(v)
            setattr(self, a, v)


class ReportSuiteActivation(JSONObject):
    """
    Data structure that contains information about a report suite's activation status.

    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-report-suite-activation-1
    """

    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('activation', 'activation')
    ])

    def __init__(
        self,
        data,  # type: Optional[Union[str, bytes, Dict]]
        rsid=None,  # type: Optional[str]
        site_title=None,  # type: Optional[str]
        activation=None,  # type: Optional[bool]
    ):
        # type: (...) -> None
        self.rsid = rsid
        self.site_title = site_title
        self.activation = activation
        if data is not None:
            self.data = data


class ReportSuiteAxleStartDate(JSONObject):
    """
    Data structure that contains information about when a report suite was migrated to axle processing from

    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-report-suite-axle-start-date
    """

    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('axle_start_date', 'axle_start_date')
    ])

    def __init__(
        self,
        data,  # type: Optional[Union[str, bytes, Dict]]
        rsid=None,  # type: Optional[str]
        site_title=None,  # type: Optional[str]
        axle_start_date=None,  # type: Optional[date]
    ):
        # type: (...) -> None
        self.rsid = rsid
        self.site_title = site_title
        self.axle_start_date = axle_start_date
        if data is not None:
            self.data = data


class Bookmark(JSONObject):

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('id', 'bookmark_id'),
        ('rsid', 'rsid')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]],
        name: Optional[str]=None,
        bookmark_id: Optional[int]=None,
        rsid: Optional[str]=None
    ):
        self.name = name
        self.bookmark_id = bookmark_id
        self.rsid = rsid
        if data is not None:
            self.data = data


class DisplayInfo(JSONObject):

    _keys_attributes = OrderedDict([
        ('row', 'row'),
        ('col', 'col'),
        ('rowspan', 'rowspan'),
        ('colspan', 'colspan'),
        ('graph', 'graph'),
        ('table', 'table'),
        ('summary', 'summary')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]],
        row: Optional[int]=None,
        col: Optional[int]=None,
        rowspan: Optional[int]=None,
        colspan: Optional[int]=None,
        graph: Optional[bool]=None,
        table: Optional[bool]=None,
        summary: Optional[bool]=None
    ):
        """
        :param row:

             Row in the dashboard layout.

        :param col:

            Column in the dashboard layout.

        :param rowspan:

            Number of rows spanned in the dashboard layout.

        :param colspan:

            Number of columns spanned in the dashboard layout.

        :param colspan:

            Number of columns spanned in the dashboard layout.

        """
        self.row = row if row is None else int(row)
        self.col = col if col is None else int(col)
        self.rowspan = rowspan if rowspan is None else int(rowspan)
        self.colspan = colspan if colspan is None else int(colspan)
        self.graph = graph
        self.table = table
        self.summary = summary
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k in ('row', 'col', 'rowspan', 'colspan'):
                v = int(v)
            setattr(self, a, v)


class DashboardBookmark(JSONObject):

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('id', 'bookmark_id'),
        ('rsid', 'rsid'),
        ('displayInfo', 'display_info')
    ])
    name = None # type: Optional[str]

    def __init__(
        self,
        data,  # type: Optional[Union[str, bytes, Dict]]
        name=None,  # type: Optional[str]
        bookmark_id=None,  # type: Optional[int]
        rsid=None,  # type: Optional[str]
        display_info=None  # type: Optional[DisplayInfo]
    ):
        """
        :param name:

            Bookmark name.

        :param bookmark_id:

            Bookmark ID. Pass this ID to `Bookmark.get_report_description` to retrieve the report
            associated with this bookmark.

        :param rsid:

            The report suite ID.

        :param display_info:

             Display information concerning the dashboard layout.
        """
        self.name = name
        self.bookmark_id = bookmark_id
        self.rsid = rsid
        self.display_info = display_info
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'displayInfo':
                v = DisplayInfo(v)
            elif k == 'id':
                v = int(v)
            setattr(self, a, v)


class BookmarkFolder(JSONObject):

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('id', 'bookmark_id'),
        ('owner', 'owner'),
        ('bookmarks', 'bookmarks')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        name=None,  # type: Optional[str]
        bookmark_id=None,  # type: Optional[int]
        owner=None,  # type: Optional[str]
        bookmarks=None  # type: Optional[Iterable[Bookmark]]
    ):
        self.name = name  # type: Optional[str]
        self.bookmark_id = bookmark_id  # type: Optional[int]
        self.owner = owner  # type: Optional[str]
        self.bookmarks = bookmarks  # type: Optional[Iterable[Bookmark]]
        if data is not None:
            self.data = data

    @property
    def data(self):
        # type: (...) -> Dict
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'bookmarks':
                v = JSONArray([
                    Bookmark(b)
                    for b in v
                ])
            setattr(self, a, v)


class GetReportDescriptionResponse(JSONObject):

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('type', 'report_type'),
        ('reportDescription', 'report_description'),
        #('segment_id', 'segment_id')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        name=None,  # type: Optional[str]
        report_type=None,  # type: Optional[str]
        report_description=None,  # type: Optional[ReportDescription]
        #segment_id=None  # type: Optional[segment_id]
    ):
        self.name = name
        self.report_type = report_type
        self.report_description = report_description
        #self.segment_id = segment_id
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            elif k == 'name':
                self.name = v
            elif k == 'type':
                self.report_type = v
            elif k == 'reportDescription':
                self.report_description = ReportDescription(v)


class DashboardPage(JSONObject):

    _keys_attributes = OrderedDict([
        ('grid', 'grid'),
        ('bookmarks', 'bookmarks')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        grid: Optional[str]=None,
        bookmarks: Optional[Sequence[Bookmark]]=None
    ):
        if isinstance(bookmarks, Bookmark):
            bookmarks = [bookmarks]
        if bookmarks is not None:
            bookmarks = JSONArray([
                b for b in bookmarks
            ])
        self.grid = grid
        self.bookmarks = bookmarks
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'bookmarks':
                v = JSONArray([
                    DashboardBookmark(b)
                    for b in v
                ])
            setattr(self, a, v)


class Dashboard(JSONObject):

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('id', 'dashboard_id'),
        ('owner', 'owner'),
        ('pages', 'pages'),
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        name: Optional[str]=None,
        dashboard_id: Optional[int]=None,
        owner: Optional[str]=None,
        pages: Optional[Sequence[DashboardPage]]=None
    ):
        if isinstance(pages, DashboardPage):
            pages = [pages]
        self.name = name
        self.dashboard_id = dashboard_id
        self.owner = owner
        self.pages = pages
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'pages' and (v is not None):
                v = JSONArray([
                    DashboardPage(dp)
                    for dp in v
                ])
            setattr(self, a, v)


class TrackingServerData(JSONObject):

    _keys_attributes = OrderedDict([
        ('namespace', 'namespace'),
        ('tracking_server', 'tracking_server')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        namespace: Optional[str]=None,
        tracking_server: Optional[str]=None
    ):
        self.namespace = namespace
        self.tracking_server = tracking_server
        if data is not None:
            self.data = data


class ReportMetric(JSONObject):

    _keys_attributes = OrderedDict([
        ('id', 'metric_id'),
        ('name', 'name'),
        ('type', 'metric_type'),
        ('decimals', 'decimals'),
        ('formula', 'formula'),
        ('latency', 'latency'),
        ('current', 'current')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        metric_id=None,  # type: Optional[str]
        name=None,  # type: Optional[str]
        metric_type=None,  # type: Optional[str]
        decimals=None,  # type: Optional[int]
        formula=None,  # type: Optional[str]
        latency=None,  # type: Optional[int]
        current=None  # type: Optional[bool]
    ):
        self.metric_id = metric_id
        self.name = name
        self.metric_type = metric_type
        self.decimals = decimals
        self.formula = formula
        self.latency = latency
        self.current = current
        if data is not None:
            self.data = data


class CreateReportSuiteResponse(JSONObject):

    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('tracking_server', 'tracking_server')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        rsid=None,  # type: Optional[str]
        site_title=None,  # type: Optional[str]
        tracking_server=None,  # type: Optional[str]
    ):
        self.rsid = rsid
        self.site_title = site_title
        self.tracking_server = tracking_server
        if data is not None:
            self.data = data


class SegmentRuleRestriction(JSONObject):

    _keys_attributes = OrderedDict([
        ('id', 'restriction_id'),
        ('value', 'value')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        restriction_id=None,  # type: Optional[str]
        value=None,  # type: Optional[Union[int, str]]
    ):
        """
        :param restriction_id:

            "hits", "visits", "pageviews", "minutes", "hours", "days", "weeks", "quarters", or "years".

        :param value:

            Restriction value, this is always an integer (in string format).
        """
        self.restriction_id = restriction_id
        if value is not None:
            value = str(int(value))
        self.value = value
        if data is not None:
            self.data = data


class SegmentRule(JSONObject):
    """
    https://marketing.adobe.com/developer/documentation/segments-1-4/r-segment-rule
    """

    _keys_attributes = OrderedDict([
        ('container', 'container'),
        ('metric', 'metric'),
        ('element', 'element'),
        ('classification', 'classification'),
        ('operator', 'operator'),
        ('value', 'value'),
        ('after', 'after'),
        ('within', 'within'),
        ('exclude', 'exclude'),
        ('name', 'name')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        container=None,  # type: Optional[SegmentContainer]
        metric=None,  # type: Optional[str]
        element=None,  # type: Optional[str]
        classification=None,  # type: Optional[str]
        operator=None,  # type: Optional[str]
        value=None,  # type: Optional[str]
        after=None,  # type: Optional[SegmentRuleRestriction]
        within=None,  # type: Optional[SegmentRuleRestriction]
        exclude=None,  # type: Optional[str]
        name=None,  # type: Optional[str]
    ):
        # type: (...) -> None
        """
        :param container:

            Nested segment container. A segment rule must have either "container" or "operator" (you cannot include
            both in the same rule). When a container is included, all other rule fields are ignored except "exclude".

        :param metric:

            Metric to segment, required if "element" is not present. Must be a metric id as returned from
            `omniture.api.report.Report.get_metrics`.

        :param element:

            Element (dimension) to segment, required if "metric" is not present or if "classification" is present.
            Must be an element id as returned from `omniture.api.report.Report.get_elements`

        :param classification:

            Element classification to segment, name of the classification as returned from
            `omniture.api.report_suite.ReportSuite.get_classifications`.

        :param operator:

            Required if "container" is not present.

            Rule Operators

            A rule operator has many different options. Those options depend on the accompanying "metric" or "element".
            Some combinations of metric/element + operator affect the compatibility of the whole segment definition with
            different Analytics reporting interfaces. Definition compatibility can be obtained from Segments.Get after
            the segment is saved. A segment definition that is incompatible with data warehouse and other Analytics
            reporting interfaces returns an error when attempting to save.

                "equals"

                    Returns items that match exactly for a numeric or string value.
                    If using wildcard characters, use the "matches" operator.

                "not_equals"

                    Returns all items that do not contain the exact match of the value entered.
                    If using wildcard characters, use the "not_matches" operator.

                "matches"

                    Returns items that match exactly based on a given numeric or string value. Use this operator when
                    using wildcard (globbing) features.

                "not_matches"

                    Returns all items that do not contain the exact match of the value entered.
                    Use this operator when using wildcard (globbing) features.

                "less_than" (data warehouse segments only)

                    Returns items whose numeric count is less than the value entered.

                "less_than_or_equals" (data warehouse segments only)

                    Returns items whose numeric count is less than or equal to the value entered.

                "greater_than" (data warehouse segments only)

                    Returns items whose numeric count is greater than the value entered.

                "greater_than_or_equals" (data warehouse segments only)

                    Returns items whose numeric count is greater than or equal to the value entered.

                "contains"

                    Returns items that compare to the substrings of the values entered. For example, if the rule
                    for "Page" contains "Search", then it will match any page that has the substring "Search" in it,
                    including "Search Results", "Search", and "Searching".

                "not_contains"

                    Returns the inverse of the "contains" rule. Specifically, all items that match the entered value
                    will be excluded from the entered values. For example, if the rule for "Page" does not contain
                    "Search", then it will not match any page that has the substring "Search" in it, including
                    "Search Results", "Search", and "Searching". These values will be excluded from the results.

                "contains_all"

                    Returns items compared to the substrings, including multiple values joined together. For
                    example, entering "Search Results" with this operator would match "Search Results" and "Results
                    of Search", but not "Search" or "Results" independently. It would match Search AND Results
                    found together.

                "not_contains_all"

                    Identifies items compared to substrings—including multiple values joined together—and then only
                    return items without these values. For example, entering "Search Results" with this operator would
                    identify "Search Results" and "Results of Search" (but not "Search" or "Results" independently) and
                    then exclude these items.

                "contains_any"

                    Returns items compared to the substrings, including multiple values joined or independently
                    identified. For example, entering "Search Results" with this operator would match "Search Results",
                    "Results of Search", "Search", and "Results". It would match either "Search" OR "Results" found
                    together or independently.

                "not_contains_any"

                    Identifies items based on substrings and then returns values that do not contain these substrings.
                    It can have multiple joined values or values independently identified. For example, entering
                    "Search Results" would match "Search Results", "Results of Search", "Search", and "Results"
                    where either "Search" or "Results" are found together or independently. It would then exclude items
                    that contain these substrings.

                "starts_with"

                    Returns items that start with the character or strings of the value entered.

                "not_starts_with"

                    Returns all items that do not start with the characters or strings of the values entered. This is
                    the inverse of "starts with" operator.

                "ends_with"

                    Returns items that end with the character or strings of the value entered.

                "not_ends_with"

                    Returns all items that do not end with the characters or strings of the value entered. This is the
                    inverse of "ends with" operator.

                "not_metric_exists" (metrics only)

                    Returns items that contain an empty string identified as a null value.

                "metric_exists" (metrics only)

                    Returns items that do not contain a null value.

                "exists" (elements only)

                    Returns the number of items that exist.

                    For example, if you evaluate the Pages Not Found dimension using the "exist" operator, the number
                    of error pages that exist is returned.

                "not_exists" (elements only)

                    Returns all items that do not exist.

                    For example, if you evaluate the Pages Not Found dimension using the " does not exist" operator,
                    the number of pages where this error page did not exist is returned.

        :param value:


            Required except when using one of the exists operators, options depend on the accompanying "metric" or
            "element".

            See Segment Definition Changes for a list of dimensions that use enumerated lists:

                https://marketing.adobe.com/resources/help/en_US/analytics/segment/seg_definition.html

        :param after:

            (Optional) The After operator is used to specify a minimum limit between two checkpoints in a sequential
            segment. Allowed on rules that are in a container that uses the "then" operator. Restrictions on the last
            rule in that container are ignored. Each rule can have at most one "after" and one "within" restriction.

                https://marketing.adobe.com/resources/help/en_US/analytics/segment

        :param within:

             (Optional) The Within operator specifies a maximum limit on the amount of time between two checkpoints in
              asequential segment. Allowed on rules that are in a container that uses the "then" operator. Restrictions
              on the last rule in that container are ignored. Each rule can have at most one "after" and one "within"
              restriction.

                http://microsite.omniture.com/t2/help/en_US/analytics/segment/?f=seg_example_time_between_within

        :param exclude:

            (Optional) Exclude rather than include data that matches the segment rule. Defaults to false.

        :param name:

            (Optional) Not used, can be provided will not be saved.
        """
        self.container = container
        self.metric = metric
        self.element = element
        self.classification = classification
        self.operator = operator
        self.value = value
        self.after = after
        self.within = within
        self.exclude = exclude
        self.name = name
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'container':
                v = SegmentContainer(v)
            elif k in ('after', 'within'):
                v = SegmentRuleRestriction(v)
            setattr(self, a, v)


class SegmentContainer(JSONObject):
    """
    Defines a segment container.

    https://marketing.adobe.com/developer/documentation/segments-1-4/r-segment-container
    """

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('type', 'segment_type'),
        ('operator', 'operator'),
        ('rules', 'rules'),
        ('exclude', 'exclude')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        name=None,  # type: Optional[str]
        segment_type=None,  # type: Optional[str]
        operator=None,  # type: Optional[str]
        rules=None,  # type: Optional[Sequence[SegmentRule]]
        exclude=None,  # type: Optional[bool]
    ):
        """
        :param name:

            (Optional) Container name.

        :param segment_type:

            (Required) Container type—one of the following values: "hits", "visits", or "visitors".

            Sequential Segments:

                - Sequential Segments place additional restrictions on container type.
                If the definition has a container that defines a sequential segment (using the "then" operator),
                the options for "type" are limited to "visits" or "visitors".

                - Sub-containers within a sequential segment container that alsoz use a "then" operator can specify a
                "type" of "hits", "visits", or "logicgroup".

        :param operator:

            (Optional) Specifies the operator used to evaluate the container rules.

            One of the following: "and", "or", "then".

            Defaults to "and" if not included, or if the container has only one rule.

        :param rules:

            (Required) Defines the data that is matched by this container.

            Each container must include at least one rule.

        :param exclude:

            (Optional) Exclude rather than include data that matches the segment rule. Defaults to `False`.
        """
        self.name = name
        self.segment_type = segment_type
        self.operator = operator
        if isinstance(rules, SegmentRule):
            rules = [rules]
        self.rules = rules
        self.exclude = exclude
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'rules':
                v = JSONArray([
                    SegmentRule(sr) for sr in v
                ])
            setattr(self, a, v)


class SegmentDefinition(JSONObject):
    """
    Specifies the top level container for a segment.

    Every definition must have a top level "container". Every container has an array of "rules".
    A rule is either a base rule, or it has a container (both is not allowed). Thus infinite nesting is allowed,
    though Adobe recommends stacking (including multiple segments) to increase reusability.
    For example, instead of defining "mobile users in the US", you could define two segments: one for mobile users,
    and one for users in the US. By combining these segments, you can reuse these segments in other reports.

    To understand how segment complexity impact report generation time, see
    Reporting Best Practices (https://marketing.adobe.com/developer/en_US/get-started/best-practices).
    """

    _keys_attributes = OrderedDict([
        ('container', 'container')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        container=None,  # type: Optional[SegmentContainer]
    ):
        """
        :param data:
        :param container:
        """
        self.container = container
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'container':
                v = SegmentContainer(v)
            setattr(self, a, v)


class SegmentShare(JSONObject):

    _keys_attributes = OrderedDict([
        ('type', 'share_type'),
        ('name', 'name')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        share_type=None,  # type: Optional[str]
        name=None  # type: Optional[str]
    ):
        """
        Identifies a user or group with which to share a segment.

        https://marketing.adobe.com/developer/documentation/segments-1-4/r-segment-share

        :param share_type:

            "group" or "user".

        :param name:

            Group name or user login according to the specified share type.
        """
        self.share_type = share_type
        self.name = name
        if data is not None:
            self.data = data
            
class CalculatedMetricShare(JSONObject):

    _keys_attributes = OrderedDict([
        ('type', 'share_type'),
        ('name', 'name')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        share_type=None,  # type: Optional[str]
        name=None  # type: Optional[str]
    ):
        """
        Identifies a user or group with which to share a segment.

        https://marketing.adobe.com/developer/documentation/segments-1-4/r-segment-share

        :param share_type:

            "group" or "user".

        :param name:

            Group name or user login according to the specified share type.
        """
        self.share_type = share_type
        self.name = name
        if data is not None:
            self.data = data
  
            
class CalculatedMetricDefinition(JSONObject):

    _keys_attributes = OrderedDict([
        ('function', 'function'),
        ('parameters', 'parameters'),
        ('metric', 'metric'),
        ('description', 'description'),
        ('calculatedMetric', 'calculated_metric'),
        ('segments', 'segments')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        function=None,
        parameters=None,
        description=None,
        calculated_metric=None,
        segments=None,
        metric=None
    ):
        """
        :param data:
        :param container:
        """
 
        self.function = function 
        self.parameters = parameters 
        self.description = description 
        self.calculated_metric = calculated_metric 
        self.segments = segments
        self.metric = metric
        
        if data is not None:
            self.data = data
           

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
           # print(k,v)
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'calculatedMetric':
                v = CalculatedMetricDefinition(v)
            setattr(self, a, v)
    
class CalculatedMetric(JSONObject):
    
    _keys_attributes = OrderedDict([
        ('id', 'metric_id'),
        ('name', 'name'),
        ('description', 'description'),
        ('polarity', 'polarity'),
        ('precision', 'precision'),
        ('type', 'metric_type'),
        ('modified', 'modified'),
        ('shares', 'shares'),
        ('definition', 'definition'),
        ('compatibility', 'compatibility'),
        ('template', 'template'),
        ('approved', 'approved'),
        ('favorite', 'favorite'),
        ('reportSuiteID', 'rsid'),
        ('owner', 'owner'),
        ('tags', 'tags'),
        ('internal', 'internal')
    ])
    
    def __init__(
        self,
        data=None,
        metric_id=None,
        name=None,
        description=None,
        polarity=None,
        precision=None,
        metric_type=None,
        shares=None,
        definition=None,
        compatibility=None,
        template=None,
        approved=None,
        favorite=None,
        rsid=None,
        modified=None,
        owner=None,
        tags=None,
        internal=None
    ):
        
        self.metric_id = metric_id 
        self.name = name
        self.description = description
        self.polarity = polarity
        self.metric_type = metric_type
        self.definition = definition
        self.compatibility = compatibility 
        self.template = template 
        self.approved = approved
        self.modified = modified
        self.internal = internal
        self.favorite = favorite 
        self.rsid = rsid
        self.owner = owner
        self.tags = tags
        if isinstance(shares, CalculatedMetricShare):
            shares = [shares]
        self.shares = shares
        
        if data is not None:
            self.data = data
            
    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'shares':
                v = JSONArray([
                    CalculatedMetricShare(ss) for ss in v
                ])
            elif k == 'definition' and isinstance(v, Dict):
                v = CalculatedMetricDefinition(v)
            elif k == 'modified':
                v = str2datetime(v)
            setattr(self, a, v)

    
class Segment(JSONObject):

    _keys_attributes = OrderedDict([
        ('id', 'segment_id'),
        ('name', 'name'),
        ('description', 'description'),
        ('reportSuiteID', 'rsid'),
        ('modified', 'modified'),
        ('compatibility', 'compatibility'),
        ('favorite', 'favorite'),
        ('tags', 'tags'),
        ('shares', 'shares'),
        ('owner', 'owner'),
        ('definition', 'definition')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        segment_id=None,  # type: Optional[str]
        name=None,  # type: Optional[str]
        description=None,  # type: Optional[str]
        rsid=None,  # type: Optional[str]
        modified=None,  # type: Optional[str]
        compatibility=None,  # type: Optional[Sequence[str]]
        favorite=None,  # type: Optional[bool]
        tags=None,  # type: Optional[Sequence[str]]
        shares=None,  # type: Optional[Union[Sequence[SegmentShare], SegmentShare]]
        owner=None,  # type: Optional[str],
        definition=None  # type: Optional[Union[SegmentDefinition, str]]
    ):
        # type: (...) -> None
        """
        Details about a segment.

        https://marketing.adobe.com/developer/documentation/segments-1-4/r-segment

        :param segment_id:

            Unique ID for this segment.

        :param name:

            Name provided for the segment. Displayed in the UI.

        :param description:

            Description provided for the segment. Displayed in the UI.

        :param rsid:

            Identifies the report suite that was used to create the segment request.

        :param modified:

            Date when the segment was last updated.

        :param compatibility:

            List of Analytics interfaces that are compatible with this segment.

            http://microsite.omniture.com/t2/help/en_US/analytics/segment/?f=seg_compatibility

        :param favorite:

            Indicates if the current user has flagged this segment as a favorite.

        :param tags:

            Tags defined for the segment.

        :param shares:

            A sequence of `SegmentShare` instances defining the groups and users with which this segment is shared.

        :param owner:

            Segment owner.

        :param definition:

            Segment definition.
        """
        self.segment_id = segment_id
        self.name = name
        self.description = description
        self.rsid = rsid
        self.modified = modified
        self.compatibility = compatibility
        self.favorite = favorite
        self.tags = tags
        if isinstance(shares, SegmentShare):
            shares = [shares]
        self.shares = shares
        self.owner = owner
        self.definition = definition
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'shares':
                v = JSONArray([
                    SegmentShare(ss) for ss in v
                ])
            elif k == 'definition' and isinstance(v, Dict):
                v = SegmentDefinition(v)
            elif k == 'modified':
                v = str2datetime(v)
            setattr(self, a, v)


class SegmentFilters(JSONObject):

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('tags', 'tags'),
        ('owner', 'owner'),
        ('reportSuiteID', 'rsid'),
        ('approved', 'approved'),
        ('favorite', 'favorite')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        name=None,  # type: Optional[str]
        tags=None,  # type: Optional[Union[str, Sequence[str]]]
        owner=None,  # type: Optional[str]
        rsid=None,  # type: Optional[str]
        approved=None,  # type: Optional[bool]
        favorite=None  # type: Optional[bool]
    ):
        """
        :param name:

            Performs "partial case insensitive matching" on segment names.

            For example, "partial case insensitive matching" means that a value of "big brother" would match
            reports named "Big Brother's Top Secret Report", "Big Brother Watches You Sleep",
            "You Can't Hide From Big Brother", etc.

        :param tags:

            Performs exact matching on a comma-separated list of tags.

            For example, if you have a segment with tag "a" and another with tag "b", setting the "tags"
            filter to "A" will find no matches, setting it to "a" will match the first, and setting it to
            "a,b" will find both.

        :param owner:

            Performs partial case insensitive matching on owner IDs.

        :param rsid:

            Performs partial case insensitive matching on report suite IDs.

        :param approved:

            If `True`, matches only approved segments. If `False`, matches only segments which have not been
            approved.

        :param favorite:

            If `True`, matches only favorited segments. If `False`, matches only segments which have not been
            favorited.
        """
        self.name = name
        if isinstance(tags, Sequence) and not isinstance(tags, str):
            tags = ','.join([t.strip() for t in tags if t is not None])
        self.tags = tags
        self.owner = owner
        self.rsid = rsid
        self.approved = approved
        self.favorite = favorite
        if data is not None:
            self.data = data
            
        @property
        def data(self):
            return super().data

        @data.setter
        def data(
            self,
            data  # type: Union[str, bytes, Dict]
        ):
            if isinstance(data, bytes):
                data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
            if isinstance(data, str):
                data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
            for k, v in data.items():
                if v is None:
                    continue
                a = self._keys_attributes[k]
                setattr(self, a, v)


class ClassificationItem(JSONObject):
    """
    Data structure that contains information about a report suite's classifications.

    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-classification-item
    """

    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('metric_id', 'metric_id'),
        ('parent_name', 'parent_name'),
        ('date_enabled', 'date_enabled'),
        ('type', 'classification_type'),
        ('options', 'options'),
        ('children', 'children'),
        ('description', 'description')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        name=None,  # type: Optional[str]
        metric_id=None,  # type: Optional[str]
        parent_name=None,  # type: Optional[str]
        date_enabled=None,  # type: Optional[bool]
        classification_type=None,  # type: Optional[str]
        options=None,  # type: Optional[Union[Sequence[str],str]]
        children=None,  # type: Optional[Sequence[ClassificationItem]]
        description=None  #type: Optional[str]
    ):
        # type: (...) -> None
        """
        :param name:

            ?

        :param metric_id:

            ?

        :param parent_name:

            Contains the parent classification's div_num if this is a sub-classification; otherwise it is 0.

        :param date_enabled:

            Determines whether to treat this classification like a campaign.

        :param classification_type:

            Classification type—one of the following: "text", "numeric", "numeric_percent", or "numeric_currency".

        :param options:

            ?

        :param children:

            A list of child `ClassificationItem` objects.
        """
        self.name = name
        self.metric_id = metric_id
        self.parent_name = parent_name
        self.date_enabled = date_enabled
        self.classification_type = classification_type
        if isinstance(options, str):
            options = [options]
        self.options = options
        self.children = children
        self.description = description
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'children':
                v = JSONArray([
                    self.__class__(ci) for ci in v
                ])
            setattr(self, a, v)


class Evars(JSONObject):
    
    _keys_attributes = OrderedDict([
        ('name', 'name'),
        ('evar_type', 'evar_type'),
        ('id', 'id'),
        ('enabled', 'enabled'),
        ('description', 'description'),
        ('binding_events', 'binding_events'),
        ('merchandising_syntax', 'merchandising_syntax'),
        ('expiration_type', 'expiration_type'),
        ('expiration_custom_days', 'expiration_custom_days'),
        ('allocation_type', 'allocation_type')
    ])
    
    def __init__(
        self,
        data=None,
        name=None,
        evar_type=None,
        id=None,
        enabled=None,
        description=None,
        binding_events=None,
        merchandising_syntax=None,
        expiration_type=None,
        expiration_custom_days=None,
        allocation_type=None
    ):
    
        self.name = name 
        self.evar_type = evar_type 
        self.id = id
        self.enabled = enabled 
        self.description = description 
        self.binding_events = binding_events
        self.merchandising_syntax = merchandising_syntax 
        self.expiration_type = expiration_type
        self.expiration_custom_days = expiration_custom_days 
        self.allocation_type = allocation_type 
        
        if data is not None:
            self.data = data 
    
    @property
    def data(self):
        return super().data

    @data.setter
    def data(self, data: Union[str, bytes, Dict]):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)
        for k, v in data.items():
            if v is None:
                continue
            
            setattr(self, k, v)
        
class ElementClassifications(JSONObject):

    _keys_attributes = OrderedDict([
        ('id', 'element_id'),
        ('name', 'name'),
        ('classifications', 'classifications')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        element_id=None,  # type: Optional[str]
        name=None,  # type: Optional[str]
        classifications=None,  # type: Optional[Union[Sequence[ClassificationItem], ClassificationItem]]
    ):
        # type: (...) -> None
        """
        Data structure that contains information about a report suite's classifications.

        https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-classification-item

        :param element_id:

            Element ID.

        :param name:

            Element Name.

        :param classifications:

            Classifications defined for the listed element.
        """
        self.element_id = element_id
        self.name = name
        self.classifications = classifications
        if isinstance(classifications, ClassificationItem):
            classifications = [classifications]
        self.classifications = classifications
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'classifications':
                v = JSONArray([
                    ClassificationItem(ci) for ci in v
                ])
            setattr(self, a, v)

class ReportSuiteEvars(JSONObject):
    
    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('evars', 'evars')
    ])
    
    def __init__(
        self,
        data=None,
        rsid=None,
        site_title=None,
        evars=None
    ):
    
        self.rsid = rsid 
        self.site_title = site_title
        if isinstance(evars, Evars):
            evars = [evars]
        self.evars = evars
        
        if data is not None:
            self.data = data 
            
    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'evars':
                v = JSONArray([
                    Evars(ec) for ec in v
                ])
            setattr(self, a, v)
            
                
class ReportSuiteElementClassifications(JSONObject):

    _keys_attributes = OrderedDict([
        ('rsid', 'rsid'),
        ('site_title', 'site_title'),
        ('element_classifications', 'element_classifications'),
        ('classifications', 'classifications')
        #('description', 'description')
    ])

    def __init__(
        self,
        data=None,  # type: Optional[Union[str, bytes, Dict]]
        rsid=None,  # type: Optional[str]
        site_title=None,  # type: Optional[str]
        element_classifications=None,  # type: Optional[Sequence[ElementClassifications]]
        classifications=None
        #description=None,  # type: Optional[str]
    ):
        # type: (...) -> None
        """
        Data structure that contains information about a report suite's classifications.

        https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-report-suite-classifications

        :param rsid:

            The report suite ID.

        :param site_title:

            The report suite friendly name.

        :param element_classifications:

            A list of elements and their associated classifications.

        """
        self.rsid = rsid
        self.site_title = site_title
        if isinstance(element_classifications, ElementClassifications):
            element_classifications = [element_classifications]
        self.element_classifications = element_classifications
        self.classifications = classifications
        #self.description = description
        if data is not None:
            self.data = data

    @property
    def data(self):
        return super().data

    @data.setter
    def data(
        self,
        data  # type: Union[str, bytes, Dict]
    ):
        if isinstance(data, bytes):
            data = str(data, 'utf-8')  # type: Union[str, bytes, Dict]
        if isinstance(data, str):
            data = loads(data, object_hook=OrderedDict)  # type: Union[str, bytes, Dict]
        for k, v in data.items():
            if v is None:
                continue
            a = self._keys_attributes[k]
            if k == 'element_classifications':
                v = JSONArray([
                    ElementClassifications(ec) for ec in v
                ])
            setattr(self, a, v)


if __name__ == '__main__':
    print(str2datetime('2016-11-10T10:24:26-0800'))
