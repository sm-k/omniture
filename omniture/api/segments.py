from collections import OrderedDict
from json import dumps, loads
from typing import Dict

import omniture as omniture_
from omniture.data import Segment, SegmentFilters, SegmentShare
from omniture.data import SegmentDefinition


class Segments:
    # TODO: Complete `Segments` implementation
    """
    https://marketing.adobe.com/developer/documentation/segments-1-4/c-segments-api-methods
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture

    def get(
        self,
        access_level=None,  # type: Optional[str]
        fields=(  # type: Optional[Sequence[str]]
            "tags", "shares", "description", "owner",
            "modified", "compatibility", "favorite",
            "reportSuiteID", "definition"
        ),
        selected=None,  # type: Optional[Sequence[str]]
        sort=None,  # type: Optional[str]
        filters=None  # type: Optional[SegmentFilters]
    ):
        # type: (...) -> Iterable[Segment]
        """
        https://marketing.adobe.com/developer/documentation/segments-1-4/r-get-1

        :param access_level:

            optional, one of: "owned", "shared", "all". Defaults to "owned". Will return an error if "all' is used by a
            non-admin.

        :param fields:

            optional, one or more of: "tags", "shares", "description", "owner", "modified", "compatibility", "favorite",
            "reportSuiteID", "definition". The response will always include "id" and "name".

        :param selected:

            optional, an array of segment IDs. Causes accessLevel to be ignored (except for the all/admin restriction),
            does not accept legacy IDs

        :param sort:

            optional, one of: "id", "name", "description", "reportSuiteID", "owner",
            "modified", "favorite". Default is "id".

        :param filters:

            A `SegmentFilters` limiting the segments returned.

        :return:
        """
        data = {}
        if access_level is not None:
            data['accessLevel'] = access_level
        if fields is not None:
            data['fields'] = fields
        if selected is not None:
            data['selected'] = selected
        if sort is not None:
            data['sort'] = sort
        if filters is not None:
            data['filters'] = filters.data
        response = self.omniture.request(
            'Segments.Get',
            data=dumps(data)
        )
        for segment in loads(str(response.read(), 'utf-8')):
            yield Segment(segment)

    def delete(
        self,
        segment_id=None,  # type: Optional[str]
    ):
        # type: (...) -> bool
        """
        Deletes a segment.

        https://marketing.adobe.com/developer/documentation/segments-1-4/r-delete
        """
        response = self.omniture.request(
            'Segments.Delete',
            data=dumps(dict(segmentID=segment_id))
        )
        return loads(str(response.read(), 'utf-8'))

    def save(
        self,
        definition=None,  # type: Optional[SegmentDefinition]
        name=None,  # type: Optional[str]
        rsid=None,  # type: Optional[str]
        segment_id=None,  # type: Optional[str]
        description=None,  # type: Optional[str]
        favorite=None,  # type: Optional[bool]
        owner=None,  # type: Optional[str]
        shares=None,  # type: Optional[Sequence[SegmentShare]]
        tags=None,  # type: Optional[Sequence[str]]
    ):
        # type: (...) -> str
        """
        Deletes a segment.

        https://marketing.adobe.com/developer/documentation/segments-1-4/r-delete
        """
        data = OrderedDict()
        if definition is not None:
            data['definition'] = definition.data
        if name is not None:
            data['name'] = name
        if rsid is not None:
            data['reportSuiteID'] = rsid
        if segment_id is not None:
            data['id'] = segment_id
        if description is not None:
            data['description'] = description
        if favorite is not None:
            data['favorite'] = favorite
        if owner is not None:
            data['owner'] = owner
        if shares is not None:
            if isinstance(shares, (SegmentShare, Dict)):
                shares = [shares]
            data['shares'] = [
                share.data
                if isinstance(share, SegmentShare)
                else share
                for share in shares
            ]
        if tags is not None:
            if isinstance(tags, str):
                tags = tags.split(',')
            data['tags'] = tags
        response = self.omniture.request(
            'Segments.Save',
            data=dumps(data)
        )
        return loads(str(response.read(), 'utf-8'))['segmentID']
