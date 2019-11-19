import logging

from shapely.geometry import Point
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks

logger = logging.getLogger("api")


def get_streams_apportionment(db: Session, search_point: Point, radius: float) -> list:
    # Test link: http://localhost:8000/api/v1/analysis/streams/apportionment?radius=1000&point=%5B122.95577320109615%2C50.11773019846987%5D
    # Query to get the nearest streams. Uses postgis KNN (nearest neighbour)
    q_nearest_streams = db.query(FreshwaterAtlasStreamNetworks) \
        .with_entities(FreshwaterAtlasStreamNetworks.GEOMETRY,
                       FreshwaterAtlasStreamNetworks.GNIS_NAME,
                       FreshwaterAtlasStreamNetworks.FEATURE_SOURCE,
                       FreshwaterAtlasStreamNetworks.LEFT_RIGHT_TRIBUTARY) \
        .order_by(FreshwaterAtlasStreamNetworks.GEOMETRY
                  .distance_box(func.ST_GeomFromText(search_point.wkt))) \
        .limit(5)

    q_nearest_streams = q_nearest_streams.cte('nearest_streams')

    q_closest_points = db.query(q_nearest_streams) \
        .with_entities(FreshwaterAtlasStreamNetworks.OGC_FID,
                       FreshwaterAtlasStreamNetworks.GNIS_NAME,
                       FreshwaterAtlasStreamNetworks.FEATURE_SOURCE,
                       FreshwaterAtlasStreamNetworks.LEFT_RIGHT_TRIBUTARY,
                       func.ST_AsText(FreshwaterAtlasStreamNetworks.GEOMETRY).label("linestring"),
                       func.ST_AsText(
                           func.ST_ClosestPoint(func.ST_SetSRID(func.ST_GeomFromText(search_point.wkt), 4326),
                                                q_nearest_streams.c.GEOMETRY)).label('streamclosestpoint')) \
        .order_by('streamclosestpoint') \
        .limit(5)
    # print(q_nearest_streams.statement)
    print(q_closest_points)

    # Select from FreshwaterAtlasStreamNetworks row geometries where closest to search_point
    # rs_nearest_streams = q_nearest_streams.all()
    rs_closest_stream_points = q_closest_points.all()
    print(rs_closest_stream_points)

    return rs_closest_stream_points
