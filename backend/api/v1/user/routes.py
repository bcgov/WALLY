"""
User management endpoints
"""
import os
from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.user.schema import User
from api.v1.user.session import get_user
import api.v1.user.controller as controller

logger = getLogger("user")

router = APIRouter()


@router.get("/profile")
def get_create_user_profile(
        user: User = Depends(get_user),
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Checks if user exists in the db first, if not then creates the user,
    then returns the existing or newly created user profile.
    x_auth_userid holds the keycloak guid that is passed as a
    header up from the proxy service (X-Auth-UserId)
    """
    # TODO: Change this to return a user and not a user map layer once user migration is complete
    # User uuid is accessible through user.user_uuid
    return controller.get_create_user_map_layer(db, x_auth_userid)


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
