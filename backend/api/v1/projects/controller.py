import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.projects.db_models import Project
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
