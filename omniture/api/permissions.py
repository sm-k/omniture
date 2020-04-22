import omniture as omniture_


class Permissions:
    # TODO: Complete `Permissions` implementation
    """
    https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-methods-permissions
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture

    def add_login(self):
        # TODO: Complete `Permissions.add_login`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-addlogin-1
        pass

    def delete_group(self):
        # TODO: Complete `Permissions.delete_group`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deletegroup-1
        pass

    def delete_login(self):
        # TODO: Complete `Permissions.delete_login`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-deletelogin-1
        pass

    def get_group(self):
        # TODO: Complete `Permissions.`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getgroup-1
        pass

    def get_login(self):
        # TODO: Complete `Permissions.get_login`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getlogin-1
        pass

    def get_logins(self):
        # TODO: Complete `Permissions.get_logins`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getlogins-1
        pass

    def get_report_suite_groups(self):
        # TODO: Complete `Permissions.get_report_suite_groups`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-getreportsuitegroups-1
        pass

    def remove_login_segment(self):
        # TODO: Complete `Permissions.remove_login_segment`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-removeloginsegment
        pass

    def save_group(self):
        # TODO: Complete `Permissions.save_group`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savegroup-1
        pass

    def save_login(self):
        # TODO: Complete `Permissions.save_login`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savelogin-1
        pass

    def save_report_suite_groups(self):
        # TODO: Complete `Permissions.save_report_suite_groups`
        # https://marketing.adobe.com/developer/documentation/analytics-administration-1-4/r-savereportsuitegroups-1
        pass
