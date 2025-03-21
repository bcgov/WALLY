"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from geojson import FeatureCollection
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.geocoder.controller import lookup_feature, address_lookup, place_name_lookup
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

    # coordinates can be calculated on the frontend, but using the geocoder box
    # triggers an API request anyway. If the user specified they only need
    # coordinates, stop the request here and return an empty collection.
    if feature_type == 'coordinates':
        return FeatureCollection(features=[])

    if feature_type == 'street_address':
        return address_lookup(query)

    if feature_type == 'place_name':
        return place_name_lookup(query)

    # if not using a special handler, lookup using the feature_lookup function which
    # will use the DataBC WMS service to find features.
    return lookup_feature(db, query, feature_type)
