from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Body, UploadFile, File
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.saved_analyses import schema, controller
import uuid

logger = getLogger("saved_analysis")

router = APIRouter()


@router.post("/saved_analyses")
def create_saved_analysis(
        saved_analysis: schema.SavedAnalysisCreate,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)) -> schema.SavedAnalysisCreate:
    """
    Saves an analysis
    """

    return controller.save_analysis(db, x_auth_userid,
                                    saved_analysis.name, saved_analysis.description,
                                    saved_analysis.geometry, saved_analysis.feature_type,
                                    saved_analysis.zoom_level, saved_analysis.map_layers)


@router.get("/saved_analyses", response_model=List[schema.SavedAnalysisGet])
def get_saved_analyses(x_auth_userid: Optional[str] = Header(None),
                       db: Session = Depends(get_db)) -> List[schema.SavedAnalysisGet]:
    return controller.get_saved_analyses_by_user(db, x_auth_userid)


@router.get("/saved_analyses/{saved_analysis_uuid}", response_model=schema.SavedAnalysisGet)
def get_saved_analyses(saved_analysis_uuid: uuid.UUID,
                       db: Session = Depends(get_db)) -> List[schema.SavedAnalysisGet]:
    return controller.get_saved_analysis(db, saved_analysis_uuid)
