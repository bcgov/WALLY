"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from geojson import FeatureCollection
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.geocoder.controller import lookup_feature
logger = getLogger("geocoder")

router = APIRouter()

# Wally's web client uses https://github.com/mapbox/mapbox-gl-geocoder as a
# search/geocoding control. To maintain compatibility with Mapbox geocoding,
# this endpoint has to handle several path parameters that we don't need (_1 and _2).
# The q parameter includes `.json` after the query string, so we need to handle that as well.
@router.get("/{_1}/{_2}/{query}.json")
def geocode_lookup(
    db: Session = Depends(get_db),
    query: str = Path(..., title="Search query",
                      description="Text to search for"),
    feature_type: str = Query(
        None,
        title="Feature type to limit search to",
        description="Feature type to limit search to. Defaults to all types",
        # note: the Mapbox geocoder may send this query in the country parameter.
        alias="country"
    )
):
    """ provides lookup/geocoding of places that users search for """

    # if no feature_type specified, return an empty collection.
    # this may happen as a side effect of the Mapbox geocoder if user is
    # using the input box to search coordinates.
    if not feature_type:
        return FeatureCollection(features=[])

    return lookup_feature(db, query, feature_type)
