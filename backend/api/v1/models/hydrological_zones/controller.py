import logging
from sqlalchemy.orm import Session
from api.v1.aggregator.controller import feature_search
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
from api.v1.aggregator.helpers import transform_4326_3005
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs, ModelOutput
from xgboost import XGBRegressor

logger = logging.getLogger("hydrological_zones")
MODEL_STATE_DIRECTORY = './xgb_model_states/'

def hydrological_zone_model(hydrological_zone: str, model_inputs: HydroZoneModelInputs):
    """
    Loads the respective zone's xgb model state and returns an estimated
    mean annual flow value for the hydrological zone.
    """
    xgb = XGBRegressor(random_state=42)
    xgb.load_model(MODEL_STATE_DIRECTORY + 'zone_{}.json'.format(hydrological_zone))
    mean_annual_flow_prediction = xgb.predict(*model_inputs)
    result = ModelOutput(mean_annual_flow=mean_annual_flow_prediction)
    return result
    