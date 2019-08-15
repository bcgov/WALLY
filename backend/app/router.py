"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from app.hydat.endpoints import router as streamsv1
from app.metadata.endpoints import router as metadatav1
from app.aggregator.endpoints import router as aggregator_v1

api_router = APIRouter()

api_router.include_router(streamsv1)
api_router.include_router(metadatav1)
api_router.include_router(aggregator_v1)
