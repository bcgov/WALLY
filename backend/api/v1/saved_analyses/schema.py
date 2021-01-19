"""
API data models for Projects.
"""
from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List
from shapely import wkt
from shapely.errors import WKTReadingError


class SavedAnalysisMapLayer(BaseModel):
    map_layer: Optional[str]


class SavedAnalysis(BaseModel):
    name: Optional[str]
    description: Optional[str]
    geometry: Optional[str]
    feature_type: Optional[str]
    zoom_level: Optional[int]
    map_layers: Optional[List[str]]

    @validator('geometry')
    def geometry_wkt(cls, v):
        try:
            geom = wkt.loads(v)
        except WKTReadingError:
            raise ValueError('Invalid geometry')
        return v

# class SavedAnalysi
