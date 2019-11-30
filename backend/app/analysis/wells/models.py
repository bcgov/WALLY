"""
API data models.
These are external facing data models/schemas that users see.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema
from geojson import Polygon


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
    distance_from_origin: float
    finished_well_depth: Optional[float]
    water_depth: Optional[float]
    ground_elevation_from_dem: Optional[float]
    distance_from_origin_pt: Optional[float]
    
    class Config:
        orm_mode = True


class Elevation(BaseModel):
    """ elevation data at a point """
    distance_from_origin: float
    elevation: float


class CrossSection(BaseModel):
    search_area: Polygon
    wells: List[WellSection]
    elevation_profile: List[Elevation]
