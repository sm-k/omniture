import omniture as omniture_
from json import dumps, loads
from typing import Dict
from collections import OrderedDict

import omniture as omniture_
from omniture.data import CalculatedMetric, CalculatedMetricShare

class CalculatedMetrics:
    # TODO: Complete `CalculatedMetrics` implementation
    """
    https://marketing.adobe.com/developer/documentation/segments-1-4/calculated-metrics
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture
    
    def get(
        self,
        access_level=None,
        fields=(
            "type", "description",
            "tags", "modified",
            "owner", "compatibility",
            "reportSuiteID", 
            "approved", "owner",
            "polarity", "precision",
            "definition",
            "favorite"
        ),
        selected=None,
        sort=None,
        filters=None
    ):
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
            data['filters'] = filters
        response = self.omniture.request(
            'CalculatedMetrics.Get',
            data=dumps(data)
        )
        for segment in loads(str(response.read(), 'utf-8')):
            yield CalculatedMetric(segment)
    
    def delete(
        self,
        calculated_metric_id=None # type: Optional[str]
    ):
        # type: (...) -> bool
        """
        Deletes a calulated metric
        """
        response = self.omniture.request(
            'CalculatedMetrics.Delete',
            data=dumps(dict(calculatedMetricID=calculated_metric_id))
        )
        return loads(str(response.read(), 'utf-8'))
        
    def save(
        self,
        definition=None,  # type: Optional[SegmentDefinition]
        name=None,  # type: Optional[str]
        rsid=None,  # type: Optional[str]
        metric_id=None,  # type: Optional[str]
        description=None,  # type: Optional[str]
        favorite=None,  # type: Optional[bool]
        owner=None,  # type: Optional[str]
        shares=None,  # type: Optional[Sequence[SegmentShare]]
        tags=None,  # type: Optional[Sequence[str]]
        polarity=None,
        metric_type=None,
        precision=None
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
        if metric_id is not None:
            data['id'] = metric_id
        if description is not None:
            data['description'] = description
        if favorite is not None:
            data['favorite'] = favorite
        if owner is not None:
            data['owner'] = owner
        if polarity is not None:
            data['polarity'] = polarity
        if precision is not None:
            data['precision'] = precision 
        if metric_type is not None:
            data['metric_type'] = metric_type
            
        if shares is not None:
            if isinstance(shares, (CalculatedMetricShare, Dict)):
                shares = [shares]
            data['shares'] = [
                share.data
                if isinstance(share, CalculatedMetricShare)
                else share
                for share in shares
            ]
        if tags is not None:
            if isinstance(tags, str):
                tags = tags.split(',')
            data['tags'] = tags
        response = self.omniture.request(
            'CalculatedMetrics.Save',
            data=dumps(data)
        )
        return loads(str(response.read(), 'utf-8'))['calculatedMetricID']