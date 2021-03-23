"""
API data models for Projects.
"""
from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List, Any

from shapely import wkt
from shapely.errors import WKTReadingError
from api.constants import FEATURE_TYPES
from uuid import UUID
import json
from shapely.geometry import shape


class SavedAnalysisMapLayer(BaseModel):
    map_layer: str

    class Config:
        orm_mode = True


class SavedAnalysisBase(BaseModel):
    name: str
    description: Optional[str]
    geometry: dict
    feature_type: str
    zoom_level: float
    map_bounds: List[List[float]]
    map_layers: List[SavedAnalysisMapLayer]

    class Config:
        orm_mode = True


class SavedAnalysisGet(SavedAnalysisBase):
    saved_analysis_uuid: UUID

    class Config:
        orm_mode = True


class SavedAnalysisCreateUpdate(SavedAnalysisBase):
    @validator('geometry')
    def geometry_wkt(cls, v):
        # Validate and convert a geojson geometry object to WKT
        # because geoalchemy2.Geometry accepts a WKT input and converts it into a geom
        try:
            shp = shape(v)
        except Exception:
            raise ValueError('Invalid geometry')
        return shp.wkt

    @validator('feature_type')
    def feature_type_valid(cls, v):

        if v not in FEATURE_TYPES:
            raise ValueError('Invalid feature type')

        return v


class SavedAnalysisUpdate(BaseModel):
    name: str
    description: str
    # TODO design UX on how to edit the following features
    # geometry: Optional[dict]
    # feature_type: Optional[str]
    # zoom_level: Optional[float]
    # map_layers: Optional[List[str]]

