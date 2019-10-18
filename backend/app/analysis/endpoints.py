"""
Analysis functions for data in the Wally system
"""
import json
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.db.utils import get_db
from app.analysis.wells.well_analysis import get_wells_by_distance
logger = getLogger("geocoder")

router = APIRouter()


@router.get("/analysis/wells/nearby")
def geocode_lookup(
    db: Session = Depends(get_db),
    point: str = Query(..., title="Point of interest",
                       description="Point of interest to centre search at"),
    radius: float = Query(1000, title="Search radius",
                          description="Search radius from point", ge=0, le=10000)
):
    """ finds wells near to a point """

    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    return get_wells_by_distance(db, point_shape, radius)
