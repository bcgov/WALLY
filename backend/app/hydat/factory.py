"""
Creates stream stations and data for dev fixtures and unit tests
"""

import factory
from typing import Optional
from app.db.session import db_session
from shapely.geometry import Point
from geoalchemy2.elements import WKTElement
from . import db_models

# base values to help generate a steady curve
BASE_FLOWS = [1.1, 1.1, 1.2, 1.3, 1.2, 1, .9, .9, 1, 1.1, 1.2, 1.2]
DEFAULT_COORDS = {"lat": 49.25, "lng": -123}


class MonthlyLevelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ factory to generate stream level values """
    class Meta:
        model = db_models.DlyLevel
        sqlalchemy_session = db_session

    station_number = None
    year = factory.Sequence(lambda n: 2011 + n // 12)  # start at 2017, increase another year after every 12th instance
    month = factory.Sequence(lambda n: (n % 12) + 1)  # always between 1-12, even n increases past 12.
    full_month = 1
    no_days = 30
    precision_code = 1

    # Use BASE_FLOWS to generate a starting set of values. BASE_FLOWS has 12 values, one for each month.
    # the map statements increase the flow by 10% every 12 months. This allows us to have
    # some variation in yearly data for visualization/testing.
    monthly_mean = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))))
    monthly_total = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) * 30)
    min = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) - 0.5)
    max = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) + 0.5)
    station = None


class MonthlyFlowFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ factory to generate flow values """
    class Meta:
        model = db_models.DlyFlow
        sqlalchemy_session = db_session

    station_number = None
    year = factory.Sequence(lambda n: 2011 + n // 12)  # start at 2017, increase another year after every 12th instance
    month = factory.Sequence(lambda n: (n % 12) + 1)  # always between 1-12, even n increases past 12.
    full_month = 1
    no_days = 30

    # Use BASE_FLOWS to generate a starting set of values. BASE_FLOWS has 12 values, one for each month.
    # the map statements increase the flow by 10% every 12 months. This allows us to have
    # some variation in yearly data for visualization/testing.
    monthly_mean = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) * 10)
    monthly_total = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) * 300)
    min = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) * 10 - 5)
    max = factory.Sequence(lambda n: (BASE_FLOWS[n % 12] + (0.1 * (n//12))) * 10 + 5)
    station = None


class StationFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ factory to generate water level stations """

    class Meta:
        model = db_models.Station
        sqlalchemy_session = db_session
        exclude = ('_stream_name',)

    # excluded
    _stream_name = factory.Faker('last_name')

    # not a password, just a convenient way to generate the same format as the regular station IDs
    station_number = factory.Faker('password', length=8, special_chars=False, digits=True, upper_case=True, lower_case=False)
    station_name = factory.LazyAttribute(lambda o: f"{o._stream_name} Creek")
    prov_terr_state_loc = 'BC'
    regional_office_id = 'VI123'
    latitude = factory.Faker('coordinate', center=DEFAULT_COORDS["lat"], radius=0.1)
    longitude = factory.Faker('coordinate', center=DEFAULT_COORDS["lng"], radius=0.1)
    drainage_area_gross = 500
    drainage_area_effect = 3000
    rhbn = 0
    real_time = 1

    geom = factory.LazyAttribute(lambda p: WKTElement(Point(p.longitude, p.latitude).wkt, srid=4326))

    monthly_flows = factory.RelatedFactoryList(MonthlyFlowFactory, 'station', size=24)
    monthly_levels = factory.RelatedFactoryList(MonthlyLevelFactory, 'station', size=24)
