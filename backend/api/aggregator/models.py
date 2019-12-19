"""
API models and response schemas for aggregating data from WMS and API sources
"""
from typing import List, Optional, Union
from pydantic import BaseModel
from geojson import Feature, FeatureCollection, Point
from asyncio import Future
from uuid import uuid4
from logging import getLogger

logger = getLogger('api')

def json_to_geojson(id_field: str = ''):
    """ returns a helper function that turns JSON results into GeoJSON,
    using the provided id_field to give each feature an ID. """

    if not id_field:
        # if function was used without specifying an id_field,
        # use a uuid as a placeholder. This will result in a
        # random id being assigned to each feature.
        id_field = uuid4()

    def helper_function(self, result_list):

        # check for pagination
        if not isinstance(result_list, list) and 'results' in result_list:
            result_list = result_list['results']

        return FeatureCollection([
            Feature(
                id=x.get(id_field, uuid4()),
                geometry=Point((x.get('longitude'), x.get('latitude'))),
                properties=dict(x)
            ) for x in result_list
        ])
    return helper_function


class WMSGetMapQuery(BaseModel):
    """ query params needed to make a WMS feature request """
    bbox: str
    width: int
    height: int
    service: str = "WMS"
    request: str = "GetMap"
    srs: str = "EPSG:3857"
    version: str = "1.1.1"
    format: str = "application/json;type=geojson"
    layers: str
    cql_filter: Optional[str]


class WMSGetFeatureQuery(BaseModel):
    """ query params needed to make a WMS feature request """
    service: str = "WFS"
    request: str = "GetFeature"
    count: int = 10000
    srs: str = "EPSG:3005"
    version: str = "2.0"
    outputFormat: str = "json"
    typeNames: str
    cql_filter: Optional[str]


class GWELLSAPIParams(BaseModel):
    """ request params for GWELLS API requests """
    within: str
    geojson: str = "true"


class ExternalAPIRequest(BaseModel):
    """ a WMS feature request """
    url: str
    layer: str
    formatter: any = json_to_geojson()  # optional formatter function that accepts a list and returns geojson
    q: Union[WMSGetMapQuery, GWELLSAPIParams, WMSGetFeatureQuery, dict]


class LayerResponse(BaseModel):
    """ contains info about and data from a response from a WMS GetMap or GetFeatureInfo request """
    layer: str

    # HTTP status code from the request.
    # The status code could be 0 if the request could not be made.
    status: int = 0
    geojson: FeatureCollection

    class Config:
        arbitrary_types_allowed = True
