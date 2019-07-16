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


class MonthlyLevel(BaseModel):
    """
    Water level at a stream flow monitoring station, grouped by month
    """

    station_number: str
    year: int
    month: int
    full_month: int
    no_days: int
    precision_code: int
    monthly_mean: Optional[float]
    monthly_total: Optional[float]
    min: Optional[float]
    max: Optional[float]

    class Config:
        orm_mode = True


class MonthlyFlow(BaseModel):
    """
    Flow at a stream flow monitoring station, grouped by month
    """

    station_number: str
    year: int
    month: int
    full_month: int
    no_days: int
    monthly_mean: Optional[float]
    monthly_total: Optional[float]
    min: Optional[float]
    max: Optional[float]

    class Config:
        orm_mode = True
