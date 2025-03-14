import uuid
from logging import getLogger
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Header, Body, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from api.db.utils import get_db
from api.v1.saved_analyses import controller
from api.v1.saved_analyses.schema import SavedAnalysisCreateUpdate, SavedAnalysisGet, SavedAnalysisUpdate
from api.v1.user.db_models import User
from api.v1.user.session import get_user

logger = getLogger("saved_analysis")

router = APIRouter()


@router.post("/saved_analyses")
def create_saved_analysis(
        saved_analysis: SavedAnalysisCreateUpdate,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)) -> SavedAnalysisCreateUpdate:
    """
    Saves an analysis
    """
    return controller.save_analysis(db, user.user_uuid,
                                    saved_analysis.name, saved_analysis.description,
                                    saved_analysis.geometry, saved_analysis.feature_type,
                                    saved_analysis.zoom_level, saved_analysis.map_bounds,
                                    saved_analysis.map_layers)


@router.get("/saved_analyses", response_model=List[SavedAnalysisGet])
def get_saved_analyses(
        user: User = Depends(get_user),
        db: Session = Depends(get_db)) -> List[SavedAnalysisGet]:
    return controller.get_saved_analyses_by_user(db, user.user_uuid)


@router.get("/saved_analyses/{saved_analysis_uuid}", response_model=SavedAnalysisGet)
def get_saved_analysis(saved_analysis_uuid: uuid.UUID,
                       db: Session = Depends(get_db)) -> List[SavedAnalysisGet]:
    return controller.get_saved_analysis(db, saved_analysis_uuid)


@router.delete("/saved_analyses/{saved_analysis_uuid}")
def delete_saved_analysis(
        saved_analysis_uuid: uuid.UUID,
        db: Session = Depends(get_db),
        user: User = Depends(get_user)):
    return controller.delete_saved_analysis(db, saved_analysis_uuid, user)


@router.put("/saved_analyses/{saved_analysis_uuid}")
def update_saved_analysis(saved_analysis_uuid: uuid.UUID,
                          saved_analysis: SavedAnalysisUpdate,
                          user: User = Depends(get_user),
                          db: Session = Depends(get_db)):
    saved_analysis_data = jsonable_encoder(saved_analysis)
    return controller.update_saved_analysis(db, saved_analysis_uuid, user.user_uuid,
                                            saved_analysis_data)
