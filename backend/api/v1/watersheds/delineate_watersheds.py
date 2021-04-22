"""
Functions for delineating watersheds
"""
import base64
import datetime
import logging
import requests
import geojson
import json
import math
import re
import os
import uuid
import rasterio
import fiona
import time
from shapely import wkt, wkb
from rasterio.features import shapes
from whitebox_tools import WhiteboxTools
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Tuple, List
from urllib.parse import urlencode, unquote
from geojson import FeatureCollection, Feature
from operator import add
from osgeo import gdal, ogr, osr
from shapely.geometry import Point, Polygon, MultiPolygon, shape, box, mapping
from shapely.ops import transform, unary_union
from starlette.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from pyeto import thornthwaite, monthly_mean_daylight_hours, deg2rad

from api.config import WATERSHED_DEBUG, RASTER_FILE_DIR
from api.utils import normalize_quantity
from api.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326, transform_4326_4140
from api.v1.models.isolines.controller import calculate_runoff_in_area
from api.v1.models.scsb2016.controller import get_hydrological_zone
from api.v1.watersheds.prism import mean_annual_precipitation
from api.v1.watersheds.cdem import CDEM
from api.v1.streams.controller import get_nearest_streams

from api.v1.watersheds.schema import LicenceDetails, SurficialGeologyDetails, FishObservationsDetails, WaterApprovalDetails

from api.v1.aggregator.controller import feature_search, databc_feature_search

from external.docgen.controller import docgen_export_to_xlsx
from external.docgen.templates import SURFACE_WATER_XLSX_TEMPLATE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WATERSHEDS')

SEC_IN_YEAR = 31536000

# create an instance of WhiteboxTools
# https://github.com/jblindsay/whitebox-tools
wbt = WhiteboxTools()

# the whitebox_tools cli is installed to /usr/local/bin by the Dockerfile.
wbt.set_whitebox_dir('/usr/local/bin/')
CDEM_FILE = f"{RASTER_FILE_DIR}/Burned_CDEM_4326.tif"
SRTM_FILE = f"{RASTER_FILE_DIR}/Burned_SRTM_3005.tif"


def augment_dem_watershed_with_fwa(
        db: Session,
        dem_watershed: Polygon,
        watershed_id: int,
        click_point: Point,
        start_polygon_buffer_distance: float = 100,
        min_valid_area: float = 5000,
        min_area_ratio: float = 0.01):
    """
    Augments a DEM-derived watershed (in vector Polygon form) with Freshwater Atlas fundamental
    watersheds.

    The DEM watershed is first clipped to the FWA fundamental watershed polygons that are upstream from
    the point of interest. This ensures that the DEM watershed does not go outside
    the boundaries of the subject stream's watershed (using Freshwater Atlas boundaries).

    Second, the query then creates a mask of watershed polygons that exclude polygons that are
    close to the point of interest.  This gap around the starting point will be filled by the DEM
    derived watershed. The reason that ST_Intersects and ST_Buffer are involved in creating this mask
    instead of merely excluding the polygon containing the point of interest is that some wider rivers
    have multiple watershed polygons representing the river itself and/or face units.  We may need to
    exclude several polygons if they are close to the dropped point.

    Arguments:
    start_polygon_buffer_distance: a buffer distance that is added to the starting polygon to ensure
    that other polygons that are very close to the start point are caught by ST_Intersects. This is 
    primarily so that face units and watershed polygons that represent the river width for larger
    rivers are both caught by ST_Intersects.

    min_valid_area: The minimum valid area that the DEM watershed must be before we consider
    it to be completely invalid.  This is meant to catch watersheds that only ended up being
    1 or 2 DEM cells (caused by some kind of data error).

    min_area_ratio: The minimum ratio between the DEM derived watershed and the FWA Upstream estimate
    before we consider the DEM derived watershed to be invalid.  For example, if the DEM watershed
    is less than 30% of the FWA upstream estimate, we assume something went wrong delineating the DEM
    catchment.
    """

    logger.info("--------------------------------")
    logger.info("WATERSHED_ID: %s", watershed_id)
    logger.info("--------------------------------")

    nearest_stream = get_nearest_streams(db, click_point, limit=1)[0]
    nearest_stream_id = nearest_stream.get('id')
    logger.info("-----stream:  %s", nearest_stream_id)

    logger.info(dem_watershed)
    q = """
        with subwscode_ltree as (
            SELECT  "WATERSHED_FEATURE_ID" as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    freshwater_atlas_watersheds
            WHERE   "WATERSHED_FEATURE_ID" = :watershed_feature_id
        ),
        stream_subwscode_ltree as (
            SELECT  
                    geom,
                    origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM (
                select  "LINEAR_FEATURE_ID" as origin_id,
                        "GEOMETRY" as geom,
                        (replace(replace(("FWA_WATERSHED_CODE")::text, '-000000'::text, ''::text), '-'::text, '.'::text))::ltree as wscode_ltree,
                        (replace(replace(("LOCAL_WATERSHED_CODE")::text, '-000000'::text, ''::text), '-'::text, '.'::text))::ltree as localcode_ltree
                FROM    freshwater_atlas_stream_networks
                WHERE   "LINEAR_FEATURE_ID" = :stream_feature_id
            ) streams_ltree 
        ),
        polygons_touching_click_point as (
            SELECT w."GEOMETRY" as geom, w."WATERSHED_FEATURE_ID" as linear_feature_id, ST_Area(w."GEOMETRY") as area
            FROM   freshwater_atlas_watersheds w, stream_subwscode_ltree s
            WHERE  ST_Intersects(w."GEOMETRY", s.geom)
        ),
        watershed_fwa_polygons as (
            SELECT  "WATERSHED_FEATURE_ID" as watershed_feature_id,
                    "GEOMETRY" as geom,
                    ST_Area("GEOMETRY") as area
            FROM    freshwater_atlas_watersheds
            WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from subwscode_ltree) OR (select origin_wscode from subwscode_ltree) = (select origin_localcode from subwscode_ltree))
        ),
        polygons_upstream_by_stream_point as (
            SELECT  "WATERSHED_FEATURE_ID" as watershed_feature_id,
                    "GEOMETRY" as geom,
                    ST_Area("GEOMETRY") as area
            FROM    freshwater_atlas_watersheds
            WHERE   wscode_ltree <@ (select origin_wscode from stream_subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from stream_subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from stream_subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from stream_subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from stream_subwscode_ltree) OR (select origin_wscode from stream_subwscode_ltree) = (select origin_localcode from stream_subwscode_ltree))
        ),
        dem_watershed AS (
            SELECT ST_Intersection(ST_Simplify(ST_SetSRID(ST_GeomFromText(:dem_watershed), 4326), 0.001), (
                select ST_Union(geom) from (
                    select geom from watershed_fwa_polygons
                    UNION SELECT geom
                    FROM polygons_touching_click_point
                ) sq
            )) as geom
        ),
        watershed_mask AS (
            SELECT  geom,
                    area
            FROM    polygons_upstream_by_stream_point
            WHERE   NOT ST_Intersects(
                geom,
                ST_Transform(
                    ST_Buffer(
                        ST_Transform(
                            (select "GEOMETRY" from freshwater_atlas_watersheds where "WATERSHED_FEATURE_ID" = :watershed_feature_id),
                            3005
                        ),
                        :buffer_distance
                    ),
                    4326
                )
            )
        )
        SELECT
        CASE
            WHEN ST_area((select ST_Transform(geom, 3005) from dem_watershed)) / ST_Area(ST_Transform((select ST_Collect(geom) from watershed_fwa_polygons), 3005)) > :min_area_ratio
            AND ST_area(ST_Transform((select geom from dem_watershed), 3005)) > :min_valid_area
        THEN (
            Select ST_AsBinary(ST_Union(geom))
            FROM (
                SELECT          geom FROM dem_watershed
                UNION SELECT    geom from watershed_mask
                UNION SELECT    ST_Intersection(p.geom, d.geom) as geom
                FROM            dem_watershed d, polygons_touching_click_point p
            ) combined
        )
        ELSE (  
            SELECT ST_AsBinary(ST_Union(geom))
            FROM watershed_fwa_polygons
        )
        END
        AS watershed

    """

    res = db.execute(q, {
        "watershed_feature_id": watershed_id,
        "stream_feature_id": nearest_stream_id,
        "dem_watershed": dem_watershed.wkt,
        "buffer_distance": start_polygon_buffer_distance,
        "min_valid_area": min_valid_area,
        "min_area_ratio": min_area_ratio
    })
    record = res.fetchone()

    if not record:
        logger.warning(
            'unable to calculate watershed from watershed feature id %s', watershed_id)
        return None

    # return a Shapely shape of the result (Polygon). This can be loaded into a GeoJSON Feature.
    feature = shape(
        wkb.loads(record['watershed'].tobytes())
    )

    logger.info("-----------------------------------")
    logger.info("AUGMENTED DEM+FWA WATERSHED AREA: %s", feature.area)
    logger.info("-----------------------------------")
    return feature


def get_cross_border_catchment_area(db: Session, point: Point):
    """
        returns a polygon comprised of Hydrosheds originating from a point
    """
    q = """
        WITH RECURSIVE hydrosheds_walkup (hybas_id, geom) AS
        (
            SELECT hybas_id, wsd.geom
            FROM hydrosheds.hybas_lev12_v1c wsd
            WHERE ST_intersects(geom, ST_SetSRID(ST_GeomFromText(:point_wkt), 3005))

            UNION ALL

            SELECT b.hybas_id, b.geom
            FROM hydrosheds.hybas_lev12_v1c b,
            hydrosheds_walkup w
            WHERE b.next_down = w.hybas_id
        )
        SELECT ST_AsBinary(ST_Transform(ST_Collect(geom), 4326))
        FROM hydrosheds_walkup
    """
    res = db.execute(q, {"point_wkt": point.wkt})
    record = res.fetchone()

    feature = shape(
        wkb.loads(record[0].tobytes())
    )

    return feature


def get_full_stream_catchment_area(db, watershed_id):
    """
    returns the catchment of the entire selected stream.
    """

    q = """
                with subwscode_ltree as (
                    SELECT  wscode_ltree as origin_wscode
                    FROM    freshwater_atlas_watersheds
                    WHERE   "WATERSHED_FEATURE_ID" = :watershed_id
                )

                SELECT
                    ST_AsBinary(ST_Union(geom)) as geom
                FROM    freshwater_atlas_watersheds
                WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)

    """

    if WATERSHED_DEBUG:
        logger.info(
            "Getting entire stream catchment area from database, feature id: %s", watershed_id)

    res = db.execute(q, {"watershed_id": watershed_id})

    if WATERSHED_DEBUG:
        logger.info("Whole stream catchment query finished %s", res)

    record = res.fetchone()

    if WATERSHED_DEBUG:
        logger.info("Whole stream catchment record %s", record)

    if not record or not record[0]:
        logger.warning(
            'unable to calculate watershed from watershed feature id %s', watershed_id)
        return None

    return transform(
        transform_3005_4326, shape(
            wkb.loads(record[0].tobytes())
        ))


def get_upstream_catchment_area(db: Session, watershed_feature_id: int, include_self=False):
    """ returns the union of all FWA watershed polygons upstream from
        the watershed polygon with WATERSHED_FEATURE_ID as a Feature

        Two methods are used:

        1. calculate_upstream_catchment_starting_upstream
        This method includes only polygons that start upstream from the base polygon indicated
        by `watershed_feature_id`. This prevents collecting too many polygons around the starting
        point and traveling up the next downstream tributary. However, this has the effect
        of not including the "starting" polygon, and may not work near the headwater of streams.

        The first method (marked with "starting_upstream") can optionally include a polygon by its
        WATERSHED_FEATURE_ID. This is used to include the starting polygon in the collection, without
        collecting additional polygons that feed into it.

        2. If no records are returned, the second method, which collects all polygons upstream from
        the closest downstream tributary, is used.

        See https://www2.gov.bc.ca/assets/gov/data/geographic/topography/fwa/fwa_user_guide.pdf
        for more info.
    """
    if WATERSHED_DEBUG:
        logger.info(
            "Getting upstream catchment area from database, feature id: %s", watershed_feature_id)

    q = """
        with subwscode_ltree as (
            SELECT  "WATERSHED_FEATURE_ID" as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    freshwater_atlas_watersheds
            WHERE   "WATERSHED_FEATURE_ID" = :watershed_feature_id
        )
        SELECT
            ST_AsBinary(ST_Transform(ST_Union("GEOMETRY"), 4326)) as geom
        FROM    freshwater_atlas_watersheds
        WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)
        AND     ltree2text(subltree(
                    localcode_ltree || '000000'::ltree,
                    (select downstream_tributary_code_pos from subwscode_ltree) - 1,
                    (select downstream_tributary_code_pos from subwscode_ltree) - 0
                ))::integer >= (select downstream_tributary from subwscode_ltree)
        AND (NOT wscode_ltree <@ (select origin_localcode from subwscode_ltree) OR (select origin_wscode from subwscode_ltree) = (select origin_localcode from subwscode_ltree))

    """

    res = db.execute(q, {"watershed_feature_id": watershed_feature_id})

    if WATERSHED_DEBUG:
        logger.info("Upstream catchment query finished %s", res)

    record = res.fetchone()

    if WATERSHED_DEBUG:
        logger.info("Upstream catchment record %s", record)

    if not record or not record[0]:
        logger.warning(
            'unable to calculate watershed from watershed feature id %s', watershed_feature_id)
        return None

    feature = shape(
        wkb.loads(record[0].tobytes())
    )
    return feature


def get_watershed_using_dem(db: Session, point: Point, watershed_id, clip_dem=True, dem_source='cdem'):
    """
    Use Whitebox Tools to calculate the upstream drainage area from point

    First generate an overestimate of the catchment using a full stream
    catchment query (full stream because it's a fast query). We also add
    Hydrosheds starting from the original FWA fundamental polygon to ensure
    we capture the cross border area, if applicable (note: could be refined to
    select Hydrosheds only if we detect that we are hitting a border).

    Next, export a new raster from the DEM (a pre-processed DEM with burned streams)
    for tiles that intersect with the above over-estimated catchment.  The catchment
    is then refined using the Whitebox Tools functions FlowAccumulationFullWorkflow,
    SnapPourPoints and Watershed. The Whitebox Tools raster to vector function is
    used to return a vector format watershed.  See `wbt_calculate_watershed` for more
    on this step.

    The resulting watershed will show a "pixelated" pattern around the edges corresponding
    to the size of the pixels (or the resolution) of the source DEM (e.g. 30m or 90m edges etc.).

    `dem_source`: either cdem or srtm.  CDEM data is generally lower resolution but may have
    fewer gaps in data further away from the US border. SRTM data is good near the US border but
    data quality needs to be investigated further north.
    `cdem` requires a stream-burned raster to be loaded in the `dem.x_ws_cdem` table.
    `srtm` requires a stream-burned raster in the `dem.x_ws_srtm` table.

    Hydrosheds data:  https://www.hydrosheds.org/ via FWAPG https://github.com/smnorris/fwapg
    Whitebox Tools: https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html
    Hydrosheds recursive query from https://github.com/smnorris/fwapg/blob/main/sql/functions/FWA_WatershedExBC.sql
    """

    border_crossings = list(set(watershed_touches_border(db, watershed_id)))
    upstream_area = None

    # get an overestimate of the catchment area so that we can crop
    # the DEM to a more manageable size.

    if len(border_crossings):
        logger.info("--------- using cross border ---------")
        logger.info("- border crossings: %s", border_crossings)

        if 'USA_49' in border_crossings:
            logger.info(
                "- Stream crosses US border.  Forcing use of SRTM as DEM source.")
            dem_source = 'srtm'

        upstream_area = get_cross_border_catchment_area(
            db, transform(transform_4326_3005, point)).envelope

        logger.info("--------------------------------------")

    else:
        upstream_area = get_upstream_catchment_area(db, watershed_id).envelope

    # setup config to be used with WBT and the spatial features.
    # CDEM uses SRID 4326, so snap_distance must be in degrees
    # our SRTM source uses 3005, so set snap_distance to meters.
    using_srid = 4326
    snap_distance = 0.002  # degrees
    dem_file = CDEM_FILE
    if dem_source == 'srtm':
        dem_file = SRTM_FILE
        point = transform(transform_4326_3005, point)
        snap_distance = 100  # metres
        using_srid = 3005
        upstream_area = transform(
            transform_4326_3005, upstream_area).buffer(1000)
    else:
        # create a buffer around the catchment.  this helps prevent accidently cutting
        # too close
        upstream_area = transform(transform_3005_4326, transform(
            transform_4326_3005, upstream_area).buffer(1000))

    (_, result) = wbt_calculate_watershed(
        upstream_area, point, dem_file,
        log=True,
        pntr=False,
        accum_out_type='sca',
        snap_distance=snap_distance, using_srid=using_srid
    )

    if dem_source == 'srtm':
        if result.area > 5000:
            return transform(transform_3005_4326, result)

    elif transform(transform_4326_3005, result).area > 5000:
        return result

    # did not get a valid result.
    return None


def watershed_touches_border(db: Session, watershed_feature_id: int) -> List[str]:
    """
    Returns an array of strings indicating which borders the watershed upstream from
    watershed_feature_id touches. The array will be zero length if no borders were reached.
    """

    q = """
    with subwscode_ltree as (
            SELECT  "WATERSHED_FEATURE_ID" as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    freshwater_atlas_watersheds
            WHERE   "WATERSHED_FEATURE_ID" = :watershed_feature_id
        ),
        upstream as (
            SELECT  "GEOMETRY" as geom
            FROM    freshwater_atlas_watersheds
            WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from subwscode_ltree) OR (select origin_wscode from subwscode_ltree) = (select origin_localcode from subwscode_ltree))
        )

    SELECT border
    FROM fwa_approx_borders b
    INNER JOIN upstream w ON ST_Intersects(b.geom, w.geom)
    """
    borders = []
    res = db.execute(q, {"watershed_feature_id": watershed_feature_id})
    return [row['border'] for row in res]


def wbt_calculate_watershed(
        watershed_area: MultiPolygon,
        point: Point,
        dem_file: str,
        log: bool = True,
        pntr: bool = True,
        accum_out_type: str = 'sca',
        snap_distance: float = 1000,
        using_srid: int = 3005) -> (Point, MultiPolygon):
    """
    Given a watershed region (an overestimate to crop the original DEM raster to), a starting point,
    and a path to a DEM file (`dem_file`), use WhiteboxTools to generate an upstream watershed from the point.
    Returns a tuple containing a snapped starting point and a watershed polygon.

    Use `get_upstream_catchment_area()` or a query like `WHERE FWA_WATERSHED_CODE LIKE 100-123456-%`
    (for example) to generate an overestimate. The input stream-burned DEM file will be cropped to
    these extents to make it easier and faster to run the watershed analysis.

    Optional arguments:
    `log`:  run WhiteboxTools D8FlowAccumulation with the --log flag.  Tranforms raster values
    using log to prevent saturating areas with max values.
    # d8flowaccumulation
    See https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html

    `snap_distance`: the max distance that SnapPourPoints should search for a suitable stream.
    Always use an appropriate value for the map unit (e.g. 1000 m for EPSG:3005; 0.01 deg for EPSG:4326).
    If the value is too large, the point might get snapped to a larger nearby stream.

    `pntr`: If True, use the output from D8Pointer as input for D8FlowAccumulation. If False, use the original
    stream-burned and filled DEM as input.

    `using_srid`: the SRID that we are working in (4326 or 3005).  All files and features (DEM, input polygons)
    should use the same projection. Results may be off or blank (and fail silently) if this is set wrong.
    """

    # callback function to suppress progress output.
    def wbt_suppress_progress_output(value):
        if not "%" in value:
            logger.info(value)

    file_000_extent = TemporaryDirectory()
    file_010_dem = NamedTemporaryFile(
        suffix='.tif', prefix="010_dem_")
    file_020_dem_filled = NamedTemporaryFile(
        suffix='.tif', prefix='020_filled_')
    file_030_fdr = NamedTemporaryFile(
        suffix='.tif', prefix='030_fdr_')
    file_040_fac = NamedTemporaryFile(
        suffix='.tif', prefix='040_fac_')
    file_050_point_shp = TemporaryDirectory()
    file_060_directory = TemporaryDirectory()
    file_060_snapped_pour_point = NamedTemporaryFile(
        dir=file_060_directory.name, suffix='.shp', prefix='060_snapped_')
    file_070_watershed = NamedTemporaryFile(
        suffix='.tif', prefix="070_ws_")
    file_080_directory = TemporaryDirectory()

    # Define a point feature geometry with one attribute
    poly_schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    # Write a new Shapefile with the envelope.
    with fiona.open(f"{file_000_extent.name}/extent.shp", 'w', 'ESRI Shapefile', poly_schema) as c:
        c.write({
            'geometry': mapping(watershed_area.envelope),
            'properties': {'id': 123},
        })
        extent_shp_file = c.name

    gdal.Warp(
        destNameOrDestDS=file_010_dem.name,
        srcDSOrSrcDSTab=dem_file,
        cutlineDSName=f"{file_000_extent.name}/{extent_shp_file}.shp",
        cropToCutline=True
    )

    # use either BreachDepressionsLeastCost or BreachDepressions, not both.
    # Author recommends BreachDepressionsLeastCost but worth testing both.
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#breachdepressionsleastcost
    # breach_dist = 100
    # wbt.breach_depressions_least_cost(
    #     file_010_dem.name,
    #     file_020_dem_filled.name,
    #     breach_dist, max_cost=10, min_dist=True,
    #     callback=wbt_suppress_progress_output
    # )

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#breachdepressions
    wbt.breach_depressions(
        file_010_dem.name,
        file_020_dem_filled.name,
    )

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#d8pointer
    wbt.d8_pointer(
        file_020_dem_filled.name,
        file_030_fdr.name,
        callback=wbt_suppress_progress_output
    )

    accum_input_file = file_030_fdr.name
    if not pntr:
        accum_input_file = file_020_dem_filled.name

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#D8FlowAccumulation
    wbt.d8_flow_accumulation(
        accum_input_file,
        file_040_fac.name,
        out_type=accum_out_type,
        log=log, pntr=pntr, callback=wbt_suppress_progress_output
    )

    # Define a point feature geometry with one attribute
    shp_schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    # Write a new Shapefile for the starting stream point. This will be used as the input vector point
    # to be snapped to the nearest stream pixel of the Flow Accumulation raster.
    with fiona.open(f"{file_050_point_shp.name}/stream_point.shp", 'w', 'ESRI Shapefile', shp_schema) as c:
        c.write({
            'geometry': mapping(point),
            'properties': {'id': 123},
        })

        if WATERSHED_DEBUG:
            logger.info('Wrote shapefile')
        point_shp_file = c.name

    #
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#JensonSnapPourPoints
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#SnapPourPoints
    snap_result = wbt.snap_pour_points(
        f"{file_050_point_shp.name}/{point_shp_file}.shp",
        file_040_fac.name,
        file_060_snapped_pour_point.name,
        snap_distance, callback=wbt_suppress_progress_output)

    with fiona.open(file_060_snapped_pour_point.name, 'r', 'ESRI Shapefile') as snp:
        snapped_pt = shape(next(iter(snp)).get('geometry'))

    if WATERSHED_DEBUG:
        logger.info('Wrote snapped point')
        logger.info('----- snap distance from stream point: %s',
                    snapped_pt.distance(point))
        logger.info('--------------------------------------------------')

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#watershed
    watershed_result = wbt.watershed(
        file_030_fdr.name,
        file_060_snapped_pour_point.name,
        file_070_watershed.name, esri_pntr=False, callback=wbt_suppress_progress_output)

    # file statistics
    if WATERSHED_DEBUG:
        logger.info('-------Watershed analysis file statistics-------')
        logger.info('%s %s', file_010_dem.name,
                    os.stat(file_010_dem.name).st_size)
        logger.info('%s %s', file_020_dem_filled.name,
                    os.stat(file_020_dem_filled.name).st_size)
        logger.info('%s %s', file_030_fdr.name,
                    os.stat(file_030_fdr.name).st_size)
        logger.info('%s %s', file_040_fac.name,
                    os.stat(file_040_fac.name).st_size)
        logger.info('%s %s', file_060_snapped_pour_point.name,
                    os.stat(file_060_snapped_pour_point.name).st_size)
        logger.info('%s %s', file_070_watershed.name,
                    os.stat(file_070_watershed.name).st_size)
        logger.info('------------------------------------------------')

    start = time.perf_counter()

    # set up GDAL settings for reading the Watershed output raster
    # and converting it to a polygon.
    sourceRaster = gdal.Open(file_070_watershed.name)
    band = sourceRaster.GetRasterBand(1)
    bandArray = band.ReadAsArray()
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outDatasource = driver.CreateDataSource(
        f"{file_080_directory.name}/watershed_result.shp")
    outLayer = outDatasource.CreateLayer("watershed", srs=None)
    gdal.Polygonize(band, band, outLayer, -1, [], callback=None)
    outDatasource.Destroy()
    sourceRaster = None

    elapsed = (time.perf_counter() - start)

    logger.info('-------------------------------')
    logger.info('VECTORIZING TOOK %s', elapsed)
    logger.info('-------------------------------')

    with fiona.open(f"{file_080_directory.name}/watershed_result.shp", 'r', 'ESRI Shapefile') as ws_result:

        watershed_result = None
        ws_result_list = None
        if using_srid == '3005':
            ws_result_list = [transform(transform_3005_4326, shape(
                poly['geometry'])) for poly in ws_result]
        else:
            ws_result_list = [shape(poly['geometry']) for poly in ws_result]
        watershed_result = MultiPolygon(ws_result_list)
    return (snapped_pt, watershed_result)
