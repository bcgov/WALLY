import math
import json
import pyproj
from geojson import dumps, FeatureCollection, Feature, Point
from shapely.geometry import mapping

from api.config import GWELLS_API_URL
from api.v1.aggregator.schema import ExternalAPIRequest, GWELLSAPIParams, json_to_geojson

EARTH_RADIUS = 6378137
MAX_LATITUDE = 85.0511287798

transform_4326_3005 = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:4326'),
    pyproj.Proj(init='epsg:3005')
).transform

transform_3005_4326 = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:3005'),
    pyproj.Proj(init='epsg:4326')
).transform

transform_4326_4140 = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:4326'),
    pyproj.Proj(init='epsg:4140')
).transform

transform_4140_4326 = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:4140'),
    pyproj.Proj(init='epsg:4326')
).transform

# Converts to x,y point array from lat lng
def spherical_mercator_project(lat, lng):
    d = math.pi / 180
    lat = max(min(MAX_LATITUDE, lat), -MAX_LATITUDE)
    sin = math.sin(lat * d)
    return [EARTH_RADIUS * math.log((1 + sin) / (1 - sin)) / 2, EARTH_RADIUS * lng * d]


# Converts to lat,lng array from point
def spherical_mercator_unproject(x, y):
    d = 180 / math.pi
    return [(2 * math.atan(math.exp(y / EARTH_RADIUS)) - (math.pi / 2)) * d, x * d / EARTH_RADIUS]


def gwells_api_request(within):
    """
    creates an ExternalAPIRequest object with params for accessing data from the
    GWELLS API.
    """
    url = f"{GWELLS_API_URL}/api/v2/wells"
    params = GWELLSAPIParams(
        within=json.dumps(mapping(within)),
        geojson="false"
    )

    return ExternalAPIRequest(
        url=url,
        layer="groundwater_wells",
        excluded_fields=["well_guid", "drilling_company"],
        id_field="well_tag_number",
        q=params
    )
