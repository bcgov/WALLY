from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session
from geojson import Point, Feature, FeatureCollection, Polygon, MultiPolygon
from typing import List
from sqlalchemy import Integer, String, Column, DateTime, Float, func
from sqlalchemy.inspection import inspect
from geoalchemy2.shape import to_shape
from shapely.geometry import Polygon
from logging import getLogger
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
            column = cls.SHAPE if cls.shape_column_exists() else cls.GEOMETRY
            q = q.filter(
                func.ST_Intersects(search_area.wkt, column)
            )

        return q.all()

    @classmethod
    def get_as_geojson(cls, db: Session, search_area: Polygon = None) -> FeatureCollection:
        """ calls get_all and formats the result as geojson """
        rows = cls.get_all(db, search_area)

        # add properties to geojson Feature objects
        points = [
            cls.get_as_feature(row) for row in rows
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
    def lat_lon_exists(cls):
        columns = cls.__table__.columns
        return "LATITUDE" in columns and \
               "LONGITUDE" in columns

    @classmethod
    def get_as_feature(cls, row):
        return Feature(
            geometry=Point((row.LONGITUDE, row.LATITUDE)) if cls.lat_lon_exists()
            else to_shape(row.SHAPE if cls.shape_column_exists() else row.GEOMETRY),
            id=getattr(row, cls.primary_key_name()),
            properties=row.row2dict()
        )

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name == "GEOMETRY" or column.name == "SHAPE":
                continue
            d[column.name] = str(getattr(self, column.name))
        return d


BaseTable = declarative_base(cls=CustomBase)
BaseLayerTable = declarative_base(cls=CustomLayerBase)
