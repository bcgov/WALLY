import logging

from shapely.geometry import Point
from sqlalchemy import func, text
from sqlalchemy.orm import Session

logger = logging.getLogger("api")


def get_streams_with_apportionment(db: Session, search_point: Point, weighting_factor=2) -> list:
    streams = get_nearest_streams(db, search_point)
    streams_with_apportionment = get_all_apportionment(streams, weighting_factor)
    return streams_with_apportionment


def get_nearest_streams(db: Session, search_point: Point) -> list:
    # Get the nearest 10 streams to the point
    sql = text("""
      SELECT
        nearest_streams."OGC_FID" as ogc_fid,
        nearest_streams."LENGTH_METRE" as length_metre,
        nearest_streams."FEATURE_SOURCE" as feature_source,
        nearest_streams."GNIS_NAME" as gnis_name,
        nearest_streams."LEFT_RIGHT_TRIBUTARY" as left_right_tributary,
        nearest_streams."GEOMETRY.LEN" as geometry_length,
        ST_AsText(nearest_streams."GEOMETRY") as geometry,
        nearest_streams."WATERSHED_GROUP_CODE" as watershed_group_code,
        ST_Distance(nearest_streams."GEOMETRY",
          ST_SetSRID(ST_GeomFromText(:search_point), 4326)
        ) AS distance_degrees,
        ST_Distance(nearest_streams."GEOMETRY"::geography,
          ST_SetSRID(ST_GeographyFromText(:search_point), 4326)
        ) AS distance,
        ST_AsText(ST_SetSRID(ST_GeomFromText(:search_point), 4326)) as search_point,
        ST_AsText(ST_ClosestPoint(
        nearest_streams."GEOMETRY", 
        ST_SetSRID(ST_GeomFromText(:search_point), 4326))) as closest_stream_point
      FROM
      freshwater_atlas_stream_networks  as nearest_streams
      ORDER BY nearest_streams."GEOMETRY" <#>
        ST_SetSRID(ST_GeomFromText(:search_point), 4326)
      LIMIT 10
    """)
    rp_nearest_streams = db.execute(sql, {'search_point': search_point.wkt})

    return [dict(row) for row in rp_nearest_streams]


# TODO: Create unit test for this
def get_all_apportionment(streams, weighting_factor, force=False):
    """Recursive function that gets the apportionment (in percentage) for all streams"""

    if len(streams) > 10 and not force:
        return True

    # Get the total apportionment
    total_apportionment = 0
    for stream in streams:
        stream['apportionment'] = get_apportionment(stream['distance'], weighting_factor)
        total_apportionment += stream['apportionment']

    # We need to loop again after we have the total so we know the percentage
    for i, stream in enumerate(streams):
        percentage = (stream['apportionment'] / total_apportionment) * 100
        # Delete stream if apportionment is less than 10% and re-calculate
        if percentage < 10:
            del streams[i]
            return get_all_apportionment(streams, weighting_factor)
        stream['apportionment_percentage'] = percentage

    return streams


# TODO: Create unit test for this
def get_apportionment(stream_distance, weighting_factor):
    return 1 / (stream_distance ** weighting_factor)
