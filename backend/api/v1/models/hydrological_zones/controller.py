import json
import datetime
import logging
import numpy as np
from xgboost import XGBRegressor
from api.minio.client import minio_client
from fastapi.responses import StreamingResponse
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs, \
  MeanAnnualRunoff, MeanMonthlyRunoff


logger = logging.getLogger("hydrological_zones")

MODELLING_BUCKET_NAME = 'modelling'
MAR_ANNUAL_PATH = 'models/mar_annual/'
MAR_MONTHLY_PATH = 'models/mar_monthly/'


def xgboost_hydrological_zone_model(
    model_inputs: HydroZoneModelInputs
):
    mean_annual_runoff = xgboost_mar_annual(model_inputs)
    mean_monthly_runoff = xgboost_mar_monthly(model_inputs)

    return {
      "mean_annual_runoff": mean_annual_runoff,
      "mean_monthly_runoff": mean_monthly_runoff
    }


def xgboost_mar_annual(
    model_inputs: HydroZoneModelInputs
):
    """
    Loads the respective zone's xgb model state and returns an estimated
    mean annual flow value for the hydrological zone.
    """
    input_values = model_inputs.dict()
    hydrological_zone = str(model_inputs.hydrological_zone)

    # Mean Annual Runoff Score
    score_object_path = MAR_ANNUAL_PATH + "model_scores.json"
    score_ba = load_minio_data(score_object_path)
    scores = json.load(score_ba)
    model_score = scores[hydrological_zone]

    # Mean Annual Runoff Model
    state_object_path = MAR_ANNUAL_PATH + "zone_{}.json".format(hydrological_zone)
    model_ba = load_minio_data(state_object_path)

    # Reshape inputs for model load
    inputs = [*input_values]
    inputs = np.array(inputs).reshape((1, len(inputs)))

    # Load MAR model
    try:
        xgb = XGBRegressor(random_state=42)
        xgb.load_model(model_ba)
    except Exception as error:
        logger.warning(error)

    # Make prediction
    mean_annual_runoff_prediction = xgb.predict(inputs)
    
    return MeanAnnualRunoff(
        mean_annual_runoff=mean_annual_runoff_prediction,
        model_score=model_score
    )


def xgboost_mar_monthly(
    model_inputs: HydroZoneModelInputs
):
    """
    Loads the respective zone's xgb model state and returns an estimated
    mean annual flow value for the hydrological zone.
    """

    input_values = model_inputs.dict()
    hydrological_zone = str(model_inputs.hydrological_zone)
    zone_name = "zone_{}".format(hydrological_zone)

    # Mean monthly runoff scores
    scores_object_path = MAR_MONTHLY_PATH + zone_name + '/' + 'model_scores.json'
    scores_ba = load_minio_data(scores_object_path)
    scores = json.load(scores_ba)

    # Make mean monthly runoff predictions 
    monthly_predictions = []
    for month in range(1, 13): # months
        # Each month model score
        month_model_score = scores[str(month)]

        # Mean Annual Runoff Model
        state_object_path = MAR_ANNUAL_PATH + zone_name + '/' + "zone_{}.json".format(hydrological_zone)
        model_ba = load_minio_data(state_object_path)

        # Reshape inputs for model load
        inputs = [*input_values]
        inputs = np.array(inputs).reshape((1, len(inputs)))

        try:
            xgb_month = XGBRegressor(random_state=42)
            xgb_month.load_model(model_ba)
        except Exception as error:
            logger.warning(error)

        mean_monthly_runoff_prediction = xgb_month.predict(inputs)
        mean_monthly_runoff = MeanMonthlyRunoff(
            mean_monthly_runoff=mean_monthly_runoff_prediction,
            model_score=month_model_score,
        )
        monthly_predictions.append(mean_monthly_runoff)
    
    return monthly_predictions


def load_minio_data(minio_path: str):
    """
    Gets and returns bytearray format of an object from Minio
    """
    try:
        response = minio_client.get_object(MODELLING_BUCKET_NAME, minio_path)
        content = bytearray(response.read())
        return content
    except Exception as error:
        logger.warning(error)


def download_training_data(model_name: str, hydrological_zone: int):
    """
    Gets the model training data from Minio using model version and hydro zone
    """
    cur_date = datetime.datetime.now().strftime("%d-%m-%Y")
    zone_name = 'zone_{}.zip'.format(str(hydrological_zone))
    minio_path = '/training_data/{}/{}'.format(model_name, zone_name)
    try:
        response = StreamingResponse(
          minio_client.get_object(MODELLING_BUCKET_NAME, minio_path),
          media_type='application/zip')
        file_name = 'training-data-' + cur_date + "-" + zone_name
        response.headers['Content-Disposition'] = f'attachment;filename={file_name}'
        return response
    except Exception as error:
        logger.warning(error)


def download_training_report(model_name: str, hydrological_zone: int):
    """
    Gets the model training report for the best fold from Minio using model version and hydro zone
    """
    cur_date = datetime.datetime.now().strftime("%d-%m-%Y")
    zone_name = 'zone_{}.zip'.format(str(hydrological_zone))
    minio_path = '/training_reports/{}/{}'.format(model_name, zone_name)
    try:
        response = StreamingResponse(
          minio_client.get_object(MODELLING_BUCKET_NAME, minio_path),
          media_type='application/zip')
        file_name = 'training-report-' + cur_date + "-" + zone_name
        response.headers['Content-Disposition'] = f'attachment;filename={file_name}'
        return response
    except Exception as error:
        logger.warning(error)
