"""
API data models.
These are external facing data models/schemas that users see.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema


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
    top_screen: Optional[float]
    top_screen_type: Optional[str]
    distance: Optional[float]
    static_water_level: Optional[float]
