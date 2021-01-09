

from api.v1.saved_analyses.controller import save_analysis
from tests.utils import get_mock_session

import logging


logger = logging.getLogger('test')


class TestSaveAnalysis:

    def test_validate_geometry(self):
        db = get_mock_session()

        geometry = 'Polygon(((0.0, 0.0), (0.0, 1.0), (-1.0, 1.0), (-1.0, 0.0)))'
        x_auth_userid = 'test_user'
        feature_type = 'CROSS_SECTION'
        zoom_level = '3'
        map_layers = ['groundwater_wells']

        save_analysis(db,
                      x_auth_userid, geometry, feature_type, '',
                      zoom_level, map_layers)
        # assert type(stations) == list

        # assert success


        # TODO: Test for ValidationError