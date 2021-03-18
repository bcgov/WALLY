"""
API data models for User Profile.
"""
from pydantic import BaseModel
from typing import List, Any, Optional
from geojson import Feature


class UpdateMapLayers(BaseModel):
    map_layers: Optional[List[str]]
