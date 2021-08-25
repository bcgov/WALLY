"""
API data models for hydrological zone regression models.
"""
from typing import Optional, List
from pydantic import BaseModel


class ModelFlowEstimates(BaseModel):
    """
    schema representing water flow information 
    """
    mad: float
    mar: float
    low7q2: Optional[float]
    dry7q10: Optional[float]
    monthlyDischarges: List[float]
    monthlyDistributions: List[float]

    class Config:
        orm_mode = True
