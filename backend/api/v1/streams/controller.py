import logging
from typing import List
from shapely.geometry import Point
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.v1.streams.schema import StreamPoint
from geojson import Point, Feature
from shapely import wkb, wkt
import json

logger = logging.getLogger("api")


def get_nearest_streams_by_ogc_fid(db: Session, search_point: Point, ogc_fids: list) -> list:
    streams_q = db.query(
        FreshwaterAtlasStreamNetworks.OGC_FID.label("ogc_fid"),
        FreshwaterAtlasStreamNetworks.LENGTH_METRE.label("length_metre"),
        FreshwaterAtlasStreamNetworks.FEATURE_SOURCE.label("feature_source"),
        FreshwaterAtlasStreamNetworks.GNIS_NAME.label("gnis_name"),
        FreshwaterAtlasStreamNetworks.LEFT_RIGHT_TRIBUTARY.label(
            "left_right_tributary"),
        FreshwaterAtlasStreamNetworks.GEOMETRY_LEN.label("geometry_length"),
        FreshwaterAtlasStreamNetworks.WATERSHED_GROUP_CODE.label(
            "watershed_group_code"),
        FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.labe(
            "fwa_watershed_code"),
        func.ST_ASText(FreshwaterAtlasStreamNetworks.GEOMETRY).label(
            "geometry"),
        # FreshwaterAtlasStreamNetworks,
        func.ST_Distance(
            FreshwaterAtlasStreamNetworks.GEOMETRY,
            func.ST_SetSRID(func.ST_GeomFromText(search_point.wkt), 4326)
        ).label('distance_degrees'),
        func.ST_Distance(
            func.Geography(FreshwaterAtlasStreamNetworks.GEOMETRY),
            func.ST_GeographyFromText(search_point.wkt)
        ).label('distance'),
        func.ST_AsGeoJSON(func.ST_ClosestPoint(
            FreshwaterAtlasStreamNetworks.GEOMETRY,
            func.ST_SetSRID(func.ST_GeomFromText(search_point.wkt), 4326))
        ).label('closest_stream_point')
    ).filter(FreshwaterAtlasStreamNetworks.OGC_FID.in_(ogc_fids))
    logging.debug(streams_q)

    rs_streams = streams_q.all()
    columns = [col['name'] for col in streams_q.column_descriptions]

    streams_with_columns = []
    for row in rs_streams:
        stream = {columns[i]: item for i, item in enumerate(row)}
        stream['geojson'] = get_feature_geojson(stream)
        stream['closest_stream_point'] = json.loads(
            stream['closest_stream_point'])
        streams_with_columns.append(stream)

    logging.debug(streams_with_columns)
    return streams_with_columns


def get_streams_with_apportionment(
        db: Session,
        search_point: Point,
        limit=10,
        get_all=False,
        with_apportionment=True,
        weighting_factor=2) -> list:
    streams = get_nearest_streams(db, search_point, limit)

    if not with_apportionment:
        return streams

    streams_with_apportionment = get_apportionment(
        streams, weighting_factor, get_all)
    return streams_with_apportionment


def get_nearest_streams(db: Session, search_point: Point, limit=10) -> list:
    # Get the nearest 10 streams to the point
    sql = text("""
      WITH nearest_streams AS (
          select    *
          from      freshwater_atlas_stream_networks streams
          order by  streams."GEOMETRY" <#>
                        ST_SetSRID(ST_GeomFromText(:search_point), 4326)
          limit     10
      )
      SELECT 
        nearest_streams."OGC_FID" as id, 
        nearest_streams."OGC_FID" as ogc_fid,
        nearest_streams."LENGTH_METRE" as length_metre,
        nearest_streams."FEATURE_SOURCE" as feature_source,
        nearest_streams."GNIS_NAME" as gnis_name,
        nearest_streams."LINEAR_FEATURE_ID" as linear_feature_id,
        nearest_streams."LEFT_RIGHT_TRIBUTARY" as left_right_tributary,
        nearest_streams."GEOMETRY.LEN" as geometry_length,
        ST_AsText(nearest_streams."GEOMETRY") as geometry,
        nearest_streams."WATERSHED_GROUP_CODE" as watershed_group_code, 
        nearest_streams."FWA_WATERSHED_CODE" as fwa_watershed_code,
        ST_Distance(nearest_streams."GEOMETRY",
          ST_SetSRID(ST_GeomFromText(:search_point), 4326)
        ) AS distance_degrees,
        ST_Distance(nearest_streams."GEOMETRY"::geography,
          ST_SetSRID(ST_GeographyFromText(:search_point), 4326)
        ) AS distance,
        ST_AsText(ST_SetSRID(ST_GeomFromText(:search_point), 4326)) as search_point,
        ST_AsGeoJSON(ST_ClosestPoint(
        nearest_streams."GEOMETRY", 
        ST_SetSRID(ST_GeomFromText(:search_point), 4326))) as closest_stream_point
      FROM      nearest_streams
      ORDER BY  ST_Distance(nearest_streams."GEOMETRY", ST_SetSRID(ST_GeomFromText(:search_point), 4326)) ASC
      LIMIT     :limit 
    """)
    rp_nearest_streams = db.execute(
        sql, {'search_point': search_point.wkt, 'limit': limit})
    nearest_streams = [
        dict(row,
             geojson=get_feature_geojson(row),
             closest_stream_point=json.loads(row['closest_stream_point'])
             ) for row in rp_nearest_streams
    ]

    return nearest_streams


def get_apportionment(streams, weighting_factor, get_all=False, force_recursion=False):
    """Recursive function that gets the apportionment (in percentage) for all streams"""

    logger.debug('get_apportionment')
    # Don't do recursion if there are more than 10 streams
    if len(streams) > 10 and not get_all and not force_recursion:
        raise RecursionError('Cannot compute apportionment for more than 10 streams. Set '
                             'force_recursion=True.')

    # Get the summation of the inverse distance formula
    total = 0
    for stream in streams:
        stream['inverse_distance'] = get_inverse_distance(
            stream['distance'], weighting_factor)
        total += stream['inverse_distance']

    # We need to loop again after we have the total so we know the percentage
    for i, stream in enumerate(streams):
        percentage = (stream['inverse_distance'] / total) * 100
        # Delete stream if apportionment is less than 10% and re-calculate
        # Skip this if get_all is True
        if percentage < 10 and not get_all:
            del streams[i]
            return get_apportionment(streams, weighting_factor)
        stream['apportionment'] = percentage

    return streams


def get_inverse_distance(stream_distance, weighting_factor):
    return 1 / (stream_distance ** weighting_factor)


def get_feature_geojson(stream) -> Feature:
    stream_copy = dict(stream)
    del stream_copy['closest_stream_point']
    del stream_copy['ogc_fid']
    feature = Feature(
        geometry=wkt.loads(stream_copy['geometry']),
        id=stream['ogc_fid'],
        properties=dict(stream_copy)
    )
    del stream_copy['geometry']
    return feature


def get_connected_streams(db: Session, outflowCode: str) -> list:
    q = db.query(FreshwaterAtlasStreamNetworks) \
        .filter(FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.startswith(outflowCode))

    results = q.all()

    feature_results = [FreshwaterAtlasStreamNetworks.get_as_feature(
        row, FreshwaterAtlasStreamNetworks.GEOMETRY) for row in results]

    return feature_results


def get_nearest_hydat_stream_segments(db: Session, station_number: str) -> List[StreamPoint]:
    """ get nearest stream segments returns the 5 stream segments nearest the
        HYDAT station that match the name of the station.

        This helps with inferring the station location (in cases where the location
        is not clear) because we can run a watershed delineation from each segment
        and compare the results with the listed drainage_area_gross to infer which
        segment the station is likely on.
    """

    q = """
      WITH stn AS (
        select station_name, geom
        from hydat.stations
        where station_number = :station_number
      ),
      nearest_streams AS (
          select    *
          from      freshwater_atlas_stream_networks streams
          order by  streams."GEOMETRY" <#>
                        (select geom from stn)
          limit     5
      )
      SELECT 
        (select ST_AsBinary(geom) from stn) as station_point,
        nearest_streams."GNIS_NAME" as gnis_name,
        nearest_streams."LINEAR_FEATURE_ID" as linear_feature_id,
        ST_AsBinary(
          ST_ClosestPoint(
            nearest_streams."GEOMETRY", 
            (select geom from stn)
          )
        ) as stream_point
      FROM      nearest_streams
      ORDER BY  
        coalesce(nearest_streams."GNIS_NAME" ILIKE '%' || (select split_part(station_name, ' ', 1) from stn) || '%', FALSE) DESC,
        ST_Distance(nearest_streams."GEOMETRY", (select geom from stn)) ASC
    """
    res = db.execute(q, {"station_number": station_number})
    streams = []
    for row in res:
        row = dict(row)
        streams.append(StreamPoint(
            stream_point=wkb.loads(row['stream_point'].tobytes()),
            stream_feature_id=row['linear_feature_id']
        ))
    return streams
