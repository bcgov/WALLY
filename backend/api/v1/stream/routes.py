"""
Analysis functions for data in the Wally system
"""
import json
import geojson
from geojson import Feature
from logging import getLogger
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import shape, MultiLineString, mapping
from shapely.ops import transform
from api.db.utils import get_db

from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.v1.stream import controller as stream_controller
from api.v1.stream import schema as stream_schema
from api.v1.aggregator.controller import fetch_geojson_features
from api.v1.aggregator.schema import WMSGetMapQuery, WMSGetFeatureQuery, ExternalAPIRequest
from api.v1.aggregator.helpers import transform_3005_4326, transform_4326_3005

logger = getLogger("stream")

router = APIRouter()


@router.get('/features')
def get_streams_by_watershed_code(
    linear_feature_id: int,
    code: str,
    buffer: int = Query(
        100,
        title="Buffer radius (m)",
        description="Distance (in metres) from the stream to search within"),
    layer: str = Query(
        None,
        title="Layer to search",
        description="The name of the layer to search. Points that are within `buffer` metres of the specified stream will be returned."),
    db: Session = Depends(get_db)
):
    """ generates a stream network based on a watershed code, and finds features from a given `layer`. """

    # Remove trailing 000000 codes (zero codes). This allows us to look up streams
    # that branch off the subject stream (if they are tributaries of
    # the subject stream, at least one of the trailing 000000 code segments will
    # contain a non-zero value).
    # There is an assumption made that no watershed codes have
    # non-zero values to the right of a zero value.
    code_parsed = [x for x in code.split('-') if x != '000000']
    code_parsed.append('%')
    code_parsed = '-'.join(code_parsed)

    # with start_elev as (
    #     select  st_zmax("GEOMETRY") as zmax, "LOCAL_WATERSHED_CODE" as loc_code
    #     from    freshwater_atlas_stream_networks
    #     where   "LINEAR_FEATURE_ID" = :linear_feature_id
    # )
    # select  "GEOMETRY"
    # from    freshwater_atlas_stream_networks, start_elev
    # where   "FWA_WATERSHED_CODE" ilike :code_parsed
    # and     ST_ZMax("GEOMETRY") > start_elev.zmax
    # union all

    q = """
    

    select  ST_AsGeoJSON(ST_Union("GEOMETRY"))
    from    freshwater_atlas_stream_networks
    where "FWA_WATERSHED_CODE" = :code
    
    """

    # q = db \
    #     .query(func.ST_AsGeoJSON(func.ST_Union(FreshwaterAtlasStreamNetworks.GEOMETRY))
    #            .label('geom')) \
    #     .filter(FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.ilike(f"{code_parsed}%"))

    geom = db.execute(q, {"code": code, "code_parsed": code_parsed, "linear_feature_id": linear_feature_id}).fetchone()

    if not geom:
        return None

    geom_geojson = geojson.loads(geom[0])

    if not layer:
        return geom_geojson

    stream_shape = shape(geom_geojson)

    return stream_controller.get_features_within_buffer(db, stream_shape,
                                                        100, layer)


def get_features_within_buffer_zone(
        req: stream_schema.BufferRequest,
        db: Session = Depends(get_db)
):
    geometry_parsed = json.loads(req.geometry)

    lines = []
    for line in geometry_parsed:
        if line:
            lines.append(shape(line))

    multi_line_string = MultiLineString(lines)

    features = stream_controller.get_features_within_buffer(db, multi_line_string,
                                                            req.buffer, req.layer)
    return features


@router.get("/connections")
def get_stream_connections(
        db: Session = Depends(get_db),
        outflowCode: str = Query(
            ...,
            title="The base outflow stream code",
            description="The code that identifies the base outflow river to ocean"),
):
    streams = stream_controller.get_connected_streams(db, outflowCode)
    return streams
