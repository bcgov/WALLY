"""
Database tables and data access functions for Wally Data Layer Meta Information
"""
from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql import select
from geojson import Feature, Point, FeatureCollection
from logging import getLogger
from app.geocoder.db_models import geocode
from shapely.geometry import Point
from shapely import wkt
from geoalchemy2.elements import WKTElement

logger = getLogger("geocoder")


def lookup_by_text(db: Session):
    """ look up features by text (e.g. name, an ID number), returning geojson """

    q = select([geocode])
    features = []

    for row in db.execute(q):
        point = wkt.loads(row.center)
        feat = Feature(geometry=point)
        feat['center'] = [point.x, point.y]
        feat['place_name'] = row.primary_id
        feat['place_type'] = row.kind
        features.append(feat)

    fc = FeatureCollection(features)
    return fc
