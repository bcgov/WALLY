"""
Functions for simple analysis of wells, including querying them using spatial functions (e.g.
along a profile line or in a given radius) and calculating values (such as available drawdown)
using existing data.
"""
import logging
import requests
from typing import List, Optional
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from shapely.geometry import Point, LineString
from api.layers.ground_water_wells import GroundWaterWells
from api.v1.wells.schema import WellDrawdown, Screen
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


def calculate_available_drawdown(wells: List[WellDrawdown]) -> List[WellDrawdown]:
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


def calculate_top_of_screen(screen_set: List[Screen]) -> Optional[float]:
    """ calculates the top of screen from a given screen set
    screen sets come from GWELLS and have a start depth and end depth."""

    top_of_screen = None

    if not screen_set or None in map(lambda x: x.start, screen_set):
        return None

    try:
        top_of_screen = min([x.start for x in screen_set if x.start])
    except ValueError:
        # we expect occasional ValueErrors due to inconsistent screen data.
        # some screens are present in the dataset but do not have start/end values.
        return None
    return top_of_screen


def get_screens(point, radius) -> List[WellDrawdown]:
    """ calls GWELLS API to get well screen information. """

    wells_results = []

    done = False
    url = f"https://gwells-staging.gov.bc.ca/gwells/api/v1/wells/screens?point={point.wkt}&radius={radius}&limit=100&offset=0"
    # helpers to prevent unbounded requests
    limit_requests = 100
    i = 0  # this i is for recording extra requests within each chunk, if necessary

    while not done and i < limit_requests:
        logger.info('external request: %s', url)
        resp = requests.get(url)

        i += 1
        # break now if we didn't receive any results.
        results = resp.json().get('results', None)
        if not results:
            done = True
            break

        # add results to a list.
        wells_results += [WellDrawdown(**well) for well in results]

        # check for a "next" attribute, indicating the next limit/offset combo.
        # when it is null, the pagination is done.
        next_url = resp.json().get('next', None)
        if not next_url:
            done = True
        url = next_url

    # return zero results if an error occurred or we did not successfully get all the results.
    # (avoid returning incomplete data)
    if not done:
        return []

    wells = calculate_available_drawdown(wells_results)

    return wells


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
    return calculate_available_drawdown([
        WellDrawdown(
            well_tag_number=well[0],
            distance=well[1],
            **well_map.get(str(well[0]).lstrip('0'), {})
        )
        for well in wells_with_distances])


def get_line_buffer_polygon(line: LineString, radius: float):
    """ returns a buffer area around a LineString. """
    return func.ST_Transform(func.ST_Buffer(
        func.St_Transform(
            func.ST_GeomFromText(line.wkt, 4326),
            3005
        ),
        radius,
        'endcap=flat join=round'
    ), 4326)


def get_parallel_line_offset(db: Session, line: LineString, radius: float):
    """ returns a parallel line perpendicular to a LineString. """
    return db.query(func.ST_AsText(func.ST_Transform(func.ST_OffsetCurve(
        func.St_Transform(
            func.ST_GeomFromText(line.wkt, 4326),
            3005
        ),
        radius
    ), 4326))).first()


def get_wells_along_line(db: Session, profile: LineString, radius: int):
    """ returns wells along a given line, including wells that are within a buffer
        determined by `radius` (m).
        `radius` creates a buffer area next to the line that does not include any area
        behind or beyond the start/end of the drawn line. The wells are ordered
        by the distance from the origin (i.e. the beginning of the line, measured
        along the axis).
    """

    # Pythagorean thereom to calculate the distance along the profile line.
    # This is necessary because we need to find the distance along the line,
    # not the distance from the origin point to the well (which is likely offset from
    # the profile line)
    distance_from_origin = func.sqrt(
        (
            func.power(
                func.ST_Distance(
                    func.ST_Transform(func.ST_StartPoint(func.ST_Force2d(
                        func.ST_GeomFromText(profile.wkt, 4326))), 3005),
                    func.ST_Transform(GroundWaterWells.GEOMETRY, 3005)
                ),
                2
            ) +
            func.power(
                func.ST_Distance(
                    func.ST_Transform(func.ST_Force2d(
                        func.ST_GeomFromText(profile.wkt, 4326)), 3005),
                    func.ST_Transform(GroundWaterWells.GEOMETRY, 3005)
                ),
                2
            )
        )
    )

    # interpolate the ground elevation at the distance from origin calculated above.
    ground_elevation = func.ST_Z(
        func.ST_LineInterpolatePoint(
            func.ST_Transform(func.ST_GeomFromText(profile.wkt, 4326), 3005),
            distance_from_origin /
            func.ST_Length(func.ST_Transform(
                func.ST_GeomFromText(profile.wkt, 4326), 3005))
        )
    )

    # Find wells along `line` that are within `radius` of the line.
    # note on this query: PostGIS recommends using ST_DWithin instead of ST_Buffer for looking up
    # points near another feature. However, we need results that are along a straight line and NOT simply
    # within a certain distance of the line (for example, we don't want any points before or beyond the endpoints
    # even if they are within the radius). Note use of endcap=flat.
    q = db.query(
        GroundWaterWells.WELL_TAG_NO.label("well_tag_number"),
        (GroundWaterWells.DEPTH_WELL_DRILLED *
         0.3048).label("finished_well_depth"),  # converted to metres
        (GroundWaterWells.WATER_DEPTH * 0.3048).label("water_depth"),
        distance_from_origin.label("distance_from_origin"),
        ground_elevation.label("ground_elevation_from_dem")) \
        .filter(
            func.ST_Contains(
                get_line_buffer_polygon(profile, radius),
                GroundWaterWells.GEOMETRY
            )
    ).order_by('distance_from_origin')

    return q.all()
