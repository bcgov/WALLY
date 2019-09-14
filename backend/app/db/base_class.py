from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session
from geojson import Point, Feature, FeatureCollection, Polygon, MultiPolygon
from typing import List
from sqlalchemy import Integer, String, Column, DateTime, Float, func
from sqlalchemy.inspection import inspect
from geoalchemy2.shape import to_shape
from logging import getLogger
logger = getLogger("CustomBase")


class CustomBase(object):
    pass


class CustomLayerBase(object):

    @classmethod
    def get_all(cls, db: Session, bbox: List[float] = []):
        """ gets all records, with an optional bounding box """
        q = db.query(cls)

        if len(bbox) == 4:
            column = cls.SHAPE if cls.shape_column_exists() else cls.GEOMETRY
            q = q.filter(
                column.intersects(func.ST_MakeEnvelope(*bbox))
            )

        return q.all()

    @classmethod
    def get_as_geojson(cls, db: Session, bbox: List[float] = []) -> FeatureCollection:
        """ calls get_all and formats the result as geojson """
        rows = cls.get_all(db, bbox)
        logger.info(rows)
        # add properties to geojson Feature objects
        points = []
        for row in rows:
            id = cls.primary_key()
            properties = row.row2dict()
            geometry = Point((row.LONGITUDE, row.LATITUDE)) if cls.lat_lon_exists() \
                else to_shape(row.SHAPE if cls.shape_column_exists() else row.GEOMETRY)
            logger.info(geometry)
            feature = Feature(geometry=geometry, id=id, properties=properties)
            points.append(feature)

        # points = [
        #     Feature(
        #         geometry=Point((row.LONGITUDE, row.LATITUDE)) if cls.lat_lon_exists()
        #         else to_shape(row.SHAPE if cls.shape_column_exists() else row.GEOMETRY),
        #         id=cls.primary_key(),
        #         properties=row.row2dict()
        #     ) for row in rows
        # ]

        return FeatureCollection(points)

    @classmethod
    def primary_key(cls):
        return inspect(cls).primary_key[0].name

    @classmethod
    def shape_column_exists(cls):
        return "SHAPE" in cls.__table__.columns

    @classmethod
    def lat_lon_exists(cls):
        columns = cls.__table__.columns
        return "LATITUDE" in columns and \
               "LONGITUDE" in columns

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name == "GEOMETRY":
                continue
            d[column.name] = str(getattr(self, column.name))
        return d

    pass


BaseTable = declarative_base(cls=CustomBase)
BaseLayerTable = declarative_base(cls=CustomLayerBase)
