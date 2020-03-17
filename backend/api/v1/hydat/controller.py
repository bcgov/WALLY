from sqlalchemy.orm import Session
from sqlalchemy import text, func
import logging

from geojson import Feature, FeatureCollection, Point
from shapely.geometry import Point, Polygon, MultiPolygon, shape, box, mapping
from api.v1.hydat.db_models import Station as StreamStation, DailyFlow, DailyLevel

logger = logging.getLogger("api")


def get_stations_in_area(db: Session, polygon: Polygon) -> list:
    """ Get hydrometric stations given a polygon area (ie watershed)"""
    logger.debug('Get hydrometric stations in polygon', polygon.wkt)

    # Search for point Lat: 49.250285 Lng: -122.953816
    stn_q = db.query(
        StreamStation,
    ).filter(
        func.ST_Intersects(
            func.ST_GeographyFromText(polygon.wkt),
            func.Geography(StreamStation.geom)
        )
    )

    rs_stations = stn_q.all()

    stations = [
        StreamStation.get_as_feature(x, StreamStation.get_geom_column(db))
        for x in rs_stations
    ]

    # TODO:
    # - import fixtures for testing
    return stations
