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
    buffer: float = Query(
        100,
        title="Buffer radius (m)",
        description="Distance (in metres) from the stream to search within",
        lte=500,
        gte=0),
    layer: str = Query(
        None,
        title="Layer to search",
        description="The name of the layer to search. Points that are within `buffer` metres of the specified stream will be returned."),
    db: Session = Depends(get_db)
):
    """ generates a stream network based on a FWA_WATERSHED_CODE and
    LINEAR_FEATURE_ID, and finds features from a given `layer`. """

    # Remove trailing 000000 codes (zero codes). This allows us to look up streams
    # that branch off the subject stream (if they are tributaries of
    # the subject stream, at least one of the trailing 000000 code segments will
    # contain a non-zero value).
    # There is an assumption made that no watershed codes have
    # non-zero values to the right of a zero value.
    root_code = stream_controller.watershed_root_code(code)

    # add a wildcard for searching
    root_code.append('%')
    root_code = '-'.join(root_code)

    # Gather up the selected stream segments (from the stream's own headwaters
    # down to the mouth of the stream where it drains into the next river),
    # as well as all *upstream* tributary networks from the selected reach.
    # This represents the entire drainage network upstream of the selected
    # reach, combined with just the stream's own geometry downstream (no
    # tributaries downstream of the selected reach are included).
    #
    # this query works by inspecting the last non-zero code of the local
    # watershed code, which roughly represents the percent distance along the
    # stream of each segment of the stream.
    q = """
    with watershed_code_stats as (
        SELECT
            "LOCAL_WATERSHED_CODE" as loc_code,
            (FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1)::int
                as loc_code_last_nonzero_code
        FROM freshwater_atlas_stream_networks
        WHERE   "LINEAR_FEATURE_ID" = :linear_feature_id
    )
    select
        ST_AsGeoJSON(
            ST_Transform(
                ST_Buffer(
                    ST_Transform(ST_Union("GEOMETRY"), 3005),
                    :buffer, 'endcap=round join=round'
                ),
                4326
            )
        )
    from    (
        select  "GEOMETRY" from freshwater_atlas_stream_networks
        where   "FWA_WATERSHED_CODE" = :code
        union all
        select  "GEOMETRY" from freshwater_atlas_stream_networks, watershed_code_stats
        where   "FWA_WATERSHED_CODE" like :root_code
        AND     split_part(
                    "FWA_WATERSHED_CODE", '-',
                    watershed_code_stats.loc_code_last_nonzero_code
                )::int > split_part(
                    watershed_code_stats.loc_code, '-',
                    watershed_code_stats.loc_code_last_nonzero_code
                )::int
    ) subq
    """

    geom = db.execute(
        q,
        {
            "code": code,
            "root_code": root_code,
            "linear_feature_id": linear_feature_id,
            "buffer": buffer
        }).fetchone()

    if not geom:
        return None

    geom_geojson = geojson.loads(geom[0])

    # if a layer was not specified, return the unioned stream network that we generated.
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
