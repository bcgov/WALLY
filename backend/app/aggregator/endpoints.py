"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from typing import List
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import Response
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.hydat.db as streams_repo
import app.layers.water_rights_licences as water_rights_licences_repo
import app.layers.ground_water_wells as ground_water_wells_repo
from app.layers.water_rights_licences import WaterRightsLicenses
from app.layers.automated_snow_weather_station_locations import AutomatedSnowWeatherStationLocations
from app.layers.bc_wildfire_active_weather_stations import BcWildfireActiveWeatherStations
from app.layers.cadastral import Cadastral
from app.layers.critical_habitat_species_at_risk import CriticalHabitatSpeciesAtRisk
from app.layers.freshwater_atlas_stream_directions import FreshwaterAtlasStreamDirections
from app.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds
from app.layers.ground_water_wells import GroundWaterWells
from app.layers.bc_major_watersheds import BcMajorWatersheds
from app.layers.ecocat_water_related_reports import EcocatWaterRelatedReports
from app.layers.ground_water_aquifers import GroundWaterAquifers
from app.layers.water_allocation_restrictions import WaterAllocationRestrictions

import app.hydat.models as streams_v1
import app.aggregator.db as agr_repo
from app.aggregator.aggregate import fetch_wms_features
from app.aggregator.models import WMSGetMapQuery, WMSGetFeatureInfoQuery, WMSRequest, LayerResponse
from app.templating.template_builder import build_templates
from app.aggregator.helpers import spherical_mercator_project

logger = getLogger("aggregator")

router = APIRouter()

# Data access functions are available for certain layers.
# if a function is not available here, default to using
# the web API listed with the layer metadata.
# These functions must accept a db session and a bbox as a list of coords
# (defined by 2 corners, e.g. x1, y1, x2, y2) and return a FeatureCollection.
# For example:  get_stations_as_geojson(db: Session, bbox: List[float])
API_DATASOURCES = {
    "HYDAT": streams_repo,
    "aquifers": GroundWaterAquifers,
    "automated_snow_weather_station_locations": AutomatedSnowWeatherStationLocations,
    "bc_major_watersheds": BcMajorWatersheds,
    "bc_wildfire_active_weather_stations": BcWildfireActiveWeatherStations,
    "cadastral": Cadastral,
    "critical_habitat_species_at_risk": CriticalHabitatSpeciesAtRisk,
    "ecocat_water_related_reports": EcocatWaterRelatedReports,
    "freshwater_atlas_stream_directions": FreshwaterAtlasStreamDirections,
    "freshwater_atlas_watersheds": FreshwaterAtlasWatersheds,
    "groundwater_wells": GroundWaterWells,
    "hydrometric_stream_flow": streams_repo,
    "water_allocation_restrictions": WaterAllocationRestrictions,
    "water_rights_licences": WaterRightsLicenses
}

@router.get("/feature")
def get_layer_feature(layer: str, pk: str, db: Session = Depends(get_db)):
    """
    Returns a geojson Feature object by primary key using display_data_name as the generic lookup field. 
    relies heavily on CustomLayerBase in app.db.base_class.py but can be overridden in any custom data layer class
    """
    try:
        layer_class = API_DATASOURCES[layer]
    except:
        raise HTTPException(status_code=404, detail="Layer not found")
    
    return agr_repo.get_layer_feature(db, layer_class, pk)


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
                              description="Height of area of interest"),
        format: str = Query('geojson', title="Format",
                            description="Format that results will be returned in (e.g. geojson, xlsx)")
):
    """
    Generate a list of features from a variety of sources and map layers (specified by `layers`)
    inside the map bounds defined by `bbox`.
    """

    # This code section converts latlng EPSG:4326 values into mercator EPSG:3857
    # and then takes the largest square to use as the bbox. Reason being that the databc
    # WMS server doesn't handle non square bbox's very well on specific layers. This section
    # also limits the max size to be no larger than 10000 meters because again WMS server has
    # issues with large bbox's
    # TODO find the limit of bbox size for layers and implement feature client side
    #  that displays a square box with max size of limit
    bottom_left = spherical_mercator_project(bbox[1], bbox[0])
    top_right = spherical_mercator_project(bbox[3], bbox[2])
    x_diff = bottom_left[0] - top_right[0]
    y_diff = bottom_left[1] - top_right[1]
    diff = min(round(abs(max(x_diff, y_diff))), 10000)
    mercator_box = [bottom_left[1], bottom_left[0],
                    bottom_left[1] + diff, bottom_left[0] + diff]
    # logger.info("diff: " + str(diff) + " bbox: " + str(mercator_box))

    # Format the bounding box (which arrives in the querystring as a comma separated list)
    bbox_string = ','.join(str(v) for v in mercator_box)

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

    # Create a WMSRequest object with all the values we need to make WMS requests for each of the
    # WMS layers that we have metadata for.
    for item in catalogue:
        if item.wms_catalogue_id is None or item.display_data_name in processed_layers:
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
            layers=item.wms_catalogue.wms_name,
            bbox=bbox_string,
            width=width,
            height=height,
        )
        req = WMSRequest(
            url=wms_url(item.wms_catalogue.wms_name),
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
        objects = API_DATASOURCES[display_data_name].get_as_geojson(db, bbox)

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


def xlsxExport(features):
    """
    packages features into an excel workbook.  Returns an HTTP response object that has the saved workbook
    ready to be returned to the client (e.g. the calling http handler can return this object directly)
    """

    wb = openpyxl.Workbook()
    ws = wb.active
    first_sheet = True

    for dataset in features:
        # avoid trying to process layers if they have no features.
        if not dataset.geojson:
            continue

        # create a list of fields for this dataset
        fields = []
        try:
            fields = [*dataset.geojson[0].properties]
        except:
            continue

        if not first_sheet:
            ws = wb.create_sheet(dataset.layer)
        else:
            ws.title = dataset.layer
            first_sheet = False

        ws.append(fields)

        features = dataset.geojson.features

        # add rows for every object in the collection, using the fields defined above.
        for f in features:
            props = f['properties']
            ws.append([props.get(x) for x in fields])

    response = Response(
        content=save_virtual_workbook(wb),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=report.xlsx'})

    return response
