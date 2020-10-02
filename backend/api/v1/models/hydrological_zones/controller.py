import json
import logging
from sqlalchemy.orm import Session
from api.v1.aggregator.controller import feature_search
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
from api.v1.aggregator.helpers import transform_4326_3005
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs, ModelOutput
from xgboost import XGBRegressor, DMatrix
import numpy as np

logger = logging.getLogger("hydrological_zones")
MODEL_STATE_DIRECTORY = "./api/v1/models/hydrological_zones/xgb_model_states/"


def get_hydrological_zone_model(
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
    xgb.load_model(MODEL_STATE_DIRECTORY + "zone_{}.json".format(hydrological_zone))
    inputs = [drainage_area, median_elevation, annual_precipitation]
    inputs = np.array(inputs).reshape((1, -1))
    mean_annual_flow_prediction = xgb.predict(inputs)
    result = ModelOutput(
        mean_annual_flow=mean_annual_flow_prediction,
        r_squared=get_zone_info(hydrological_zone),
    )
    return result


def get_zone_info(zone):
    """
    Returns model fit in r^2 value based on hydrological zone
    """
    with open(MODEL_STATE_DIRECTORY + 'zone_models_r2.json') as zone_models_r2_file:
        zone_r_squares = json.load(zone_models_r2_file)
        return zone_r_squares[str(zone)]

    return None
