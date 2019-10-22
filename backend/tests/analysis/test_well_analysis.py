from app.analysis.endpoints import merge_wells_datasources
from app.analysis.wells.well_analysis import with_drawdown, calculate_top_of_screen
from tests.utils import get_mock_session
import logging
logger = logging.getLogger('test')


def test_well_distance_merge():
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


def test_well_distance_merge_with_padded_ids():
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


def test_well_drawdown_calcs():

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
    test_data = with_drawdown(test_data)

    assert test_data[0].swl_to_screen = 3
    assert test_data[1].swl_to_bottom_of_well = 10
