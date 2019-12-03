"""
API data models for First Nations communities, treaty areas and treaty lands.
These are external facing data models/schemas that users see.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema


class Community(BaseModel):
    """
    model for displaying nearby communities
    """

    distance: float
    FIRST_NATION_BC_NAME: str
    URL_TO_BC_WEBSITE: str

    class Config:
        orm_mode = True


class TreatyLands(BaseModel):
    """ model for nearby treaty lands """
    distance: float
    TREATY: str
    FIRST_NATION_NAME: str
    EFFECTIVE_DATE: str
    LAND_TYPE: str

    class Config:
        orm_mode = True


class TreatyAreas(BaseModel):
    """ model for nearby treaty lands """
    distance: float
    TREATY: str
    FIRST_NATION_NAME: str
    EFFECTIVE_DATE: str
    AREA_TYPE: str
    LAND_TYPE: str

    class Config:
        orm_mode = True


class NearbyAreasResponse(BaseModel):
    """
    API response model for providing information about nearby communities, treaty lands and treaty areas
    """

    nearest_communities: List[Community]
    nearest_treaty_lands: List[TreatyLands]
    nearest_treaty_areas: List[TreatyAreas]
