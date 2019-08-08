"""
Map layers (layers module) API endpoints/handlers.
"""
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.meta.db as meta_repo

logger = getLogger("api")

router = APIRouter()


@router.get("/layers/wms")
def list_wms_layers(db: Session = Depends(get_db)):
    """
    List all supported wms layers and their config
    """
    return meta_repo.get_wms_layers(db)


@router.get("/layers/wms/{id}/columns")
def list_wms_layers(db: Session = Depends(get_db)):
    """
    List all supported wms layers and their config
    """
    return meta_repo.get_wms_layers(db)


@router.get("/layers/api")
def list_api_layers(db: Session = Depends(get_db)):
    """
    List all supported api layers and their config
    """
    return meta_repo.get_api_layers(db)


@router.get("/datamarts")
def list_data_marts(db: Session = Depends(get_db)):
    """
    List all data marts in wally
    """
    return meta_repo.get_data_marts(db)
