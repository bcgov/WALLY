"""
API data models for hydrological zone regression models.
"""
from typing import Optional
from pydantic import BaseModel


class HydroZoneModelInputs(BaseModel):
    """
    inputs needed to create model prediction
    """
    hydrological_zone: int
    drainage_area: Optional[float]
    average_slope: Optional[float]
    glacial_coverage: Optional[float]
    potential_evapotranspiration: Optional[float]
    annual_precipitation: Optional[float]
    median_elevation: Optional[float]
    solar_exposure: Optional[float]

    class Config:
        orm_mode = True


class MeanAnnualRunoff(BaseModel):
    """ output values of the wally hydrological zone model """
    mean_annual_runoff: float
    model_score: object

    class Config:
        orm_mode = True


class MeanMonthlyRunoff(BaseModel):
    """ output values of the wally hydrological zone model """
    mean_monthly_runoff: float
    model_score: object

    class Config:
        orm_mode = True
