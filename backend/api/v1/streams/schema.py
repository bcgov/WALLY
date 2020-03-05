"""
API data models for FreshWater Stream Atlas analysis.
These are external facing data models/schemas that users see.
"""
from pydantic import BaseModel
from typing import List, Any, Optional
from geojson import Feature


class Stream(BaseModel):
    # search_point

    ogc_fid: int
    geojson: Feature
    linear_feature_id: Optional[int]
    length_metre: Any
    feature_source: Any
    gnis_name: Any
    left_right_tributary: Any
    geometry_length: Any
    # geometry: str
    watershed_group_code: str
    fwa_watershed_code: str
    distance_degrees: float
    distance: float

    closest_stream_point: Any
    inverse_distance: float
    apportionment: float


class Streams(BaseModel):
    weighting_factor: int

    streams: List[Stream]


class StreamDetailsExport(BaseModel):
    """ details about an apportioned link
    to a single stream for the purpose of exporting data."""

    gnis_name: Optional[str]
    linear_feature_id: Optional[int]
    distance: float
    apportionment: float


class ApportionmentExportRequest(BaseModel):
    """ the data required to export stream apportionment data,
    after the user has applied their own adjustments """

    streams: List[StreamDetailsExport]
    point: List[float]
    generated: Optional[str]
    weighting_factor: float


class ApportionmentTemplateFile(BaseModel):
    """ the metadata and encoded file for
        a stream apportionment excel template.
        This is the format required by the Common Services
        Document Generator.
    """

    filename: str
    contentEncodingType: str
    content: str  # base64 encoded


class ApportionmentDocGenRequest(BaseModel):
    """ the request body for making document generator requests """

    contexts: List[ApportionmentExportRequest]
    template: ApportionmentTemplateFile
