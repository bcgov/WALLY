import pytest

from pydantic import ValidationError
from api.v1.saved_analyses.controller import save_analysis
from api.v1.saved_analyses.schema import SavedAnalysis
from tests.utils import get_mock_session

import logging

logger = logging.getLogger('test')


class TestSaveAnalysis:

    def test_validate_geometry_validation_error(self):
        """
        Throw validation error in invalid geometry
        """
        geometry = 'LINESTRING (30 10, 10 30-sdfs)'
        x_auth_userid = 'test_user'
        name = 'Test analysis'
        description = 'Test'
        feature_type = 'cross_section'
        zoom_level = 3
        map_layers = ['groundwater_wells']

        with pytest.raises(ValidationError) as e:
            assert SavedAnalysis(
                user_id=x_auth_userid,
                name=name,
                description=description,
                geometry=geometry,
                feature_type=feature_type,
                zoom_level=zoom_level,
                map_layers=map_layers
            )
        assert 'Invalid geometry' in str(e.value)
        assert e.type == ValidationError

    def test_validate_geometry_valid(self):
        """
        Test create schema if fields are all valid
        """
        geometry = 'LINESTRING (30 10, 10 30)'
        x_auth_userid = 'test_user'
        name = 'Test analysis'
        description = 'Test'
        feature_type = 'cross_section'
        zoom_level = 3
        map_layers = ['groundwater_wells']

        assert SavedAnalysis(
            user_id=x_auth_userid,
            name=name,
            description=description,
            geometry=geometry,
            feature_type=feature_type,
            zoom_level=zoom_level,
            map_layers=map_layers
        )
