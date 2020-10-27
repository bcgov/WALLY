import json
import logging
from sqlalchemy.orm import Session
from api.v1.aggregator.controller import feature_search
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
from api.v1.aggregator.helpers import transform_4326_3005
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs, MeanAnnualFlow, MeanMonthlyFlow
from xgboost import XGBRegressor, DMatrix
import numpy as np

logger = logging.getLogger("hydrological_zones")
V1_ANNUAL_FLOW_DIR = "./api/v1/models/hydrological_zones/model_states/v1_hydro_zone_annual_flow/"
V2_ANNUAL_FLOW_DIR = "./api/v1/models/hydrological_zones/model_states/v2_hydro_zone_annual_flow/"
V2_MONTHLY_DISTRIBUTIONS_DIR = "./api/v1/models/hydrological_zones/model_states/v2_hydro_zone_monthly_distributions/"


def get_hydrological_zone_model_v1(
    hydrological_zone: str,
    drainage_area: float,
    median_elevation: float,
    annual_precipitation: float,
):
    """
    Loads the respective zone's xgb model state and returns an estimated
    mean annual flow value for the hydrological zone.
    """
    if (
        not hydrological_zone
        or not drainage_area
        or not median_elevation
        or not annual_precipitation
    ):
        return {"error": "Missing wally zone model parameters."}
    xgb = XGBRegressor(random_state=42)
    xgb.load_model(V1_ANNUAL_FLOW_DIR + "zone_{}.json".format(hydrological_zone))
    inputs = [drainage_area, median_elevation, annual_precipitation]
    inputs = np.array(inputs).reshape((1, -1))
    mean_annual_flow_prediction = xgb.predict(inputs)
    result = MeanAnnualFlow(
        mean_annual_flow=mean_annual_flow_prediction,
        r_squared=get_zone_info(hydrological_zone),
    )
    return result


def get_zone_info(zone):
    """
    Returns model fit in r^2 value based on hydrological zone
    """
    with open(V1_ANNUAL_FLOW_DIR + 'zone_models_r2.json') as zone_models_r2_file:
        zone_r_squares = json.load(zone_models_r2_file)
        return zone_r_squares[str(zone)]

    return None


def get_hydrological_zone_model_v2(
    hydrological_zone: str,
    drainage_area: float,
    annual_precipitation: float,
    glacial_coverage: float,
    glacial_area: float
):
    """
    Loads the respective zone's xgb model state and returns an estimated
    mean annual flow value for the hydrological zone.
    """
    print(hydrological_zone, drainage_area, annual_precipitation, glacial_coverage, glacial_area)
    if (
        not hydrological_zone
        or not drainage_area
        or not annual_precipitation
        # or not glacial_coverage
        # or not glacial_area
    ):
        return {"error": "Missing wally zone model parameters."}
    
    xgb = XGBRegressor(random_state=42)
    inputs = [drainage_area, annual_precipitation, glacial_coverage, glacial_area]
    inputs = np.array(inputs).reshape((1, -1))

    # ANNUAL FLOW
    xgb.load_model(V2_ANNUAL_FLOW_DIR + "zone_{}.json".format(hydrological_zone))
    mean_annual_flow_prediction = xgb.predict(inputs)
    mean_annual_flow = MeanAnnualFlow(
        mean_annual_flow=mean_annual_flow_prediction,
        r_squared=get_zone_info(hydrological_zone),
    )

    # MONTHLY FLOW
    monthly_predictions = []
    for month in range(1, 13): # months
        zone_name = "zone_{}".format(hydrological_zone)
        file_path = V2_MONTHLY_DISTRIBUTIONS_DIR + zone_name + '/' + str(month) + '.json'
        xgb.load_model(file_path)
        mean_monthly_flow_prediction = xgb.predict(inputs)
        mean_monthly_flow = MeanMonthlyFlow(
            mean_monthly_flow=mean_monthly_flow_prediction,
            r_squared=0,
        )
        monthly_predictions.append(mean_monthly_flow)

    result = {
      "mean_annual_flow": mean_annual_flow,
      "mean_monthly_flows": monthly_predictions
    }

    return result
