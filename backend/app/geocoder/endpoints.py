"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.utils import get_db
from app.geocoder.db import lookup_by_text
logger = getLogger("geocoder")

router = APIRouter()


@router.get("/geocode")
def geocode_lookup(
    db: Session = Depends(get_db),
    kind: str = Query(None, title="Feature type", description="The type of feature to search for (optional; default: all)", alias="type"),
    q: str = Query(None, title="Search query",
                   description="Text to search for")
):

    if not q:
        raise HTTPException(
            status_code=400, detail="Provide a string to search for in the `q` parameter, e.g. `?q=Main St`")
    return lookup_by_text(db)
