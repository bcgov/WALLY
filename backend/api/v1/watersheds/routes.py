"""
Endpoints for returning statistics about watersheds
"""
from logging import getLogger
import datetime
import json
import geojson
from geojson import FeatureCollection, Feature
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from shapely.geometry import shape, MultiPolygon, Polygon, Point
from shapely.ops import transform


from api.db.utils import get_db
from api.v1.hydat.db_models import Station as StreamStation

from api.v1.aggregator.controller import (
    databc_feature_search,

    EXTERNAL_API_REQUESTS,
    API_DATASOURCES,
    DATABC_GEOMETRY_FIELD,
    DATABC_LAYER_IDS)
from api.v1.aggregator.schema import WMSGetMapQuery, WMSGetFeatureQuery, ExternalAPIRequest, LayerResponse
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326
from api.v1.aggregator.excel import xlsxExport
from api.v1.watersheds.controller import (
    calculate_glacial_area,
    pcic_data_request,
    surface_water_rights_licences,
    calculate_watershed,
    get_watershed,
    get_upstream_catchment_area,
    surficial_geology,
    get_temperature,
    get_annual_precipitation,
    calculate_potential_evapotranspiration_thornthwaite,
    calculate_potential_evapotranspiration_hamon,
    get_slope_elevation_aspect,
    get_hillshade,
    export_summary_as_xlsx
)
from api.v1.hydat.controller import (get_stations_in_area)
from api.v1.watersheds.schema import (
    WatershedDetails,
    LicenceDetails,
    SurficialGeologyDetails,
    SurficialGeologyTypeSummary
)
from api.v1.models.isolines.controller import calculate_runoff_in_area
from api.v1.models.scsb2016.controller import get_hydrological_zone, calculate_mean_annual_runoff, model_output_as_dict

logger = getLogger("aggregator")

router = APIRouter()

watershed_feature_description = """
    Watershed features follow the format <dataset>.<id>. Dataset is either
    the DataBC dataset code or 'calculated' for Wally generated watersheds.
    If using a calculated watershed, `id` is the FWA Watershed feature ID
    to start calculating a watershed from.
    Example:
    'WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY.1111111'
    'calculated.1111111'.
    """


@router.get('/')
def get_watersheds(
    db: Session = Depends(get_db),
    point: str = Query(
        "", title="Search point",
        description="Point to search within"),
    include_self: bool = Query(
        False, title="Include the area around the point of interest in generated polygons")
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

    watershed_features = []

    calculated_ws = calculate_watershed(db, point, include_self=include_self)

    if calculated_ws:
        watershed_features.append(calculated_ws)

    for ws in watersheds.features:
        watershed_features.append(
            Feature(
                geometry=transform(transform_3005_4326, shape(ws.geometry)),
                properties=dict(ws.properties),
                id=ws.id
            )
        )

    return FeatureCollection(watershed_features)


@router.get('/{watershed_feature}')
def watershed_stats(
    db: Session = Depends(get_db),
    watershed_feature: str = Path(...,
                                  title="The watershed feature ID at the point of interest",
                                  description=watershed_feature_description),
    format: str = Query(
        "json",
        title="Format",
        description="Format to return results in. Options: json (default), xlsx"
    )
):
    """ aggregates statistics/info about a watershed """

    # watershed area calculations
    watershed = get_watershed(db, watershed_feature)
    watershed_poly = shape(watershed.geometry)
    watershed_area = transform(transform_4326_3005, watershed_poly).area
    watershed_rect = watershed_poly.minimum_rotated_rectangle

    # watershed characteristics lookups
    drainage_area = watershed_area / 1e6  # needs to be in km²
    glacial_area_m, glacial_coverage = calculate_glacial_area(
        db, watershed_rect)
    temperature_data = get_temperature(watershed_poly)
    annual_precipitation = get_annual_precipitation(watershed_poly)
    potential_evapotranspiration_hamon = calculate_potential_evapotranspiration_hamon(
        watershed_poly, temperature_data)
    potential_evapotranspiration_thornthwaite = calculate_potential_evapotranspiration_thornthwaite(
        watershed_poly, temperature_data
    )
    hydrological_zone = get_hydrological_zone(watershed_poly.centroid)
    average_slope, median_elevation, aspect = get_slope_elevation_aspect(
        watershed_poly)
    solar_exposure = get_hillshade(average_slope, aspect)

    # custom model outputs
    isoline_runoff = calculate_runoff_in_area(db, watershed_poly)
    scsb2016_model = calculate_mean_annual_runoff(db, hydrological_zone, median_elevation,
                                                  glacial_coverage, annual_precipitation, potential_evapotranspiration_thornthwaite,
                                                  drainage_area, solar_exposure, average_slope)

    hydrometric_stations = get_stations_in_area(db, shape(watershed.geometry))

    data = {
        "watershed_name": watershed.properties.get("name", None),
        "watershed_source": watershed.properties.get("watershed_source", None),
        "watershed_area": watershed_area,
        "drainage_area": drainage_area,
        "glacial_area": glacial_area_m,
        "glacial_coverage": glacial_coverage,
        "temperature_data": temperature_data,
        "annual_precipitation": annual_precipitation,
        "potential_evapotranspiration_hamon": potential_evapotranspiration_hamon,
        "potential_evapotranspiration_thornthwaite": potential_evapotranspiration_thornthwaite,
        "hydrological_zone": hydrological_zone,
        "average_slope": average_slope,
        "median_elevation": median_elevation,
        "aspect": aspect,
        "runoff_isoline_avg": (isoline_runoff['runoff'] /
                               isoline_runoff['area'] * 1000) if isoline_runoff['area'] else 0,
        "runoff_isoline_discharge_m3s": isoline_runoff['runoff'] / 365 / 24 / 60 / 60,
        "scsb2016_model": scsb2016_model,
        "scsb2016_output": model_output_as_dict(scsb2016_model),
        "hydrometric_stations": hydrometric_stations
    }

    if format == 'xlsx':
        licence_data = surface_water_rights_licences(watershed_poly)
        data['generated_date'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        if licence_data.licences and licence_data.licences.features:
            data['licences'] = [dict(**x.properties)
                                for x in licence_data.licences.features]

            data['licences_count_pod'] = len(licence_data.licences.features)

        return export_summary_as_xlsx(jsonable_encoder(data))

    return data


@router.get('/{watershed_feature}/licences')
def get_watershed_demand(
    db: Session = Depends(get_db),
    watershed_feature: str = Path(...,
                                  title="The watershed feature ID at the point of interest",
                                  description=watershed_feature_description)
):
    """ returns data about watershed demand by querying DataBC """

    watershed = get_watershed(db, watershed_feature)

    return surface_water_rights_licences(shape(watershed.geometry))


@router.get('/{watershed_feature}/surficial_geology')
def get_surficial_geology(
    db: Session = Depends(get_db),
    watershed_feature: str = Path(...,
                                  title="The watershed feature ID at the point of interest",
                                  description=watershed_feature_description)
):
    """ returns data about watershed demand by querying DataBC """

    watershed = get_watershed(db, watershed_feature)

    surf_geol_summary = surficial_geology(shape(watershed.geometry))

    return surf_geol_summary
