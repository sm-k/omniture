from collections import OrderedDict
from typing import Optional, Union, Dict

from omniture.data import JSONObject


class OmnitureError(JSONObject, Exception):

    def __hash__(self):
        return hash((self.error, self.description, self.uri))

    _keys_attributes = OrderedDict([
        ('error', 'error'),
        ('error_description', 'description'),
        ('error_uri', 'uri')
    ])

    def __init__(
        self,
        data: Optional[Union[str, bytes, Dict]]=None,
        error: Optional[str]=None,
        description: Optional[str]=None,
        uri: Optional[str]=None
    ):
        self.error = error
        self.description = description
        self.uri = uri
        if data:
            self.data = data


class BadRequest(OmnitureError):

    pass


class AuthenticationError(BadRequest):

    pass


class ReportNotReadyError(OmnitureError):

    pass


class InvalidReportID(BadRequest):

    pass


class BookmarkNotSupportedError(BadRequest):

    pass
