"""
API data models.
These are external facing data models/schemas that users see.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema


class StreamStation(BaseModel):
    """
    Information about a monitoring station where stream flow data is collected.
    """
    name: str
    url: str
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
    flow_years: List[int] = Schema(
        [], description="Years for which flow data is available")
    level_years: List[int] = Schema(
        [], description="Years for which stream level data is available")
    stream_flows_url: Optional[str] = Schema(
        None, description="URL where stream flow data is accessible")
    stream_levels_url: Optional[str] = Schema(
        None, description="URL where stream level data is accessible")
    stream_stats_url: Optional[str] = Schema(
        None, description="URL where stream statistics (monthly and annual means, and low flow frequencies) are accessible")
    external_urls: List[dict] = Schema(
        [], description="External links (e.g. links out to the original source of data")

    class Config:
        orm_mode = True


class MonthlyLevel(BaseModel):
    """
    Water level at a stream flow monitoring station, grouped by month
    """

    station_number: Optional[str]
    year: Optional[int]
    month: int
    full_month: Optional[int]
    no_days: Optional[int]
    precision_code: Optional[int]
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

    station_number: Optional[str]
    year: Optional[int]
    month: int
    monthly_mean: Optional[float]
    min: Optional[float]
    max: Optional[float]

    class Config:
        orm_mode = True


class FlowStatistics(BaseModel):
    """
    Flow statistics such as mean annual discharge, monthly means,
    and low flows for specified return periods
    """

    station_number: str
    low_30q10: float
    low_30q5: float
    low_7q10: float
    low_30q10_summer: float
    low_30q5_summer: float
    low_7q10_summer: float

    class Config:
        orm_mode = True
