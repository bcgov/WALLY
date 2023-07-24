import math
from api.v1.wells.controller import distance_along_line
from shapely.geometry import LineString, Point
import logging
logger = logging.getLogger('test')


def test_distance_along_line_1():
    """ test calculating the distance along a line (point 200m from line,
    at 100m distance along line)"""

    line = LineString(((0, 0), (0, 100)))
    point = Point((200, 100))

    distance = distance_along_line(line, point, srid=3005)
    expected_distance = 100

    assert math.isclose(distance, expected_distance, rel_tol=1e-9, abs_tol=0.0)


def test_distance_along_line_2():
    """ test calculating the distance along a line (point falls on line) """

    line = LineString(((0, 0), (0, 100)))
    point = Point((0, 1))

    distance = distance_along_line(line, point, srid=3005)
    expected_distance = 1

    assert math.isclose(distance, expected_distance, rel_tol=1e-9, abs_tol=0.0)
