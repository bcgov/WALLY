import logging

from shapely.geometry import Point
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape

from app.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks

logger = logging.getLogger("api")


def get_streams_apportionment(db: Session, search_point: Point, radius: float) -> list:
    # Test link: http://localhost:8000/api/v1/analysis/streams/apportionment?radius=1000&point=%5B-122.97742734601722%2C50.1054240550059%5D
    # Query to get the nearest streams. Uses postgis KNN (nearest neighbour)
    q_nearest_streams = db.query(FreshwaterAtlasStreamNetworks) \
        .with_entities(FreshwaterAtlasStreamNetworks.GEOMETRY,
                       FreshwaterAtlasStreamNetworks.GNIS_NAME,
                       FreshwaterAtlasStreamNetworks.FEATURE_SOURCE,
                       FreshwaterAtlasStreamNetworks.LEFT_RIGHT_TRIBUTARY) \
        .order_by(FreshwaterAtlasStreamNetworks.GEOMETRY
                  .distance_box(func.ST_GeomFromText(search_point.wkt))) \

    q_nearest_streams = q_nearest_streams.cte('nearest_streams')

    q_closest_points = db.query(q_nearest_streams) \
        .with_entities(FreshwaterAtlasStreamNetworks.OGC_FID,
                       FreshwaterAtlasStreamNetworks.GNIS_NAME,
                       FreshwaterAtlasStreamNetworks.FEATURE_SOURCE,
                       FreshwaterAtlasStreamNetworks.LEFT_RIGHT_TRIBUTARY,
                       func.ST_AsText(FreshwaterAtlasStreamNetworks.GEOMETRY).label("linestring"),
                       func.ST_Distance(q_nearest_streams.c.GEOMETRY, func.ST_SetSRID(func.ST_GeomFromText(search_point.wkt), 4326)),
                       func.ST_AsText(
                           func.ST_ClosestPoint(q_nearest_streams.c.GEOMETRY,
                                                func.ST_SetSRID(func.ST_GeomFromText(search_point.wkt), 4326)
                                                )).label('streamclosestpoint')) \
        .order_by('streamclosestpoint') \
        .limit(5)

    # print(q_nearest_streams.statement)
    print(q_closest_points)

    # Select from FreshwaterAtlasStreamNetworks row geometries where closest to search_point
    # rs_nearest_streams = q_nearest_streams.all()
    rs_closest_stream_points = q_closest_points.all()
    print(rs_closest_stream_points)

    return rs_closest_stream_points


def get_nearest_streams(db: Session, search_point: Point) -> list:
    print('getting nearest streams')
    sql = text("""
  SELECT
    nearest_streams."OGC_FID" as ogc_fid,
    nearest_streams."FEATURE_SOURCE" as feature_source,
    nearest_streams."GNIS_NAME" as gnis_name,
    nearest_streams."LEFT_RIGHT_TRIBUTARY" as left_right_tributary,
    nearest_streams."GEOMETRY.LEN" as geometry_length,
    nearest_streams."GEOMETRY" as geometry,
    nearest_streams."WATERSHED_GROUP_CODE" as watershed_group_code,
    ST_Distance(nearest_streams."GEOMETRY",
      ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    ) AS distance,
    ST_AsText(ST_SetSRID(ST_GeomFromText(:search_point), 4326)) as search_point,
    ST_AsText(ST_ClosestPoint(
    nearest_streams."GEOMETRY", 
    ST_SetSRID(ST_GeomFromText(:search_point), 4326))) as closest_stream_point
  FROM
  freshwater_atlas_stream_networks  as nearest_streams
  WHERE ST_DWithin(
    nearest_streams."GEOMETRY", 
    ST_SetSRID(ST_GeomFromText(:search_point), 4326), 
    :distance_scope)
  ORDER BY nearest_streams."GEOMETRY" <#>
    ST_SetSRID(ST_GeomFromText(:search_point), 4326)
""")
    distance_scope = 0.005  # 500 metresdw

    print(sql)
    print(search_point, search_point.wkt, distance_scope)
    wkb_element = from_shape(search_point, srid=4326)

    rp_nearest_streams = db.execute(sql, {'search_point': search_point.wkt, 'distance_scope': distance_scope})
    print(rp_nearest_streams)

    # print(q_nearest_streams.all())
    # rs_nearest_streams = q_nearest_streams.all()
    return [dict(row) for row in rp_nearest_streams]


def calculate_apportionment(db: Session, search_point: Point):
    nearest_streams = get_nearest_streams(db, search_point)
    for stream in nearest_streams:
        d = stream['distance']
        f = 1/d
        n = len(nearest_streams)
        m = 2 # weighting factor
        stream['apportionment_']