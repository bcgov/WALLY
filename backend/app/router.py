"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from app.hydat.endpoints import router as hydat_streams_v1
from app.metadata.endpoints import router as metadata_v1
from app.aggregator.endpoints import router as aggregator_v1
from app.geocoder.endpoints import router as geocoder_v1
from app.analysis.endpoints import router as analysis_v1
from app.v1.streams import endpoints as streams
# from app.v1.router import streams

api_router = APIRouter()

api_router.include_router(metadata_v1)
api_router.include_router(aggregator_v1)
api_router.include_router(geocoder_v1)
api_router.include_router(analysis_v1)
api_router.include_router(hydat_streams_v1)


api_router.include_router(
    streams.router,
    prefix="/streams",
    tags=["streams"],
    responses={404: {"description": "Not found"}},
)
