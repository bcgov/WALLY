"""
API data models.
These are external facing data models/schemas that users see.
"""
from pydantic import BaseModel
from typing import Optional


class StreamStation(BaseModel):
    """
    API data model for a station where stream flow data is collected.
    """
    station_number: str
    station_name: str
    prov_terr_state_loc: str
    regional_office_id: str
    hyd_status: Optional[str]
    sed_status: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    drainage_area_gross: Optional[float]
    drainage_area_effect: Optional[float]
    rhbn: int
    real_time: int

    class Config:
        orm_mode = True
