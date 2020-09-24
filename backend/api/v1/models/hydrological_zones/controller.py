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


def hydrological_zone_model(
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
    logger.warning(mean_annual_flow_prediction)
    result = ModelOutput(
        mean_annual_flow=mean_annual_flow_prediction,
        r_squared=zone_info(hydrological_zone),
    )
    return result


def zone_info(zone):
    """
    Returns model fit in r^2 value based on hydrological zone
    """
    r_squares = {
        1: 0.5505,
        2: 0.7847,
        3: 0.9471,
        4: 0.9256,
        5: -0.2123,
        6: 0.7902,
        7: 0.582,
        8: 0.9487,
        9: 0.3911,
        10: 0.983,
        11: 0.5981,
        12: 0.8577,
        13: 0.6475,
        14: 0.8629,
        15: 0.6826,
        16: 0.6963,
        17: 0.4159,
        18: 0.9905,
        19: 0.5956,
        20: 0.5565,
        21: 0.8606,
        22: 0.7755,
        23: 0.6376,
        24: 0.2729,
        25: 0.9048,
        26: 0.654,
        27: 0.827,
        28: 0.8762,
        29: 0.806,
    }

    return r_squares[zone]
