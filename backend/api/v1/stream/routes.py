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
from shapely.geometry import shape, MultiLineString, mapping, MultiPolygon, Point
from shapely.ops import transform, cascaded_union
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
    point: str = Query(...,
        title="Point of interest",
        description="Point of interest close to stream."),
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


    up_geom_geojson = geojson.loads(up_geom[0]) if up_geom[0] else None
    down_geom_geojson = geojson.loads(down_geom[0]) if down_geom[0] else None

    up_shape = shape(up_geom_geojson)
    down_shape = shape(down_geom_geojson)

    # take only the largest polygon from any multi-polygons
    # this eliminates any error shapes that occasionally
    # popup in the freshwater atlas data
    up_poly = max(up_shape, key=lambda a: a.area) if \
      isinstance(up_shape, MultiPolygon) else up_shape
    down_poly = max(down_shape, key=lambda a: a.area) if \
      isinstance(down_shape, MultiPolygon) else down_shape

    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    # calculate the junction between up and down streams
    # and return the buffered line segments
    junction_lines = stream_controller \
      .get_split_line_stream_buffers(db, linear_feature_id, buffer, point_shape)

    # join the junction calculations with the existing up and down polys
    up_poly = cascaded_union([up_poly, junction_lines[-1]])
    down_poly = cascaded_union([down_poly, junction_lines[0]])

    # remove overlapping geometry at the up/down stream junction point
    # the selected point will always be upstream from this junction
    # so we remove the intersecting geometry from the upstream poly
    # down_poly = down_poly.difference(junction_lines[-1])
    up_poly = up_poly.difference(down_poly)

    # if a layer was not specified, return the stream network polys that we generated.
    if not layer:
        return {
            "upstream": mapping(up_poly),
            "downstream": mapping(down_poly)
        }

    features_upstream = stream_controller. \
      get_features_within_buffer(db, up_poly, buffer, layer)
    features_downstream = stream_controller \
      .get_features_within_buffer(db, down_poly, buffer, layer)

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
