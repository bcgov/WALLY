"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from typing import List
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from shapely.geometry import box, MultiPolygon, Polygon

from api.db.utils import get_db

from api.v1.aggregator.controller import (
    fetch_geojson_features,
    databc_feature_search,
    get_layer_feature,
    feature_search,
    EXTERNAL_API_REQUESTS,
    API_DATASOURCES,
    DATABC_GEOMETRY_FIELD,
    DATABC_LAYER_IDS)
from api.v1.aggregator.schema import WMSGetMapQuery, WMSGetFeatureQuery, ExternalAPIRequest, LayerResponse
from api.v1.aggregator.excel import xlsxExport

logger = getLogger("aggregator")

router = APIRouter()


@router.get("/feature")
def get_layer_feature(layer: str, pk: str, db: Session = Depends(get_db)):
    """
    Returns a geojson Feature object by primary key using display_data_name as the generic lookup field.
    relies heavily on CustomLayerBase in api.db.base_class.py but can be overridden in any custom data layer class
    """
    try:
        layer_class = API_DATASOURCES[layer]
    except:
        raise HTTPException(status_code=404, detail="Layer not found")

    # check if layer_class is a SQLAlchemy instance. If so, use the classmethod
    # on BaseLayerTable.
    return get_layer_feature(db, layer_class, pk)


@router.get("/")
def aggregate_sources(
        db: Session = Depends(get_db),
        layers: List[str] = Query(
            ..., title="Layers to search",
            description="Search for features in a given area for each of the specified layers.",
            min_length=1
        ),
        polygon: str = Query(
            "", title="Search polygon",
            description="Polygon to search within"
        ),
        bbox: List[float] = Query(
            [], title="Bounding box",
            description="Bounding box to constrain search, in format x1,y1,x2,y2.", max_length=4),
        width: float = Query(500, title="Width",
                             description="Width of area of interest"),
        height: float = Query(500, title="Height",
                              description="Height of area of interest"),
        format: str = Query('geojson', title="Format",
                            description="Format that results will be returned in (e.g. geojson, xlsx)"),
        srs: str = Query(
            "EPSG:3005", title="SRS Name",
            description="SRS name required in response"
        ),
):
    """
    Generate a list of features from a variety of sources and map layers (specified by `layers`)
    inside the map bounds defined by `bbox`.
    """

    if not polygon and not bbox:
        raise HTTPException(
            status_code=400, detail="No search bounds. Supply either a `polygon` or set of 4 `bbox` values")

    # the polygon search area comes formatted the same way a MultiPolygon would be.
    # (e.g., an array of polygons).  Here we process it by creating a MultiPolygon
    # of all the polygons in the supplied shape.
    if polygon:
        poly_parsed = json.loads(polygon)
        polygon = MultiPolygon([Polygon(x) for x in poly_parsed])

    # define a search area out of the polygon shape
    search_area = polygon or box(*bbox)

    feature_list = feature_search(db, layers, search_area, srs)

    # if xlsx format was requested, package the response as xlsx and return the xlsx notebook.
    if format == 'xlsx':
        return xlsxExport(feature_list)

    response = {
        'display_data': feature_list
    }

    return response


def wms_url(wms_id):
    return "https://openmaps.gov.bc.ca/geo/pub/" + wms_id + "/ows?"
