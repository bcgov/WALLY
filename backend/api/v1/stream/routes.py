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
    full_upstream_area: bool = Query(
        None,
        title="Search full upstream area",
        description="Indicates that the search should use the full upstream area, instead of only searching within a stream buffer. This is faster."),
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

    up_geom = stream_controller.get_upstream_area(
        db, linear_feature_id, buffer, full_upstream_area)
    down_geom = stream_controller.get_downstream_area(
      db, linear_feature_id, buffer)

    if not up_geom or not down_geom:
        return None
    
    logger.warn("*** up_geom ***")
    logger.warn(up_geom)
    logger.warn("*** down_geom ***")
    logger.warn(down_geom)

    up_geom_geojson = geojson.loads(up_geom[0]) if up_geom[0] else ""
    down_geom_geojson = geojson.loads(down_geom[0]) if down_geom[0] else ""

    # if a layer was not specified, return the unioned stream network that we generated.
    if not layer:
        return {
          "upstream": up_geom_geojson,
          "downstream": down_geom_geojson
        }

    upstream_shape = shape(up_geom_geojson)
    downstream_shape = shape(down_geom_geojson)

    features_upstream = stream_controller.get_features_within_buffer(db, upstream_shape,
                                                        buffer, layer)
    features_downstream = stream_controller.get_features_within_buffer(db, downstream_shape,
                                                        buffer, layer)

    return {
      "upstream": features_upstream,
      "downstream": features_downstream
    }


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
