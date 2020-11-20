import json
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.v1.aggregator.controller import feature_search
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
from api.v1.aggregator.helpers import transform_4326_3005
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs, MeanAnnualFlow, MeanMonthlyFlow
from xgboost import XGBRegressor, DMatrix
import numpy as np
from api.minio.client import minio_client
from minio.error import ResponseError

logger = logging.getLogger("hydrological_zones")

WORKING_DIR = "./api/v1/models/hydrological_zones/working_files/"
V1_ANNUAL_FLOW_BUCKET = "v1/hydro_zone_annual_flow/"
V2_ANNUAL_FLOW_BUCKET = "v2/hydro_zone_annual_flow/"
V2_MONTHLY_DISTRIBUTIONS_BUCKET = "v2/hydro_zone_monthly_distributions/"


def get_hydrological_zone_model_v1(
    hydrological_zone: str,
    drainage_area: float,
    median_elevation: float,
    annual_precipitation: float
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

    # Get model state file from minio storage
    state_object_path = V1_ANNUAL_FLOW_BUCKET + "zone_{}.json".format(hydrological_zone)
    state_file_name = "v1_annual_model_state.json"
    get_set_model_data(state_object_path, state_file_name)

    xgb = XGBRegressor(random_state=42)
    xgb.load_model(state_file_name)
    inputs = [drainage_area, median_elevation, annual_precipitation]
    inputs = np.array(inputs).reshape((1, -1))
    mean_annual_flow_prediction = xgb.predict(inputs)
    mean_annual_flow = MeanAnnualFlow(
        mean_annual_flow=mean_annual_flow_prediction,
        r_squared=get_zone_info(hydrological_zone),
    )

    return mean_annual_flow


def get_zone_info(zone):
    """
    Returns model fit in r^2 value based on hydrological zone
    """
    # Get model state file from minio storage
    r2_file = None
    try:
        r2_file = minio_client.get_object('models', V1_ANNUAL_FLOW_BUCKET + "zone_models_r2.json")
    except ResponseError as err:
        print(err)

    if r2_file:
        zone_r_squares = json.load(r2_file)
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

    # ANNUAL FLOW

    # get annual_model state
    state_object_path = V2_ANNUAL_FLOW_BUCKET + "zone_{}.json".format(hydrological_zone)
    state_file_name = "annual_model_state.json"
    get_set_model_data(state_object_path, state_file_name)

    # get annual_model score
    score_object_path = V2_ANNUAL_FLOW_BUCKET + "annual_model_scores.json"
    score_file_name = "annual_model_scores.json"
    get_set_model_data(score_object_path, score_file_name)

    # load model score
    with open(score_file_name) as json_file:
        scores = json.load(json_file)
        annual_model_score = scores[str(hydrological_zone)]['score']
        best_inputs = scores[str(hydrological_zone)]['best_inputs']

    if len(best_inputs) <= 0: 
        raise HTTPException(
            status_code=400, detail="model inputs not found.")

    # Set best model inputs from scores file
    inputs = np.array(best_inputs).reshape((1, -1))

    # Load model
    try:
        xgb = XGBRegressor(random_state=42)
        xgb.load_model(state_file_name)
    except Exception as error:
        print(error)

    # make annual prediction
    mean_annual_flow_prediction = xgb.predict(inputs)
    mean_annual_flow = MeanAnnualFlow(
        mean_annual_flow=mean_annual_flow_prediction,
        r_squared=annual_model_score
    )

    # MONTHLY FLOW
    
    zone_name = "zone_{}".format(hydrological_zone)
    # get monthly model scores
    monthly_scores_object_path = V2_MONTHLY_DISTRIBUTIONS_BUCKET + zone_name + '/' + 'monthly_model_scores.json'
    monthly_scores_file_name = "monthly_model_scores.json"
    get_set_model_data(monthly_scores_object_path, monthly_scores_file_name)
    
    monthly_scores = {}
    with open(monthly_scores_file_name) as json_file:
        monthly_scores = json.load(json_file)

    monthly_predictions = []
    for month in range(1, 13): # months
        object_path = V2_MONTHLY_DISTRIBUTIONS_BUCKET + zone_name + '/' + str(month) + '.json'
        file_name = "monthly_model_state.json"
        get_set_model_data(object_path, file_name)

        xgb.load_model(file_name)
        mean_monthly_flow_prediction = xgb.predict(inputs)
        month_model_score = monthly_scores[str(month)]
        mean_monthly_flow = MeanMonthlyFlow(
            mean_monthly_flow=mean_monthly_flow_prediction,
            r_squared=month_model_score,
        )
        monthly_predictions.append(mean_monthly_flow)

    result = {
      "mean_annual_flow": mean_annual_flow,
      "mean_monthly_flows": monthly_predictions
    }

    return result


def get_set_model_data(minio_path: str, file_name: str):
    """
    Gets a model object from Minio and sets the file by file_name
    """
    try:
        response = minio_client.get_object('models', minio_path)
        content = response.read().decode('utf-8')
        with open(file_name, "w+") as local_file:
            local_file.write(content)

    except Exception as error:
        logger.warning(error)
