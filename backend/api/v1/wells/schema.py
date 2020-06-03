"""
API data models.
These are external facing data models/schemas that users see.
"""
import json
import logging
from typing import Optional, List, Any
from pydantic import BaseModel, Schema
from geojson import Polygon
from uuid import uuid4
from geojson import Feature, FeatureCollection, Point

logger = logging.getLogger('wells')


def flatten_geojson_property(value):
    """ flattens json values for use in geojson properties
    """
    if isinstance(value, list):
        return ', '.join(json.dumps(value))

    return value


def export_formatter():
    """ 
    returns a helper function that turns JSON results into GeoJSON,
    using the provided id_field to give each feature an ID. 
    """

    def helper_function(self, result):

        logger.warn("result")
        logger.warn(type(result))

        return FeatureCollection([
            Feature(
                id=result.get(self.id_field, str(uuid4())),
                geometry=Point((result.get('longitude'), result.get('latitude'))),
                properties=result
            )
        ])
            
    return helper_function


class Screen(BaseModel):
    """
    Information about a screen installed into a well. Normally part of a set of
    screen information broken down by depth intervals.
    """
    start: Optional[float]
    end: Optional[float]
    diameter: Optional[float]
    assembly_type: Optional[str]


class WellDrawdown(BaseModel):
    """
    Well data focused on drawdown impact assessments
    """
    well_tag_number: int
    latitude: float
    longitude: float
    well_yield: Optional[float]
    diameter: Optional[str]
    aquifer: Optional[int]
    well_yield_unit: Optional[str]
    finished_well_depth: Optional[float]
    street_address: Optional[str]
    intended_water_use: Optional[str]
    aquifer_subtype: Optional[str]
    aquifer_hydraulically_connected: Optional[bool]
    screen_set: Optional[List[Screen]]
    top_of_screen: Optional[float] = Schema(
        None, title="Top of screen", description="The depth of the start of the uppermost reported screen segment.")
    top_of_screen_type: Optional[str] = Schema(
        None, title="Screen type at top of screen", description="The reported screen material type at the top of screen")
    distance: Optional[float] = Schema(
        None, title="Distance from search point", description="The distance from the search point in meters")
    static_water_level: Optional[float]
    swl_to_screen: Optional[float] = Schema(None, title="Static water level to top of screen (ft)",
                                            description="The calculated distance between the reported static water level and the start of the uppermost screen segment. The type of screen is not taken into account. This information is based on reported values and should be confirmed.")
    swl_to_bottom_of_well: Optional[float] = Schema(None, title="Static water level to bottom of well (ft)",
                                                    description="The calculated distance between the reported static water level and the finished well depth. This information is based on reported values and should be confirmed.")


class WellSection(BaseModel):
    """
    Well data for use in sections
    """
    well_tag_number: int
    finished_well_depth: Optional[float]
    water_depth: Optional[float]
    ground_elevation_from_dem: Optional[float]
    distance_from_origin: Optional[float]

    class Config:
        orm_mode = True


class Elevation(BaseModel):
    """ elevation data at a point """
    distance_from_origin: float
    elevation: float


class CrossSection(BaseModel):
    search_area: Any
    wells: List[WellSection]
    elevation_profile: List[Elevation]
    surface: List


class CrossSectionExport(BaseModel):
    wells: List[int]


class ExportApiParams(BaseModel):
    """ request params for GWELLS API request """
    geojson: str = "true"


class ExportApiRequest(BaseModel):
    """ a WMS feature request """
    url: str
    layer: str
    # optional formatter function that accepts a list and returns geojson
    formatter = export_formatter()
    q: Optional[Any]
    # an id field to populate geojson feature IDs (if not specified, a uuid will be created)
    id_field: Optional[str]
    # paginate: if set to False, do not follow pagination links (get one set of results only)
    paginate = False
