"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from typing import List
import json
import pyproj
import requests
import geojson
from geojson import FeatureCollection, Feature
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from shapely.geometry import shape, box, MultiPolygon, Polygon, Point
from shapely.ops import transform
from urllib.parse import urlencode

from api.db.utils import get_db
from api.v1.hydat.db_models import Station as StreamStation

from api.v1.aggregator.controller import (
    fetch_geojson_features,
    databc_feature_search,
    get_layer_feature,
    feature_search,
    calculate_glacial_area,
    precipitation,
    EXTERNAL_API_REQUESTS,
    API_DATASOURCES,
    DATABC_GEOMETRY_FIELD,
    DATABC_LAYER_IDS)
from api.v1.aggregator.schema import WMSGetMapQuery, WMSGetFeatureQuery, ExternalAPIRequest, LayerResponse, WatershedDetails
from api.templating.template_builder import build_templates
from api.v1.aggregator.helpers import spherical_mercator_project, transform_4326_3005, transform_3005_4326
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
                            description="Format that results will be returned in (e.g. geojson, xlsx)")
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

    feature_list = feature_search(db, layers, search_area)

    # if xlsx format was requested, package the response as xlsx and return the xlsx notebook.
    if format == 'xlsx':
        return xlsxExport(feature_list)

    hydrated_templates = None
    if feature_list:
        hydrated_templates = build_templates(db, feature_list)

    response = {
        'display_data': feature_list,
        'display_templates': hydrated_templates
    }

    return response


def wms_url(wms_id):
    return "https://openmaps.gov.bc.ca/geo/pub/" + wms_id + "/ows?"


@router.get("/stats/glacier_coverage")
def glacier_coverage(
        db: Session = Depends(get_db),
        polygon: str = Query(
            "", title="Search polygon",
            description="Polygon to search within"
        )):
    """
    Generate a list of features from a variety of sources and map layers (specified by `layers`)
    inside the map bounds defined by `bbox`.
    """

    glaciers_layer = 'freshwater_atlas_glaciers'

    if not polygon:
        raise HTTPException(
            status_code=400, detail="No search bounds. Supply a `polygon` (geojson geometry)")

    if polygon:
        poly_parsed = json.loads(polygon)
        polygon = MultiPolygon([Polygon(x) for x in poly_parsed])

    if polygon.area <= 0:
        raise HTTPException(
            status_code=400, detail="Polygon has zero area")
    polygon = transform(transform_4326_3005, polygon)

    coverage = glacial_area(db, polygon)

    return {
        "coverage": coverage
    }


@router.get("/stats/precipitation")
def get_precipitation(
    polygon: str = Query(
        "", title="Search polygon",
        description="Polygon to search within"),
    output_variable: str = Query(
        # pr - precipitation
        # tasmax - maximum temp
        # tasmin - minimum temp
        # prsn - precipitation as snow
        "pr",
        title="Output variable",
        description="Output variable (e.g. pr - precipitation). See https://services.pacificclimate.org/pcex/app/"),
    dataset: str = Query(
        # dataset code: default to CanESM2 1981-2010 precipitation
        "pr_mClim_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19810101-20101231_Canada",
        title="Dataset code",
        description="Code for dataset to query. See https://services.pacificclimate.org/pcex/app/")
):
    """ Returns an average precipitation from the pacificclimate.org climate explorer service """
    if not polygon:
        raise HTTPException(
            status_code=400, detail="No search bounds. Supply a `polygon` (geojson geometry)")

    if polygon:
        poly_parsed = json.loads(polygon)
        polygon = MultiPolygon([Polygon(x) for x in poly_parsed])

    return precipitation(polygon, output_variable, dataset)


@router.get('/watersheds')
def get_watersheds(
    db: Session = Depends(get_db),
    point: str = Query(
        "", title="Search point",
        description="Point to search within")
):
    """ returns a list of watersheds at this point, if any.
    Watersheds are sourced from the following datasets:
    https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-assessment-watersheds
    https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries
    https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-watersheds

    """
    assessment_watershed_layer_id = 'WHSE_BASEMAPPING.FWA_ASSESSMENT_WATERSHEDS_POLY'
    fwa_watersheds_layer_id = 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY'
    hydrometric_watershed_layer_id = 'WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY'

    search_layers = ','.join([
        assessment_watershed_layer_id,
        fwa_watersheds_layer_id,
        hydrometric_watershed_layer_id
    ])

    if not point:
        raise HTTPException(
            status_code=400, detail="No search point. Supply a `point` (geojson geometry)")

    if point:
        point_parsed = json.loads(point)
        point = Point(point_parsed)

    watersheds = databc_feature_search(search_layers, search_area=point)

    if not len(watersheds.features):
        return FeatureCollection([])

    watershed_features = [
        Feature(
            geometry=transform(transform_3005_4326, shape(ws.geometry)),
            properties=dict(ws.properties),
            id=ws.id
        ) for i, ws in enumerate(watersheds.features)]
    return FeatureCollection(watershed_features)


@router.get('/watersheds/{dataset_watershed_id}')
def watershed_stats(
    db: Session = Depends(get_db),
    dataset_watershed_id: str = Path(...,
                                     title="The watershed ID prefixed by dataset name")
):
    """ aggregates statistics/info about a watershed """

    watershed_layer = '.'.join(dataset_watershed_id.split('.')[:2])
    watershed_id = dataset_watershed_id.split('.')[-1:]

    id_props = {
        'WHSE_BASEMAPPING.FWA_ASSESSMENT_WATERSHEDS_POLY': 'WATERSHED_FEATURE_ID',
        'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY': 'WATERSHED_FEATURE_ID',
        'WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY': 'HYD_WATERSHED_BND_POLY_ID'
    }

    cql_filter = f"{id_props[watershed_layer]}={watershed_id}"

    watershed = databc_feature_search(watershed_layer, cql_filter=cql_filter)
    if len(watershed.features) != 1:
        raise HTTPException(
            status_code=404, detail=f"Watershed with id {dataset_watershed_id} not found")

    watershed = watershed.features[0]

    watershed_area = watershed.properties['FEATURE_AREA_SQM']

    watershed_poly = shape(watershed.geometry)
    projected_geometry_area = watershed_poly.area

    if len(list(zip(*watershed_poly.exterior.coords.xy))) > 100:
        watershed_poly = watershed_poly.simplify(
            watershed.properties['FEATURE_LENGTH_M'] / 100, preserve_topology=False)

    projected_geometry_area_simplified = watershed_poly.area

    precip_search_area = watershed_poly.simplify(
        watershed.properties['FEATURE_LENGTH_M'] / 10)

    precip = precipitation(
        transform(transform_3005_4326, precip_search_area))
    glacial_area_m, glacial_coverage = calculate_glacial_area(
        db, transform(transform_3005_4326, watershed_poly))

    return WatershedDetails(
        precipitation=precip,
        glacial_coverage=glacial_coverage,
        glacial_area=glacial_area_m,
        watershed_area=watershed_area,
        projected_geometry_area=projected_geometry_area,
        projected_geometry_area_simplified=projected_geometry_area_simplified,
        precip_search_area=precip_search_area.area
    )
