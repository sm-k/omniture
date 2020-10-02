from collections import OrderedDict
from json import loads, dumps
from typing import Optional, Union

import omniture as omniture_
from omniture.data import DataWarehouseRequest

class DataWarehouse:
    # TODO: Complete `DataWarehouse` implementation
    """
    https://marketing.adobe.com/developer/documentation/data-warehouse/c-data-warehouse-api
    """

    def __init__(self, omniture):
        # type: (omniture_.Omniture) -> None
        self.omniture = omniture

    def is_enabled(
        self,
        rsid=None # type: Optional[str]
    ):
        # type: (...) -> bool
        
        data = OrderedDict()
        data['rsid'] = rsid
        
        response = self.omniture.request(
            'DataWarehouse.IsEnabled',
            data=dumps(data)
        )
        
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        
        return data
        
    def cancel_request(
        self,
        request_id
    
    ):
        # type: (...) -> str
        
        data = OrderedDict()
        data['Request_Id'] = request_id 
        
        response = self.omniture.request(
            'DataWarehouse.CancelRequest',
            data=dumps(data)
        )
        
        return response
    
    def check_request(
        self,
        request_id=None
    ):
        
        data = OrderedDict()
        data['Request_Id'] = request_id
        
        response = self.omniture.request(
            'DataWarehouse.CheckRequest',
            data=dumps(data)
        )
        
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        
        return data
    
    def get_segments(
        self,
        rsid,
        start_date,
        end_date
    ):
        
        data = OrderedDict()
        data['rsid'] = rsid
        data['start_date'] = start_date 
        data['end_date'] = end_date
    
        response = self.omniture.request(
            'DataWarehouse.GetSegments',
            data=dumps(data)
        )
        
        data = loads(str(response.read(), 'utf-8'), object_hook=OrderedDict)
        
        return data
        
    def create_request(
        self,
        request
    ):
        data = OrderedDict()
        data = request.data 
        
        response = self.omniture.request(
            'DataWarehouse.Request',
            data=dumps(data)
        )
        
        return response.read()
    
    def get_report_data(
        self,
        request_id=None,
        rsid=None,
        start_row=None
    ):
        pass