import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.projects.db_models import Project, ProjectDocument
from api.v1.saved_analyses.db_models import SavedAnalysis, ProjectSavedAnalysis, SavedAnalysisMapLayer
from datetime import datetime

logger = logging.getLogger("projects")


def save_analysis_to_project(db: Session, user_id: str, project_id: int):
    """ Saves an analysis into a project """

    # date = datetime.now()
    analysis = SavedAnalysis(
        project_id=project_id,
        create_date=date,
        update_date=date
    )
    db.add(projectDocument)
    db.commit()



    return projectDocument