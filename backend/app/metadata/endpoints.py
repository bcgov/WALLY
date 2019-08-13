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


@router.get("/maplayers", response_model=List[view_model.MapLayer])
def list_map_layers(db: Session = Depends(get_db)):
    """
    List all supported map layers
    """
    return meta_repo.get_map_layers(db)


class LayerNames(BaseModel):
    layer_names: List[str] = []


@router.post("/contextdata")
def get_context_data(layer_names: LayerNames, db: Session = Depends(get_db)):
    return meta_repo.get_context_data(layer_names, db)


