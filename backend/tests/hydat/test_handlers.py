from app.hydat.endpoints import list_stations
from tests.utils import get_mock_session


def test_list_stations():
    """ test that the list_stations handler returns a geojson FeatureCollection """
    db = get_mock_session()
    geojson = list_stations(db)
    assert geojson.type == 'FeatureCollection'
