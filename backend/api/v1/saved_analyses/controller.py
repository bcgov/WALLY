import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.projects.db_models import Project, ProjectDocument
from api.v1.saved_analyses.db_models import SavedAnalysis, SavedAnalysisMapLayer
from uuid import UUID

logger = logging.getLogger("projects")


def save_analysis(db: Session, user_id: str,
                  name: str, description: str,
                  geometry: str, feature_type: str, zoom_level: float,
                  map_layers: [], project_id: int = None):
    # validate user
    # validate geometry
    # try:
    #     geom = wkt.loads(geometry)
    # except shapely.errors.WKTReadingError e:
    #     raise ValueError('Invalid geometry')

        # return ValidationError
    # print('geom is')
    # print(geom)

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
    print(analysis)
    db.add(analysis)
    db.flush()

    print('ID is')
    print(analysis.saved_analysis_uuid)

    for layer in map_layers:

        saved_analysis_map_layer = SavedAnalysisMapLayer(
            saved_analysis_uuid=analysis.saved_analysis_uuid,
            map_layer=layer
        )
        db.add(saved_analysis_map_layer)

    db.commit()
    return get_saved_analysis(analysis.saved_analysis_uuid)


def get_saved_analyses(db: Session, user_id: str):
    analyses = db.query(SavedAnalysis) \
        .filter(SavedAnalysis.user_id == user_id) \

    print(analyses)
    return analyses.all()


def get_saved_analysis(saved_analysis_uuid: UUID):
    analysis = SavedAnalysis.query.get(saved_analysis_uuid)
    return analysis
