"""
Analysis functions for data in the Wally system
"""
import json
from logging import getLogger
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from api.v1.models.hydrological_zones.controller import get_hydrological_zone_model_v1, \
  get_hydrological_zone_model_v2
from api.v1.models.hydrological_zones.schema import HydroZoneModelInputs
from api.db.utils import get_db

logger = getLogger("hydrological_zones")

router = APIRouter()

# returns v1 annual flow estimates based upon 3 model inputs
@router.get("/v1_watershed_drainage_model")
def v1_watershed_drainage_model(
        hydrological_zone: str,
        drainage_area: float,
        median_elevation: float,
        annual_precipitation: float,
        db: Session = Depends(get_db)
):
    if (not hydrological_zone
        or not drainage_area
        or not median_elevation
        or not annual_precipitation
    ):
        raise HTTPException(
            status_code=400, detail="Missing model parameters.")
    
    model_output = get_hydrological_zone_model_v1(
      hydrological_zone,
      drainage_area,
      median_elevation,
      annual_precipitation
    )

    return model_output


# returns v2 annual flow estimates and monthly distributions based upon 2 model inputs
# @router.get("/v2_watershed_drainage_model")
# def v2_watershed_drainage_model(
#         hydrological_zone: str,
#         drainage_area: float,
#         annual_precipitation: float,
#         glacial_coverage: float,
#         glacial_area: float,
#         db: Session = Depends(get_db)
# ):
#     if (not hydrological_zone
#         or not drainage_area
#         or not annual_precipitation
#         # or not glacial_coverage # can be 0
#         # or not glacial_area # can be 0
#     ):
#         raise HTTPException(
#             status_code=400, detail="Missing model parameters.")

#     model_output = get_hydrological_zone_model_v2(
#       hydrological_zone,
#       drainage_area,
#       annual_precipitation,
#       glacial_coverage,
#       glacial_area
#     )

#     return model_output

@router.post("/v2_watershed_drainage_model")
def v2_watershed_drainage_model(
        model_inputs: HydroZoneModelInputs,
        db: Session = Depends(get_db)
):
    print(model_inputs)
    # if (not hydrological_zone
    #     or not drainage_area
    #     or not annual_precipitation
    #     # or not glacial_coverage # can be 0
    #     # or not glacial_area # can be 0
    # ):
    #     raise HTTPException(
    #         status_code=400, detail="Missing model parameters.")

    model_output = get_hydrological_zone_model_v2(
      model_inputs
    )

    return model_output