"""
API data models for Projects.
"""
from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List
from shapely import wkt
from shapely.errors import WKTReadingError
from api.constants import FEATURE_TYPES
from uuid import UUID


class SavedAnalysisMapLayer(BaseModel):
    map_layer: Optional[str]

    class Config:
        orm_mode = True


class SavedAnalysisBase(BaseModel):
    name: str
    description: Optional[str]
    geometry: str
    feature_type: str
    zoom_level: str
    map_layers: Optional[List[SavedAnalysisMapLayer]]

    class Config:
        orm_mode = True


class SavedAnalysisGet(SavedAnalysisBase):
    saved_analysis_uuid: UUID


class SavedAnalysisCreateUpdate(SavedAnalysisBase):
    map_layers: Optional[List[str]]

    @validator('geometry')
    def geometry_wkt(cls, v):
        try:
            geom = wkt.loads(v)
        except WKTReadingError:
            raise ValueError('Invalid geometry')
        return v

    @validator('feature_type')
    def feature_type_valid(cls, v):

        if v not in FEATURE_TYPES:
            raise ValueError('Invalid feature type')

        return v
