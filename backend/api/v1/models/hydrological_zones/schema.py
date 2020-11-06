"""
API data models for hydrological zone regression models.
"""
from typing import Optional, List
from pydantic import BaseModel, Schema


class HydroZoneModelInputs(BaseModel):
    """
    inputs needed to create model prediction
    """
    drainage_area: float
    median_elevation: float
    annual_precipitation: float

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
