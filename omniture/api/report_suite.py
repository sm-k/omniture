from collections import OrderedDict
from json import loads, dumps
from typing import Optional, Union

import omniture as omniture_
from omniture.data import CreateReportSuiteResponse, ReportSuiteActivation, ReportSuiteAxleStartDate, \
    ReportSuiteElementClassifications, ReportSuiteEvars, AvailableElementsResponse, AvailableMetricsResponse


class ReportSuite:
    """
    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-methods-reportsuite
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture

    def create(
        self,
        full_response=None,  # type: Optional[bool],
        base_url=None,  # type: Optional[str]
        default_page=None,  # type: Optional[str]
        duplicate_rsid=None,  # type: Optional[str]
        go_live_date=None,  # type: Optional[date]
        hits_per_day=None,  # type: Optional[int]
        japanese_keyword_processing=None,  # type: Optional[bool]
        rsid=None,  # type: Optional[str],
        site_title=None,  # type: Optional[str]
        simplified_menu=None,  # type: Optional[bool]
        time_zone=None  # type: Optional[str]
    ):
        # type: (...) -> Union[bool, CreateReportSuiteResponse]
        """
        Creates a new report suite.

        :param full_response:

            (Optional) If this parameter is `True`, the response will be a `CreateReportSuiteResponse` object
            instead of a boolean.

        :param base_url:

            (Optional) Defines the base domain for the report suite. This URL functions as an internal URL filter if
            you do not explicitly define internal URL filters for the report suite.

        :param default_page:

            (Optional) Strips occurrences of the Default Page value from URLs it encounters. If your Most Popular Pages
            report contains URLs rather than page names, this setting prevents multiple URLs for the same web page.

            For example, the URLs http://mysite.com and http://mysite.com/index.html are typically the same page.
            Analytics lets you remove extraneous filenames so that both these URLs show up as http://mysite.com in
            your reports.

            If you do not set this value, Analytics automatically removes the following filenames from URLs:
            index.htm, index.html, index.cgi, index.asp, default.htm, default.html, default.cgi, default.asp,
            home.htm, home.html, home.cgi, and home.asp.

            To disable filename stripping, specify a Default Page value that never occurs in your URLs.

        :param duplicate_rsid:

            The type of report suite to create. You must specify either an existing rsid to duplicate, or one of the
            following report suite templates:

                - admin.template.01 (Aggregator Portal)
                - admin.template.02 (Commerce)
                - admin.template.03 (Content & Media)
                - admin.template.04 (Financial Services)
                - admin.template.05 (Job Portal)
                - admin.template.06 (Lead Generation)
                - admin.template.07 (Subscription)
                - admin.template.08 (Support Media)
                - admin.template.09 (Default)

        :param go_live_date:

            The date the report suite starts collecting data.

        :param hits_per_day:

            The estimated number of hits per day this report suite will receive.

        :param japanese_keyword_processing:

            (Optional)

        :param rsid:

            The report suite ID. All report suite IDs must contain your company prefix to be accepted. The company
            prefix can be seen on the Create Report Suites tool in the Admin Console. The rsid can contain only
            alphanumeric characters and periods (".").

        :param site_title:

            (Optional) The report suite's friendly name.

        :param simplified_menu:

            (Optional) Enables the simplified menu in reports & analytics.

        :param time_zone:

            One of the following strings:
            'Europe/London', 'US/Samoa', 'US/Hawaii', 'US/Alaska', 'America/Tijuana', 'US/Pacific', 'US/Arizona',
            'US/Mountain', 'America/Mexico_City', 'Canada/Saskatchewan', 'US/Central', 'America/Lima', 'US/Eastern',
            'US/East-Indiana', 'America/Caracas', 'Canada/Atlantic', 'America/Santiago', 'America/La_Paz',
            'Canada/Newfoundland', 'America/Sao_Paulo', 'America/Buenos_Aires', 'America/Guyana', 'America/Montevideo',
            'Etc/GMT+2', 'Atlantic/Azores', 'Atlantic/Cape_Verde', 'GMT', 'Europe/Berlin', 'Europe/Paris',
            'Europe/Prague', 'Europe/Warsaw', 'Europe/Athens', 'Africa/Cairo', 'EET', 'Africa/Harare', 'Israel',
            'Europe/Istanbul', 'Asia/Baghdad', 'Asia/Kuwait', 'Asia/Tehran', 'Asia/Muscat', 'Europe/Samara',
            'Europe/Moscow', 'Asia/Tbilisi', 'Europe/Volgograd', 'Asia/Kabul', 'Asia/Yekaterinburg', 'Asia/Karachi',
            'Asia/Tashkent', 'Asia/Calcutta', 'Asia/Colombo', 'Asia/Almaty', 'Asia/Dhaka', 'Asia/Bangkok',
            'Asia/Chongqing', 'Asia/Hong_Kong', 'Australia/Perth', 'Asia/Tokyo', 'Asia/Yakutsk', 'Australia/Adelaide',
            'Australia/Darwin', 'Australia/Brisbane', 'Australia/Sydney', 'Pacific/Guam', 'Australia/Hobart',
            'Pacific/Port_Moresby', 'Asia/Vladivostok', 'Asia/Magadan', 'Pacific/Guadalcanal', 'Pacific/Kwajalein',
            'Pacific/Fiji', 'Asia/Kamchatka', 'Pacific/Majuro', 'NZ'

        :return:
        """
        data = OrderedDict()
        if full_response is not None:
            data['full_response'] = full_response
        if base_url is not None:
            data['base_url'] = base_url
        if default_page is not None:
            data['default_pages'] = default_page
        if duplicate_rsid is not None:
            data['duplicate_rsid'] = duplicate_rsid
        if go_live_date is not None:
            data['go_live_date'] = go_live_date
        if hits_per_day is not None:
            data['hits_per_day'] = hits_per_day
        if japanese_keyword_processing is not None:
            data['japanese_keyword_processing'] = japanese_keyword_processing
        if rsid is not None:
            data['rsid'] = rsid
        if site_title is not None:
            data['site_title'] = site_title
        if simplified_menu is not None:
            data['simplified_menu'] = simplified_menu
        if time_zone is not None:
            data['time_zone'] = time_zone
        time_zone = None
        response = self.omniture.request(
            'ReportSuite.Create',
            data=dumps(data)
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        if full_response:
            return CreateReportSuiteResponse(data)
        else:
            return data

    def delete_calculated_metrics(self):
        # TODO: Complete `ReportSuite.delete_calculated_metrics`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-create-1
        pass

    def get_available_elements(
        self,
        rsid_list,
        return_datawarehouse_elements=None 
    ):
        if isinstance(rsid_list, str):
            rsid_list = [rsid_list]
        response = self.omniture.request(
            'ReportSuite.GetAvailableElements',
            data=dumps({
                'rsid_list': [rsid for rsid in rsid_list]
            })
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        return AvailableElementsResponse(data)
        
    def get_available_metrics(
        self,
        rsid_list,
        return_datawarehouse_elements=None 
    ):
        if isinstance(rsid_list, str):
            rsid_list = [rsid_list]
        response = self.omniture.request(
            'ReportSuite.GetAvailableMetrics',
            data=dumps({
                'rsid_list': [rsid for rsid in rsid_list]
            })
        )
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        return AvailableMetricsResponse(data)
        
    def delete_classification(self):
        # TODO: Complete `ReportSuite.delete_classification`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deleteclassification
        pass

    def delete_internal_url_filters(self):
        # TODO: Complete `ReportSuite.delete_internal_url_filters`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deleteinternalurlfilters-1
        pass

    def delete_ip_address_exclusion(self):
        # TODO: Complete `ReportSuite.delete_ip_address_exclusion`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deleteipaddressexclusion
        pass

    def delete_key_visitors(self):
        # TODO: Complete `ReportSuite.delete_key_visitors`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deletekeyvisitors-1
        pass

    def delete_marketing_channel_cost(self):
        # TODO: Complete `ReportSuite.delete_marketing_channel_cost`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deletemarketingchannelcost
        pass

    def delete_paid_search_detection(self):
        # TODO: Complete `ReportSuite.delete_paid_search_detection`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deletepaidsearchdetection
        pass

    def get_activation(self, rsid_list):
        # type: (Union[Sequence[str], str]) -> Iterable[ReportSuiteActivation]
        """
        Retrieves the activation status for each of the specified report suites.

        https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getactivation-1

        :param rsid_list:

            A list of report suite IDs.

        :return:

            A list of report suites and the activation status of each.
        """
        if isinstance(rsid_list, str):
            rsid_list = [rsid_list]
        response = self.omniture.request(
            'ReportSuite.GetActivation',
            data=dumps({
                'rsid_list': [rsid for rsid in rsid_list]
            })
        )
        for rsa in loads(str(response.read(), 'utf-8'), object_hook=OrderedDict):
            yield ReportSuiteActivation(rsa)

    def get_axle_start_date(self, rsid_list):
        # type: (Union[Sequence[str], str]) -> Iterable[ReportSuiteActivation]
        """
        Retrieves the date a report suite was migrated from SiteCatalyst 14 to axle processing (version 15).

        https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getaxlestartdate

        :param rsid_list:

            A list of report suite IDs.

        :return:

            A list of report suites and the axle start date for each.
        """
        if isinstance(rsid_list, str):
            rsid_list = [rsid_list]
        response = self.omniture.request(
            'ReportSuite.GetAxleStartDate',
            data=dumps({
                'rsid_list': [rsid for rsid in rsid_list]
            })
        )
        for rsa in loads(str(response.read(), 'utf-8'), object_hook=OrderedDict):
            yield ReportSuiteAxleStartDate(rsa)

    def get_base_currency(self):
        # TODO: Complete `ReportSuite.get_base_currency`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getbasecurrency-1
        pass

    def get_base_url(self):
        # TODO: Complete `ReportSuite.get_base_url`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getbaseurl-1
        pass

    def get_classifications(self, rsid_list, element_list=None):
        # type: (Sequence[str], Optional[Sequence[str]]) -> Sequence[ReportSuiteElementClassifications]
        """
        Retrieves a list of classifications (associated with the specified element) for each of the specified
        report suites.

        https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getclassifications-1

        :param rsid_list:

            (required) The list of report suite IDs for which you want to retrieve classifications.

        :param element_list:

            (required) The list of elements for which you want to retrieve classifications.

            Values can be any of the following:

            "prop1" - "prop75", "evar1" - "evar75", "listvar1" - "listvar3", "trackingcode", "days_between_buys",
            "days_till_purchase", "domain", "first_touch_marketing_channel", "first_touch_marketing_channel_detail",
            "last_touch_marketing_channel", "last_touch_marketing_channel_detail", "loyalty", "media",
            "page", "sitesection", "server", "product", "sitetime", "state", "surveybase",
            "tntbase", "visitdepth", "visitnum", or "zip".

        :return:

            List that includes each report suite's classifications hierarchy for the specified element(s).
        """
        if isinstance(rsid_list, str):
            rsid_list = [rsid_list]
        if isinstance(element_list, str):
            element_list = [element_list]
        data = OrderedDict()
        if rsid_list is not None:
            data['rsid_list'] = rsid_list
        if element_list is not None:
            data['element_list'] = element_list
        response = self.omniture.request(
            'ReportSuite.GetClassifications',
            data=dumps(data)
        )
        for rsec in loads(str(response.read(), 'utf-8'), object_hook=OrderedDict):
            yield ReportSuiteElementClassifications(rsec)

    def get_calculated_metrics(self):
        # TODO: Complete `ReportSuite.get_calculated_metrics`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getcalculatedmetrics-1
        pass

    def get_custom_calendar(self):
        # TODO: Complete `ReportSuite.get_custom_calendar`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getcustomcalendar-1
        pass

    def get_data_warehouse_display(self):
        # TODO: Complete `ReportSuite.get_data_warehouse_display`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getdatawarehousedisplay
        pass

    def get_default_page(self):
        # TODO: Complete `ReportSuite.get_default_page`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getdefaultpage-1
        pass

    def get_discover_enabled(self):
        # TODO: Complete `ReportSuite.get_discover_enabled`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getdiscoverenabled
        pass

    def get_ecommerce(self):
        # TODO: Complete `ReportSuite.get_ecommerce`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getecommerce-1
        pass

    def get_evars(
        self,
        rsid_list
    ):
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getevars-1
        
        if isinstance(rsid_list, str):
            rsid_list = [rsid_list]
        
        data = OrderedDict()
        if rsid_list is not None:
            data['rsid_list'] = rsid_list

        response = self.omniture.request(
            'ReportSuite.GetEvars',
            data=dumps(data)
        )
        for rsec in loads(str(response.read(), 'utf-8'), object_hook=OrderedDict):
            yield ReportSuiteEvars(rsec)

    def get_events(self):
        # TODO: Complete `ReportSuite.get_events`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getevents
        pass

    def get_geo_segmentation(self):
        # TODO: Complete `ReportSuite.get_geo_segmentation`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getgeosegmentation
        pass

    def get_ip_address_exclusions(self):
        # TODO: Complete `ReportSuite.get_ip_address_exclusions`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getipaddressexclusions-1
        pass

    def get_ip_obfuscation(self):
        # TODO: Complete `ReportSuite.get_ip_obfuscation`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getipobfuscation-1
        pass

    def get_internal_url_filters(self):
        # TODO: Complete `ReportSuite.get_internal_url_filters`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getinternalurlfilters-1
        pass

    def get_key_visitors(self):
        # TODO: Complete `ReportSuite.get_key_visitors`
        # https://marketing.adobe.com/developer/documentation/an_alytics-administration-1-4/r-getkeyvisitors-1
        pass

    def get_list_variables(self):
        # TODO: Complete `ReportSuite.get_list_variables`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getlistvariables-1
        pass

    def get_localization(self):
        # TODO: Complete `ReportSuite.get_localization`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getlocalization-1
        pass

    def get_marketing_channel_cost(self):
        # TODO: Complete `ReportSuite.get_marketing_channel_cost`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getmarketingchannelcosts
        pass

    def get_marketing_channel_expiration(self):
        # TODO: Complete `ReportSuite.get_marketing_channel_expiration`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getmarketingchannelexpiration-1
        pass

    def get_marketing_channel_rules(self):
        # TODO: Complete `ReportSuite.get_marketing_channel_rules`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getmarketingchannelrules-1
        pass

    def get_marketing_channels(self):
        # TODO: Complete `ReportSuite.get_marketing_channels`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getmarketingchannels-1
        pass

    def get_mobile_app_reporting(self):
        # TODO: Complete `ReportSuite.get_mobile_app_reporting`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getmobileappreporting
        pass

    def get_paid_search_detection(self):
        # TODO: Complete `ReportSuite.get_paid_search_detection`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getpaidsearchdetection
        pass

    def get_permanent_traffic(self):
        # TODO: Complete `ReportSuite.get_permanent_traffic`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getpermanenttraffic-1
        pass

    def get_processing_status(self):
        # TODO: Complete `ReportSuite.get_processing_status`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getprocessingstatus
        pass

    def get_props(self):
        # TODO: Complete `ReportSuite.get_props`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getprops
        pass

    def get_real_time_settings(self):
        # TODO: Complete `ReportSuite.get_real_time_settings`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getrealtimesettings
        pass

    def get_scheduled_spike(self):
        # TODO: Complete `ReportSuite.get_scheduled_spike`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getscheduledspike-1
        pass

    def get_segments(self):
        # TODO: Complete `ReportSuite.get_segments`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getsegments-1
        pass

    def get_settings(self):
        # TODO: Complete `ReportSuite.get_settings`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getsettings-1
        pass

    def get_site_title(self):
        # TODO: Complete `ReportSuite.get_site_title`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getsitetitle-1
        pass

    def get_template(self):
        # TODO: Complete `ReportSuite.get_template`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-gettemplate-2
        pass

    def get_time_zone(self):
        # TODO: Complete `ReportSuite.get_time_zone`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-gettimezone-1
        pass

    def get_transaction_enabled(self):
        # TODO: Complete `ReportSuite.get_transaction_enabled`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-gettransactionenabled
        pass

    def get_unique_visitor_variable(self):
        # TODO: Complete `ReportSuite.get_unique_visitor_variable`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getuniquevisitorvariable-1
        pass

    def get_video_settings(self):
        # TODO: Complete `ReportSuite.get_video_settings`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getvideosettings
        pass

    def save_base_currency(self):
        # TODO: Complete `ReportSuite.save_base_currency`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savebasecurrency-1
        pass

    def save_base_url(self):
        # TODO: Complete `ReportSuite.save_base_url`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savebaseurl-1
        pass

    def save_calculated_metrics(self):
        # TODO: Complete `ReportSuite.save_calculated_metrics`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savecalculatedmetrics-1
        pass

    def save_classification(self):
        # TODO: Complete `ReportSuite.save_classification`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveclassification
        pass

    def save_custom_calendar(self):
        # TODO: Complete `ReportSuite.save_custom_calendar`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savecustomcalendar-1
        pass

    def save_data_warehouse_display(self):
        # TODO: Complete `ReportSuite.save_data_warehouse_display`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savedatawarehousedisplay
        pass

    def save_default_page(self):
        # TODO: Complete `ReportSuite.save_default_page`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savedefaultpage-1
        pass

    def save_discover_enabled(self):
        # TODO: Complete `ReportSuite.save_discover_enabled`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savediscoverenabled
        pass

    def save_ecommerce(self):
        # TODO: Complete `ReportSuite.save_ecommerce`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveecommerce-1
        pass

    def save_evars(self):
        # TODO: Complete `ReportSuite.save_evars`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveevars-1
        pass

    def save_events(self):
        # TODO: Complete `ReportSuite.save_events`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveevents
        pass

    def save_geo_segmentation(self):
        # TODO: Complete `ReportSuite.save_geo_segmentation`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savegeosegmentation
        pass

    def save_ip_address_exclusion(self):
        # TODO: Complete `ReportSuite.save_ip_address_exclusion`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveipaddressexclusion
        pass

    def save_ip_obfuscation(self):
        # TODO: Complete `ReportSuite.save_ip_obfuscation`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveipobfuscation-1
        pass

    def save_internal_url_filters(self):
        # TODO: Complete `ReportSuite.save_internal_url_filters`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveinternalurlfilters
        pass

    def save_key_visitors(self):
        # TODO: Complete `ReportSuite.save_key_visitors`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savekeyvisitors
        pass

    def save_list_variables(self):
        # TODO: Complete `ReportSuite.save_list_variables`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savelistvariables-1
        pass

    def save_marketing_channel_cost(self):
        # TODO: Complete `ReportSuite.save_marketing_channel_cost`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savemarketingchannelcost-1
        pass

    def save_marketing_channel_expiration(self):
        # TODO: Complete `ReportSuite.save_marketing_channel_expiration`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savemarketingchannelexpiration-1
        pass

    def save_marketing_channel_rules(self):
        # TODO: Complete `ReportSuite.save_marketing_channel_rules`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savemarketingchannelrules-1
        pass

    def save_marketing_channels(self):
        # TODO: Complete `ReportSuite.save_marketing_channels`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savemarketingchannels-1
        pass

    def save_mobile_app_reporting(self):
        # TODO: Complete `ReportSuite.save_mobile_app_reporting`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savemobileappreporting
        pass

    def save_paid_search_detection(self):
        # TODO: Complete `ReportSuite.save_paid_search_detection`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savepaidsearchdetection
        pass

    def save_permanent_traffic(self):
        # TODO: Complete `ReportSuite.save_permanent_traffic`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savepermanenttraffic-1
        pass

    def save_real_time_settings(self):
        # TODO: Complete `ReportSuite.save_real_time_settings`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saverealtimesettings
        pass

    def save_scheduled_spike(self):
        # TODO: Complete `ReportSuite.save_scheduled_spike`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savescheduledspike-1
        pass

    def save_site_title(self):
        # TODO: Complete `ReportSuite.save_site_title`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savesitetitle-1
        pass

    def save_time_zone(self):
        # TODO: Complete `ReportSuite.save_time_zone`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savetimezone-1
        pass

    def save_props(self):
        # TODO: Complete `ReportSuite.save_props`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveprops
        pass

    def save_unique_visitor_variable(self):
        # TODO: Complete `ReportSuite.save_unique_visitor_variable`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-saveuniquevisitorvariable-1
        pass


if __name__ == '__main__':
    pass
