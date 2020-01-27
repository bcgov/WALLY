"""
API models and response schemas for aggregating data from WMS and API sources
"""
import json
from typing import List, Optional, Union
from pydantic import BaseModel
from geojson import Feature, FeatureCollection, Point
from asyncio import Future
from uuid import uuid4
from logging import getLogger

logger = getLogger('api')


def flatten_geojson_property(value):
    """ flattens json values for use in geojson properties
    """
    if isinstance(value, list):
        return ', '.join(json.dumps(value))

    return value


def json_to_geojson():
    """ returns a helper function that turns JSON results into GeoJSON,
    using the provided id_field to give each feature an ID.
    Accepts a list of fields to exclude. """

    def helper_function(self, result_list):

        # check for pagination
        if not isinstance(result_list, list) and 'results' in result_list:
            result_list = result_list['results']

        return FeatureCollection([
            Feature(
                id=x.get(self.id_field, str(uuid4())),
                geometry=Point((x.get('longitude'), x.get('latitude'))),
                properties={k: flatten_geojson_property(
                    v) for k, v in x.items() if k not in self.excluded_fields}
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
    typeName: Optional[str]
    cql_filter: Optional[str]


class GWELLSAPIParams(BaseModel):
    """ request params for GWELLS API requests """
    within: str
    geojson: str = "true"
    limit = 100


class ExternalAPIRequest(BaseModel):
    """ a WMS feature request """
    url: str
    layer: str
    # optional formatter function that accepts a list and returns geojson
    formatter = json_to_geojson()
    q: Union[WMSGetMapQuery,
             GWELLSAPIParams, WMSGetFeatureQuery, dict]
    # fields to exclude from responses (to avoid filling excel sheets with internal IDs, etc.)
    excluded_fields = []
    # an id field to populate geojson feature IDs (if not specified, a uuid will be created)
    id_field: Optional[str]
    # paginate: if set to False, do not follow pagination links (get one set of results only)
    paginate = True


class LayerResponse(BaseModel):
    """ contains info about and data from a response from a WMS GetMap or GetFeatureInfo request """
    layer: str

    # HTTP status code from the request.
    # The status code could be 0 if the request could not be made.
    status: int = 0
    geojson: FeatureCollection

    class Config:
        arbitrary_types_allowed = True


class WatershedDetails(BaseModel):
    """ info about a watershed"""
    precipitation: dict
    glacial_coverage: float
    glacial_area: float
    watershed_area: float
    projected_geometry_area: float
    projected_geometry_area_simplified: float
    precip_search_area: float


class LicenceDetails(BaseModel):
    """ statistics about licences in a given area """
    licences: FeatureCollection
    total_qty: float
    total_qty_by_purpose: List
    projected_geometry_area: Optional[float]
    projected_geometry_area_simplified: Optional[float]

    class Config:
        arbitrary_types_allowed = True


class SurficialGeologyTypeSummary(BaseModel):
    """ 
    Summary of features belonging to single type of surficial geology in a search area.
    e.g. summary of all bedrock features in a search area, with a FeatureCollection,
    total area, etc.
    """
    soil_type: str
    area_within_watershed: float
    geojson: FeatureCollection

    class Config:
        arbitrary_types_allowed = True


class SurficialGeologyDetails(BaseModel):
    """ statistics about surficial geology
    """
    summary_by_type: List
    coverage_area: Optional[float]
    projected_geometry_area: Optional[float]
    projected_geometry_area_simplified: Optional[float]
