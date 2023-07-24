import random
import pytest
import math
from api.v1.watersheds.controller import calculate_daylight_hours_usgs
import logging

logger = logging.getLogger('test')


class TestHamonEquation:
    def test_daylight_hours(self):
        """
        Test case from page 60 of the following USGS publication:
        https://pubs.usgs.gov/sir/2012/5202/pdf/sir2012-5202.pdf
        """

        day = 105
        latitude = 30

        daylight = calculate_daylight_hours_usgs(day, latitude * math.pi / 180)

        # page 60 of the above referenced publication gives 12.7 as the daylight hours
        # for latitude 30 degrees north on day 105. Check that the returned value is
        # within 0.1 hrs of the correct value.
        assert abs(daylight - 12.7) < 0.1
