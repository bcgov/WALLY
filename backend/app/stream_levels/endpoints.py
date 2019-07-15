"""
Map layers (layers module) API endpoints/handlers.
"""
from logging import getLogger
import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.utils import get_db
from app.stream_levels.db import get_stations

import app.stream_levels.models as streams_v1

router = APIRouter()


logger = getLogger("api")


@router.get("/stations", response_model=List[streams_v1.StreamStation])
def list_stations(db: Session = Depends(get_db)):
    """ returns available stations """

    return get_stations(db)
