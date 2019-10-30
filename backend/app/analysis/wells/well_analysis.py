"""
Database tables and data access functions for Water Survey of Canada's
National Water Data Archive Hydrometic Data
"""
import json
import logging
import requests
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.layers.ground_water_wells import GroundWaterWells
from app.analysis.wells.models import WellDrawdown
logger = logging.getLogger("api")


def get_wells_by_distance(db: Session, search_point: Point, radius: float) -> list:
    """ List wells by distance from a point.
    """

    if radius > 10000:
        # some regions have thousands of wells in a 10km radius... limit search to that.
        radius = 10000

    # search within a given radius, adding a distance column denoting
    # distance from the centre point in metres
    # geometry columns are cast to geography to use metres as the base unit.
    q = db.query(GroundWaterWells) \
        .filter(
            func.ST_DWithin(func.Geography(GroundWaterWells.GEOMETRY),
                            func.ST_GeographyFromText(search_point.wkt), radius)
    ) \
        .with_entities(
            GroundWaterWells.WELL_TAG_NO,
            func.ST_Distance(func.Geography(GroundWaterWells.GEOMETRY),
                             func.ST_GeographyFromText(search_point.wkt)).label('distance')
    ).order_by('distance')

    return q.all()


def with_drawdown(wells: List[WellDrawdown]) -> List[WellDrawdown]:
    """ takes a list of WellDrawdown objects and fills in drawdown calculations """

    for well in wells:
        if well.screen_set:
            # well has a screen set: calculate the top of screen using
            # the screen set supplied by GWELLS.
            well.top_of_screen = calculate_top_of_screen(well.screen_set)

        if well.top_of_screen and well.static_water_level:
            # calculate the difference between the static water level
            # and the top of the screen.  This value indicates the
            # available drawdown. This calculation depends on the reported
            # values available at the time that the well report was filed.
            well.swl_to_screen = well.top_of_screen - well.static_water_level

        if well.finished_well_depth and well.static_water_level:
            # calculate difference between static water level and
            # the finished well depth.  The finished well depth is available
            # on more wells than screen depths are.
            well.swl_to_bottom_of_well = well.finished_well_depth - well.static_water_level

    return wells


def calculate_top_of_screen(screen_set: list = []) -> float:
    """ calculates the top of screen from a given screen set
    screen sets come from GWELLS and have a start depth and end depth."""

    return min([x.start for x in screen_set if x.start])


def get_screens(wells_to_search: List[str]) -> List[WellDrawdown]:
    """ calls GWELLS API to get well screen information. """

    wells_results = []

    # avoid making queries with an excessively long list of wells.
    chunk_length = 50

    # split requests into chunks based on chunk_length
    chunks = [wells_to_search[i:i+chunk_length]
              for i in range(0, len(wells_to_search), chunk_length)]

    for chunk in chunks:
        # helpers to prevent unbounded requests
        done = False
        limit_requests = 100
        i = 0  # this i is for recording extra requests within each chunk, if necessary

        # we are already making small chunks within the known API pagination limit,
        # but in case that limit changes, we can still handle offset paging.
        offset = 0

        search_string = ','.join(chunk)

        while not done and i < limit_requests:
            logger.info('making request to GWELLS API')
            resp = requests.get(
                f"https://gwells-staging.pathfinder.gov.bc.ca/gwells/api/v1/wells/screens?wells={search_string}&limit=100&offset={offset}")

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
        well_map[str(well.pop('well_tag_number'))] = well

    # create WellDrawdown data objects for every well we found nearby.  The last argument to WellDrawdown() is
    # the supplemental data that comes from GWELLS for each well.
    return with_drawdown([
        WellDrawdown(
            well_tag_number=well[0],
            distance=well[1],
            **well_map.get(str(well[0]).lstrip('0'), {})
        )
        for well in wells_with_distances])
