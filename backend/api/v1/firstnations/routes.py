import json
from logging import getLogger
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from shapely.geometry import shape

from api.db.utils import get_db
from api.v1.firstnations.controller import get_nearest_locations
from api.v1.firstnations.schema import NearbyAreasResponse

logger = getLogger("firstnations")

router = APIRouter()


@router.get("/nearby", response_model=NearbyAreasResponse)
def get_nearby_first_nations_areas(
        db: Session = Depends(get_db),
        geometry: str = Query(...,
                              title="Geometry to search near",
                              description="Geometry (such as a point or polygon) to search within "
                                          "and near to")
):
    """
    Search for First Nations Communities, First Nations Treaty Areas and First Nations Treaty Lands
    near a feature
    """
    geometry_parsed = json.loads(geometry)
    geometry_shape = shape(geometry_parsed)
    nearest = get_nearest_locations(db, geometry_shape)
    return nearest
