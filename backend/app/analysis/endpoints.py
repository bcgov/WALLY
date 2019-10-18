"""
Analysis functions for data in the Wally system
"""
import json
import requests
from typing import List
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.db.utils import get_db
from app.analysis.wells.well_analysis import get_wells_by_distance
from app.analysis.wells.models import WellDrawdown
logger = getLogger("geocoder")

router = APIRouter()


@router.get("/analysis/wells/nearby")
def get_nearby_wells(
    db: Session = Depends(get_db),
    point: str = Query(..., title="Point of interest",
                       description="Point of interest to centre search at"),
    radius: float = Query(1000, title="Search radius",
                          description="Search radius from point", ge=0, le=10000)
):
    """ finds wells near to a point
        fetches distance data using the Wally database, and combines
        it with screen data from GWELLS
    """

    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    wells_with_distances = get_wells_by_distance(db, point_shape, radius)

    # convert nearby wells to a list of strings of well tag numbers
    wells_to_search = map(lambda x: str(int(x[0])).lstrip("0"), wells_with_distances)

    wells_with_screens = get_screens(wells_to_search)

    wells_drawdown_data = merge_wells_datasources(wells_with_screens, wells_with_distances)

    return wells_drawdown_data


def get_screens(wells_to_search: List[str]) -> List[WellDrawdown]:
    """ calls GWELLS API to get well screen information. """

    wells_results = []
    done = False
    offset = 0

    # helpers to prevent unbounded requests
    limit_requests = 100
    i = 0

    search_string = ','.join(wells_to_search)

    # TODO: break up requests

    while not done and i < limit_requests:
        logger.info(f"https://gwells-dev-pr-1442.pathfinder.gov.bc.ca/gwells/api/v1/wells/screens?wells={search_string}&limit=100&offset={offset}")
        resp = requests.get(f"https://gwells-dev-pr-1442.pathfinder.gov.bc.ca/gwells/api/v1/wells/screens?wells={search_string}&limit=100&offset={offset}")

        # break now if we didn't receive any results.
        results = resp.json().get('results', None)

        i += 1

        if not results:
            done = True
            break

        # add results to a list.
        wells_results += results
        offset += len(results)

        # check for a "next" attribute, indicating the next limit/offset combo.
        # when it is null, the pagination is done.
        if not resp.json().get('next', None):
            done = True

    # return zero results if an error occurred or we did not successfully get all the results.
    # (avoid returning incomplete data)
    if not done:
        return []

    return wells_results
    # merge distance from Wally with screen/water info from GWELLS


def merge_wells_datasources(wells: list, wells_with_distances: object) -> List[WellDrawdown]:
    """
    Merges a list of well details (from GWELLS), with a key/value dict of wells: distance (m)
    to create a list of WellDrawdown data.
    e.g. combines:
        {
            123: 50,
            124: 55
        }
    with:
        [
            {
                well_tag_number: 123,
                static_water_level: 12
            },
            {
                well_tag_number: 124,
                static_water_level: 12
            }
        ]
    to create:
        [
            {
                well_tag_number: 123,
                static_water_level: 12,
                distance: 50
            },
            {
                well_tag_number: 124,
                static_water_level: 12,
                distance: 55
            }
        ]
    """

    well_map = {}

    # make a dict with keys being the well tag numbers
    for well in wells:
        well_map[well.pop('well_tag_number')] = well

    # create WellDrawdown data objects for every well we found nearby.  The last argument to WellDrawdown() is
    # the supplemental data that comes from GWELLS for each well.
    return [WellDrawdown(well_tag_number=well[0], distance=well[1], **well_map.get(well[0], {})) for well in wells_with_distances]
