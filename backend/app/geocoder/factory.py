"""
Creates stream stations and data for dev fixtures and unit tests
"""

import factory
import decimal
from app.db.session import db_session
from shapely.geometry import MultiPolygon, Polygon
from geoalchemy2.elements import WKTElement
from . import db_models

DEFAULT_COORDS = {"lat": 49.25, "lng": -123}


class ParcelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ factory to generate water level stations """

    class Meta:
        model = db_models.Parcel
        sqlalchemy_session = db_session
        exclude = ('_latitude', '_longitude', '_num')

    _latitude = factory.Faker(
        'coordinate', center=DEFAULT_COORDS["lat"], radius=0.1)
    _longitude = factory.Faker(
        'coordinate', center=DEFAULT_COORDS["lng"], radius=0.1)
    _num = factory.Faker('ean', length=8)

    PARCEL_FABRIC_POLY_ID = factory.LazyAttribute(lambda p: f"0{p._num}")

    PARCEL_NAME = factory.LazyAttribute(lambda p: f"0{p._num}")
    PID = factory.LazyAttribute(lambda p: f"0{p._num}")

    geom = factory.LazyAttribute(lambda p: WKTElement(
        MultiPolygon([
            Polygon([
                [float(p._longitude), float(p._latitude)],
                [float(p._longitude +
                       decimal.Decimal(0.01)), float(p._latitude + decimal.Decimal(0.01))],
                [float(p._longitude +
                       decimal.Decimal(0.01)), float(p._latitude)]
            ]),
        ]).wkt, srid=4326))
