from pydantic import BaseModel
from typing import List, Any


class Stream(BaseModel):
    # search_point

    ogc_fid: int
    length_metre: Any
    feature_source: Any
    gnis_name: Any
    left_right_tributary: Any
    geometry_length: Any
    geometry: str
    watershed_group_code: str
    distance_degrees: float
    distance: float

    closest_stream_point: str
    inverse_distance: float
    apportionment: float


class Streams(BaseModel):
    weighting_factor: int

    streams: List[Stream]
