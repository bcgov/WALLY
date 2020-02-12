"""
Functions for aggregating data from web requests and database records
"""
import logging
import requests
from typing import Tuple
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from shapely.geometry import Polygon, MultiPolygon, shape, box
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from shapely.ops import transform
from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326
from api.v1.watersheds.schema import LicenceDetails, SurficialGeologyDetails

from api.v1.aggregator.controller import feature_search, databc_feature_search

logger = logging.getLogger('api')


def calculate_mean_annual_discharge_model(db: Session, polygon: MultiPolygon, hydrological_zone: int):
    """
    This method pulls the model information for the selected hydrological zone and 
    calculates estimated discharge and runoff values for the selected watershed area.
    """
    median_elevation = 1
    glacial_coverage = 1
    annual_precipitation = 1
    evapo_transpiration = 1
    drainage_area = 1
    solar_exposure = 1
    average_slope = 1

    # Gather up all the required inputs and co-efficient tables
    q = """
        select * from mad_model_coefficients where hydrologic_zone_id = :hydro_zone_id
    """
    models = db.execute(q, {"hydro_zone_id": hydrological_zone})

    if not models:
        return HTTPException(204, "Selection point not within supported hydrological zone.")

    model_output = []

    # calculate models outputs for gathered data
    for m in models:
        model_result = m.median_elevation_co * median_elevation + \
          m.glacial_coverage_co * glacial_coverage + \
            m.precipitation_co * annual_precipitation + \
              m.potential_evapo_transpiration_co * evapo_transpiration + \
                m.drainage_area_co * drainage_area + \
                  m.solar_exposure_co * solar_exposure + \
                    m.average_slope_co * average_slope + \
                      m.intercept_co

        model_output.append({
          "output_type": m.model_output_type,
          "model_result": model_result,
          "month": m.month,
          "r2": m.r2,
          "adjusted_r2": m.adjusted_r2,
          "steyx": m.steyx
        })
        
    return model_output


def get_hydrological_zone(point: str = Query("", title="Search point", description="Point to search within")):

    hydrologic_zones = databc_feature_search('WHSE_WATER_MANAGEMENT.HYDZ_HYDROLOGICZONE_SP', search_area=point)

    if hydrologic_zones.features:
        hydrologic_zone_number = hydrologic_zones.features[0].properties["HYDROLOGICZONE_NO"]
    else:
        hydrologic_zone_number = None

    return hydrologic_zone_number