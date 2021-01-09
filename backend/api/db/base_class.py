from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session
from geojson import Point, Feature, FeatureCollection, Polygon, MultiPolygon
from typing import List
from sqlalchemy import Integer, String, Column, DateTime, Float, func, text
from sqlalchemy.inspection import inspect
from geoalchemy2.shape import to_shape
from shapely.geometry import Polygon
from logging import getLogger
from datetime import datetime

logger = getLogger("CustomBase")


class CustomBase(object):
    pass


class CustomLayerBase(object):

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    @classmethod
    def get_all(cls, db: Session, search_area: Polygon = None):
        """ gets all records, with an optional bounding box """
        q = db.query(cls)

        if search_area:
            column = cls.get_geom_column(db)
            q = q.filter(
                func.ST_Intersects(func.ST_GeomFromText(
                    search_area.wkt, 4326), column)
            )
        objs = q.all()
        # logger.info(objs)
        return objs

    @classmethod
    def get_as_geojson(cls, db: Session, search_area: Polygon = None) -> FeatureCollection:
        """ calls get_all and formats the result as geojson """
        rows = cls.get_all(db, search_area)
        geom = cls.get_geom_column(db)

        # add properties to geojson Feature objects
        points = [
            cls.get_as_feature(row, geom) for row in rows
        ]

        return FeatureCollection(points)

    @classmethod
    def primary_key(cls):
        return inspect(cls).primary_key[0]

    @classmethod
    def primary_key_name(cls):
        return inspect(cls).primary_key[0].name

    @classmethod
    def shape_column_exists(cls):
        return "SHAPE" in cls.__table__.columns

    @classmethod
    def get_geom_column(cls, db: Session):
        geom_cols = db.execute(text(
            """SELECT f_geometry_column FROM geometry_columns WHERE f_table_name=:tablename"""),
            {"tablename": cls.__table__.name})

        col = None

        # uses only the first geometry column found on this table;
        # if more are present, only warnings are outputted.
        for i, row in enumerate(geom_cols):
            if i > 0:
                logger.warning("More than one geometry column found for table %s: %s",
                               cls.__table__.name, row[0])
            else:
                col = row[0]
        return getattr(cls, col)

    @classmethod
    def lat_lon_exists(cls):
        columns = cls.__table__.columns
        return "LATITUDE" in columns and \
               "LONGITUDE" in columns

    @classmethod
    def get_as_feature(cls, row, geom_col):
        return Feature(
            geometry=Point((row.LONGITUDE, row.LATITUDE)) if cls.lat_lon_exists()
            else to_shape(getattr(row, geom_col.name)),
            id=getattr(row, cls.primary_key_name()),
            properties=row.row2dict()
        )

    @classmethod
    def get_as_properties(cls, row):
        return row.row2dict()

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name == "GEOMETRY" or column.name == "SHAPE" or column.name == "geom":
                continue
            d[column.name] = str(getattr(self, column.name))
        return d


class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_date = Column(
        DateTime,
        comment='Date and time (UTC) when the physical record was created in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')


class BaseAudit(object):
    __table_args__ = {'schema': 'metadata'}

    create_user = Column(
        String(100), comment='The user who created this record in the database.')
    create_date = Column(
        DateTime,
        default=datetime.now,
        comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(
        String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         default=datetime.now,
                         onupdate=datetime.now,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(
        DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


BaseTable = declarative_base(cls=CustomBase)
BaseLayerTable = declarative_base(cls=CustomLayerBase)

Base = declarative_base(cls=Base)
BaseAudit = declarative_base(cls=BaseAudit)
