"""
Analysis functions for data in the Wally system
"""
import base64
import datetime
import json
import requests
from logging import getLogger
from fastapi import APIRouter, Depends, Query, HTTPException
from starlette.responses import Response
from sqlalchemy.orm import Session
from shapely.geometry import Point

from external.docgen.schema import DocGenRequest, DocGenTemplateFile
from external.docgen.request_token import get_docgen_token
from api import config
from api.db.utils import get_db

from api.v1.streams import controller as streams_controller
from api.v1.streams import schema as streams_schema
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
    template_data = open(
        "./api/v1/streams/templates/StreamApportionment.xlsx", "rb").read()
    base64_encoded = base64.b64encode(template_data).decode("UTF-8")
    filename = f"{cur_date}_StreamApportionment"
    token = get_docgen_token()
    auth_header = f"Bearer {token}"

    body = streams_schema.ApportionmentDocGenRequest(
        data=req,
        options=streams_schema.ApportionmentDocGenOptions(
            reportName=filename
        ).dict(),
        template=streams_schema.ApportionmentTemplateFile(
            encodingType="base64",
            content=base64_encoded,
            fileType="xlsx"
        ).dict()
    )

    logger.info('making POST request to common docgen: %s',
                "https://cdogs-master-idcqvl-dev.pathfinder.gov.bc.ca/api/v2/template/render")

    try:
        res = requests.post("https://cdogs-master-idcqvl-dev.pathfinder.gov.bc.ca/api/v2/template/render", json=body.dict(), headers={
                            "Authorization": auth_header, "Content-Type": "application/json"})
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.info(e)
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return Response(
        content=res.content,
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
