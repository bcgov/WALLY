"""
API data models for FreshWater Stream Atlas analysis.
These are external facing data models/schemas that users see.
"""
from pydantic import BaseModel
from typing import List, Any, Optional
from geojson import Feature
from shapely.geometry import Point


class Stream(BaseModel):
    # search_point

    id: int
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
    inverse_distance: Optional[float]
    apportionment: Optional[float]


class Streams(BaseModel):
    weighting_factor: int

    streams: List[Stream]


class StreamDetailsExport(BaseModel):
    """ details about an apportioned link
    to a single stream for the purpose of exporting data."""

    gnis_name: Optional[str]
    linear_feature_id: Optional[int]
    distance: float
    length_metre: float
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

    encodingType: str
    content: str  # base64 encoded
    fileType: str


class ApportionmentDocGenOptions(BaseModel):
    """ options for docgen requests """
    reportName: str
    overwrite: str = "true"


class ApportionmentDocGenRequest(BaseModel):
    """ the request body for making document generator requests """

    data: dict
    template: dict
    options: dict = {}


class StreamPoint(BaseModel):
    """a point on a stream along with the stream_feature_id associated with it.
    """
    stream_point: Point
    stream_feature_id: int

    class Config:
        arbitrary_types_allowed = True


class _FreshWaterAtlasStreamNetworks(BaseModel):
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
