from app.analysis.endpoints import merge_wells_datasources
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
