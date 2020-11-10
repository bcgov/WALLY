import math
import pyproj
from shapely.ops import transform, nearest_points
from shapely.geometry import Point, LineString
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326

COMPASS_BRACKETS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]


def distance_from_line(line: LineString, point: Point, srid=4326):
    """
    calculates the shortest distance between the point and line.
    """
    if srid == 4326:
        # transform to BC Albers, which has a base unit of metres
        point = transform(transform_4326_3005, point)
        line = transform(transform_4326_3005, line)

    elif srid != 3005:
        raise ValueError("SRID must be either 4326 or 3005")

    return point.distance(line)


def compass_direction_point_to_line(line: LineString, point: Point, srid=4326):
    """
    calculates the azimuth from a point along a line to a point.
    angle then used to lookup the compass direction
    """
    if srid == 4326:
        # transform to BC Albers, which has a base unit of metres
        point = transform(transform_4326_3005, point)
        line = transform(transform_4326_3005, line)

    elif srid != 3005:
        raise ValueError("SRID must be either 4326 or 3005")

    nearest_point = nearest_points(line, point)[0]
    angle = math.atan2(point.x - nearest_point.x, point.y - nearest_point.y)
    degrees = math.degrees(angle) if angle >= 0 else math.degrees(angle) + 360
    compass_lookup = round(degrees / 45)
    compass_direction = COMPASS_BRACKETS[compass_lookup]

    return compass_direction
