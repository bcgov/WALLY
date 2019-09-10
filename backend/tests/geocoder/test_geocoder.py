from app.geocoder.db import lookup_by_text
from tests.utils import get_mock_session


def test_geocode_lookup_handler():
    """ test that the geocode lookup function returns a geojson FeatureCollection """
    db = get_mock_session()
    geojson = lookup_by_text(db, 'test')
    assert geojson.type == 'FeatureCollection'
