"""
Project management endpoints
"""
import os
from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Body
from geojson import FeatureCollection, Feature, Point
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.projects.schema import Project
import api.v1.projects.controller as controller

logger = getLogger("projects")

router = APIRouter()


@router.get("/projects")
def get_user_projects(
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Retrieves a users created projects.
    x_auth_userid holds the keycloak guid that is passed as a
    header up from the proxy service (X-Auth-UserId)
    """
    return controller.get_projects(db, x_auth_userid)


@router.post("/projects")
def create_project(
        project: Project,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Creates a new project and associates it to the user who created it
    """
    return controller.create_project(db, x_auth_userid, project.name, project.description)
