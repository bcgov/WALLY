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
from api.v1.marmodel.controller import calculate_mean_annual_runoff, get_hydrological_zone
from api.v1.watersheds.controller import get_watershed

logger = getLogger("marmodel")

router = APIRouter()


@router.get('/{watershed_feature}')
def get_mean_annual_runoff(
        watershed_feature: str,
        db: Session = Depends(get_db)
):

    watershed = get_watershed(db, watershed_feature)

    if not watershed:
        raise HTTPException(
            status_code=400, detail="No watershed found. Supply a proper id.")

    watershed_poly = shape(watershed.geometry)

    hydrological_zone = get_hydrological_zone(watershed_poly.centroid)

    if not hydrological_zone:
        raise HTTPException(
            status_code=400, detail="Watershed not within hydrological zone that we support analysis for.")
    
    model_results = calculate_mean_annual_runoff(db, watershed_poly, hydrological_zone)

    return model_results


@router.get('/by_polygon')
def get_mean_annual_runoff_by_polygon(
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