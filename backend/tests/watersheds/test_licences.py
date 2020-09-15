import geojson
import pytest
import unittest
from shapely.geometry import Polygon, shape
from shapely.ops import transform
from api.v1.watersheds.controller import water_licences_summary
from api.v1.aggregator.helpers import transform_4326_3005
import logging

logger = logging.getLogger('test')


class TestWaterLicencesSummary(unittest.TestCase):
    def setUp(self):
        """
        load test data for water licence calculation tests        
        """
        with open('./tests/watersheds/test_watershed_area.geojson') as test_area_geojson:
            test_area_fc = geojson.load(test_area_geojson)
            self.test_area = shape(test_area_fc.features[0].geometry)

        with open('./tests/watersheds/test_licences.geojson') as test_licences_geojson:
            self.data = geojson.load(test_licences_geojson)

    def test_calculate_quantities(self):
        """
        Test case for calculating water rights licences quantities.
        The test loads a snapshot of licences in the Alta Lake area of Whistler
        from the public water rights licences dataset.
        """
        summary = water_licences_summary(self.data.features, self.test_area)

        assert round(summary.total_qty) == 8740332

    def test_canceled_licences(self):
        """ test that canceled licences are filtered out of the licences list
            and put in a separate inactive_licences list.
        """

        summary = water_licences_summary(self.data.features, self.test_area)
        test_purpose = next(
            (purpose for purpose in summary.total_qty_by_purpose if purpose["purpose"] == "Domestic  (01A)"), None)

        assert len(test_purpose["licences"]) == 4
        assert len(test_purpose["inactive_licences"]) == 2

    def test_licences_with_m_flag(self):
        """ test calculating licences with a QUANTITY_FLAG of M, which indicates
            that multiple points of diversion share one quantity under a single licence.
            See https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public
        """

        summary = water_licences_summary(self.data.features, self.test_area)

        # use the "Land Improve: General (04A)" category, since it contains licences with the flag "M"
        test_purpose = next(
            (purpose for purpose in summary.total_qty_by_purpose if purpose["purpose"] == "Land Improve: General  (04A)"), None)

        # the summed quantity values for each record in the test dataset is 486182 m3/yr
        # however, the quantity for licences with flag M can't be added. All records share one max quantity.
        # this assert is just to show that "sum" produces a different result than the water_licences_summary function.
        assert round(sum([x.properties['quantityPerYear']
                          for x in test_purpose["licences"]])) == 486182

        # the proper quantity is 127768.
        assert round(test_purpose["qty"]) == 127768
