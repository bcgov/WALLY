"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from api.hydat.endpoints import router as hydat_streams_v1
from api.metadata.endpoints import router as metadata_v1
from api.aggregator.endpoints import router as aggregator_v1
from api.geocoder.endpoints import router as geocoder_v1
from api.analysis.endpoints import router as analysis_v1
from api.v1.streams import routes as streams
from api.v1.stream import routes as stream

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

api_router.include_router(
    stream.router,
    prefix="/stream",
    tags=["stream"],
    responses={404: {"description": "Not found"}},
)
