"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from api.v1.hydat import routes as hydat_streams
from api.v1.catalogue import routes as catalogue
from api.v1.aggregator import routes as aggregator
from api.v1.geocoder import routes as geocoder
from api.v1.licences import routes as licences
from api.v1.streams import routes as streams
from api.v1.stream import routes as stream
from api.v1.firstnations import routes as firstnations
from api.v1.wells import routes as wells
from api.v1.watersheds import routes as watersheds
from api.v1.config import routes as config

api_router = APIRouter()

api_router.include_router(
    catalogue.router,
    prefix="/catalogue",
    tags=["catalogue"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    aggregator.router,
    prefix="/aggregate",
    tags=["aggregate"],
    responses={404: {"description": "Not found"}},
)

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

api_router.include_router(
    licences.router,
    prefix="/licences",
    tags=["licences"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    config.router,
    prefix="/config",
    tags=["config"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    watersheds.router,
    prefix="/watersheds",
    tags=["watersheds"],
    responses={404: {"description": "Not found"}},
)
