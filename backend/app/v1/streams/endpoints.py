"""
Analysis functions for data in the Wally system
"""
import json
from logging import getLogger
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.db.utils import get_db

from app.v1.streams import controller as stream_controller
from app.v1.streams import schema as stream_schema
logger = getLogger("streams")

router = APIRouter()


@router.get("/nearby", response_model=stream_schema.Streams)
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

    streams_nearby = stream_controller.get_streams_with_apportionment(
        db, point_shape, limit, get_all, with_apportionment, weighting_factor)

    return {
        'weighting_factor': weighting_factor,
        'streams': streams_nearby
    }


@router.get("/apportionment", response_model=stream_schema.Streams)
def get_streams_apportionment(
        db: Session = Depends(get_db),
        point: str = Query(...,
                           title="Point of interest",
                           description="Point of interest to centre search at"),
        ogc_fid: list = Query(..., title="A list of ogc_fid of streams",
                              description="A list of ogc_fid of streams"),
        weighting_factor: int = Query(2, title="Weighting factor", description="Weighting factor")
):
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)
    streams_by_ocg_fid = stream_controller.get_nearest_streams_by_ogc_fid(db, point_shape, ogc_fid)
    streams_with_apportionment = stream_controller.get_apportionment(streams_by_ocg_fid, weighting_factor)
    return {
        'weighting_factor': weighting_factor,
        'streams': streams_with_apportionment
    }

