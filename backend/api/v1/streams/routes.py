"""
Analysis functions for data in the Wally system
"""
import datetime
import json
from logging import getLogger
from fastapi import APIRouter, Depends, Query
from starlette.responses import Response
from sqlalchemy.orm import Session
from shapely.geometry import Point

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
    xlsx_template = dirname + "templates/StreamApportionment.xlsx"

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
