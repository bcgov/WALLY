"""
API models and response schemas for aggregating data from WMS and API sources
"""
from typing import List, Optional
from pydantic import BaseModel
from geojson import Feature, FeatureCollection
from asyncio import Future


class WMSGetMapQuery(BaseModel):
    """ query params needed to make a WMS feature request """
    bbox: str
    width: int
    height: int
    service: str = "WMS"
    request: str = "GetMap"
    srs: str = "EPSG:3857"
    version: str = "1.1.1"
    format: str = "application/json;type=geojson"
    layers: str


class WMSGetFeatureInfoQuery(BaseModel):
    """ query params needed to make a WMS feature request """
    bbox: str
    x: int
    y: int
    width: int
    height: int
    service: str = "WMS"
    request: str = "GetFeatureInfo"
    srs: str = "EPSG:4326"
    version: str = "1.1.1"
    format: str = "application/json;type=geojson"
    layers: str


class WMSRequest(BaseModel):
    """ a WMS feature request """
    url: str
    layer: str
    q: WMSGetMapQuery


class LayerResponse(BaseModel):
    """ contains info about and data from a response from a WMS GetMap or GetFeatureInfo request """
    layer: str

    # HTTP status code from the request.
    # The status code could be 0 if the request could not be made.
    status: int = 0
    geojson: FeatureCollection

    class Config:
        arbitrary_types_allowed = True
