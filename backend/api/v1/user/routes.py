"""
User management endpoints
"""
import os
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from geojson import FeatureCollection, Feature, Point
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.user.schema import User
import api.v1.user.controller as controller

logger = getLogger("catalogue")

router = APIRouter()


@router.post("/profile")
def get_create_user_profile(
        req: User,
        db: Session = Depends(get_db)
):
    """
    Checks if user exists in the db first, if not then creates the user,
    then returns the existing or newly created user profile.
    """
    return controller.get_create_user(db, req.uuid)


@router.post("/maplayers")
def update_default_map_layers(
        req: User,
        db: Session = Depends(get_db)
):
    """
    Updates the user profile with new default map layers.
    """
    return controller.update_map_layers(db, req)
