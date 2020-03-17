import random
import pytest

# from api.v1.watersheds.controller import get_hydrometric_stations
from api.v1.hydat.controller import get_stations_in_area
import logging

logger = logging.getLogger('test')


class TestHydrometricStations:
    """Add tests
    - When there are no stations
    - When there is at least one station
    - That a list is returned
    - That a list contains a collection of Feature() objects
    """
    def test_hydrometric_station(self):
        # Watershed data returns hydrometric stations
        return True