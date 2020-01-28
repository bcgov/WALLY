"""
API data models for Isoline Runoff.
"""
from typing import Optional
from pydantic import BaseModel


class IsolineRunoff(BaseModel):
    """
    Normal annual runoff isolines estimate the rainfall in different hydrological zones of BC.
    """

    id: int
    ANNUAL_RUNOFF_IN_MM: int

    class Config:
        orm_mode = True
