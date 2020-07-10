import logging

import geojson
from geojson import Feature, FeatureCollection
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from shapely.geometry import LineString, CAP_STYLE, JOIN_STYLE, shape, mapping, Point
from shapely.ops import transform, split, snap
from api.v1.aggregator.controller import feature_search
from api.v1.aggregator.helpers import transform_3005_4326, transform_4326_3005
from api.v1.wells.controller import create_line_buffer
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
import json

logger = logging.getLogger("api")


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
        select  ST_Transform(
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
            AND     split_part(
                        "FWA_WATERSHED_CODE", '-',
                        watershed_code_stats.loc_code_last_nonzero_code
                    )::int > split_part(
                        watershed_code_stats.loc_code, '-',
                        watershed_code_stats.loc_code_last_nonzero_code
                    )::int
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

    logger.info('-------------------')
    logger.info('using %s', str(feat_proj))
    logger.info('-------------------')

    line_3005 = transform(transform_4326_3005, line)

    features_intersecting = [
        Feature(
            geometry=feat['geometry'],
            properties=feat['properties']) for feat in features if to_3005(feat_proj, shape(feat['geometry'])
                                                                           ).intersects(line_3005)
    ]

    return FeatureCollection(features_intersecting)
