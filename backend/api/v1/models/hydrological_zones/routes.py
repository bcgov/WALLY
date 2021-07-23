"""
Analysis functions for data in the Wally system
"""
from logging import getLogger
from fastapi import APIRouter
from api.v1.models.hydrological_zones.controller import xgboost_hydrological_zone_model, \
  download_training_data, download_training_report
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs

logger = getLogger("hydrological_zones")

router = APIRouter()


@router.post("/watershed_drainage_model")
def v2_watershed_drainage_model(
        model_inputs: HydroZoneModelInputs
):
    model_output = xgboost_hydrological_zone_model(model_inputs)
    return model_output


@router.get("/training_data/download")
def get_training_data(
        model_name: str,
        hydrological_zone: int
):
    return download_training_data(model_name, hydrological_zone)


@router.get("/training_report/download")
def get_training_report(
        model_name: str,
        hydrological_zone: int
):
    return download_training_report(model_name, hydrological_zone)
