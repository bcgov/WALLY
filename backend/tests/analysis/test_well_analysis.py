from api.analysis.endpoints import merge_wells_datasources
from api.analysis.wells.well_analysis import calculate_available_drawdown, calculate_top_of_screen
from api.analysis.wells.models import Screen
from tests.utils import get_mock_session
import logging
logger = logging.getLogger('test')


def test_merge_wells_datasources():
    """
    test merging GWELLS data with Wally distances
    """

    distance_results_from_db = (
        (123, 50),
        (124, 55)
    )

    wells_list = [
        {
            "well_tag_number": 123,
            "static_water_level": 12
        },
        {
            "well_tag_number": 124,
            "static_water_level": 12
        }
    ]

    test_data = merge_wells_datasources(wells_list, distance_results_from_db)

    assert test_data[0].well_tag_number == 123
    assert test_data[0].distance == 50
    assert test_data[1].well_tag_number == 124
    assert test_data[1].distance == 55


def test_merge_wells_datasources_with_padded_ids():
    """
    the wells dataset currently comes with padded IDs
    """

    distance_results_from_db = (
        ("0000123", 50),
        ("0000124", 55)
    )

    wells_list = [
        {
            "well_tag_number": 123,
            "static_water_level": 12
        },
        {
            "well_tag_number": 124,
            "static_water_level": 12
        }
    ]

    test_data = merge_wells_datasources(wells_list, distance_results_from_db)

    assert test_data[0].well_tag_number == 123
    assert test_data[0].distance == 50
    assert test_data[1].well_tag_number == 124
    assert test_data[1].distance == 55


def test_calculate_available_drawdown():

    distance_results_from_db = (
        ("0000123", 50),
        ("0000124", 55)
    )

    wells_list = [
        {
            "well_tag_number": 123,
            "static_water_level": 12,
            "screen_set": [
                {"start": 15},
                {"start": 25}
            ]
        },
        {
            "well_tag_number": 124,
            "static_water_level": 12,
            "finished_well_depth": 22
        }
    ]

    test_data = merge_wells_datasources(wells_list, distance_results_from_db)
    test_data = calculate_available_drawdown(test_data)

    assert test_data[0].top_of_screen == 15
    assert test_data[0].swl_to_screen == 3
    assert test_data[1].swl_to_bottom_of_well == 10


def test_calculate_available_drawdown_bad_input():
    """ test that calculate_top_of_screen can handle bad input (data input errors),
        specifically missing top/bottom screen depth
    """
    distance_results_from_db = (
        ("0000123", 50),
        ("0000124", 55)
    )

    wells_list = [
        {
            "well_tag_number": 123,
            "static_water_level": 12,
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
            "finished_well_depth": 22
        }
    ]

    test_data = merge_wells_datasources(wells_list, distance_results_from_db)
    test_data = calculate_available_drawdown(test_data)

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
