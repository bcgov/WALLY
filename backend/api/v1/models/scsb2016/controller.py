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
from api.v1.watersheds.controller import calculate_glacial_area, pcic_data_request, get_temperature, calculate_potential_evapotranspiration_thornthwaite
from api.v1.aggregator.controller import feature_search, databc_feature_search
from api.v1.models.isolines.controller import calculate_runoff_in_area

logger = logging.getLogger('api')

# South Coast Stewardship Baseline MAR Model controller


def calculate_mean_annual_runoff(db: Session,
                                 hydrological_zone: int,
                                 median_elevation: Decimal,
                                 glacial_coverage: Decimal,
                                 annual_precipitation: Decimal,
                                 evapo_transpiration: Decimal,
                                 drainage_area: Decimal,
                                 solar_exposure: Decimal,
                                 average_slope: Decimal
                                 ):
    """
    This method pulls the model information for the selected hydrological zone and
    calculates estimated runoff and montly distribution values for the selected watershed area.
    We can use these values to then calculate flow values for the watershed.
    """

    if not hydrological_zone or not median_elevation or glacial_coverage is None \
            or not annual_precipitation or not evapo_transpiration or not drainage_area \
            or not solar_exposure or not average_slope:
        return {"error": "Missing scsb2016 model parameters."}
        # raise HTTPException(
        #     status_code=400, detail="Missing scsb2016 model parameters.")

    # query the co-efficient table for this hydrological zone
    query = """
        select * from modeling.mad_model_coefficients where hydrologic_zone_id = :hydro_zone_id
    """
    models = db.execute(query, {"hydro_zone_id": hydrological_zone})
    if not models:
        return {"error": "Selection point not within supported hydrological zone."}
        # raise HTTPException(204, "Selection point not within supported hydrological zone.")

    # logger.warning("**** CALCULATED VALUES ****")
    # logger.warning("med.elev.: " + str(median_elevation) + " m")
    # logger.warning("avg slope: " + str(average_slope))
    # logger.warning("sol.exp.: " + str(solar_exposure))
    # logger.warning("dra.area:" + str(drainage_area) + " km2")
    # logger.warning("gla.cov.: " + str(glacial_coverage))
    # logger.warning("ann.prec.: " + str(annual_precipitation) + " mm")

    model_outputs = []
    mean_annual_discharge = 0
    # calculate model outputs for gathered inputs,
    # model output types, MAR, MD(x12months), 7Q2, S-7Q10
    for model in models:
        model_result = model.median_elevation_co * Decimal(median_elevation) + \
            model.glacial_coverage_co * Decimal(glacial_coverage) + \
            model.precipitation_co * Decimal(annual_precipitation) + \
            model.potential_evapo_transpiration_co * Decimal(evapo_transpiration) + \
            model.drainage_area_co * Decimal(drainage_area) + \
            model.solar_exposure_co * Decimal(solar_exposure) + \
            model.average_slope_co * Decimal(average_slope) + \
            model.intercept_co

        model_outputs.append({
            "output_type": model.model_output_type,
            "model_result": model_result,
            "month": model.month,
            "r2": model.r2,
            "adjusted_r2": model.adjusted_r2,
            "steyx": model.steyx
        })

        # this is a helper ouput that calculates MAD from MAR
        if model.model_output_type == 'MAR':
            mean_annual_discharge = model_result / \
                1000 * Decimal(drainage_area)
            model_outputs.append({
                "output_type": 'MAD',
                "model_result": mean_annual_discharge,
                "month": 0,
                "r2": 0,
                "adjusted_r2": 0,
                "steyx": 0
            })

    if not model_outputs:
        return {"error": "No model output calculated."}
        # raise HTTPException(204, "No model output calculated.")

    months = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
              7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    # helper to add mad monthly values to result based on Monthly Distributions
    mad_monthlys = []
    for model in model_outputs:
        if model["output_type"] == 'MD':
            mad_monthlys.append({
                "output_type": 'MAD',
                "model_result": mean_annual_discharge * model["model_result"] *
                Decimal(365/months[model["month"]]),
                "month": model["month"],
                "r2": 0,
                "adjusted_r2": 0,
                "steyx": 0
            })

    return model_outputs + mad_monthlys


def get_hydrological_zone(point=None):
    """
    Lookup which hydrological zone a point falls within
    """
    if not point:
        return None

    hydrologic_zones = databc_feature_search('WHSE_WATER_MANAGEMENT.HYDZ_HYDROLOGICZONE_SP',
                                             search_area=point)
    if hydrologic_zones.features:
        hydrologic_zone_number = hydrologic_zones.features[0].properties["HYDROLOGICZONE_NO"]
    else:
        hydrologic_zone_number = None

    return hydrologic_zone_number


def model_output_as_dict(data: list):
    """
        organizes SCSB model output in dict format
    """

    # if data is already a dict indicating an error, return it now.
    if isinstance(data, dict) and data.get('error', None):
        data['status'] = "Unavailable"
        return data

    monthly_discharge = {}
    monthly_distributions = {}
    mar = None
    mad = None
    ind_7q2 = None
    ind_s7q10 = None

    for item in data:
        output_type = item.get('output_type')

        if output_type == 'MAR':
            # MAR should only appear once.
            assert mar is None
            mar = item

        elif output_type == 'MD':
            month = item.pop('month')
            # each month must only have one record in the model output,
            # so assert that this month has not been more than once
            assert monthly_distributions.get(month, None) is None

            monthly_distributions[month] = item

        elif output_type == '7Q2':
            assert ind_7q2 is None
            item.pop('month', None)  # month is not needed
            ind_7q2 = item

        elif output_type == 'S-7Q10':
            assert ind_s7q10 is None
            item.pop('month', None)
            ind_s7q10 = item

        elif output_type == 'MAD':
            month = item.pop('month')

            if month == 0:
                # month = 0 is the annual result
                mad = item.get('model_result')
                continue

            assert monthly_discharge.get(month, None) is None

            monthly_discharge[month] = item

        else:
            raise ValueError("unrecognized model output %s", output_type)

    return {
        "monthly_discharge": monthly_discharge,
        "monthly_distributions": monthly_distributions,
        "7q2": ind_7q2,
        "s7q10": ind_s7q10,
        "mar": mar,
        "mad": mad,
        "status": "Available"
    }
