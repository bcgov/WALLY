"""
Analysis functions for data in the Wally system
"""
import json
from logging import getLogger
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from api.v1.models.scsb2016.controller import calculate_mean_annual_runoff
from shapely.geometry import Polygon, MultiPolygon, shape
from shapely.ops import transform
from api.db.utils import get_db

logger = getLogger("isolines")

router = APIRouter()

# test endpoint for validating the scsb2016 implementation
@router.get("/test")
def get_scsb2016_values(
        hydrological_zone: int,
        median_elevation: float,
        glacial_coverage: float,
        annual_precipitation: float,
        evapo_transpiration: float,
        drainage_area: float,
        solar_exposure: float,
        average_slope: float,
        db: Session = Depends(get_db),
):

    result = calculate_mean_annual_runoff(db, hydrological_zone, median_elevation, \
        glacial_coverage, annual_precipitation, evapo_transpiration, \
        drainage_area, solar_exposure, average_slope)

    return { "result": result }
