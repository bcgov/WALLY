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
import app.aggregator.db as agr_repo
from app.aggregator.aggregate import fetch_wms_features
from app.aggregator.models import WMSGetMapQuery, WMSGetFeatureInfoQuery, WMSRequest, LayerResponse
from app.templating.template_builder import build_templates

logger = getLogger("aggregator")

router = APIRouter()

# Data access functions are available for certain layers.
# if a function is not available here, default to using
# the web API listed with the layer metadata.
# These functions must accept a db session and a bbox as a list of coords
# (defined by 2 corners, e.g. x1, y1, x2, y2) and return a FeatureCollection.
# For example:  get_stations_as_geojson(db: Session, bbox: List[float])
API_DATASOURCES = {
    "HYDAT": streams_repo.get_stations_as_geojson
}


@router.get("/aggregate")
def aggregate_sources(
        db: Session = Depends(get_db),
        layers: List[str] = Query(
            ..., title="Layers to search",
            description="Search for features in a given area for each of the specified layers.",
            min_length=1
        ),
        bbox: List[float] = Query(
            ..., title="Bounding box",
            description="Bounding box to constrain search, in format x1,y1,x2,y2.",
            min_length=4, max_length=4),
        width: float = Query(500, title="Width", description="Width of area of interest"),
        height: float = Query(500, title="Height",
                              description="Height of area of interest")
):
    """
    Generate a list of features from a variety of sources and map layers (specified by `layers`)
    inside the map bounds defined by `bbox`.
    """

    # Format the bounding box (which arrives in the querystring as a comma separated list)
    bbox_string = ','.join(str(v) for v in bbox)

    # Compare requested layers against layers we keep track of.  The valid WMS layers and their
    # respective WMS endpoints will come from our metadata.
    catalogue = agr_repo.get_display_catalogue(db, layers)

    wms_requests = []

    # Create a WMSRequest object with all the values we need to make WMS requests for each of the
    # WMS layers that we have metadata for.
    for item in catalogue:
        if item.wms_catalogue_id is None:
            continue

        # query = WMSGetFeatureInfoQuery(
        #     x=1000,
        #     y=1000,
        #     layers=layer.wms_name,
        #     bbox=bbox_string,
        #     width=width,
        #     height=height,
        # )
        query = WMSGetMapQuery(
            layers=item.wms_name,
            bbox=bbox_string,
            width=width,
            height=height,
        )
        req = WMSRequest(
            url=wms_url(item.wms_name),
            layer=item.layer_id,
            q=query
        )
        wms_requests.append(req)

    # Go and fetch features for each of the WMS endpoints we need, and make a FeatureCollection
    # out of all the aggregated features.
    feature_list = fetch_wms_features(wms_requests)

    # Internal datasets:
    # Gather valid internal sources that were included in the request's `layers` param
    internal_data = []
    for item in catalogue:
        if item.api_catalogue_id is None or item.display_data_name not in API_DATASOURCES:
            continue
        internal_data.append(item)

    # Loop through all datasets that are available internally.
    # We will make use of the data access function registered in API_DATASOURCES
    # to avoid making api calls to our own web server.
    for dataset in internal_data:
        display_data_name = dataset.display_data_name

        # use function registered for this source
        objects = API_DATASOURCES[display_data_name](db, bbox)

        feat_layer = LayerResponse(
            layer=display_data_name,
            status=200,
            geojson=objects
        )

        feature_list.append(feat_layer)

    hydrated_templates = build_templates(db, feature_list)

    response = {
        'display_data': feature_list,
        'display_templates': hydrated_templates
    }

    return response


def wms_url(wms_id):
    return "https://openmaps.gov.bc.ca/geo/pub/" + wms_id + "/ows?"
