import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.projects.db_models import Project, ProjectDocument
from api.v1.saved_analyses.db_models import SavedAnalysis, SavedAnalysisMapLayer
from datetime import datetime

logger = logging.getLogger("projects")


def save_analysis(db: Session, user_id: str, name: str, description: str,
                  geometry: str, feature_type: str, zoom_level: int,
                  map_layers: [], project_id: int = None):
    # validate geometry

    # validate map layers

    # validate feature type

    # validate zoom level

    analysis = SavedAnalysis(user_id=user_id,
                             name=name,
                             description=description,
                             geometry=geometry,
                             feature_type=feature_type,
                             zoom_level=zoom_level,
                             project_id=project_id)
    db.add(analysis)
    db.flush()

    for layer in map_layers:
        saved_analysis_map_layer = SavedAnalysisMapLayer(
            analysis.saved_analysis_id,
            layer
        )
        db.add(saved_analysis_map_layer)


def get_saved_analyses(db: Session, user_id: str):
    analyses = db.query(SavedAnalysis) \
        .filter(SavedAnalysis.user_id == user_id) \
        .all()

    return analyses
