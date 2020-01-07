"""
API data models for Water Rights Licence analysis.
These are external facing data models/schemas that users see.
"""
from typing import Optional

from pydantic import BaseModel


class FreshWaterAtlasStreamNetworks(BaseModel):
    distance: float
    LICENCE_NUMBER: Optional[str]
    LICENCE_STATUS: Optional[str]
    POD_NUMBER: Optional[str]
    POD_SUBTYPE: Optional[str]
    PURPOSE_USE: Optional[str]
    SOURCE_NAME: Optional[str]
    QUANTITY: Optional[float]
    QUANTITY_UNITS: Optional[str]
    QTY_DIVERSION_MAX_RATE: Optional[float]
    QTY_UNITS_DIVERSION_MAX_RATE: Optional[str]
    QUANTITY_FLAG: Optional[str]
    QUANTITY_FLAG_DESCRIPTION: Optional[str]

    class Config:
        orm_mode = True


class BufferRequest(BaseModel):
    geometry: str
    buffer: float
    layer: str
