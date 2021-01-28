import logging
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from api.v1.saved_analyses.db_models import SavedAnalysis, SavedAnalysisMapLayer
from api.v1.user.db_models import User
from api.v1.catalogue.db_models import DisplayCatalogue
from uuid import UUID
from datetime import datetime

from typing import List

logger = logging.getLogger("saved_analyses")


def validate_user(db: Session, user_id: str):
    # TODO: Deprecate this when auth middleware is in place
    user = db.query(func.count(User.uuid)).filter(User.uuid == user_id).scalar()
    if user == 0:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user")


def validate_layers(db: Session, layers: List):
    """
    Validate map layers with a single sql query
    :param db: db session
    :param layers: list of map layers
    """
    layer_count = db.query(func.count(DisplayCatalogue.display_data_name)).filter(
        DisplayCatalogue.display_data_name.in_(layers)
    ).scalar()

    if len(layers) != layer_count:
        raise HTTPException(status_code=422, detail=f"Invalid map layer(s)")


def save_analysis(db: Session, user_id: str,
                  name: str, description: str,
                  geometry: dict, feature_type: str, zoom_level: float,
                  map_layers: [], project_id: int = None):
    """
    Create a saved analysis
    :param db: db session
    :param user_id: owner of this saved analysis
    :param name: name of this saved analysis
    :param description: description of this saved analysis
    :param geometry: geometry, usually needed as a starting point by the analysis
    :param feature_type: feature type, must be one of the constants.FEATURE_TYPE allowed
    :param zoom_level: set the map to this zoom level when analysis is loaded
    :param map_layers: map layers loaded in this analysis
    :param project_id: tie analysis to a project
    :return:
    """

    validate_user(db, user_id)
    validate_layers(db, map_layers)

    analysis = SavedAnalysis(user_id=user_id,
                             name=name,
                             description=description,
                             _geometry=geometry,
                             feature_type=feature_type,
                             zoom_level=zoom_level,
                             project_id=project_id)
    db.add(analysis)
    db.flush()

    for layer in map_layers:
        saved_analysis_map_layer = SavedAnalysisMapLayer(
            saved_analysis_uuid=analysis.saved_analysis_uuid,
            map_layer=layer
        )
        db.add(saved_analysis_map_layer)

    db.commit()
    return analysis.saved_analysis_uuid


def get_saved_analyses_by_user(db: Session, user_id: str):
    """
    Get a list of saved analyses for this user
    :param db: db session
    :param user_id: User id
    :return: list of saved analyses
    """
    analyses = db.query(
        SavedAnalysis
    ).filter(
        SavedAnalysis.user_id == user_id,
        SavedAnalysis.deleted_on.is_(None)
    )

    return analyses.all()


def get_saved_analysis(db: Session, saved_analysis_uuid: UUID, include_deleted=False):
    """
    Get a saved analysis by uuid
    :param db: db session
    :param saved_analysis_uuid: the saved analysis uuid
    :param include_deleted: optional parameter to include deleted, default is False
    :return: a saved analysis object
    """
    if include_deleted:
        analysis = db.query(SavedAnalysis).get(saved_analysis_uuid)
    else:
        analysis = db.query(SavedAnalysis).filter(
            SavedAnalysis.saved_analysis_uuid == saved_analysis_uuid,
            SavedAnalysis.deleted_on.is_(None)
        ).first()

    if analysis:
        return analysis
    else:
        raise HTTPException(status_code=404, detail=f"Item not found")


def delete_saved_analysis(db: Session, saved_analysis_uuid: UUID):
    """
    Delete a saved analysis
    Performs a soft delete on a saved analysis
    :param db: db session
    :param saved_analysis_uuid: the saved analysis uuid
    """
    analysis = db.query(SavedAnalysis).get(saved_analysis_uuid)
    analysis.deleted_on = datetime.now()
    db.commit()


def update_saved_analysis(db: Session, saved_analysis_uuid: UUID,
                          user_id: str,
                          update_data: dict = None):
    """
    Update the saved analysis
    :param update_data:
    :param db: db session
    :param saved_analysis_uuid: the saved analysis uuid
    :param user_id: the user id
    """
    # TODO: Deprecate when auth middleware is in place
    validate_user(db, user_id)

    analysis = db.query(SavedAnalysis).get(saved_analysis_uuid)

    # Replace all map layers if needed
    if update_data['map_layers'] is not None:
        new_map_layers = update_data.pop('map_layers')
        validate_layers(db, new_map_layers)

        d = db.query(SavedAnalysisMapLayer).filter(
            SavedAnalysisMapLayer.saved_analysis_uuid == saved_analysis_uuid) \
            .delete(synchronize_session=False)
        db.commit()

        for layer in new_map_layers:
            saved_analysis_map_layer = SavedAnalysisMapLayer(
                saved_analysis_uuid=analysis.saved_analysis_uuid,
                map_layer=layer
            )
            db.add(saved_analysis_map_layer)

    # Replace geometry if needed
    if update_data['geometry'] is not None:
        analysis._geometry = update_data.pop('geometry')

    # Update the rest of the fields if needed
    for field in update_data.keys():
        if update_data[field] is not None:
            setattr(analysis, field, update_data[field])

    db.commit()
