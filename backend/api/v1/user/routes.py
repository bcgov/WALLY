"""
User management endpoints
"""
import os
from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.user.db_models import User
from api.v1.user.session import get_user
from api.v1.user.schema import UpdateMapLayers
import api.v1.user.controller as controller

logger = getLogger("user")

router = APIRouter()


@router.get("/profile")
def get_create_user_profile(
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    returns the user and saved map layers
    """
    map_layers = controller.get_create_user_map_layer(db, user.user_idir)
    result = {
        **user.__dict__,
        "default_map_layers": map_layers.default_map_layers
    }
    return result


@router.post("/maplayers")
def update_default_map_layers(
        map_layers: UpdateMapLayers,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Updates the user profile with new default map layers.
    """
    return controller.update_map_layers(db, user, map_layers.map_layers)
