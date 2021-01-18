from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Body, UploadFile, File
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.saved_analyses import schema, controller

logger = getLogger("projects")

router = APIRouter()


@router.post("/")
def create_saved_analysis(
        saved_analysis: schema.SavedAnalysis,
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)) -> schema.SavedAnalysis:
    """
    Saves an analysis
    """

    return controller.save_analysis(db, x_auth_userid,
                                    saved_analysis.name, saved_analysis.description,
                                    saved_analysis.geometry, saved_analysis.feature_type,
                                    saved_analysis.zoom_level, saved_analysis.map_layers)


@router.get("/")
def get_saved_analyses(x_auth_userid: Optional[str] = Header(None),
                       db: Session = Depends(get_db)) -> List[schema.SavedAnalysis]:
    return controller.get_saved_analyses(db, x_auth_userid)
