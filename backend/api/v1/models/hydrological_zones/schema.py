"""
API data models for hydrological zone regression models.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema


class HydroZoneModelInputs(BaseModel):
    """
    inputs needed to create model prediction
    """
    hydrological_zone: str
    year: Optional[str]
    drainage_area: Optional[float]
    average_slope: Optional[float]
    glacial_coverage: Optional[float]
    glacial_area: Optional[float]
    watershed_area: Optional[float]
    potential_evapotranspiration_thornthwaite: Optional[float]
    potential_evapotranspiration_hamon: Optional[float]
    annual_precipitation: Optional[float]
    median_elevation: Optional[float]
    aspect: Optional[float]
    solar_exposure: Optional[float]

    class Config:
        orm_mode = True


class MeanAnnualFlow(BaseModel):
    """ output values of the wally hydrological zone model """
    mean_annual_flow: float
    r_squared: float

    class Config:
        orm_mode = True


class MeanMonthlyFlow(BaseModel):
    """ output values of the wally hydrological zone model """
    mean_monthly_flow: float
    r_squared: float

    class Config:
        orm_mode = True
