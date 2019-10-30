"""
Analysis functions for data in the Wally system
"""
import json
from typing import List
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.db.utils import get_db
from app.analysis.wells.well_analysis import get_wells_by_distance, with_drawdown, merge_wells_datasources, get_screens
from app.analysis.licences.licence_analysis import get_licences_by_distance
from app.analysis.wells.models import WellDrawdown
from app.analysis.licences.models import WaterRightsLicence
logger = getLogger("geocoder")

router = APIRouter()


@router.get("/analysis/wells/nearby", response_model=List[WellDrawdown])
def get_nearby_wells(
    db: Session = Depends(get_db),
    point: str = Query(..., title="Point of interest",
                       description="Point of interest to centre search at"),
    radius: float = Query(1000, title="Search radius",
                          description="Search radius from point", ge=0, le=10000)
):
    """ finds wells near to a point
        fetches distance data using the Wally database, and combines
        it with screen data from GWELLS
    """

    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    wells_with_distances = get_wells_by_distance(db, point_shape, radius)

    # convert nearby wells to a list of strings of well tag numbers
    wells_to_search = map(lambda x: str(
        int(x[0])).lstrip("0"), wells_with_distances)

    wells_with_screens = get_screens(list(wells_to_search))

    wells_drawdown_data = merge_wells_datasources(
        wells_with_screens, wells_with_distances)

    return wells_drawdown_data


@router.get("/analysis/licences/nearby", response_model=List[WaterRightsLicence])
def get_nearby_licences(
    db: Session = Depends(get_db),
    point: str = Query(..., title="Point of interest",
                       description="Point of interest to centre search at"),
    radius: float = Query(1000, title="Search radius",
                          description="Search radius from point", ge=0, le=10000)
):
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    licences_with_distances = get_licences_by_distance(db, point_shape, radius)
    return licences_with_distances
