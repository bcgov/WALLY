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
from utils.whitebox_tools import WhiteboxTools
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
from api.config import WATERSHED_DEBUG, RASTER_FILE_DIR, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST_URL
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


gdal.SetConfigOption('AWS_ACCESS_KEY_ID', MINIO_ACCESS_KEY)
gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', MINIO_SECRET_KEY)
gdal.SetConfigOption('AWS_S3_ENDPOINT', MINIO_HOST_URL)
gdal.SetConfigOption('AWS_HTTPS', 'FALSE')
gdal.SetConfigOption('AWS_VIRTUAL_HOSTING', 'FALSE')


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

    return wkb.loads(record[0].tobytes())


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
                    ST_AsBinary(ST_Union("GEOMETRY")) as geom
                FROM    freshwater_atlas_watersheds
                WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)

    """

    if WATERSHED_DEBUG:
        logger.debug(
            "Getting entire stream catchment area from database, feature id: %s", watershed_id)

    res = db.execute(q, {"watershed_id": watershed_id})
    record = res.fetchone()

    if not record or not record[0]:
        logger.warning(
            'unable to calculate watershed from watershed feature id %s', watershed_id)
        return None

    return wkb.loads(record[0].tobytes())


def get_fwa_polygons_for_dem(db: Session, watershed_feature_id: int, stream_feature_id: int, click_point: Point,
                             start_polygon_buffer_distance: float = 100):
    """ returns the union of all FWA watershed polygons upstream from
        the watershed polygon with WATERSHED_FEATURE_ID as a Feature

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
        polygons_touching_streamline as (
            SELECT w."GEOMETRY" as geom, w."WATERSHED_FEATURE_ID" as linear_feature_id
            FROM   freshwater_atlas_watersheds w, stream_subwscode_ltree s
            WHERE  ST_Intersects(w."GEOMETRY", s.geom)
        ),
        polygons_upstream_by_stream_point as (
            SELECT  "WATERSHED_FEATURE_ID" as watershed_feature_id,
                    localcode_ltree,
                    "GEOMETRY" as geom
            FROM    freshwater_atlas_watersheds
            WHERE   wscode_ltree <@ (select origin_wscode from stream_subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from stream_subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from stream_subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from stream_subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from stream_subwscode_ltree) OR (select origin_wscode from stream_subwscode_ltree) = (select origin_localcode from stream_subwscode_ltree))
        ),
        fwa_polygons_upstream AS (
            SELECT "GEOMETRY" as geom
            FROM    freshwater_atlas_watersheds
            WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from subwscode_ltree) OR (select origin_wscode from subwscode_ltree) = (select origin_localcode from subwscode_ltree))
        ),
        working_area AS (
            SELECT geom FROM fwa_polygons_upstream
            UNION SELECT geom FROM polygons_touching_streamline
        ),
        watershed_mask AS (
            SELECT  geom
            FROM    polygons_upstream_by_stream_point
            WHERE   NOT ST_Intersects(
                geom,
                ST_Transform(
                    ST_Buffer(
                        ST_Transform(
                            ST_SetSRID(ST_GeomFromText(:click_point), 4326),
                            3005
                        ),
                        :buffer_distance
                    ),
                    4326
                )
            )
            AND NOT localcode_ltree = (select origin_localcode from subwscode_ltree)
        )
        SELECT
            (select ST_AsBinary(ST_Union(geom)) from working_area) as working_area,
            (select ST_AsBinary(ST_Union(geom)) from watershed_mask) as watershed_mask
    """

    res = db.execute(
        q,
        {
            "watershed_feature_id": watershed_feature_id,
            "stream_feature_id": stream_feature_id,
            "buffer_distance": start_polygon_buffer_distance,
            "click_point": click_point.wkt
        }
    )

    record = res.fetchone()
    working_area = record["working_area"]
    watershed_mask = record["watershed_mask"]

    if not working_area:
        logger.warning(
            'unable to calculate watershed from watershed feature id %s', watershed_feature_id)
        return None

    working_area = wkb.loads(working_area.tobytes())

    if watershed_mask:
        watershed_mask = wkb.loads(watershed_mask.tobytes())

    return (working_area, watershed_mask)


def get_upstream_catchment_area(db: Session, watershed_feature_id: int):
    """ returns the union of all FWA watershed polygons upstream from
        the watershed polygon with WATERSHED_FEATURE_ID as a Feature

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
            ST_AsBinary(ST_Union("GEOMETRY")) as geom
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

    record = res.fetchone()

    if not record or not record[0]:
        logger.warning(
            'unable to calculate watershed from watershed feature id %s', watershed_feature_id)
        return None

    return wkb.loads(record[0].tobytes())


def get_watershed_using_dem(
        db: Session, point: Point, stream_feature_id, watershed_id, dem_source='cdem', use_fwa: bool = False):
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

    Hydrosheds data:  https://www.hydrosheds.org/ via FWAPG https://github.com/smnorris/fwapg
    Whitebox Tools: https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html
    Hydrosheds recursive query from https://github.com/smnorris/fwapg/blob/main/sql/functions/FWA_WatershedExBC.sql
    """

    border_crossings = list(set(watershed_touches_border(db, watershed_id)))
    working_area = None
    dem_error = False

    # upstream_mask: for use with DEM only.
    # this will be added to the DEM delineated watershed to fill out
    # the watershed into the FWA polygons.
    upstream_mask = None

    if len(border_crossings):
        logger.debug("- border crossings: %s", border_crossings)

        if 'USA_49' in border_crossings:
            logger.debug(
                "- Stream crosses US border.  Forcing use of SRTM as DEM source.")
            dem_source = 'srtm'

        working_area = get_cross_border_catchment_area(
            db, transform(transform_4326_3005, point))

    elif use_fwa:
        working_area, upstream_mask = get_fwa_polygons_for_dem(db, watershed_id, stream_feature_id, point)
        working_area = working_area

    else:
        working_area = get_upstream_catchment_area(db, watershed_id)

    # setup config to be used with WBT and the spatial features.
    # CDEM uses SRID 4326, so snap_distance must be in degrees
    # our SRTM source uses 3005, so set snap_distance to meters.
    using_srid = 4326
    snap_distance = 0.001  # degrees
    smoothing_tolerance = 0.002  # degrees
    dem_file = CDEM_FILE
    if dem_source == 'srtm':
        dem_file = SRTM_FILE
        point = transform(transform_4326_3005, point)
        snap_distance = 100  # metres
        smoothing_tolerance = 20  # metres
        using_srid = 3005
        working_area = transform(
            transform_4326_3005, working_area)

    max_tries = 8
    dem_error_threshold = 4  # tries before warning that this watershed may have some issues.
    for n in range(max_tries):
        (result, snapped_point) = wbt_calculate_watershed(
            working_area.envelope, point, dem_file,
            log=True,
            pntr=False,
            accum_out_type='sca',
            snap_distance=snap_distance, using_srid=using_srid
        )

        # if we have an upstream mask, test to make sure the DEM watershed
        # at least reached the masked area.
        if upstream_mask and result.is_valid and result.intersects(upstream_mask) and result.area / working_area.area > 0.01:
            break

        # if the resulting DEM-delineated watershed area is less than 1% of the upstream overestimate,
        # try again with an increased snap distance.
        # Even though we expect the DEM derived watershed to be smaller than the upstream overestimate,
        # we assume that an error occurred if it is 1% or less of the size. The most common error is
        # that the snapped point did not hit the the target stream in the Flow Accumulation raster, so
        # increasing the distance has a good chance of returning a good watershed.
        elif result.is_valid and result.area / working_area.area > 0.01:
            break
        else:
            # if we've tried `dem_error_threshold` times without a good result, set the dem_error.
            # even though we will keep trying, we'll warn the user to double check the result.
            # 4 tries is generally the point where the DEM refinement starts to get noticeably worse.
            if n == dem_error_threshold:
                dem_error = True

            # increase the snap distance and retry.
            if n < max_tries - 1:
                snap_distance *= 2
                logger.info(
                    '-- watershed less than 1%% of the upstream area overestimate, trying again with a larger snap point radius: %s',
                    snap_distance)
            else:
                logger.info("Could not validate that the DEM-delineated polygon is correct")

    # do a quick smooth of the otherwise jagged DEM-derived polygon.
    if use_fwa and smoothing_tolerance:
        result = result \
            .buffer(smoothing_tolerance, join_style=1) \
            .buffer(-smoothing_tolerance, join_style=1)

    if dem_source == 'srtm':
        logger.info('transforming SRTM derived watershed back to 4326')
        result = transform(transform_3005_4326, result)
        snapped_point = transform(transform_3005_4326, snapped_point)

    # join the result to the upstream mask.
    # this will fill out the upstream area to the bounds of the upstream FWA polygons
    if upstream_mask:
        result = result.union(upstream_mask)

    # clip the polygon to the working area.  This will prevent the areas delineated by the DEM
    # from "spilling over" the bounds of the FWA polygons.  This most commonly occurs if the
    # DEM "jumps" between very close streams and gets 2 catchments.  The FWA can handle this
    # since it will never include the catchment of the incorrect stream.
    if working_area:
        result = result.intersection(working_area)

    if hasattr(result, "exterior"):
        result = Polygon(result.exterior)

    return (result, snapped_point, dem_error)


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
    INNER JOIN upstream w ON ST_Intersects(b.geom, ST_Transform(w.geom, 3005))
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
        using_srid: int = 3005) -> Tuple[Point, MultiPolygon]:
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
            logger.debug(value)

    # WhiteboxTools reads and writes files from/to disk.
    # Set up some filename references in a TemporaryDirectory.
    watershed_files = TemporaryDirectory()
    file_001_cutline = f"{watershed_files.name}/001_cutline.shp"
    file_010_dem = f"{watershed_files.name}/010_dem.tif"
    file_020_dem_filled = f"{watershed_files.name}/020_filled_dem.tif"
    file_030_fdr = f"{watershed_files.name}/030_fdr.tif"
    file_040_fac = f"{watershed_files.name}/040_fac.tif"
    file_050_point_shp = f"{watershed_files.name}/050_point.shp"
    file_060_snapped = f"{watershed_files.name}/060_snapped.shp"
    file_070_watershed = f"{watershed_files.name}/070_ws_raster.tif"
    file_080_watershed_vector = f"{watershed_files.name}/080_ws_vector.shp"

    # use gdal.Warp to request a clipped portion of the DEM.
    # the DEM file must be a Cloud Optimized GeoTIFF.
    # when using the /vsis3/ S3 virtual filesystem notation together with cutline,
    # gdal.Warp will download only the area of interest. For more info, see
    # https://gdal.org/drivers/raster/cog.html
    # https://trac.osgeo.org/gdal/wiki/CloudOptimizedGeoTIFF
    start = time.perf_counter()

    # Define a point feature geometry with one attribute
    poly_schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    # Write a new Shapefile for the starting stream point. This will be used as the input vector point
    # to be snapped to the nearest stream pixel of the Flow Accumulation raster.
    with fiona.open(file_001_cutline, 'w', 'ESRI Shapefile', poly_schema, crs=f"EPSG:{using_srid}") as c:
        c.write({
            'geometry': mapping(watershed_area),
            'properties': {'id': 123},
        })

    gdal.Warp(
        file_010_dem,
        f'/vsis3/{dem_file}',
        cutlineDSName=file_001_cutline,
        cropToCutline=True
    )

    elapsed = (time.perf_counter() - start)
    logger.debug('CLIPPING TOOK %s', elapsed)

    # use either BreachDepressionsLeastCost or BreachDepressions, not both.
    # Author recommends BreachDepressionsLeastCost but worth testing both.
    # Initial testing: BreachDepressions is working consistently
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#breachdepressionsleastcost
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#breachdepressions
    wbt.breach_depressions(
        file_010_dem,
        file_020_dem_filled,
        callback=wbt_suppress_progress_output
    )

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#d8pointer
    wbt.d8_pointer(
        file_020_dem_filled,
        file_030_fdr,
        callback=wbt_suppress_progress_output
    )

    accum_input_file = file_030_fdr
    if not pntr:
        accum_input_file = file_020_dem_filled

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#D8FlowAccumulation
    wbt.d8_flow_accumulation(
        accum_input_file,
        file_040_fac,
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
    with fiona.open(file_050_point_shp, 'w', 'ESRI Shapefile', shp_schema) as c:
        c.write({
            'geometry': mapping(point),
            'properties': {'id': 123},
        })

        if WATERSHED_DEBUG:
            logger.debug('Wrote shapefile')
        point_shp_file = c.name

    #
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#JensonSnapPourPoints
    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#SnapPourPoints
    snap_result = wbt.snap_pour_points(
        file_050_point_shp,
        file_040_fac,
        file_060_snapped,
        snap_distance, callback=wbt_suppress_progress_output)

    with fiona.open(file_060_snapped, 'r', 'ESRI Shapefile') as snp:
        snapped_pt = shape(next(iter(snp)).get('geometry'))

    if WATERSHED_DEBUG:
        logger.debug('Wrote snapped point')
        logger.debug('-- snap distance from stream point: %s',
                     snapped_pt.distance(point))

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#watershed
    watershed_result = wbt.watershed(
        file_030_fdr,
        file_060_snapped,
        file_070_watershed, esri_pntr=False, callback=wbt_suppress_progress_output)

    start = time.perf_counter()
    gdal_raster_to_polygon(file_070_watershed, file_080_watershed_vector)
    elapsed = (time.perf_counter() - start)

    logger.debug('VECTORIZING TOOK %s', elapsed)

    with fiona.open(file_080_watershed_vector, 'r', 'ESRI Shapefile') as ws_result:

        watershed_result = None
        ws_result_list = None
        if using_srid == '3005':
            ws_result_list = [transform(transform_3005_4326, shape(
                poly['geometry'])) for poly in ws_result]
        else:
            ws_result_list = [shape(poly['geometry']) for poly in ws_result]
        watershed_result = MultiPolygon(ws_result_list)

    return (watershed_result, snapped_pt)


def gdal_raster_to_polygon(in_file, out_file):
    """
    use GDAL Polygonize to convert a raster watershed to a vector watershed.
    Will write to `out_file`.  Use `fiona.open(outfile, 'r', 'ESRI Shapefile')`
    to read from outfile into Python.
    """
    # set up GDAL settings for reading the Watershed output raster
    # and converting it to a polygon.
    try:
        # Read in the raster with the watershed.
        # the watershed is always in band 1.
        sourceRaster = gdal.Open(in_file)
        band = sourceRaster.GetRasterBand(1)

        # create a shapefile with a layer for our watershed.
        driver = ogr.GetDriverByName("ESRI Shapefile")
        outDatasource = driver.CreateDataSource(out_file)
        outLayer = outDatasource.CreateLayer("watershed", srs=None)

        # write polygon to the output layer in `out_file`
        gdal.Polygonize(band, band, outLayer, -1, [], callback=None)

        # clean up
        outDatasource.Destroy()
        sourceRaster = None
    except:
        raise Exception("unable to convert from raster watershed to vector watershed")
