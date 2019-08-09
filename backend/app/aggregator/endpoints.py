"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.hydat.db as streams_repo
import app.hydat.models as streams_v1

logger = getLogger("api")

router = APIRouter()


@router.get("/aggregate")
def aggregate_sources():
    pass
