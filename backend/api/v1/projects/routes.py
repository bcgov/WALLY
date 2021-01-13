"""
Project management endpoints
"""
import os
import sys
import uuid
import magic
import shutil
from os import path
from pathlib import Path
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
from api.minio.client import minio_client
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_415_UNSUPPORTED_MEDIA_TYPE

logger = getLogger("projects")

router = APIRouter()

ALLOWED_FILE_EXTENSIONS = [".gif", ".jpg", ".jpeg", ".txt", ".geojson", ".json",
                           ".png", ".pdf", ".doc", ".docx", ".csv", ".xlsx"]
PROJECTS_BUCKET_NAME = "projects"


@router.get("/")
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
    file = files
    file_ext = get_file_ext(file.filename)
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        logger.warning("upload_document - Unsupported media type")
        raise HTTPException(status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'unsupported media type: {file_ext}')
    
    print('filename', file.filename)
    print('content_type', file.content_type)
    print('extension', file_ext)
    # print('starting - Stage 1')

    try:
        replacement_file_name = generate_file_name(file.filename)
        with NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_upload_file_path = Path(tmp.name)
            new_file_path = str(tmp_upload_file_path.resolve())
    except Exception as exc:
        error_msg = f'error: {sys.exc_info()[0]}'
        logger.error(
            f'upload_document - Unknown Error During Upload Process {error_msg}')
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unknown Error During Upload Process - Stage 1')
    finally:
        if file.file:
            file.file.close()

    # print('starting - Stage 2')
    try:
        # get the content type
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(new_file_path)
        s3_path = '{}/{}'.format(project_id, replacement_file_name)
        # send file to minio
        upload = upload_file_to_minio(
            s3_path, new_file_path, content_type)
        # create new document in database once upload is successful
        document = controller.create_document(
            db, x_auth_userid, project_id, s3_path, file.filename)
        return document

    except FileNotFoundError as exc:
        logger.error(f'upload_file - unknown upload error - {str(exc)}')
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unknown Error Uploading File - FileNotFound - {str(exc)} - Stage 2')
    except Exception as exc:
        error_msg = f'error: {sys.exc_info()[0]}'
        logger.error(
            f'upload_file - Unknown Error During Upload Process {error_msg} {exc}')
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unknown Error During Upload Process - Stage 2')
    finally:
        try:
            tmp_upload_file_path.unlink()
        except:
            pass


def upload_file_to_minio(destination_file_name: str, local_file_path: str, content_type: str):
    """
    Uploads a file to s3 Minio storage and returns the file response object
    """
    if not path.exists(local_file_path):
        raise FileNotFoundError(
            f'file_path: {local_file_path} is not a valid file')

    try:
        # filesize = os.stat(local_file_path).st_size
        # metadata = {
        #   'category': 'general',
        # }
        result = minio_client.fput_object(bucket_name=PROJECTS_BUCKET_NAME,
                                          object_name=destination_file_name,
                                          file_path=local_file_path,
                                          content_type=content_type
                                          # metadata=metadata
                                          )
        return result
    except Exception as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unknown Error During Upload Process {exc}')


def get_file_ext(file_path: str) -> str:
    file_name, file_extension = os.path.splitext(file_path)
    return file_extension


def get_file_name(file_path: str) -> str:
    file_name, file_extension = os.path.splitext(file_path)
    return file_name


def generate_file_name(file_name: str) -> str:
    file_ext = get_file_ext(file_name)
    return f'{str(uuid.uuid4())}{file_ext}'
