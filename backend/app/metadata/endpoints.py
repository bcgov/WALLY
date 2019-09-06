"""
Map layers (layers module) API endpoints/handlers.
"""
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from geojson import FeatureCollection, Feature, Point
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.metadata.db as meta_repo
import app.metadata.models as view_model

logger = getLogger("api")

router = APIRouter()


@router.get("/catalogue", response_model=List[view_model.Catalogue])
def list_catalogue(db: Session = Depends(get_db)):
    """
    List all supported catalogue entries
    """
    return meta_repo.get_display_catalogue(db)

