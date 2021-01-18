"""
API data models for Projects.
"""
from pydantic import BaseModel
from typing import Optional


class SavedAnalysisMapLayer(BaseModel):
    map_layer: Optional[str]


class SavedAnalysis(BaseModel):
    name: Optional[str]
    description: Optional[str]
    geometry: Optional[str]
    feature_type: Optional[str]
    zoom_level: Optional[int]
    map_layers: Optional[SavedAnalysisMapLayer]
