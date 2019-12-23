"""
Map layers (layers module) API endpoints/handlers.
"""
import os
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from geojson import FeatureCollection, Feature, Point
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.utils import get_db
import api.v1.catalogue.db as meta_repo
import api.v1.catalogue.models as view_model

logger = getLogger("api")

router = APIRouter()


@router.get("/catalogue", response_model=view_model.Catalogue)
def list_catalogue(db: Session = Depends(get_db)):
    """
    List all supported catalogue entries
    """
    layers = [view_model.Layer.from_orm(layer)
              for layer in meta_repo.get_display_catalogue(db)]
    categories = [view_model.LayerCategory.from_orm(
        category) for category in meta_repo.get_layer_categories(db)]

    return view_model.Catalogue(layers=layers, categories=categories)

