import os
import io
import sys
import json
import magic
import shutil
import logging
import zipfile
from os import path
from pathlib import Path
from typing import List, Optional
from fastapi.responses import StreamingResponse, Response
from sqlalchemy import text, func
from sqlalchemy.orm import Session, joinedload
from tempfile import NamedTemporaryFile
from api.v1.projects.db_models import Project, ProjectDocument
from fastapi import UploadFile, HTTPException
from datetime import datetime
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_415_UNSUPPORTED_MEDIA_TYPE
from api.minio.client import minio_client, s3_upload_file, s3_delete_file, s3_list_directory, s3_get_file
from api.utils import get_file_ext, get_file_name, generate_file_name

logger = logging.getLogger("projects")


ALLOWED_FILE_EXTENSIONS = [".gif", ".jpg", ".jpeg", ".txt", ".geojson", ".json",
                           ".png", ".pdf", ".doc", ".docx", ".csv", ".xlsx", ".kml"]
PROJECTS_BUCKET_NAME = "projects"


def get_projects(db: Session, user_uuid: str):
    """ gets all projects that a user is associated with """

    projects = db.query(Project).filter(Project.user_uuid == user_uuid).all()

    return projects


def get_projects_with_documents(db: Session, user_uuid: str):
    """ gets all projects that a user is associated with, and associated documents """
    projects_with_documents = db.query(Project).options(joinedload(Project.children)) \
        .filter(Project.user_uuid == user_uuid) \
        .all()

    return projects_with_documents


def create_project(db: Session, user_uuid: str, project_name: str, project_description: str):
    """ creates a new project associated with a user """
    date = datetime.now()
    project = Project(
        name=project_name,
        description=project_description,
        user_uuid=user_uuid,
        create_date=date,
        update_date=date
    )
    db.add(project)
    db.commit()

    return project


def delete_project(db: Session, user_uuid: str, project_id: int):
    """ deletes a project and all associated documents """
    try:
        project_with_documents = db.query(Project).options(joinedload(Project.children)) \
          .filter(Project.project_id == project_id) \
          .filter(Project.user_uuid == user_uuid) \
          .one()

        print('deleting s3 project files')
        for doc in project_with_documents.children:
            # delete document from minio
            s3_delete_file(PROJECTS_BUCKET_NAME, doc.s3_path)
            # delete document in database
            db.delete(doc)

        db.delete(project_with_documents)

        db.commit()
        return True
    except Exception as exc:
        logger.error(exc)
        return False


def get_documents(db: Session, user_uuid: str, project_id: int):
    """ gets all project documents """

    documents = db.query(ProjectDocument) \
      .filter(ProjectDocument.project_id == project_id) \
      .all()

    return documents


def create_and_upload_document(db: Session, user_uuid: str, project_id: int, files: UploadFile):
    file = files

    file_ext = get_file_ext(file.filename)
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        logger.warning("upload_document - Unsupported media type")
        raise HTTPException(status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'unsupported media type: {file_ext}')

    # print('filename', file.filename)
    # print('content_type', file.content_type)
    # print('extension', file_ext)
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
        upload = s3_upload_file(
            s3_path, new_file_path, content_type, PROJECTS_BUCKET_NAME)
        # create new document in database once upload is successful
        document = create_document(
            db, user_uuid, project_id, s3_path, file.filename)
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


def create_document(db: Session, user_uuid: str, project_id: int, s3_path: str, filename: str):
    """ creates a new project document """

    date = datetime.now()
    project_document = ProjectDocument(
        project_id=project_id,
        s3_path=s3_path,
        filename=filename,
        create_date=date,
        update_date=date
    )
    db.add(project_document)
    db.commit()

    return project_document


def delete_project_document(db: Session, user_uuid: str, project_document_id: int):
    """ deletes a document object """
    try:
        print('deleting document')
        document = db.query(ProjectDocument) \
          .filter(ProjectDocument.project_document_id == project_document_id) \
          .one()

        print('document', document)

        project = db.query(Project) \
          .filter(Project.project_id == document.project_id) \
          .one()

        print('project', project)

        # only allow the project owner to delete the document
        if project.user_uuid == user_uuid:
            try:
                file_deleted = s3_delete_file(PROJECTS_BUCKET_NAME, document.s3_path)
                db.delete(document)
                db.commit()
            except Exception as exc:
                error_msg = f'error: {sys.exc_info()[0]}'
                logger.error(
                    f'delete_project_document - Unknown Error During Delete Process {error_msg} {exc}')
                raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f'Unknown Error During Document Delete Process')

        return True
    except FileNotFoundError as exc:
        logger.error(
                    f'delete_project_document - FileNotFound - {error_msg} {exc}')
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'FileNotFound')

        return False


def download_project_document(db: Session, user_uuid: str, project_document_id: int):
    """ gets a project document and downloads it to the client """

    document = db.query(ProjectDocument) \
      .filter(ProjectDocument.project_document_id == project_document_id) \
      .one()

    project = db.query(Project) \
      .filter(Project.project_id == document.project_id) \
      .one()

    # only allow the project owner to download the document
    if project.user_uuid == user_uuid:
        try:
            response = StreamingResponse(s3_get_file(PROJECTS_BUCKET_NAME, document.s3_path))
            response.headers['Content-Disposition'] = document.filename
            return response
        except Exception as error:
            logger.warning(error)


def download_project(db: Session, user_uuid: str, project_id: int):
    """ gets all a projects documents and downloads them as a zip file """

    project_with_documents = db.query(Project).options(joinedload(Project.children)) \
      .filter(Project.project_id == project_id) \
      .filter(Project.user_uuid == user_uuid) \
      .one()

    # only allow the project owner to download the document
    if project_with_documents.user_uuid == user_uuid:
        documents = []
        # get all project documents
        for document in project_with_documents.children:
            result = s3_get_file(PROJECTS_BUCKET_NAME, document.s3_path)
            documents.append({"filename": document.filename, "data": result.read()})

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for doc in documents:
                zip_file.writestr(doc["filename"], doc["data"])
        try:
            response = Response(zip_buffer.getvalue())
            response.headers['Content-Disposition'] = 'project_{}.zip'.format(project_id)
            return response
        except Exception as error:
            logger.warning(error)
