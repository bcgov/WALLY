"""
Project management endpoints
"""
from logging import getLogger
from typing import List, Optional
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, HTTPException, Header, Body, UploadFile, File
from geojson import FeatureCollection, Feature, Point
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.projects.schema import Project, ProjectDocument, ProjectCreate
import api.v1.projects.controller as controller
from api.v1.user.db_models import User
from api.v1.user.session import get_user

logger = getLogger("projects")

router = APIRouter()


@router.get("", response_model=List[Project])
def get_projects(
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Retrieves a users created projects.
    x_auth_subject holds the keycloak guid that is passed as a
    header up from the proxy service (X-Auth-Subject)
    """
    
    return controller.get_projects_with_documents(db, user.user_uuid)


@router.post("", response_model=Project)
def create_project(
        project: ProjectCreate,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Creates a new project and associates it to the user who created it
    """

    return controller.create_project(db, user.user_uuid, project.name, project.description)


@router.get("/{project_uuid}/delete", response_model=bool)
def delete_project(
        project_uuid: str,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Deletes a project and all associated documents
    """

    return controller.delete_project(db, user.user_uuid, project_uuid)


@router.post("/{project_uuid}/documents", response_model=ProjectDocument)
def upload_document_to_project(
        project_uuid: str,
        files: UploadFile = File(...),
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    allows an authenticated user to upload a file of the supported file extension types.
    the file being uploaded is run thru a few filters to determine its type
    """
    return controller.create_and_upload_document(db, user.user_uuid, project_uuid, files)


@router.get("/documents/{project_document_uuid}/delete", response_model=bool)
def delete_project_document(
        project_document_uuid: str,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Deletes a project document
    """

    return controller.delete_project_document(db, user.user_uuid, project_document_uuid)


@router.get("/{project_uuid}/documents", response_model=List[ProjectDocument])
def get_project_documents(
        project_uuid: str,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Gets all documents associated with a project
    """

    return controller.get_documents(db, user.user_uuid, project_uuid)


@router.get("/documents/{project_document_uuid}")
def download_project_document(
        project_document_uuid: str,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Downloads a project document
    """

    return controller.download_project_document(db, user.user_uuid, project_document_uuid)


@router.get("/{project_uuid}/download")
def download_project(
        project_uuid: str,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    """
    Downloads a projects documents in zip format
    """

    return controller.download_project(db, user.user_uuid, project_uuid)
