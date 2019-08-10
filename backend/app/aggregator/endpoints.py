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

    # format the bounding box (which arrives in the querystring as a comma separated list)
    bbox_string = ','.join(str(v) for v in bbox)

    # compare requested layers against layers we keep track of.  The valid WMS layers and their
    # respective WMS endpoints will come from our metadata.
    valid_layers = get_wms_layers(layers)

    wms_requests = []

    # create a WMSRequest object with all the values we need to make WMS requests for each of the
    # layers that we have metadata for.
    for layer in valid_layers:
        query = WMSGetMapQuery(
            layers=layer["id"],
            bbox=bbox_string,
            width=width,
            height=height,
        )
        req = WMSRequest(
            url=layer["api_url"],
            layer=layer["id"],
            q=query
        )
        wms_requests.append(req)

    # go and fetch features for each of the WMS endpoints we need to hit, and make a FeatureCollection
    # out of all the aggregated features.
    return fetch_wms_features(wms_requests)
