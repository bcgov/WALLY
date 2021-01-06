import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.projects.db_models import Project, ProjectDocument
from datetime import datetime

logger = logging.getLogger("projects")


def get_projects(db: Session, user_id: str):
    """ gets all projects that a user is associated with """

    projects = db.query(Project).filter(Project.user_id == user_id).all()

    return projects


def create_project(db: Session, user_id: str, project_name: str, project_description: str):
    """ creates a new project associated with a user """

    date = datetime.now()
    project = Project(
        name=project_name,
        description=project_description,
        user_id=user_id,
        create_date=date,
        update_date=date
    )
    db.add(project)
    db.commit()

    return project


def get_documents(db: Session, user_id: str, project_id: int):
    """ gets all project documents """

    documents = db.query(ProjectDocument) \
      .filter(ProjectDocument.project_id == project_id) \
      .all()

    return documents


def create_document(db: Session, user_id: str, project_id: int, s3_path: str, filename: str):
    """ creates a new project document """

    date = datetime.now()
    projectDocument = ProjectDocument(
        project_id=project_id,
        s3_path=s3_path,
        filename=filename,
        create_date=date,
        update_date=date
    )
    db.add(projectDocument)
    db.commit()

    return projectDocument