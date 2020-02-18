"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
import json
import geojson
from geojson import FeatureCollection, Feature
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from shapely.geometry import shape, MultiPolygon, Polygon, Point
from shapely.ops import transform
from api.db.utils import get_db
from api.v1.marmodel.controller import calculate_mean_annual_runoff


logger = getLogger("marmodel")

router = APIRouter()


@router.get('/')
def get_mean_annual_runoff(
        zone: int,
        db: Session = Depends(get_db),
        polygon: str = Query(
            "", title="Watershed polygon",
            description="Watershed polygon to search within"
        )
):
    if not polygon:
        raise HTTPException(
            status_code=400, detail="No search bounds. Supply a `polygon` (geojson geometry)")

    if not zone:
        raise HTTPException(
            status_code=400, detail="No hydrological zone. Supply a zone id (int)")

    if polygon:
        poly_parsed = json.loads(polygon)
        polygon = MultiPolygon([Polygon(x) for x in poly_parsed])

    if polygon.area <= 0:
        raise HTTPException(
            status_code=400, detail="Polygon has zero area")
    
    model_results = calculate_mean_annual_runoff(db, polygon, zone)

    return model_results