from api.v1.wells.routes import merge_wells_datasources
from api.v1.wells.controller import calculate_available_drawdown, calculate_top_of_screen
from api.v1.wells.schema import Screen, WellDrawdown
import logging
logger = logging.getLogger('test')


def test_calculate_available_drawdown():

    wells_list = [
        {
            "well_tag_number": 123,
            "static_water_level": 12,
            "latitude": 48.420133,
            "longitude": -123.370083,
            "screen_set": [
                {"start": 15},
                {"start": 25}
            ]
        },
        {
            "well_tag_number": 124,
            "static_water_level": 12,
            "finished_well_depth": 22,
            "latitude": 48.420233,
            "longitude": -123.370283,
        }
    ]

    test_data = calculate_available_drawdown([WellDrawdown(**x) for x in wells_list])

    assert test_data[0].top_of_screen == 15
    assert test_data[0].swl_to_screen == 3
    assert test_data[1].swl_to_bottom_of_well == 10


def test_calculate_available_drawdown_bad_input():
    """ test that calculate_top_of_screen can handle bad input (data input errors),
        specifically missing top/bottom screen depth
    """
    wells_list = [
        {
            "well_tag_number": 123,
            "static_water_level": 12,
            "latitude": 48.420133,
            "longitude": -123.370083,
            "screen_set": [
                # some wells may have invalid screen sets, e.g. screen entries exist but don't have
                # the top and/or bottom depth filled in.
                {"start": None},
                {"start": None}
            ]
        },
        {
            "well_tag_number": 124,
            "static_water_level": 12,
            "finished_well_depth": 22,
            "latitude": 48.420233,
            "longitude": -123.370283,
        }
    ]

    test_data = calculate_available_drawdown([WellDrawdown(**x) for x in wells_list])

    # returns none without throwing an exception
    assert test_data[0].top_of_screen is None


def test_calculate_top_of_screen():
    """ test calculating the top of a list of screen segments """
    screen_set = [
        Screen(start=3.2),
        Screen(start=15.1),
    ]
    top = calculate_top_of_screen(screen_set=screen_set)
    assert top == 3.2


def test_calculate_top_of_screen_bad_input():
    """ test case when all screens have invalid data (no start value) """
    screen_set = [
        Screen(start=None),
        Screen(start=None),
    ]
    top = calculate_top_of_screen(screen_set=screen_set)
    assert top is None


def test_calculate_top_of_screen_partial_bad_input():
    """ test case when one screen has invalid data (no start value) """

    screen_set = [
        Screen(start=None),
        Screen(start=15.1),
    ]
    top = calculate_top_of_screen(screen_set=screen_set)
    assert top is None
