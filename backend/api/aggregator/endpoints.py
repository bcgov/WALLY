"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from typing import List
import json
import pyproj

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import Response
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from shapely.geometry import shape, box, MultiPolygon, Polygon
from shapely.ops import transform

from api.db.utils import get_db
from api.db.base_class import BaseLayerTable
from api.hydat.db_models import Station as StreamStation
import api.layers.water_rights_licences as water_rights_licences_repo
import api.layers.ground_water_wells as ground_water_wells_repo
from api.layers.water_rights_licences import WaterRightsLicenses
from api.layers.water_rights_applications import WaterRightsApplications
from api.layers.automated_snow_weather_station_locations import AutomatedSnowWeatherStationLocations
from api.layers.bc_wildfire_active_weather_stations import BcWildfireActiveWeatherStations
from api.layers.cadastral import Cadastral
from api.layers.critical_habitat_species_at_risk import CriticalHabitatSpeciesAtRisk
from api.layers.freshwater_atlas_stream_directions import FreshwaterAtlasStreamDirections
from api.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds
from api.layers.ground_water_wells import GroundWaterWells
from api.layers.bc_major_watersheds import BcMajorWatersheds
from api.layers.ecocat_water_related_reports import EcocatWaterRelatedReports
from api.layers.ground_water_aquifers import GroundWaterAquifers
from api.layers.water_allocation_restrictions import WaterAllocationRestrictions
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.layers.first_nations import CommunityLocations, TreatyLands, TreatyAreas

import api.hydat.models as streams_v1
import api.aggregator.db as agr_repo
from api.aggregator.aggregate import fetch_wms_features
from api.aggregator.models import WMSGetMapQuery, WMSGetFeatureQuery, ExternalAPIRequest, LayerResponse
from api.aggregator.helpers import gwells_api_request
from api.templating.template_builder import build_templates
from api.aggregator.helpers import spherical_mercator_project
from api.aggregator.excel import xlsxExport

logger = getLogger("aggregator")

router = APIRouter()

# Data access functions are available for certain layers.
# if a function is not available here, default to using
# the web API listed with the layer metadata.

# returns a module or class that has `get_as_geojson` and `get_details` functions for looking up data from a layer
API_DATASOURCES = {
    "HYDAT": StreamStation,
    "aquifers": GroundWaterAquifers,
    # "automated_snow_weather_station_locations": AutomatedSnowWeatherStationLocations,
    "bc_major_watersheds": BcMajorWatersheds,
    # "bc_wildfire_active_weather_stations": BcWildfireActiveWeatherStations,
    "cadastral": Cadastral,
    # "critical_habitat_species_at_risk": CriticalHabitatSpeciesAtRisk,
    # "ecocat_water_related_reports": EcocatWaterRelatedReports,
    # "groundwater_wells": GroundWaterWells,
    "hydrometric_stream_flow": StreamStation,
    # "water_allocation_restrictions": WaterAllocationRestrictions,
    "water_rights_licences": WaterRightsLicenses,
    "water_rights_applications": WaterRightsApplications,
    "freshwater_atlas_stream_networks": FreshwaterAtlasStreamNetworks,
    "fn_treaty_areas": TreatyAreas,
    "fn_community_locations": CommunityLocations,
    "fn_treaty_lands": TreatyLands

    # these layers are causing performance issues.
    # leaving them commented out allows them to fall back to WMS fetching from DataBC.
    # "freshwater_atlas_stream_directions": FreshwaterAtlasStreamDirections,
    # "freshwater_atlas_watersheds": FreshwaterAtlasWatersheds,

    # NOTE: Stream analysis also uses this dictionary for information lookup
}

# For external APIs that may require different parameters (e.g. not a WMS/GeoServer with
# relatively consistent request params), add a helper function that returns an ExternalAPIRequest
# object.
EXTERNAL_API_REQUESTS = {
    "groundwater_wells": gwells_api_request
}

# DataBC names geometry fields either GEOMETRY or SHAPE
# We will assume GEOMETRY, except for layers listed here.
DATABC_GEOMETRY_FIELD = {
    "automated_snow_weather_station_locations": "SHAPE",
    "bc_wildfire_active_weather_stations": "SHAPE",
    "critical_habitat_species_at_risk": "SHAPE",
}


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
    return agr_repo.get_layer_feature(db, layer_class, pk)


@router.get("/aggregate")
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
        width: float = Query(500, title="Width", description="Width of area of interest"),
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

    albers_search_area = transform(pyproj.Transformer.from_proj(
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(init='epsg:3005')
    ).transform, search_area)

    # Compare requested layers against layers we keep track of.  The valid WMS layers and their
    # respective WMS endpoints will come from our metadata.
    catalogue = agr_repo.get_display_catalogue(db, layers)

    wms_requests = []

    # keep track of layers that are processed.
    # this enables us to use internal data, marking it as done, but fall
    # back on making a WMS request if needed.
    processed_layers = {}

    # Internal datasets:
    # Gather valid internal sources that were included in the request's `layers` param
    internal_data = []
    # logger.info([c.display_data_name for c in catalogue])
    for item in catalogue:
        if item.display_data_name in API_DATASOURCES:
            internal_data.append(item)
            processed_layers[item.display_data_name] = True

    # Create a ExternalAPIRequest object with all the values we need to make WMS requests for each of the
    # WMS layers that we have metadata for.
    for item in catalogue:
        if item.display_data_name in processed_layers:
            continue

        logger.info(item.display_data_name)

        if item.display_data_name in EXTERNAL_API_REQUESTS:

            # use the helper function in EXTERNAL_API_REQUESTS (if available)
            # to return an ExternalAPIRequest directly.
            wms_requests.append(
                EXTERNAL_API_REQUESTS[item.display_data_name](search_area)
            )
            logger.info('added external API request!')
            continue

        # if we don't have a direct API to access, fall back on WMS.
        if item.wms_catalogue_id is not None:
            query = WMSGetFeatureQuery(
                typeNames=item.wms_catalogue.wms_name,
                cql_filter=f"""
                    INTERSECTS({DATABC_GEOMETRY_FIELD.get(item.display_data_name, 'GEOMETRY')}, {albers_search_area.wkt})
                """
            )
            req = ExternalAPIRequest(
                url=f"https://openmaps.gov.bc.ca/geo/pub/wfs?",
                layer=item.display_data_name,
                q=query
            )
            wms_requests.append(req)

    # Go and fetch features for each of the WMS endpoints we need, and make a FeatureCollection
    # out of all the aggregated features.
    feature_list = fetch_wms_features(wms_requests)

    # Loop through all datasets that are available internally.
    # We will make use of the data access function registered in API_DATASOURCES
    # to avoid making api calls to our own web server.
    for dataset in internal_data:
        display_data_name = dataset.display_data_name

        # use function registered for this source
        # API_DATASOURCES is a map of layer names to a module or class;
        # Use it here to look up a module/class that has a `get_as_geojson`
        # function for looking up data in a layer. This function will return geojson
        # features in the bounding box for each layer, which we will package up
        # into a response.
        objects = API_DATASOURCES[display_data_name].get_as_geojson(
            db, search_area)

        feat_layer = LayerResponse(
            layer=display_data_name,
            status=200,
            geojson=objects
        )

        feature_list.append(feat_layer)

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
