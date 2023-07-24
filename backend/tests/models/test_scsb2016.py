import random
from decimal import *
import unittest
import pytest

import sqlalchemy
from api import config
import pandas as pd

# from api.v1.watersheds.controller import get_hydrometric_stations
from api.v1.hydat.controller import get_stations_in_area
from tests.utils import get_mock_session
from shapely.geometry import Polygon
from api.v1.models.scsb2016.controller import calculate_mean_annual_runoff
from api.db.utils import get_db

import logging


logger = logging.getLogger('test')


class TestSCSB2016(unittest.TestCase):

    def setUp(self):
        # Setup models
        url = config.TEST_DATABASE_URL
        if not url:
            self.skipTest("No database URL set")
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()
        self.connection.execute("ATTACH DATABASE ':memory:' AS modeling")

        # Get MAD Model data from fixtures
        df = pd.read_json(r'./fixtures/models/mad_model_coefficients.json')
        df.to_sql(con=self.engine,
                  index=False,
                  index_label='mad_model_coefficients_id',
                  schema='modeling',
                  name='mad_model_coefficients',
                  if_exists='replace')

    # def tearDown(self) -> None:
    #     # self.connection.execute("DROP DATABASE testdb")
    #     pass

    def test_proof_1_stwamus_river(self):
        """ SCSB2016 Test Proof 1 - Stawamus River
        """
        hydrological_zone = 26
        median_elevation = Decimal(953)
        glacial_coverage = Decimal(0)
        annual_precipitation = Decimal(3292)
        evapo_transpiration = Decimal(668)
        drainage_area = Decimal(51)
        solar_exposure = Decimal(0.57)
        average_slope = Decimal(26)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 77 < model[0]['model_result'] < 79

    def test_proof_2_mashiter_creek(self):
        """SCSB2016 Test Proof 2 - Mashiter Creek
        """
        hydrological_zone = 26
        median_elevation = Decimal(1096)
        glacial_coverage = Decimal(0)
        annual_precipitation = Decimal(3304)
        evapo_transpiration = Decimal(666)
        drainage_area = Decimal(42)
        solar_exposure = Decimal(0.67)
        average_slope = Decimal(19)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 77 < model[0]['model_result'] < 79

    def test_proof_3_slesse_creek(self):
        """SCSB2016 Test Proof 3 - Slesse Creek
        """
        hydrological_zone = 26
        median_elevation = Decimal(1320)
        glacial_coverage = Decimal(0)
        annual_precipitation = Decimal(2229)
        evapo_transpiration = Decimal(648)
        drainage_area = Decimal(165)
        solar_exposure = Decimal(0.66)
        average_slope = Decimal(31)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 49 < model[0]['model_result'] < 50

    def test_proof_4_sumas_river(self):
        """SCSB2016 Test Proof 4 - Sumas River
        """
        hydrological_zone = 26
        median_elevation = Decimal(917)
        glacial_coverage = Decimal(0)
        annual_precipitation = Decimal(2010)
        evapo_transpiration = Decimal(701)
        drainage_area = Decimal(1617)
        solar_exposure = Decimal(0.67)
        average_slope = Decimal(23)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 50 < model[0]['model_result'] < 52

    def test_proof_5_tahumming_river(self):
        """SCSB2016 Test Proof 5 - Tahumming River
        """
        hydrological_zone = 26
        median_elevation = Decimal(1363)
        glacial_coverage = Decimal(0.15)
        annual_precipitation = Decimal(3482)
        evapo_transpiration = Decimal(640)
        drainage_area = Decimal(255)
        solar_exposure = Decimal(0.59)
        average_slope = Decimal(37)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 97 < model[0]['model_result'] < 99

    def test_proof_6_lillooet_river(self):
        """SCSB2016 Test Proof 6 - Lillooet River
                """
        hydrological_zone = 26
        median_elevation = Decimal(1528)
        glacial_coverage = Decimal(0.1)
        annual_precipitation = Decimal(1972)
        evapo_transpiration = Decimal(640)
        drainage_area = Decimal(5543)
        solar_exposure = Decimal(0.63)
        average_slope = Decimal(28)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 54 < model[0]['model_result'] < 56

    def test_proof_7_millar_creek(self):
        """SCSB2016 Test Proof 7 - Millar Creek
        """
        hydrological_zone = 25
        median_elevation = Decimal(1694)
        glacial_coverage = Decimal(0.24)
        annual_precipitation = Decimal(2388)
        evapo_transpiration = Decimal(609)
        drainage_area = Decimal(77)
        solar_exposure = Decimal(0.59)
        average_slope = Decimal(24)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 41 < model[0]['model_result'] < 43

    def test_proof_8_meslilloet_creek(self):
        """SCSB2016 Test Proof 8 - Meslilloet Creek
        """
        hydrological_zone = 27
        median_elevation = Decimal(1042)
        glacial_coverage = Decimal(0.02)
        annual_precipitation = Decimal(4098)
        evapo_transpiration = Decimal(659)
        drainage_area = Decimal(40)
        solar_exposure = Decimal(0.62)
        average_slope = Decimal(25)

        result = calculate_mean_annual_runoff(self.connection,
                                              hydrological_zone,
                                              median_elevation,
                                              glacial_coverage,
                                              annual_precipitation,
                                              evapo_transpiration,
                                              drainage_area,
                                              solar_exposure,
                                              average_slope)

        model = [{column: value for column, value in rowproxy.items()} for rowproxy in result]
        assert model[0]['output_type'] == 'MAR'
        assert 117 < model[0]['model_result'] < 119
