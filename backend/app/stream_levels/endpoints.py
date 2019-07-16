"""
Map layers (layers module) API endpoints/handlers.
"""
from logging import getLogger
import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.stream_levels.db as streams_repo
import app.stream_levels.models as streams_v1

router = APIRouter()


logger = getLogger("api")


@router.get("/streams", response_model=List[streams_v1.StreamStation])
def list_stations(db: Session = Depends(get_db)):
    """ Returns available stream monitoring stations """

    return streams_repo.get_stations(db)


@router.get("/streams/{station_number}/levels", response_model=List[streams_v1.MonthlyLevel])
def list_monthly_levels_by_year(station_number: str, year: int = 2018, db: Session = Depends(get_db)):
    """ Monthly average levels for a given station and year """

    return streams_repo.get_monthly_levels_by_station(db, station_number, year)


@router.get("/streams/{station_number}/flows", response_model=List[streams_v1.MonthlyFlow])
def list_monthly_flows_by_year(station_number: str, year: int = 2018, db: Session = Depends(get_db)):
    """ Monthly average flows for a given station and year """

    return streams_repo.get_monthly_flows_by_station(db, station_number, year)
