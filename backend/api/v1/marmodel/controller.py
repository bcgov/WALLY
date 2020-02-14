"""
Functions for aggregating data from web requests and database records
"""
import logging
import math
from decimal import Decimal
import requests
from geojson import FeatureCollection, Feature
from shapely.geometry import MultiPolygon
from shapely.ops import transform
from shapely import geometry
from api.v1.aggregator.helpers import transform_4326_3005
from fastapi import Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from api.v1.watersheds.controller import calculate_glacial_area, precipitation
from api.v1.aggregator.controller import feature_search, databc_feature_search
from api.v1.isolines.controller import calculate_runnoff_in_area

logger = logging.getLogger('api')


def calculate_mean_annual_runoff(db: Session, polygon: MultiPolygon, hydrological_zone: int):
    """
    This method pulls the model information for the selected hydrological zone and
    calculates estimated runoff and montly distribution values for the selected watershed area.
    We can use these values to then calculate flow values for the watershed.
    """

    if not polygon or not hydrological_zone:
        raise HTTPException(
            status_code=400, detail="Missing search polygon, or hydrological zone.")
    
    # async data lookups
    glacier_result = calculate_glacial_area(db, polygon)
    sea_result = get_slope_elevation_aspect(polygon)
    logger.warning(sea_result)
    precipitation_result = calculate_runnoff_in_area(db, polygon)#precipitation(polygon)

    # set input variables
    # * TODO * ask sea folks to include median elevation in result
    median_elevation = Decimal(sea_result["averageElevation"]) # api doesn't return median elevation
    average_slope = Decimal(sea_result["slope"])
    solar_exposure = Decimal(hillshade(sea_result["slope"], sea_result["aspect"]))
    drainage_area = Decimal(transform(transform_4326_3005, polygon).area) / 1000
    glacial_coverage = Decimal(glacier_result[1])
    annual_precipitation = Decimal(precipitation_result["avg_mm"])
    
    logger.warning("**** CALCULATED VALUES ****")
    logger.warning("med.elev.: " + str(median_elevation) + " m")
    logger.warning("avg slope: " + str(average_slope))
    logger.warning("sol.exp.: " + str(solar_exposure))
    logger.warning("dra.area:" + str(drainage_area) + " km2")
    logger.warning("gla.cov.: " + str(glacial_coverage))
    logger.warning("ann.prec.: " + str(annual_precipitation) + " mm")

    evapo_transpiration = 650 # temporary default

    # query the co-efficient table for this hydrological zone
    query = """
        select * from modeling.mad_model_coefficients where hydrologic_zone_id = :hydro_zone_id
    """
    models = db.execute(query, {"hydro_zone_id": hydrological_zone})

    if not models:
        raise HTTPException(204, "Selection point not within supported hydrological zone.")

    model_output = []

    # calculate model outputs for gathered inputs,
    # model output types, MAR, MD(x12months), 7Q2, S-7Q10
    for model in models:
        model_result = model.median_elevation_co * median_elevation + \
          model.glacial_coverage_co * glacial_coverage + \
            model.precipitation_co * annual_precipitation + \
              model.potential_evapo_transpiration_co * evapo_transpiration + \
                model.drainage_area_co * drainage_area + \
                  model.solar_exposure_co * solar_exposure + \
                    model.average_slope_co * average_slope + \
                      model.intercept_co

        model_output.append({
            "output_type": model.model_output_type,
            "model_result": model_result,
            "month": model.month,
            "r2": model.r2,
            "adjusted_r2": model.adjusted_r2,
            "steyx": model.steyx
        })
        # this is a helper ouput that calculates MAD from MAR
        if model.model_output_type == 'MAR':
            model_output.append({
                "output_type": 'MAD',
                "model_result": model_result / 1000 * drainage_area,
                "month": 0,
                "r2": 0,
                "adjusted_r2": 0,
                "steyx": 0
            })


    if not model_output:
        raise HTTPException(204, "No model output calculated.")

    return model_output


def get_hydrological_zone(point: str = Query("", title="Search point",
                                             description="Point to search within")):
    """
    Lookup which hydrological zone a point falls within
    """
    hydrologic_zones = databc_feature_search('WHSE_WATER_MANAGEMENT.HYDZ_HYDROLOGICZONE_SP',
                                             search_area=point)

    if hydrologic_zones.features:
        hydrologic_zone_number = hydrologic_zones.features[0].properties["HYDROLOGICZONE_NO"]
    else:
        hydrologic_zone_number = None

    return hydrologic_zone_number


def get_slope_elevation_aspect(polygon: MultiPolygon):
    """
    This calls the sea api with a polygon and receives back 
    slope, elevation and aspect information.
    """
    sea_url = "https://apps.gov.bc.ca/gov/sea/slopeElevationAspect/json"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    }

    exterior = extract_poly_coords(polygon)["exterior_coords"]
    coordinates = [[list(elem) for elem in exterior]]

    payload = "format=json&aoi={\"type\":\"Feature\",\"properties\":{},\"geometry\":{\"type\":\"MultiPolygon\", \"coordinates\":" \
        + str(coordinates) + \
        "},\"crs\":{\"type\":\"name\",\"properties\":{\"name\":\"urn:ogc:def:crs:EPSG:4269\"}}}"
    logger.warning(payload)

    try:
        response = requests.post(sea_url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise HTTPException(status_code=error.response.status_code, detail=str(error))
    
    result = response.json()
    logger.warning(result)

    if result["status"] != "SUCCESS":
        raise HTTPException(500, detail=result["message"])

    # response object from sea example
    # {"status":"SUCCESS","message":"717 DEM points were used in the calculations.",
    # "SlopeElevationAspectResult":{"slope":44.28170006222049,
    # "minElevation":793.0,"maxElevation":1776.0,
    # "averageElevation":1202.0223152022315,"aspect":125.319019998603,
    # "confidenceIndicator":46.840837384501654}}
    return result["SlopeElevationAspectResult"]


def hillshade(slope: float, aspect: float):
    """
    Calculates the percentage hillshade value
    based on the average slope and aspect of a point
    """
    azimuth = 180.0 # 0-360 we are using values from the baseline paper
    altitude = 45.0 # 0-90 " "
    azimuth_rad = azimuth * math.pi / 2.
    altitude_rad = altitude * math.pi / 180.

    # Hillshade = 255.0 * (( cos(zenith_I) * cos(slope_T))+(sin(zenith_I) * sin(slope_T)*cos(azimuth_I-aspect_T))

    shade_value = math.sin(altitude_rad) * math.sin(slope) \
        + math.cos(altitude_rad) * math.cos(slope) \
        * math.cos((azimuth_rad - math.pi / 2.) - aspect)

    # logger.warning(shade_value)

    return abs(shade_value) # 255 * (shade_value + 1) / 2


def extract_poly_coords(geom):
    if geom.type == 'Polygon':
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for interior in geom.interiors:
            interior_coords += interior.coords[:]
    elif geom.type == 'MultiPolygon':
        exterior_coords = []
        interior_coords = []
        for part in geom:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc['exterior_coords']
            interior_coords += epc['interior_coords']
    else:
        raise ValueError('Unhandled geometry type: ' + repr(geom.type))
    return {'exterior_coords': exterior_coords,
            'interior_coords': interior_coords}