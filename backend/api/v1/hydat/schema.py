"""
API data models.
These are external facing data models/schemas that users see.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema
from shapely.geometry import Point


class StreamStation(BaseModel):
    """
    Information about a monitoring station where stream flow data is collected.
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
    geom: Point

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StreamStationResponse(BaseModel):
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


class FASSTRMonthlyFlow(BaseModel):
    """
    Monthly summary from FASSTR Longterm Daily Stats
    https://bcgov.github.io/fasstr/reference/calc_longterm_daily_stats.html
    """

    month: str
    mean: float
    median: float
    maximum: float
    minimum: float
    p10: float
    p90: float


class FASSTRLongTermSummary(BaseModel):
    """
    Summary of FASSTR longterm daily stats
    https://bcgov.github.io/fasstr/reference/calc_longterm_daily_stats.html

    mean, median, maximum, minimum, p10 and p90 are stats computed by FASSTR
    from the long-term data.

    `months` provides a breakdown by month with the same headings.

    """
    station_number: str
    months: List[FASSTRMonthlyFlow]
    mean: float
    median: float
    maximum: float
    minimum: float
    p10: float
    p90: float


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


class FlowStat(BaseModel):
    """
    Flow statistics such as mean annual discharge, monthly means,
    and low flows for specified return periods
    """

    stat: str
    display_name: Optional[str]
    value: float


class FASSTRFlowStatsSummary(BaseModel):
    """
    Summary of flow statistics
    """

    station_number: str
    stats: List[FlowStat]

    class Config:
        orm_mode = True
