"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from app.hydat.endpoints import router as streams_v1
from app.metadata.endpoints import router as metadata_v1
from app.aggregator.endpoints import router as aggregator_v1
from app.geocoder.endpoints import router as geocoder_v1
from app.utils.endpoints import router as utils_v1
api_router = APIRouter()

api_router.include_router(streams_v1)
api_router.include_router(metadata_v1)
api_router.include_router(aggregator_v1)
api_router.include_router(geocoder_v1)
api_router.include_router(utils_v1)
