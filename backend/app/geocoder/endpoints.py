"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.db.utils import get_db
from app.geocoder.db import lookup_by_text
logger = getLogger("geocoder")

router = APIRouter()

# Wally's web client uses https://github.com/mapbox/mapbox-gl-geocoder as a
# search/geocoding control. To maintain compatibility with Mapbox geocoding,
# this endpoint has to handle several path parameters that we don't need (_1 and _2).
# The q parameter includes `.json` after the query string, so we need to handle that as well.
@router.get("/geocoding/{_1}/{_2}/{query}.json")
def geocode_lookup(
    db: Session = Depends(get_db),
    query: str = Path(..., title="Search query",
                      description="Text to search for")
):
    """ provides lookup/geocoding of places that users search for """

    return lookup_by_text(db, query)
