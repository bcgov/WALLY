import json
import logging
from typing import List

from sqlalchemy.orm import Session
from api.v1.saved_analyses.db_models import SavedAnalysis, SavedAnalysisMapLayer
from api.v1.saved_analyses.schema import SavedAnalysis as Analysis
import shapely.wkt

logger = logging.getLogger("projects")


def save_analysis(db: Session, x_auth_userid: str, geometry: str,
                  feature_type: str, description: str, zoom_level: int,
                  map_layers: List[str], project_id: int = None):
    # date = datetime.now()

    # check if geometry is valid
    geom = shapely.wkt.loads(geometry)
    print(geom)

    # check if feature type is valid

    # check if map layers are valid
    analysis = SavedAnalysis(
        project_id=project_id,
        description=description,
        geometry=geometry,
        feature_type=feature_type,
        zoom_level=zoom_level,
        user_id=x_auth_userid
    )
    db.add(analysis)

    for layer in map_layers:
        # Verify layer exists in metadata.display_catalogue.display_data_name
        analysis_map_layers = SavedAnalysisMapLayer(
            saved_analysis_id=analysis.analysis_id,
            map_layer_name=layer
        )
        db.add(analysis_map_layers)

    # db.commit()


def get_analyses_by_user(db: Session, x_auth_userid: str) -> List[Analysis]:
    """ Gets all analyses saved by the user"""

    saved_analyses = db.query(SavedAnalysis) \
        .filter(SavedAnalysis.user_id == x_auth_userid)

    print(saved_analyses)

    return saved_analyses.all()
