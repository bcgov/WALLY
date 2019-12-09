from pydantic import BaseModel
from typing import List


class Stream(BaseModel):
    # search_point

    ogc_fid: int
    length_metre: float
    feature_source: str
    gnis_name: str
    left_right_tributary: str
    geometry_length: str
    geometry: str
    watershed_group_code: str
    distance_degrees: float
    distance: float

    closest_stream_point: str
    inverse_distance: float
    apportionment: float


class Streams(BaseModel):
    search_point: str
    limit: int
    get_all: bool
    with_apportionment: bool
    weighting_factor: int

    streams: List[Stream]
