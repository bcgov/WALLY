"""
Project management endpoints
"""
from logging import getLogger
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.saved_analyses import controller

logger = getLogger("analysis")

router = APIRouter()


@router.get("/")
def get_user_analyses(
        x_auth_userid: Optional[str] = Header(None),
        db: Session = Depends(get_db)
):
    """
    Retrieves a user's list of saved analysis

    :param x_auth_userid: holds the keycloak idir that is passed as a
                          header up from the proxy service (X-Auth-UserId)
    :param db: Database session
    """

    if not x_auth_userid:
        return HTTPException(status_code=401)

    return controller.get_analyses_by_user(db, x_auth_userid)


@router.post("/")
def save_analysis(
        x_auth_userid: Optional[str] = Header(None),
        geometry: str = Query(
            "", title="Starting geometry",
            description="Geometry to load into feature starting point"
        ),
        feature_type: str = Query("", title="Feature",
                                  description="Feature used by this analysis"),
        description: Optional[str] = Query("", title="Description",
                                           description="Description of the analysis"),
        zoom_level: Optional[int] = None,
        map_layers: List[str] = None,
        db: Session = Depends(get_db)
):
    """
    Saves an analysis to a user

    """
    controller.save_analysis(
        db,
        x_auth_userid, geometry, feature_type, description,
        zoom_level, map_layers
    )




