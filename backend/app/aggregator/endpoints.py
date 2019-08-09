"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.hydat.db as streams_repo
import app.hydat.models as streams_v1

logger = getLogger("api")

router = APIRouter()

# data access functions are available for certain layers.
# if a function is not available here, default to using
# the web API listed with the layer metadata.
API_DATASOURCES = {
    "HYDAT": streams_repo.get_stations
}


@router.get("/aggregate")
def aggregate_sources(
    layers: List[str] = Query(
        ..., title="Layers to search",
        description="Search for features in a given area for each of the specified layers.",
        min_length=1
    ),
    bbox: List[float] = Query(
        ..., title="Bounding box",
        description="Bounding box to constrain search, in format x1,y1,x2,y2.",
        min_length=4, max_length=4)
):
    """
    Generate a list of features from a variety of sources and map layers (specified by `layers`)
    inside the map bounds defined by `bbox`.
    """
    pass
