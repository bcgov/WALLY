"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from api.v1.hydat import routes as hydat_streams
from api.metadata.endpoints import router as metadata_v1
from api.aggregator.endpoints import router as aggregator_v1
from api.v1.geocoder import routes as geocoder
from api.analysis.endpoints import router as analysis_v1
from api.v1.streams import routes as streams
from api.v1.stream import routes as stream
from api.v1.firstnations import routes as firstnations
from api.v1.wells import routes as wells

api_router = APIRouter()

api_router.include_router(metadata_v1)
api_router.include_router(aggregator_v1)
api_router.include_router(analysis_v1)


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

api_router.include_router(
    geocoder.router,
    prefix="/geocoding",
    tags=["geocoding"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    hydat_streams.router,
    prefix="/hydat",
    tags=["hydat"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    firstnations.router,
    prefix="/firstnations",
    tags=["firstnations"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    wells.router,
    prefix="/wells",
    tags=["wells"],
    responses={404: {"description": "Not found"}},
)
