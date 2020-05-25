"""
Analysis functions for data in the Wally system
"""
import json
from typing import List
from logging import getLogger
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from shapely.geometry import Point
from shapely.ops import transform
from api.db.utils import get_db
from api.v1.aggregator.helpers import transform_4326_3005
from api.v1.licences.controller import (
    get_surface_water_approval_points_databc,
    get_licences_by_distance_databc,
    get_applications_by_distance_databc
)
from api.v1.licences.schema import WaterRightsLicence, LicenceApplicationApproval


logger = getLogger("geocoder")

router = APIRouter()


@router.get("/nearby", response_model=List[LicenceApplicationApproval])
def get_nearby_licences(
        db: Session = Depends(get_db),
        point: str = Query(..., title="Point of interest",
                           description="Point of interest to centre search at"),
        radius: float = Query(1000, title="Search radius",
                              description="Search radius from point", ge=0, le=10000)
):
    point_parsed = json.loads(point)
    point_shape = transform(transform_4326_3005, Point(point_parsed))

    licences_with_distances = get_licences_by_distance_databc(point_shape, radius) + \
        get_applications_by_distance_databc(point_shape, radius) + \
        get_surface_water_approval_points_databc(point_shape, radius)

    return sorted([LicenceApplicationApproval(**(item.properties)) for item in licences_with_distances], key=lambda x: x.distance)
