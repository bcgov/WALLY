"""
Functions for simple analysis of wells, including querying them using spatial functions (e.g.
along a profile line or in a given radius) and calculating values (such as available drawdown)
using existing data.
"""
import json
import logging
import math
from typing import List, Optional, Dict, Union

import requests
from shapely.geometry import (
    Point,
    LineString,
    CAP_STYLE,
    JOIN_STYLE,
    shape,
    MultiPolygon,
    Polygon)
from shapely.ops import transform, nearest_points
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.config import GWELLS_API_URL
from api.layers.ground_water_wells import GroundWaterWells
from api.v1.aggregator.controller import fetch_geojson_features, databc_feature_search
from api.v1.aggregator.helpers import transform_3005_4326, transform_4326_3005
from api.v1.aggregator.schema import ExternalAPIRequest
from api.v1.wells.excel import cross_section_xlsx_export
from api.v1.wells.schema import WellDrawdown, Screen, ExportApiRequest, ExportApiParams, \
    CrossSectionExport
from api.v1.wells.helpers import distance_from_line, compass_direction_point_to_line

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


def get_wells_by_aquifer(point, radius, well_tag_numbers=None) -> Dict[Union[int, str], List[WellDrawdown]]:
    """Get wells, grouped by aquifer number"""
    wells = get_wells_with_drawdown(point, radius, well_tag_numbers)

    aquifers = set()

    # Get aquifers
    for well in wells:

        if well.aquifer:
            aquifers.add(well.aquifer.aquifer_id)
        else:
            aquifers.add(None)

    wells_by_aquifer = {}

    for a in aquifers:
        wells_by_aquifer[a if a else ''] = [w for w in wells if
                                            (w.aquifer and w.aquifer.aquifer_id == a) or (
                                                    a is None and not w.aquifer)]
    return wells_by_aquifer


def get_wells_with_drawdown(point, radius, well_tag_numbers=None) -> List[WellDrawdown]:
    """ Find wells near a given point, with a buffer radius,
        or a list of wells (comma separated well tag numbers)
        This function gets wells and their corresponding subsurface data using the GWELLS API
        and then computes the distance of the point to the wells
    """

    if well_tag_numbers is None:
        well_tag_numbers = ''

    wells_results = []

    done = False

    if well_tag_numbers:
        url = f"{GWELLS_API_URL}/api/v2/wells/subsurface?wells={well_tag_numbers}"
    else:
        buffer = create_circle_polygon(point, radius)
        url = f"{GWELLS_API_URL}/api/v2/wells/subsurface?within={buffer.wkt}&limit=100"

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

        for well in results:
            # calculate distance from well to click point
            center_point = transform(transform_4326_3005, point)
            well_point = transform(transform_4326_3005, Point(well["longitude"], well["latitude"]))
            distance = center_point.distance(well_point)
            well["distance"] = distance

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

    # create WellDrawdown data objects for every well we found nearby.
    # The last argument to WellDrawdown() is
    # the supplemental data that comes from GWELLS for each well.
    return calculate_available_drawdown([
        WellDrawdown(
            well_tag_number=well[0],
            distance=well[1],
            **well_map.get(str(well[0]).lstrip('0'), {})
        )
        for well in wells_with_distances])


def create_circle_polygon(point: Point, radius: float):
    point = transform(transform_4326_3005, point)
    circle = point.buffer(radius)
    return transform(transform_3005_4326, circle)


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


def distance_along_line(line: LineString, point: Point, srid=4326):
    """
    calculates the distance that `point` is along `line`. Note that
    this is the distance along the line, not from the beginning of the line
    to the point.
    """

    if srid == 4326:
        # transform to BC Albers, which has a base unit of metres
        point = transform(transform_4326_3005, point)
        line = transform(transform_4326_3005, line)

    elif srid != 3005:
        raise ValueError("SRID must be either 4326 or 3005")

    # note.  shapely's geom.distance calculates distance on a 2d plane
    c = point.distance(line.interpolate(0))
    b = point.distance(line)
    return math.sqrt(abs(c ** 2 - b ** 2))


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
        url=f"{GWELLS_API_URL}/api/v2/wells/subsurface",
        q={
            "within": buf.wkt,
            "limit": 100
        },
        layer="gwells"
    )
    feature_collection = fetch_geojson_features([req])[0].geojson

    wells_results = []

    for well in feature_collection.features:
        line = LineString([coords[:2] for coords in list(profile.coords)])
        point = Point(shape(well.geometry))

        shortest_line = distance_from_line(line, point)
        distance = distance_along_line(line, point)
        compass_direction = compass_direction_point_to_line(line, point)

        # Separate the well aquifer info from the feature info
        well_aquifer = well.properties.pop('aquifer', None)

        # Add (flattened) aquifer into feature info
        well.properties['aquifer'] = well_aquifer.get('aquifer_id') if well_aquifer else None

        well.properties['distance_from_line'] = shortest_line
        well.properties['compass_direction'] = compass_direction

        # Remove lithologydescription_set from well properties as it's not formatted properly
        well.properties.pop('lithologydescription_set')

        # load screen data from the geojson response
        screenset = well.properties.get('screen_set', '')
        screenset = json.loads(screenset)

        well_data = {
            "well_tag_number": well.properties['well_tag_number'],
            "finished_well_depth": float(well.properties['finished_well_depth']) * 0.3048
            if well.properties['finished_well_depth'] else None,
            "water_depth": float(well.properties['static_water_level']) * 0.3048 if well.properties[
                'static_water_level'] else None,
            "distance_from_origin": distance,
            "ground_elevation_from_dem": elevation_along_line(profile, distance),
            "aquifer": well_aquifer,
            "aquifer_lithology": well.properties['aquifer_lithology'],
            "feature": well,
            "screen_set": screenset
        }

        wells_results.append(well_data)

    return wells_results


def get_waterbodies_along_line(section_line: LineString, profile: LineString):
    """ retrieves streams that cross the cross section profile line """

    line_3005 = transform(transform_4326_3005, section_line)

    streams_layer = "WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP"
    lakes_layer = "WHSE_BASEMAPPING.FWA_LAKES_POLY"

    cql_filter = f"""INTERSECTS(GEOMETRY, {line_3005.wkt})"""

    intersecting_lakes = databc_feature_search(
        lakes_layer, cql_filter=cql_filter)
    intersecting_streams = databc_feature_search(
        streams_layer, cql_filter=cql_filter)

    stream_features = []
    lake_features = []

    # create a MultiPolygon of all the lake geometries.
    # this will be used to check if a stream intersection falls inside a lake
    # (lake names will supersede stream names inside lakes)
    lake_polygons = []
    for lake in intersecting_lakes.features:
        geom = shape(lake.geometry)
        if isinstance(geom, MultiPolygon):
            lake_polygons = lake_polygons + [poly for poly in geom]
        elif isinstance(geom, Polygon):
            lake_polygons.append(geom)

    lakes_multipoly_shape = MultiPolygon(lake_polygons)

    # convert each intersecting stream into a Point or MultiPoint using .intersection().
    # check each point of intersection to make sure it doesn't lie on a lake (stream lines in
    # the Freshwater Atlas extend through lakes, but when we are over a lake, we want the lake
    # name not the stream name).
    # the elevation for points comes from the Freshwater Atlas,
    # so it's possible it could be slightly off
    # the CDEM value from the Canada GeoGratis DEM API.
    for stream in intersecting_streams.features:
        intersecting_points = line_3005.intersection(shape(stream.geometry))

        # the intersection may either be a MultiPoint (which is iterable),
        # or a single Point instance (not iterable). If not iterable, convert
        # to a list of 1 Point.
        if isinstance(intersecting_points, Point):
            intersecting_points = [intersecting_points]

        for point in intersecting_points:
            if point.intersects(lakes_multipoly_shape):
                # skip so that we can defer to the lake's name
                continue

            distance = distance_along_line(
                LineString([coords[:2] for coords in list(line_3005.coords)]),
                point,
                srid=3005
            )
            stream_data = {
                "name": stream.properties['GNIS_NAME'] or "Unnamed Stream",
                "distance": distance,
                "elevation": point.z,
                "geometry": transform(transform_3005_4326, point)
            }
            stream_features.append(stream_data)

    # for lakes, use a representative point (using the centroid).
    # Lakes don't come with an elevation, so the elevation uses the profile
    # retrieved from the GeoGratis CDEM API.
    for lake in intersecting_lakes.features:
        intersecting_points = line_3005.intersection(shape(lake.geometry))

        if isinstance(intersecting_points, LineString):
            intersecting_points = [intersecting_points]

        for line in intersecting_points:
            point = line.centroid
            distance = distance_along_line(
                LineString([coords[:2] for coords in list(line_3005.coords)]),
                point,
                srid=3005
            )
            lake_data = {
                "name": lake.properties['GNIS_NAME_1'] or f"Unnamed Lake",
                "distance": distance,
                "elevation": elevation_along_line(profile, distance),
                "geometry": transform(transform_3005_4326, line)
            }
            lake_features.append(lake_data)

    return stream_features + lake_features


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

    return cross_section_xlsx_export(feature_collection, xs.coordinates, xs.buffer)
