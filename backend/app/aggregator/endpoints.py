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
from app.aggregator.db import get_wms_layers
from app.aggregator.aggregate import fetch_wms_features
from app.aggregator.models import WMSGetMapQuery, WMSRequest

logger = getLogger("aggregator")

router = APIRouter()

# data access functions are available for certain layers.
# if a function is not available here, default to using
# the web API listed with the layer metadata.
API_DATASOURCES = {
    "HYDAT": streams_repo.get_stations
}

ONE_LAYER = {
    "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?",
    "request": "GetMap",
    "service": "WMS",
    "srs": "EPSG%3A4326",
    "version": "1.1.1",
    "format": "application/json%3Btype%3Dtopojson",
    "bbox": "-125.99807739257814,53.86062638824399,-125.46661376953126,54.10893027534094",
    "height": "1243",
    "width": "1445",
    "layers": "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
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
            min_length=4, max_length=4),
        x: float = Query(None, title="Longitude", description="Longitude at point of interest"),
        y: float = Query(None, title="Latitude", description="Latitude at point of interest"),
        width: float = Query(..., title="Width", description="Width of area of interest"),
        height: float = Query(..., title="Height",
                              description="Height of area of interest")
):
    """
    Generate a list of features from a variety of sources and map layers (specified by `layers`)
    inside the map bounds defined by `bbox`.
    """

    valid_layers = get_wms_layers(layers)
    bbox_string = ','.join(str(v) for v in bbox)

    wms_requests = []

    for layer in valid_layers:
        query = WMSGetMapQuery(
            layers=layer["id"],
            bbox=bbox_string,
            width=width,
            height=height,
        )
        req = WMSRequest(
            url=layer["api_url"],
            q=query
        )
        wms_requests.append(req)

    logger.info("prepared requests")

    wms_features = fetch_wms_features(wms_requests)

    fc = FeatureCollection(wms_features)

    logger.info("fetched features")

    return fc
