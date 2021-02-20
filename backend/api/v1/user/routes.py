"""
User management endpoints
"""
import os
from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.user.schema import User
import api.v1.user.controller as controller

logger = getLogger("catalogue")

router = APIRouter()


@router.get("/profile")
def get_create_user_profile(
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Checks if user exists in the db first, if not then creates the user,
    then returns the existing or newly created user profile.
    x_auth_userid holds the keycloak guid that is passed as a
    header up from the proxy service (X-Auth-UserId)
    """
    return controller.get_create_user(db, x_auth_userid)


@router.post("/maplayers")
def update_default_map_layers(
        user: User,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Updates the user profile with new default map layers.
    """
    return controller.update_map_layers(db, x_auth_userid, user.map_layers)
