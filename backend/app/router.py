"""
Registers endpoints from different apps.
"""
from fastapi import APIRouter

from app import config
from app.hydat.endpoints import router as streamsv1

api_router = APIRouter()

api_router.include_router(streamsv1)
