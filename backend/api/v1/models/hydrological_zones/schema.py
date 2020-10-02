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


class ModelOutput(BaseModel):
    """ output values of the wally hydrological zone model """
    mean_annual_flow: float
    r_squared: float
    
    class Config:
        orm_mode = True
