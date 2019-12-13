"""
API models and response schemas for aggregating data from WMS and API sources
"""
from typing import List, Optional
from pydantic import BaseModel
from geojson import Feature, FeatureCollection
from asyncio import Future


class GeocoderResponse(BaseModel):
    pass
