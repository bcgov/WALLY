"""
Project management endpoints
"""
# import os
# import sys
# import uuid
# import magic
# import shutil
# from os import path
# from pathlib import Path
from logging import getLogger
from typing import List, Optional
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, HTTPException, Header, Body, UploadFile, File
from geojson import FeatureCollection, Feature, Point
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.projects.schema import Project
import api.v1.projects.controller as controller
# from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
# from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_415_UNSUPPORTED_MEDIA_TYPE

logger = getLogger("projects")

router = APIRouter()


@router.get("/")
def get_projects(
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Retrieves a users created projects.
    x_auth_userid holds the keycloak guid that is passed as a
    header up from the proxy service (X-Auth-UserId)
    """

    return controller.get_projects_with_documents(db, x_auth_userid)


@router.post("/")
def create_project(
        project: Project,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Creates a new project and associates it to the user who created it
    """

    return controller.create_project(db, x_auth_userid, project.name, project.description)


@router.get("/{project_id}/delete")
def delete_project(
        project_id: int,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Deletes a project and all associated documents
    """

    return controller.delete_project(db, x_auth_userid, project_id)


@router.post("/{project_id}/documents")
def upload_document_to_project(
        project_id: int,
        files: UploadFile = File(...),
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    allows an authenticated user to upload a file of the supported file extension types.
    the file being uploaded in run thru a few filters to determine its type
    """
    return controller.create_and_upload_document(db, x_auth_userid, project_id, files)


@router.get("/documents/{project_document_id}/delete")
def delete_project_document(
        project_document_id: int,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Deletes a project document
    """

    return controller.delete_project_document(db, x_auth_userid, project_document_id)


@router.get("/{project_id}/documents")
def get_project_documents(
        project_id: int,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Gets all documents associated with a project
    """

    return controller.get_documents(db, x_auth_userid, project_id)


@router.get("/documents/{project_document_id}")
def download_project_document(
        project_document_id: int,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Downloads a project document
    """

    return controller.download_project_document(db, x_auth_userid, project_document_id)