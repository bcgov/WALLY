"""
Analysis functions for data in the Wally system
"""

import datetime
import geojson
import json
import os
from logging import getLogger
from fastapi import APIRouter, Depends, Query
from starlette.responses import Response
from sqlalchemy.orm import Session
from shapely.geometry import shape, MultiLineString, mapping, MultiPolygon, Point
from shapely.ops import cascaded_union


from api.db.utils import get_db

from api.v1.streams import controller as streams_controller
from api.v1.streams import schema as streams_schema

from external.docgen.controller import docgen_export_to_xlsx
logger = getLogger("streams")

router = APIRouter()


@router.get("/nearby", response_model=streams_schema.Streams)
def get_nearby_streams(
        db: Session = Depends(get_db),
        point: str = Query(...,
                           title="Point of interest",
                           description="Point of interest to centre search at"),
        limit: int = Query(10,
                           title="Limit",
                           description="Number of nearby streams to be returned"),
        get_all: bool = Query(False,
                              title="Get all",
                              description="Get all nearby streams, even if its apportionment is "
                                          "less than 10%"),
        with_apportionment: bool = Query(True,
                                         title="Include Apportionment",
                                         description="Get stream apportionment data"),
        weighting_factor: int = Query(2,
                                      title="Weighting factor",
                                      description="Weighting factor for calculating apportionment")
):
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    streams_nearby = streams_controller.get_streams_with_apportionment(
        db, point_shape, limit, get_all, with_apportionment, weighting_factor)

    return {
        'weighting_factor': weighting_factor,
        'streams': streams_nearby
    }


@router.post("/apportionment/export")
def export_stream_apportionment(
    req: streams_schema.ApportionmentExportRequest
):
    """ export a table of stream apportionment data, after the user
        has chosen a set of streams and parameters using the Wally UI.
    """

    req.generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur_date = datetime.datetime.now().strftime("%Y%m%d")

    filename = f"{cur_date}_HydraulicConnectivityAnalysis"

    dirname = os.path.dirname(__file__)
    xlsx_template = dirname + "/templates/StreamApportionment.xlsx"

    excel_file = docgen_export_to_xlsx(
        req, xlsx_template, filename)

    return Response(
        content=excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}.xlsx"}
    )


@router.get("/apportionment", response_model=streams_schema.Streams)
def get_streams_apportionment(
        db: Session = Depends(get_db),
        point: str = Query(...,
                           title="Point of interest",
                           description="Point of interest to centre search at"),
        ogc_fid: list = Query(..., title="A list of ogc_fid of streams",
                              description="A list of ogc_fid of streams"),
        weighting_factor: int = Query(
            2, title="Weighting factor", description="Weighting factor")
):
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)
    streams_by_ocg_fid = streams_controller.get_nearest_streams_by_ogc_fid(
        db, point_shape, ogc_fid)
    streams_with_apportionment = streams_controller.get_apportionment(
        streams_by_ocg_fid, weighting_factor)
    return {
        'weighting_factor': weighting_factor,
        'streams': streams_with_apportionment
    }


"""
Analysis functions for data in the Wally system
"""


@router.get('/features')
def get_streams_by_watershed_code(
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

    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    closest_segment = streams_controller.get_closest_stream_segment(db, point_shape)

    logger.warning(closest_segment)

    up_geom = streams_controller.get_upstream_area(
        db, closest_segment["linear_feature_id"], buffer, full_upstream_area)
    down_geom = streams_controller.get_downstream_area(
        db, closest_segment["linear_feature_id"], buffer)

    if not up_geom or not down_geom:
        return None

    up_geom_geojson = geojson.loads(up_geom[0]) if up_geom[0] else None
    down_geom_geojson = geojson.loads(down_geom[0]) if down_geom[0] else None

    if not up_geom_geojson and not down_geom_geojson:
        return None

    # calculate the junction between up and down streams
    # and return the buffered line segments
    junction_lines = streams_controller \
        .get_split_line_stream_buffers(db, closest_segment["linear_feature_id"], buffer, point_shape)

    # if either a up or down stream segment is not found,
    # it means we are at the last segment ie a final tributary
    # this means we can skip the union and just return the junction
    if not up_geom_geojson or not down_geom_geojson or \
            shape(up_geom_geojson).equals(shape(down_geom_geojson)):
        up_poly = junction_lines[-1]
        down_poly = junction_lines[0]
    else:
        up_shape = shape(up_geom_geojson)
        down_shape = shape(down_geom_geojson)
        # take only the largest polygon from any multi-polygons
        # this eliminates any error shapes that occasionally
        # popup in the freshwater atlas data
        up_poly = max(up_shape, key=lambda a: a.area) if \
            isinstance(up_shape, MultiPolygon) else up_shape
        down_poly = max(down_shape, key=lambda a: a.area) if \
            isinstance(down_shape, MultiPolygon) else down_shape
        # join the junction calculations with the existing up and down polys
        up_poly = cascaded_union([up_poly, junction_lines[-1]])
        # if we're at the bottom of a stream junction then set
        # the down_poly to be the down junction line, to avoid
        # an overlapping downstream result
        if closest_segment["downstream_route_measure"] == 0:
            down_poly = junction_lines[0]
        else:
            down_poly = cascaded_union([down_poly, junction_lines[0]])

    # remove overlapping geometry at the up/down stream junction point
    # the selected point will always be upstream from this junction
    # so we remove the intersecting geometry from the upstream poly
    # down_poly = down_poly.difference(junction_lines[-1])
    up_poly = up_poly.difference(down_poly)

    # if a layer was not specified, skip the feature collection
    if not layer:
        features_upstream = None
        features_downstream = None
    else:
        features_upstream = streams_controller. \
            get_features_within_buffer(db, up_poly, buffer, layer)
        features_downstream = streams_controller \
            .get_features_within_buffer(db, down_poly, buffer, layer)

    return {
        "gnis_name": closest_segment["gnis_name"],
        "upstream_features": features_upstream,
        "upstream_poly": mapping(up_poly),
        "downstream_features": features_downstream,
        "downstream_poly": mapping(down_poly)
    }


def get_features_within_buffer_zone(
        req: streams_schema.BufferRequest,
        db: Session = Depends(get_db)
):
    geometry_parsed = json.loads(req.geometry)

    lines = []
    for line in geometry_parsed:
        if line:
            lines.append(shape(line))

    multi_line_string = MultiLineString(lines)

    features = streams_controller.get_features_within_buffer(db, multi_line_string,
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
    streams = streams_controller.get_connected_streams(db, outflowCode)
    return streams
