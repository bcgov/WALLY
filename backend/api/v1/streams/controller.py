

import json

import geojson
import logging

from geojson import Point, Feature, FeatureCollection
from shapely import wkb, wkt
from shapely.geometry import LineString, CAP_STYLE, JOIN_STYLE, shape, mapping, Point
from shapely.ops import transform, split, snap
from typing import List
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.v1.streams.schema import StreamPoint
from api.v1.aggregator.controller import feature_search
from api.v1.aggregator.helpers import transform_3005_4326, transform_4326_3005
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks

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


def get_connected_streams(db: Session, outflowCode: str) -> list:
    q = db.query(FreshwaterAtlasStreamNetworks).filter(
        FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.startswith(outflowCode))

    results = q.all()

    feature_results = [FreshwaterAtlasStreamNetworks.get_as_feature(
        row, FreshwaterAtlasStreamNetworks.GEOMETRY) for row in results]

    return feature_results


def watershed_root_code(code: str) -> str:
    """ truncates zero values from the end of watershed codes, .
        Watershed codes have 21 segments, but most of the segments will
        be a "zero value". E.g.:
        100-123333-432123-000000-000000-000000- .... etc
    """

    return [x for x in code.split('-') if x != '000000']


def to_3005(from_proj, feat):
    """ returns a feature in EPSG:3005, transforming if necessary
        `from_proj` supports 4326 and 3005.
    """

    if from_proj == 3005:
        return feat

    elif from_proj == 4326:
        return transform(transform_4326_3005, feat)

    logger.warn(
        'to_3005: from_proj must be either 4326 or 3005. Feature returned without transforming to 3005.')
    return feat


def get_closest_stream_segment(db: Session, point: Point):
    sql = text("""
      SELECT
        streams."GNIS_NAME" as gnis_name,
        streams."LINEAR_FEATURE_ID" as linear_feature_id,
        streams."DOWNSTREAM_ROUTE_MEASURE" as downstream_route_measure,
        ST_AsGeoJSON(ST_ClosestPoint(
        streams."GEOMETRY", 
        ST_SetSRID(ST_GeomFromText(:search_point), 4326))) as closest_stream_point
      FROM
      freshwater_atlas_stream_networks as streams
      ORDER BY streams."GEOMETRY" <->
        ST_SetSRID(ST_GeomFromText(:search_point), 4326)
      LIMIT 1
    """)
    segment = db.execute(sql, {'search_point': point.wkt}).fetchone()
    return dict(segment,
                closest_stream_point=json.loads(segment.closest_stream_point))


def split_line_by_closest_point(
        line: LineString,
        point: Point):

    distance = line.project(transform(transform_4326_3005, point))
    interpolated_point = line.interpolate(distance)
    snap_line = snap(line, interpolated_point, 0.001)
    split_lines = split(snap_line, interpolated_point)

    return split_lines


def get_stream_line(
        db: Session,
        linear_feature_id: int):

    return db.execute(
        """
        select ST_AsGeoJSON(ST_Transform("GEOMETRY", 3005))
        as "GEOMETRY" from freshwater_atlas_stream_networks
        where "LINEAR_FEATURE_ID" = :linear_feature_id
        """,
        {
            "linear_feature_id": linear_feature_id
        }).fetchone()


def get_split_line_stream_buffers(
        db: Session,
        linear_feature_id: int,
        buffer: float,
        point: Point):

    db_line = get_stream_line(db, linear_feature_id)
    segment = shape(geojson.loads(db_line[0]) if db_line[0] else None)
    split_lines = split_line_by_closest_point(segment, point)
    buffer_lines = [transform(transform_3005_4326, line.buffer(buffer)) for line in split_lines]

    return buffer_lines


def get_downstream_area(
        db: Session,
        linear_feature_id: int,
        buffer: float):

    q = """
        with watershed_code_stats as (
            SELECT DISTINCT
                "FWA_WATERSHED_CODE" as fwa_code,
                "LOCAL_WATERSHED_CODE" as loc_code,
                "DOWNSTREAM_ROUTE_MEASURE" as downstream_route_measure,
                left(
                    regexp_replace(
                        "FWA_WATERSHED_CODE",
                        '000000',
                        '%'
                    ),
                    strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'),
                    '%'
                )) as fwa_prefix
            FROM freshwater_atlas_stream_networks
            WHERE   "LINEAR_FEATURE_ID" = :linear_feature_id
        ),
        selected_stream as (
            select  ST_Transform(
                ST_Buffer(
                    ST_Transform("GEOMETRY", 3005),
                    :buffer),
                    4326
                ) as "GEOMETRY" from freshwater_atlas_stream_networks, watershed_code_stats
            where "FWA_WATERSHED_CODE" = fwa_code
            and
            (CASE
              WHEN "DOWNSTREAM_ROUTE_MEASURE" = 0
              THEN "DOWNSTREAM_ROUTE_MEASURE" <= watershed_code_stats.downstream_route_measure
              ELSE "DOWNSTREAM_ROUTE_MEASURE" < watershed_code_stats.downstream_route_measure
            END)
        )
        select
            ST_AsGeoJSON(ST_Union("GEOMETRY"))
        from    (
            select ST_MakeValid("GEOMETRY") "GEOMETRY" from watershed_code_stats, selected_stream
        ) subq   
        """

    return db.execute(
        q,
        {
            "linear_feature_id": linear_feature_id,
            "buffer": buffer,
        }).fetchone()


def get_upstream_area(
        db: Session,
        linear_feature_id: int,
        buffer: float,
        full_upstream_area: bool):
    """ returns the polygon area upstream from the selected stream feature
    (using the linear_feature_id property of a Freshwater Atlas Stream Networks stream segment) """

    # Gather up the selected stream segments (from the stream's own headwaters
    # down to the mouth of the stream where it drains into the next river),
    # as well as all *upstream* tributary networks from the selected reach.
    # This represents the entire drainage network upstream of the selected
    # reach, combined with just the stream's own geometry downstream (no
    # tributaries downstream of the selected reach are included).
    #
    # these queries work by inspecting the last non-zero code of the local
    # watershed code, which roughly represents the percent distance along the
    # stream of each segment of the stream.

    # First default to the full upstream area by using Freshwater Atlas Watershed polygons that match the
    # stream network codes. This is faster than creating a buffer from all the stream segments,
    # but only works well upstream from the point of interest. This produces a large, filled in
    # polygon that follows the shape of the drainage basin.
    q = """
    with watershed_code_stats as (
        SELECT DISTINCT
            "FWA_WATERSHED_CODE" as fwa_code,
            "LOCAL_WATERSHED_CODE" as loc_code,
            "DOWNSTREAM_ROUTE_MEASURE" as downstream_route_measure,
            (FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1)::int
                as loc_code_last_nonzero_code,
            left(
                regexp_replace(
                    "FWA_WATERSHED_CODE",
                    '000000',
                    '%'
                ),
                strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'),
                '%'
            )) as fwa_prefix
        FROM freshwater_atlas_stream_networks
        WHERE   "LINEAR_FEATURE_ID" = :linear_feature_id
    ),
    streams as (
        select ST_Transform(
            ST_Buffer(
                ST_Transform("GEOMETRY", 3005),
                :buffer),
                4326
            ) as "GEOMETRY" from freshwater_atlas_stream_networks, watershed_code_stats
        where   "FWA_WATERSHED_CODE" = fwa_code and "DOWNSTREAM_ROUTE_MEASURE" >= watershed_code_stats.downstream_route_measure
    )
    select
        ST_AsGeoJSON(ST_Union("GEOMETRY"))
    from    (
        select ST_MakeValid("GEOMETRY") "GEOMETRY" from streams 
        union all
        select  ST_MakeValid("GEOMETRY") "GEOMETRY" from freshwater_atlas_watersheds, watershed_code_stats
        where   "FWA_WATERSHED_CODE" like fwa_prefix
        AND     split_part(
                    "LOCAL_WATERSHED_CODE", '-',
                    watershed_code_stats.loc_code_last_nonzero_code
                )::int > split_part(
                    watershed_code_stats.loc_code, '-',
                    watershed_code_stats.loc_code_last_nonzero_code
                )::int
    ) subq   
    """

    # if the user overrides searching within the full upstream catchment area, search only within <buffer>
    # metres of the stream. This produces a polygon with narrow branches that follows the shape of
    # the stream network.
    # The main difference between this query and the default query is that the "from" subquery selects
    # from FWA Stream Networks, returning buffered linestrings, which takes longer.
    if not full_upstream_area:
        q = """
        with watershed_code_stats as (
            SELECT
                "FWA_WATERSHED_CODE" as fwa_code,
                "LOCAL_WATERSHED_CODE" as loc_code,
                "DOWNSTREAM_ROUTE_MEASURE" as downstream_route_measure,
                (FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1)::int
                    as loc_code_last_nonzero_code,
                left(
                    regexp_replace("FWA_WATERSHED_CODE", '000000', '%'),
                    strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'),
                    '%')
                ) as fwa_prefix
            FROM freshwater_atlas_stream_networks
            WHERE   "LINEAR_FEATURE_ID" = :linear_feature_id
        )
        select
            ST_AsGeoJSON(
                ST_Transform(
                    ST_Buffer(
                        ST_Transform(ST_Collect("GEOMETRY"), 3005),
                        :buffer, 'endcap=round join=round'
                    ),
                    4326
                )
            )
        from    (
            select  "GEOMETRY" from freshwater_atlas_stream_networks, watershed_code_stats
            where   "FWA_WATERSHED_CODE" = fwa_code and "DOWNSTREAM_ROUTE_MEASURE" >= downstream_route_measure
            union all
            select  "GEOMETRY" from freshwater_atlas_stream_networks, watershed_code_stats
            where   "FWA_WATERSHED_CODE" like fwa_prefix
            AND     
            (CASE
              WHEN watershed_code_stats.downstream_route_measure = 0
              THEN 
                split_part(
                  "LOCAL_WATERSHED_CODE", '-',
                  watershed_code_stats.loc_code_last_nonzero_code + 1
                )::int > split_part(
                    watershed_code_stats.loc_code, '-',
                    watershed_code_stats.loc_code_last_nonzero_code + 1
                )::int
              ELSE 
                split_part(
                  "LOCAL_WATERSHED_CODE", '-',
                  watershed_code_stats.loc_code_last_nonzero_code
                )::int > split_part(
                    watershed_code_stats.loc_code, '-',
                    watershed_code_stats.loc_code_last_nonzero_code
                )::int
            END)
        ) subq
        """

    return db.execute(
        q,
        {
            "linear_feature_id": linear_feature_id,
            "buffer": buffer,
        }).fetchone()


def get_features_within_buffer(db: Session, line, distance: float, layer: str) -> FeatureCollection:
    """ List features within a buffer zone from a geometry
    """
    if not line:
        return None

    buf_simplified = line.minimum_rotated_rectangle

    fc = feature_search(db, [layer], buf_simplified)[0].geojson

    features = fc.get('features')
    feat_proj = 4326

    # indicate if features are BC Albers projection
    # DataBC feature collections have a `crs` property containing the
    # name `urn:ogc:def:crs:EPSG::3005`
    if fc.get('crs') and fc.get('crs', {}).get('properties', {}).get('name', "").endswith("3005"):
        feat_proj = 3005

    line_3005 = transform(transform_4326_3005, line)

    features_intersecting = [
        Feature(
            geometry=feat['geometry'],
            properties=feat['properties']) for feat in features if to_3005(feat_proj, shape(feat['geometry'])
                                                                           ).intersects(line_3005)
    ]

    return FeatureCollection(features_intersecting)
