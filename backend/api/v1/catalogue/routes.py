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
import api.v1.catalogue.schema as schema

logger = getLogger("catalogue")

router = APIRouter()


@router.get("/all", response_model=schema.Catalogue)
def list_catalogue(db: Session = Depends(get_db)):
    """
    List all supported catalogue entries
    """
    layers = [schema.Layer.from_orm(layer)
              for layer in meta_repo.get_display_catalogue(db)]
    categories = [schema.LayerCategory.from_orm(
        category) for category in meta_repo.get_layer_categories(db)]

    return schema.Catalogue(layers=layers, categories=categories)

