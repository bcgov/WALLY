import json
import datetime
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
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
MODELLING_BUCKET_NAME = 'modelling'
V1_ANNUAL_FLOW_BUCKET = "v1/hydro_zone_annual_flow/"
V2_ANNUAL_FLOW_BUCKET = "v2/hydro_zone_annual_flow/"
V2_MONTHLY_DISTRIBUTIONS_BUCKET = "v2/hydro_zone_monthly_distributions/"


def get_hydrological_zone_model_v1(
    hydrological_zone: int,
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

    hydrological_zone = str(hydrological_zone)

    # Get model state file from minio storage
    state_object_path = V1_ANNUAL_FLOW_BUCKET + "zone_{}.json".format(hydrological_zone)
    model_ba = load_raw_model_data(state_object_path)

    xgb = XGBRegressor(random_state=42)
    xgb.load_model(model_ba)
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
        r2_file = minio_client.get_object(MODELLING_BUCKET_NAME, V1_ANNUAL_FLOW_BUCKET + "zone_models_r2.json")
    except ResponseError as err:
        logger.warning(err)

    if r2_file:
        zone_r_squares = json.load(r2_file)
        return zone_r_squares[str(zone)]

    return None


def get_hydrological_zone_model_v2(
    model_inputs: HydroZoneModelInputs
):
    """
    Loads the respective zone's xgb model state and returns an estimated
    mean annual flow value for the hydrological zone.
    """
    input_values = model_inputs.dict()
    hydrological_zone = str(model_inputs.hydrological_zone)

    # ANNUAL FLOW

    # get annual_model state
    state_object_path = V2_ANNUAL_FLOW_BUCKET + "zone_{}.json".format(hydrological_zone)
    state_file_name = "annual_model_state.json"
    load_model_data(state_object_path, state_file_name)

    # get annual_model score
    score_object_path = V2_ANNUAL_FLOW_BUCKET + "annual_model_scores.json"
    score_file_name = "annual_model_scores.json"
    load_model_data(score_object_path, score_file_name)

    # load model score
    with open(score_file_name) as json_file:
        scores = json.load(json_file)
        annual_model_score = scores[hydrological_zone]['score']
        best_inputs = scores[hydrological_zone]['best_inputs']

    if len(best_inputs) <= 0: 
        raise HTTPException(
            status_code=400, detail="model inputs not found.")

    # Set best model inputs from scores file
    # extract inputs from request params
    inputs = [input_values[x] for x in best_inputs]
    inputs = np.array(inputs).reshape((1, len(inputs)))

    # Load model
    try:
        xgb = XGBRegressor(random_state=42)
        xgb.load_model(state_file_name)
    except Exception as error:
        logger.warning(error)

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
    load_model_data(monthly_scores_object_path, monthly_scores_file_name)

    monthly_scores = {}
    with open(monthly_scores_file_name) as json_file:
        monthly_scores = json.load(json_file)

    monthly_predictions = []
    for month in range(1, 13): # months
        object_path = V2_MONTHLY_DISTRIBUTIONS_BUCKET + zone_name + '/' + str(month) + '.json'
        monthly_state_file_name = "monthly_model_state.json"
        load_model_data(object_path, monthly_state_file_name)

        month_model_score = monthly_scores[str(month)]['score']
        month_best_inputs = monthly_scores[str(month)]['best_inputs']
        # extract inputs from request params
        month_inputs = [input_values[x] for x in month_best_inputs]
        month_inputs = np.array(month_inputs).reshape((1, -1))

        try:
            xgb_month = XGBRegressor(random_state=42)
            xgb_month.load_model(monthly_state_file_name)
        except Exception as error:
            logger.warning(error)

        mean_monthly_flow_prediction = xgb_month.predict(month_inputs)
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


def load_model_data(minio_path: str, file_name: str):
    """
    Gets a model object from Minio and sets the file by file_name
    """
    try:
        response = minio_client.get_object(MODELLING_BUCKET_NAME, minio_path)
        content = response.read().decode('utf-8')
        with open(file_name, "w+") as local_file:
            local_file.write(content)

    except Exception as error:
        logger.warning(error)


def load_raw_model_data(minio_path: str):
    """
    Gets and returns bytearray format of a model object from Minio
    """
    try:
        response = minio_client.get_object(MODELLING_BUCKET_NAME, minio_path)
        content = bytearray(response.read()) #.decode('utf-8')
        return content

    except Exception as error:
        logger.warning(error)


def download_training_data(model_version: str, hydrological_zone: int):
    """
    Gets the model training data from Minio using model version and hydro zone
    """
    cur_date = datetime.datetime.now().strftime("%d-%m-%Y")
    name = 'zone_{}.zip'.format(str(hydrological_zone))
    minio_path = '/{}/training_data/{}'.format(model_version, name)
    try:
        response = StreamingResponse(
          minio_client.get_object(MODELLING_BUCKET_NAME, minio_path),
          media_type='application/zip')
        file_name = 'training-data-' + cur_date + "-" + name
        response.headers['Content-Disposition'] = f'attachment;filename={file_name}'
        return response
    except Exception as error:
        logger.warning(error)


def download_training_report(model_version: str, hydrological_zone: int):
    """
    Gets the model training report for the best fold from Minio using model version and hydro zone
    """
    cur_date = datetime.datetime.now().strftime("%d-%m-%Y")
    name = 'zone_{}.zip'.format(str(hydrological_zone))
    minio_path = '/{}/training_reports/{}'.format(model_version, name)
    try:
        response = StreamingResponse(
          minio_client.get_object(MODELLING_BUCKET_NAME, minio_path),
          media_type='application/zip')
        file_name = 'training-report-' + cur_date + "-" + name
        response.headers['Content-Disposition'] = f'attachment;filename={file_name}'
        return response
    except Exception as error:
        logger.warning(error)
