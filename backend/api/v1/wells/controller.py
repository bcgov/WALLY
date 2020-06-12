"""
Functions for simple analysis of wells, including querying them using spatial functions (e.g.
along a profile line or in a given radius) and calculating values (such as available drawdown)
using existing data.
"""
import logging
import requests
import math
import pyproj
import time
from typing import List, Optional
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from shapely.geometry import Point, LineString, CAP_STYLE, JOIN_STYLE, mapping, shape
from shapely.ops import transform
from api.config import GWELLS_API_URL
from api.layers.ground_water_wells import GroundWaterWells
from api.v1.aggregator.schema import ExternalAPIRequest, LayerResponse
from api.v1.aggregator.controller import fetch_geojson_features
from api.v1.aggregator.helpers import transform_3005_4326, transform_4326_3005
from api.v1.wells.schema import WellDrawdown, Screen, ExportApiRequest, ExportApiParams, CrossSectionExport
from api.v1.wells.excel import crossSectionXlsxExport
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
    url = f"{GWELLS_API_URL}/api/v2/wells/screens?point={point.wkt}&radius={radius}&limit=100&offset=0"
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


def create_line_buffer(line: LineString, radius: float):
    line = transform(transform_4326_3005, line)
    buf = line.buffer(radius, cap_style=CAP_STYLE.flat,
                      join_style=JOIN_STYLE.round)
    return transform(transform_3005_4326, buf)


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


def distance_along_line(line: LineString, point: Point):
    """ 
    calculates the distance that `point` is along `line`. Note that 
    this is the distance along the line, not from the beginning of the line
    to the point.
    """

    # transform to BC Albers, which has a base unit of metres
    point = transform(transform_4326_3005, point)
    line = transform(transform_4326_3005, line)

    # note.  shapely's geom.distance calculates distance on a 2d plane
    a = point.distance(line.interpolate(0))
    b = point.distance(line)
    return math.sqrt(a**2 + b**2)


def elevation_along_line(profile, distance):
    """ returns the elevation at `distance` metres along LineString Z `profile` """
    profile = transform(transform_4326_3005, profile)
    return profile.interpolate(distance).z


def get_wells_along_line(db: Session, profile: LineString, radius: float):
    """ returns wells along a given line, including wells that are within a buffer
        determined by `radius` (m).
        `radius` creates a buffer area next to the line that does not include any area
        behind or beyond the start/end of the drawn line. The wells are ordered
        by the distance from the origin (i.e. the beginning of the line, measured
        along the axis).
    """
    buf = create_line_buffer(profile, radius)

    req = ExternalAPIRequest(
        url=f"{GWELLS_API_URL}/api/v2/wells/screens",
        q={
            "within": buf.wkt,
            "limit": 100
        },
        layer="gwells"
    )
    feature_collection = fetch_geojson_features([req])[0].geojson

    wells_results = []

    for well in feature_collection.features:
        distance = distance_along_line(
            LineString([coords[:2] for coords in list(profile.coords)]),
            Point(shape(well.geometry))
        )

        well_data = {
            "well_tag_number": well.properties['well_tag_number'],
            "finished_well_depth": float(well.properties['finished_well_depth']) * 0.3048 if well.properties['finished_well_depth'] else None,
            "water_depth": float(well.properties['static_water_level']) * 0.3048 if well.properties['static_water_level'] else None,
            "distance_from_origin": distance,
            "ground_elevation_from_dem": elevation_along_line(profile, distance),
            "feature": well
        }

        wells_results.append(well_data)

    return wells_results


def get_cross_section_export(xs: CrossSectionExport):
    """ 
    Gathers together well information and returns an excel report 
    describing a cross section area
    """
    params = ExportApiParams(
        geojson="true"
    )

    requests = []
    for well_tag_number in xs.wells:
        url = f"{GWELLS_API_URL}/api/v2/wells/{well_tag_number}"
        req = ExportApiRequest(
            url=url,
            layer="gwells",
            id_field="well_tag_number",
            q=params
        )
        requests.append(req)

    feature_collection = fetch_geojson_features(requests)

    return crossSectionXlsxExport(feature_collection, xs.coordinates, xs.buffer)


