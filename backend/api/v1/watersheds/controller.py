"""
Functions for aggregating data from web requests and database records
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
from osgeo import gdal, ogr
from shapely.geometry import Point, Polygon, MultiPolygon, shape, box, mapping
from shapely.ops import transform, unary_union
from starlette.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from pyeto import thornthwaite, monthly_mean_daylight_hours, deg2rad

from api.config import WATERSHED_DEBUG
from api.utils import normalize_quantity
from api.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatershedsFWAPG as FreshwaterAtlasWatersheds
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworksFWAPG as FreshwaterAtlasStreamNetworks
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


def calculate_glacial_area(db: Session, polygon: MultiPolygon) -> Tuple[float, float]:
    """
    Calculates percent glacial coverage using the area of `polygon` which intersects with features from
    the DataBC FWA Glaciers dataset.
    returns a tuple of floats with the form (glacial_area, coverage).
    """

    glaciers_layer = 'freshwater_atlas_glaciers'

    glacial_features = feature_search(db, [glaciers_layer], polygon.minimum_rotated_rectangle)[
        0].geojson.features

    glacial_area = 0

    polygon = transform(transform_4326_3005, polygon)

    for glacier in glacial_features:
        glacier_clipped = shape(glacier.geometry).intersection(polygon)

        if not glacier_clipped.area:
            continue

        glacial_area += glacier_clipped.area

    coverage = glacial_area / polygon.area

    return (glacial_area, coverage)


def pcic_data_request(
        polygon: Polygon,
        output_variable: str = 'pr',
        dataset=None):
    """ Returns an average precipitation from the pacificclimate.org climate explorer service """

    pcic_url = "https://services.pacificclimate.org/pcex/api/timeseries?"

    if not dataset:
        dataset = f"{output_variable}_mClim_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19810101-20101231_Canada"

    params = {
        "id_": dataset,
        "variable": output_variable,
        "area": polygon.minimum_rotated_rectangle.wkt
    }

    req_url = pcic_url + urlencode(params)

    if WATERSHED_DEBUG:
        logger.info('pcic request: %s', req_url)

    try:
        resp = requests.get(req_url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return resp.json()


def water_licences_summary(licences: List[Feature], polygon: Polygon) -> LicenceDetails:
    """ takes a list of licences and the search polygon, and returns a
        summary of the licences that fall within the search area.

    """

    total_licenced_qty_m3_yr = 0
    licenced_qty_by_use_type = {}
    active_licences_within_search_area = []
    inactive_licences_within_search_area = []

    # max_quantity_by_licence tracks quantities for licences
    # that have multiple points of diversion (PODs). The quantity
    # is treated differently based on the QUANTITY_FLAG attribute:
    #
    # M       - QUANTITY is the max quantity for the licence, shared across multiple
    #             points of diversion. QUANTITY should be the same for all
    #             records under a licence with this flag and will not be summed.
    # T, D, P - QUANTITY is the quantity per POD record and will be summed
    #             to determine the total quantity for the licence.
    #
    # note: the above is the explanation of how this is handled here in this function,
    # refer to https://catalogue.data.gov.bc.ca/dataset/5549cae0-c2b1-4b96-9777-529d9720803c
    # for the official quantity flag definitions.
    max_quantity_by_licence = {}

    for lic in licences:
        feature_shape = shape(lic.geometry)

        # skip licences outside search area
        if not feature_shape.within(polygon):
            continue

        # skip licence if not a surface water point of diversion (POD)
        # other pod_subtype codes are associated with groundwater.
        if lic.properties['POD_SUBTYPE'] != 'POD':
            continue

        licence_number = lic.properties['LICENCE_NUMBER']
        qty = lic.properties['QUANTITY']
        qty_unit = lic.properties['QUANTITY_UNITS'].strip()
        purpose = lic.properties['PURPOSE_USE']

        # normalize the quantity units to m3/year. This function returns None
        # if the quantity cannot be normalized; for example, there is an invalid
        # unit (or the unit is "total flow"). In this case, the original quantity
        # will still be available for users to view, but the normalized m3/year
        # table column will be empty. The licence will also not be considered
        # in the sum total if the quantity cannot be converted due to invalid input.
        normalized_qty = normalize_quantity(qty, qty_unit)

        lic.properties['qty_m3_yr'] = normalized_qty

        # List of statuses to watch for when deciding whether or not
        # to consider the licenced quantity for the total licenced usage.
        # It may be possible to only consider POD_STATUS but we should assume
        # there may be data discrepancies, so skip if either POD_STATUS or LICENCE_STATUS
        # is an inactive code.
        LICENCE_STATUSES_TO_SKIP = [
            'Abandoned', 'Canceled', 'Cancelled', 'Expired', 'Inactive'
        ]
        POD_STATUSES_TO_SKIP = [
            'Inactive'
        ]

        # by default, add licence quantities together
        licence_qty_action_function = add

        # licences with a QUANTITY_FLAG of "M" need to be handled separately (see above note
        # for `max_quantity_by_licence`). The `max` function is used.
        # Some QUANTITY_FLAG values are null, so check for that before we process the value as a string.
        if lic.properties.get("QUANTITY_FLAG", None) and lic.properties.get("QUANTITY_FLAG", "").strip() == "M":
            licence_qty_action_function = max

        if lic.properties["LICENCE_STATUS"] not in LICENCE_STATUSES_TO_SKIP and \
                lic.properties["POD_STATUS"] not in POD_STATUSES_TO_SKIP:
            # if the licence has a quantity that we can convert to m3/year,
            # use the action function (either `add` or `max`, as above).
            # some licences have a quantity of 0 and a unit of "total flow",
            # these will be skipped here.
            if normalized_qty is not None:
                max_quantity_by_licence[licence_number] = licence_qty_action_function(
                    max_quantity_by_licence.get(licence_number, 0),
                    normalized_qty
                )
            active_licences_within_search_area.append(lic)
        else:
            inactive_licences_within_search_area.append(lic)

        # organize the licence by purpose use.The WALLY web app will primary display
        # licences broken down by purpose use.
        if purpose is not None:
            # move id to back of purpose name
            try:
                code, name = purpose.split(' - ')
                purpose = f"{name} ({code})"
            except ValueError:
                logger.error(f"Error formatting {purpose}")

            # format licences for each purpose type
            purpose_data = licenced_qty_by_use_type.setdefault(purpose, {
                "qty": 0,
                "licences": [],
                "inactive_licences": []
            })

            licence = Feature(
                geometry=transform(transform_3005_4326,
                                   shape(lic.geometry)),
                id=lic.id,
                properties={
                    "fileNumber": lic.properties["FILE_NUMBER"],
                    "status": lic.properties["LICENCE_STATUS"],
                    "licensee": lic.properties["PRIMARY_LICENSEE_NAME"],
                    "source": lic.properties["SOURCE_NAME"],
                    "quantityPerSec": normalized_qty / SEC_IN_YEAR if normalized_qty else None,
                    "quantityPerYear": normalized_qty,
                    "quantityFlag": lic.properties["QUANTITY_FLAG"],
                    "quantity": lic.properties["QUANTITY"],
                    "quantityUnits": lic.properties["QUANTITY_UNITS"]
                }
            )

            # add licenced quantity if the licence is not canceled.
            if lic.properties["LICENCE_STATUS"] not in LICENCE_STATUSES_TO_SKIP and \
                    lic.properties["POD_STATUS"] not in POD_STATUSES_TO_SKIP:
                if normalized_qty is not None:
                    purpose_data["qty"] = licence_qty_action_function(
                        purpose_data["qty"], normalized_qty)

                licenced_qty_by_use_type[purpose]["licences"].append(licence)

            else:
                licenced_qty_by_use_type[purpose]["inactive_licences"].append(
                    licence)

    # create the list of purpose types.
    licence_purpose_type_list = []
    for purpose, purpose_obj in licenced_qty_by_use_type.items():
        licence_purpose_type_list.append({
            "purpose": purpose,
            "qty": purpose_obj["qty"],
            "licences": purpose_obj["licences"],
            "inactive_licences": purpose_obj["inactive_licences"],
            "units": "m3/year"
        })

    # Create the LicenceDetails summary and populate it with the licences (separated by
    # active/inactive), and statistics for the WALLY web client to display.
    return LicenceDetails(
        licences=FeatureCollection([
            Feature(
                geometry=transform(transform_3005_4326, shape(feat.geometry)),
                id=feat.id,
                properties=feat.properties
            ) for feat in active_licences_within_search_area
        ]),
        inactive_licences=FeatureCollection([
            Feature(
                geometry=transform(transform_3005_4326, shape(feat.geometry)),
                id=feat.id,
                properties=feat.properties
            ) for feat in inactive_licences_within_search_area
        ]),
        total_qty=sum(max_quantity_by_licence.values()),
        total_qty_by_purpose=licence_purpose_type_list,
        projected_geometry_area=polygon.area,
    )


def surface_water_rights_licences(polygon: Polygon):
    """ returns surface water rights licences (filtered by POD subtype)"""
    water_rights_layer = 'water_rights_licences'

    # search with a simplified rectangle representing the polygon.
    # we will do an intersection on the more precise polygon after
    polygon_rect = polygon.minimum_rotated_rectangle
    licences = databc_feature_search(
        water_rights_layer, search_area=polygon_rect)

    polygon_3005 = transform(transform_4326_3005, polygon)

    licence_summary = water_licences_summary(licences.features, polygon_3005)
    licence_summary.projected_geometry_area_simplified = polygon_rect.area
    return licence_summary


def surface_water_approval_points(polygon: Polygon):
    """ returns surface water approval points (filtered by APPROVAL_STATUS)"""
    water_approvals_layer = 'water_approval_points'

    # search with a simplified rectangle representing the polygon.
    # we will do an intersection on the more precise polygon after
    polygon_rect = polygon.minimum_rotated_rectangle
    approvals = databc_feature_search(
        water_approvals_layer, search_area=polygon_rect)

    polygon_3005 = transform(transform_4326_3005, polygon)

    features_within_search_area = []
    total_qty_m3_yr = 0

    for apr in approvals.features:
        feature_shape = shape(apr.geometry)

        # skip approvals outside search area
        if not feature_shape.within(polygon_3005):
            continue

        # skip approval if its not an active licence
        # other approval status' are associated with inactive licences
        if apr.properties['APPROVAL_STATUS'] != 'Current':
            continue

        features_within_search_area.append(apr)

        # the rare water approval record has the units
        # as a suffix in the QUATITY property
        # these are considered bad data points
        # and will be skipped
        try:
            qty = float(apr.properties['QUANTITY'])
        except:
            continue

        qty_unit = apr.properties['QUANTITY_UNITS']

        # null if approval is a works project, most of them are
        if qty and qty_unit:
            qty = normalize_quantity(qty, qty_unit)
            total_qty_m3_yr += qty
            apr.properties['qty_m3_yr'] = qty
        else:
            apr.properties['qty_m3_yr'] = 0

    return WaterApprovalDetails(
        approvals=FeatureCollection([
            Feature(
                geometry=transform(transform_3005_4326, shape(feat.geometry)),
                id=feat.id,
                properties=feat.properties
            ) for feat in features_within_search_area
        ]),
        total_qty=total_qty_m3_yr,
        projected_geometry_area=polygon.area,
        projected_geometry_area_simplified=polygon_rect.area
    )


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
            SELECT  watershed_feature_id as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    whse_basemapping.fwa_watersheds_poly
            WHERE   "watershed_feature_id" = :watershed_feature_id
        )
        SELECT
            ST_AsBinary(ST_Transform(ST_Union(geom), 4326)) as geom
        FROM    whse_basemapping.fwa_watersheds_poly
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


def wbt_calculate_watershed(
        watershed_area: MultiPolygon,
        point: Point,
        log: bool = False,
        pntr: bool = True,
        accum_out_type: str = 'sca',
        snap_distance: float = 1000,
        using_srid: int = 3005) -> (Point, MultiPolygon):
    """
    Given a watershed region (an overestimate to crop the original DEM raster to) and a starting point,
    use WhiteboxTools to generate an upstream watershed from the point.  Returns a tuple containing a
    snapped starting point and a watershed polygon.

    Use `get_upstream_catchment_area()` or a query like `WHERE FWA_WATERSHED_CODE LIKE 100-123456-%`
    (for example) to generate an overestimate. The input stream-burned DEM file will be cropped to
    these extents to make it easier and faster to run the watershed analysis.

    Optional arguments:
    `log`:  run WhiteboxTools D8FlowAccumulation with the --log flag.  Tranforms raster values
    using log to prevent saturating areas with max values.
    See https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#d8flowaccumulation

    `snap_distance`: the max distance that JensonSnapPourPoints should search for a suitable stream.
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
    file_030_fdr = NamedTemporaryFile(suffix='.tif', prefix='030_fdr_')
    file_040_fac = NamedTemporaryFile(suffix='.tif', prefix='040_fac_')
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
        file_010_dem.name,
        "/app/api/v1/watersheds/test/Burned_CDEM_BC_49_51.tif",
        cutlineDSName=f"{file_000_extent.name}/{extent_shp_file}.shp",
        cropToCutline=True,
    )

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#breachdepressionsleastcost
    wbt.breach_depressions(
        file_010_dem.name,
        file_020_dem_filled.name,
        callback=wbt_suppress_progress_output
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
        file_030_fdr.name,
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

    # https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html#JensonSnapPourPoints
    snap_result = wbt.jenson_snap_pour_points(
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
    return watershed_result


def watershed_touches_border(db: Session, watershed_feature_id: int) -> List[str]:
    """
    Returns an array of strings indicating which borders the watershed upstream from
    watershed_feature_id touches. The array will be zero length if no borders were reached.
    """

    q = """
    with subwscode_ltree as (
            SELECT  watershed_feature_id as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    whse_basemapping.fwa_watersheds_poly
            WHERE   "watershed_feature_id" = :watershed_feature_id
        ),
        upstream as (
            SELECT  geom
            FROM    whse_basemapping.fwa_watersheds_poly
            WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from subwscode_ltree) OR (select origin_wscode from subwscode_ltree) = (select origin_localcode from subwscode_ltree))
        )

    SELECT border
    FROM whse_basemapping.fwa_approx_borders b
    INNER JOIN upstream w ON ST_Intersects(b.geom, w.geom)
    """
    borders = []
    res = db.execute(q, {"watershed_feature_id": watershed_feature_id})
    return [row['border'] for row in res]


def wbt_options(log: bool = True, pntr: bool = True, accum_out_type: str = 'sca', snap_distance: float = '1000', using_srid: int = 3005):
    """ returns an object with WBT Watershed settings"""
    return {
        "log": log,
        "pntr": pntr,
        "accum_out_type": accum_out_type,
        "snap_distance": snap_distance,
        "using_srid": using_srid
    }


def get_watershed_using_dem(db: Session, click_point: Point, watershed_id, clip_dem=True, dem_source='cdem'):
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
    JensonSnapPoints and Watershed. The Whitebox Tools raster to vector function is
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

    # move the click point to the nearest stream based on the FWA Stream Networks.
    # this will make it easier to snap the point to the Flow Accumulation raster
    # we will generate.
    nearest_stream = get_nearest_streams(db, click_point, limit=1)[0]
    nearest_stream_point = nearest_stream.get('closest_stream_point')
    point = shape(nearest_stream_point)

    if WATERSHED_DEBUG:
        logger.info('--------- nearest stream -------------')
        logger.info(point)
        logger.info('distance: %s', transform(
            transform_4326_3005, point
        ).distance(
            transform(transform_4326_3005, click_point)))
        logger.info('--------------------------------------')

    # get an overestimate of the catchment area so that we can crop
    # the DEM to a more manageable size.
    fwa_upstream_area = get_upstream_catchment_area(db, watershed_id)

    # setup config to be used with WBT and the spatial features.
    # CDEM uses SRID 4326, so jenson_radius must be in degrees
    # our SRTM source uses 3005, so set jenson_radius to meters.
    using_srid = 4326
    jenson_radius = 0.001  # degrees
    if dem_source == 'srtm':
        rast_q = srtm_q
        point = transform(transform_4326_3005, point)
        jenson_radius = 500  # metres
        using_srid = 3005

    # TODO: ensure that we use SRTM or at least bring in
    # the US watershed data if we are hitting a border.
    if WATERSHED_DEBUG:
        logger.info('---------------------------------')
        logger.info('WS CROSSES BORDER?  %s',
                    watershed_touches_border(db, watershed_id))
        logger.info('---------------------------------')

    # further settings for WhiteboxTools.
    # we hopefully get a valid watershed using the first set
    # of settings, but sometimes we get a one-cell (small "stub")
    # watershed.  If that happens, we can run through a few different
    # settings quickly to see if we can get a full watershed.
    # NOTE: not sure if this is a good idea.  we want to make sure
    # the watersheds are relatively repeatable.
    config_matrix = [
        wbt_options(log=True, pntr=True, accum_out_type='sca',
                    snap_distance=jenson_radius),
        # wbt_options(log=True, pntr=True, accum_out_type='ca',
        #             snap_distance=jenson_radius),
        # wbt_options(log=True, pntr=True, accum_out_type='cells',
        #             snap_distance=jenson_radius),
        # wbt_options(log=True, pntr=False, accum_out_type='sca',
        #             snap_distance=jenson_radius),
        # wbt_options(log=False, pntr=True, accum_out_type='sca',
        #             snap_distance=jenson_radius),
    ]

    for config in config_matrix:
        logger.info('Using WhiteboxTools with settings %s', config)
        result = wbt_calculate_watershed(fwa_upstream_area, point, **config)

        if transform(transform_4326_3005, result).area > 5000:
            if WATERSHED_DEBUG:
                logger.info("Generated watershed from DEM")
            return result

    # did not get a result from any config setting.
    return None


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
    nearest_stream_point = nearest_stream.get('id')

    q = """
        with subwscode_ltree as (
            SELECT  watershed_feature_id as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    whse_basemapping.fwa_watersheds_poly
            WHERE   "watershed_feature_id" = :watershed_feature_id
        ),
        stream_subwscode_ltree as (
            SELECT  
                    geom,
                    linear_feature_id as origin_id,
                    wscode_ltree as origin_wscode,
                    localcode_ltree as origin_localcode,
                    ltree2text(subpath(localcode_ltree, -1))::integer as downstream_tributary,
                    nlevel(localcode_ltree) as downstream_tributary_code_pos
            FROM    whse_basemapping.fwa_stream_networks_sp
            WHERE   "linear_feature_id" = :stream_feature_id
        ),
        polygons_touching_click_point as (
            SELECT w.geom, w.watershed_feature_id, ST_Area(w.geom) as area
            FROM   whse_basemapping.fwa_watersheds_poly w, stream_subwscode_ltree s
            WHERE  ST_Intersects(w.geom, s.geom)
        ),
        watershed_fwa_polygons as (
            SELECT  watershed_feature_id,
                    geom,
                    ST_Area(geom) as area
            FROM    whse_basemapping.fwa_watersheds_poly
            WHERE   wscode_ltree <@ (select origin_wscode from subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from subwscode_ltree) OR (select origin_wscode from subwscode_ltree) = (select origin_localcode from subwscode_ltree))
        ),
        polygons_upstream_by_stream_point as (
            SELECT  watershed_feature_id,
                    geom,
                    ST_Area(geom) as area
            FROM    whse_basemapping.fwa_watersheds_poly
            WHERE   wscode_ltree <@ (select origin_wscode from stream_subwscode_ltree)
            AND     ltree2text(subltree(
                        localcode_ltree || '000000'::ltree,
                        (select downstream_tributary_code_pos from stream_subwscode_ltree) - 1,
                        (select downstream_tributary_code_pos from stream_subwscode_ltree) - 0
                    ))::integer >= (select downstream_tributary from stream_subwscode_ltree)
            AND (NOT wscode_ltree <@ (select origin_localcode from stream_subwscode_ltree) OR (select origin_wscode from stream_subwscode_ltree) = (select origin_localcode from stream_subwscode_ltree))
        ),
        dem_watershed AS (
            SELECT ST_Intersection(ST_Simplify(ST_Transform(ST_ChaikinSmoothing(ST_SetSRID(ST_GeomFromText(:dem_watershed), 4326)), 3005), 50), (
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
            WHERE   NOT ST_Intersects(geom, ST_Buffer(
                (select geom from whse_basemapping.fwa_watersheds_poly where watershed_feature_id = :watershed_feature_id),
                :buffer_distance
            ))
        )
        SELECT
        CASE
            WHEN ST_area((select geom from dem_watershed)) / ST_Area((select ST_Collect(geom) from watershed_fwa_polygons)) > :min_area_ratio
            AND ST_area((select geom from dem_watershed)) > :min_valid_area
        THEN (
            Select ST_AsBinary(ST_Transform(ST_Union(geom), 4326))
            FROM (
                SELECT geom FROM dem_watershed
                UNION   SELECT  geom from watershed_mask
                UNION   SELECT  ST_Intersection(p.geom, d.geom) as geom
                        FROM    dem_watershed d, polygons_touching_click_point p
            ) combined
        )
        --/**  If the condition for the first case failed, we don't think the DEM watershed is valid.
        --*    Fall back on using the FWA Upstream polygons estimate.
        --**/
        ELSE (  
            SELECT ST_AsBinary(ST_Transform(ST_Union(geom), 4326))
            FROM watershed_fwa_polygons
        )
        END
        AS watershed

    """

    """
    (
                SELECT geom FROM dem_watershed
                UNION   SELECT  geom from watershed_mask
                UNION   SELECT  ST_Intersection(p.geom, d.geom) as geom
                        FROM    dem_watershed d, polygons_touching_click_point p
            ) combined
    """

    res = db.execute(q, {
        "watershed_feature_id": watershed_id,
        "stream_feature_id": nearest_stream_point,
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


def calculate_catchment_of_full_stream(db, watershed_id):
    """
    returns the catchment of the entire selected stream.
    """

    q = """
                with subwscode_ltree as (
                    SELECT  wscode_ltree as origin_wscode
                    FROM    whse_basemapping.fwa_watersheds_poly
                    WHERE   "watershed_feature_id" = :watershed_id
                )

                SELECT
                    ST_AsBinary(ST_Union(geom)) as geom
                FROM    whse_basemapping.fwa_watersheds_poly
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


def calculate_watershed(
    db: Session,
    point: Point = None,
    watershed_id: int = None,
    include_self: bool = False,
    upstream_method='DEM',
    dem_source='srtm'
):
    """ estimates the watershed area upstream of a POI

        Optional arguments:
        upstream_method: 'FWA', 'DEM', or 'DEM+FWA'.
            FWA+FULLSTREAM: Use the Freshwater Atlas to return the catchment area of the entire
                        selected stream.
            FWA+UPSTREAM: Estimate the upstream catchment area using only the Freshwater Atlas.
                 This will be accurate to the FWA linework around the outer perimeter
                 but will over or under-estimate the area around the point of interest (because
                 the watershed polygons forming the catchment area will not be split, even if
                 the point of interest is in the middle of a polygon)

            DEM: Use the DEM (Digital Elevation Model) to delineate the catchment.
                 WhiteboxTools is used. See `get_watershed_using_dem` for more info.
                 This is more accurate around the point of interest but the outer reaches
                 are less smooth than the FWA linework and may slightly under or overestimate
                 around the outer perimeter of the watershed.

            DEM+FWA: Attempt to combine both the DEM and FWA methods by using the DEM close
                     to the point of interest, and the FWA around the outer perimeter. This
                     is the default.
    """

    if point and watershed_id:
        raise ValueError(
            "Do not provide both point and watershed_id at the same time")

    if not point and not watershed_id:
        raise ValueError(
            "Must provide either a starting point (lat, long) or a starting watershed ID")

    if watershed_id and not upstream_method.startswith("FWA"):
        raise ValueError(
            f"Starting watershed ID incompatible with {upstream_method}. Use only FWA methods.")

    if WATERSHED_DEBUG:
        logger.info("calculating watershed")

    if point:
        # first get the ID of the watershed we are starting in.
        # this will be used later to help with queries against the fundamental watersheds.
        q = db.query(FreshwaterAtlasWatersheds.WATERSHED_FEATURE_ID).filter(
            func.ST_Contains(
                FreshwaterAtlasWatersheds.GEOMETRY,
                func.ST_Transform(func.ST_GeomFromText(point.wkt, 4326), 3005)
            )
        )

        if WATERSHED_DEBUG:
            logger.info("watershed query %s", q)

        watershed_id = q.first()
        if not watershed_id:
            if WATERSHED_DEBUG:
                logger.warning("No watershed found")
            return None
        watershed_id = watershed_id[0]

    if WATERSHED_DEBUG:
        logger.info("watershed id %s", watershed_id)

    watershed_point = None
    watershed = None
    # stream_name = get_watershed_stream_name(db, watershed_id)
    stream_name = ""
    # choose method based on function argument.

    if upstream_method.startswith('DEM'):
        # estimate the watershed using the DEM
        watershed = get_watershed_using_dem(
            db, point, watershed_id, clip_dem=not upstream_method == 'DEM+FWA')
        watershed_source = "Estimated using CDEM and WhiteboxTools."
        generated_method = 'generated_dem'
        watershed_point = base64.urlsafe_b64encode(point.wkb).decode('utf-8')

        # optionally augment the watershed using the FWA.
        if upstream_method == 'DEM+FWA':
            watershed = augment_dem_watershed_with_fwa(
                db, watershed, watershed_id, point)
            watershed_source = "Estimated by combining the result from CDEM/WhiteboxTools " + \
                               "with Freshwater Atlas fundamental watershed polygons."
            generated_method = 'generated_dem_fwa'

    elif upstream_method == 'FWA+UPSTREAM':
        watershed = get_upstream_catchment_area(db, watershed_id)
        watershed_source = "Estimated by combining Freshwater Atlas watershed polygons that are " + \
            "determined to be part of the selected stream based on FWA_WATERSHED_CODE and upstream " + \
            "of the selected point based on LOCAL_WATERSHED_CODE. Note: the watershed polygon " + \
            "containing the selected point is included."
        generated_method = 'generated'
        watershed_point = watershed_id

    elif upstream_method == 'FWA+FULLSTREAM':
        watershed = calculate_catchment_of_full_stream(db, watershed_id)
        watershed_source = "Estimated by combining Freshwater Atlas watershed polygons that are " + \
            "determined to be part of the selected stream based on FWA_WATERSHED_CODE."
        generated_method = 'generated_full_stream'
        watershed_point = watershed_id

    else:
        raise ValueError(
            f"Invalid method {upstream_method}. Valid methods are DEM, DEM+FWA, FWA+UPSTREAM, FWA+FULLSTREAM")

    # combined_result = wbt_clipped_polygon.union(feat)
    feature = Feature(
        geometry=watershed,
        id=f"{generated_method}.{watershed_point}",
        properties={
            "name": f"Estimated catchment area {f'({stream_name})' if stream_name else ''}",
            "watershed_source": watershed_source,
            "stream_name": stream_name
        }
    )
    if not feature:
        # was not able to calculate a watershed with the provided params.
        # return None; the calling function will skip this calculated watershed
        # and return other pre-generated ones.
        logger.info(
            "skipping calculated watershed based on watershed feature id %s", watershed_id)
        return None

    feature.properties['FEATURE_AREA_SQM'] = transform(
        transform_4326_3005, shape(feature.geometry)).area

    return feature


def get_databc_watershed(watershed_id: str):
    """ finds a watershed in DataBC watershed layers

    """
    watershed_layer = '.'.join(watershed_id.split('.')[:2])
    watershed_feature = watershed_id.split('.')[-1:]

    id_props = {
        'WHSE_BASEMAPPING.FWA_ASSESSMENT_WATERSHEDS_POLY': 'WATERSHED_FEATURE_ID',
        'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY': 'WATERSHED_FEATURE_ID',
        'WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY': 'HYD_WATERSHED_BND_POLY_ID'
    }

    source_urls = {
        'WHSE_BASEMAPPING.FWA_ASSESSMENT_WATERSHEDS_POLY': 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-assessment-watersheds',
        'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY': 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-watersheds',
        'WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY': 'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries'
    }

    cql_filter = f"{id_props[watershed_layer]}={watershed_feature}"

    watershed = databc_feature_search(watershed_layer, cql_filter=cql_filter)
    if len(watershed.features) != 1:
        raise HTTPException(
            status_code=404, detail=f"Watershed with id {watershed_id} not found")

    ws = watershed.features[0]

    ws.properties['name'] = ws.properties.get(
        'GNIS_NAME_1', None) or ws.properties.get('SOURCE_NAME', None)
    ws.properties['watershed_source'] = source_urls.get(watershed_layer, None)

    return ws


def surficial_geology(polygon: Polygon):
    """ surficial geology information from DataBC
    https://catalogue.data.gov.bc.ca/dataset/terrain-inventory-mapping-tim-detailed-polygons-with-short-attribute-table-spatial-view

    """

    surf_geol_layer = "WHSE_TERRESTRIAL_ECOLOGY.STE_TER_INVENTORY_POLYS_SVW"

    polygon_rect = polygon.minimum_rotated_rectangle

    fc = databc_feature_search(surf_geol_layer, polygon_rect)

    polygon_3005 = transform(transform_4326_3005, polygon)

    surficial_geology_dominant_types = {}
    surficial_geology_features_by_type = {}

    coverage_area = 0

    for feature in fc.features:

        feature_shape = shape(feature.geometry)
        feature_shape_intersect = feature_shape.intersection(polygon_3005)

        # DOMINANT_SURFICIAL_MATERIAL is the property we are looking for.
        # it is a description of the surficial geology deposition method.
        dominant_type = feature.properties.get(
            'DOMINANT_SURFICIAL_MATERIAL', None)

        if not dominant_type or not feature_shape_intersect.area:
            continue

        # initialize area for new soil types
        if not surficial_geology_dominant_types.get(dominant_type, None):
            surficial_geology_dominant_types[dominant_type] = 0

        # initialize list of features for new soil types
        if not surficial_geology_features_by_type.get(dominant_type, None):
            surficial_geology_features_by_type[dominant_type] = []

        # add to total area for this soil type
        surficial_geology_dominant_types[dominant_type] += feature_shape_intersect.area

        # create a SRID 4326 feature
        # this feature will be returned in the JSON response and can
        # be displayed on the map.
        geom_4326 = transform(transform_3005_4326, feature_shape_intersect)
        feat_4326 = Feature(
            geometry=geom_4326,
            id=feature.id,
            properties=feature.properties
        )

        # adding the centroid makes it easier to add labels later
        feat_4326.properties['centre'] = geom_4326.centroid.coords

        surficial_geology_features_by_type[dominant_type].append(feat_4326)

        coverage_area += feature_shape_intersect.area

    surf_geol_list = []
    geol_type_features = []

    for soil_type, area in surficial_geology_dominant_types.items():

        soil_type_fc = FeatureCollection(
            surficial_geology_features_by_type.get(soil_type, []))

        surf_geol_list.append({
            "soil_type": soil_type,
            "area_within_watershed": area,
            "geojson": soil_type_fc

        })

    return SurficialGeologyDetails(
        summary_by_type=surf_geol_list,
        coverage_area=coverage_area,
    )


def get_watershed(db: Session, watershed_feature: str):
    """ finds a watershed by either generating it or looking it up in DataBC watershed datasets """
    watershed_layer = '.'.join(watershed_feature.split('.')[:-1])
    watershed_feature_id = watershed_feature.split('.')[-1:]
    watershed = None

    if WATERSHED_DEBUG:
        logger.info(watershed_feature_id)

    # if we generated this watershed, use the catchment area
    # generation function to get the shape.
    if watershed_layer == 'generated':
        watershed_id = int(watershed_feature_id[0])
        watershed = calculate_watershed(
            db, watershed_id=watershed_id, upstream_method='FWA+UPSTREAM')

    elif watershed_layer == 'generated_dem_fwa':
        logger.info(watershed_feature_id[0])
        point = wkb.loads(base64.urlsafe_b64decode(watershed_feature_id[0]))
        watershed = calculate_watershed(
            db, point=point, upstream_method='DEM+FWA')

    elif watershed_layer == 'generated_dem':
        point = wkb.loads(base64.urlsafe_b64decode(watershed_feature_id[0]))
        watershed = calculate_watershed(db, point=point, upstream_method='DEM')

    elif watershed_layer == 'generated_full_stream':
        watershed_id = watershed_feature_id[0]
        watershed = calculate_watershed(
            db, watershed_id=watershed_id, upstream_method='FWA+FULLSTREAM')

    # otherwise, fetch the watershed from DataBC. The layer is encoded in the
    # feature id.
    else:
        watershed = get_databc_watershed(watershed_feature)
        watershed_poly = transform(
            transform_3005_4326, shape(watershed.geometry))
        watershed.geometry = mapping(watershed_poly)

    return watershed


def parse_pcic_temp(min_temp, max_temp):
    """ parses monthly temperatures from pcic to return an array of min,max,avg """

    temp_by_month = []

    for k, v in sorted(min_temp.items(), key=lambda x: x[0]):
        min_t = v
        max_t = max_temp[k]
        avg_t = (min_t + max_t) / 2
        temp_by_month.append((min_t, max_t, avg_t))

    return temp_by_month


def get_temperature(poly: Polygon):
    """
    gets temperature data from PCIC, and returns a list of 12 tuples (min, max, avg)
    """
    try:
        min_temp = pcic_data_request(poly, 'tasmin')
    except:
        raise Exception

    try:
        max_temp = pcic_data_request(poly, 'tasmax')
    except:
        raise Exception

    return parse_pcic_temp(min_temp.get('data'), max_temp.get('data'))


def get_annual_precipitation(poly: Polygon):
    """
    gets precipitation data from PCIC, and returns an annual precipitation
    value calculated by summing monthly means.
    """
    response = pcic_data_request(poly)

    months_data = list(response["data"].values())
    months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_totals = [a*b for a, b in zip(months_data, months_days)]

    annual_precipitation = sum(month_totals)
    # logger.warning("annual_precipitation")
    # logger.warning(annual_precipitation)

    return annual_precipitation


def calculate_daylight_hours_usgs(day: int, latitude_r: float):
    """ calculates daily radiation for a given day and latitude (latitude in radians)
        https://pubs.usgs.gov/sir/2012/5202/pdf/sir2012-5202.pdf
    """

    declination = 0.4093 * math.sin((2 * math.pi * day / 365) - 1.405)
    acos_input = -1 * math.tan(declination) * math.tan(latitude_r)
    sunset_angle = math.acos(acos_input)

    return (24 / math.pi) * sunset_angle


def calculate_potential_evapotranspiration_hamon(poly: Polygon, temp_data):
    """
    calculates potential evapotranspiration using the Hamon equation
    http://data.snap.uaf.edu/data/Base/AK_2km/PET/Hamon_PET_equations.pdf
    """

    average_annual_temp = sum([x[2] for x in temp_data])/12

    cent = poly.centroid
    xy = cent.coords.xy
    _, latitude = xy
    latitude_r = latitude[0] * (math.pi / 180)

    day = 1
    k = 1

    daily_sunlight_values = [calculate_daylight_hours_usgs(
        n, latitude_r) for n in range(1, 365 + 1)]

    avg_daily_sunlight_hours = sum(daily_sunlight_values) / \
        len(daily_sunlight_values)

    saturation_vapour_pressure = 6.108 * \
        (math.e ** (17.27 * average_annual_temp / (average_annual_temp + 237.3)))

    pet = k * 0.165 * 216.7 * avg_daily_sunlight_hours / 12 * \
        (saturation_vapour_pressure / (average_annual_temp + 273.3))

    return pet * 365


def calculate_potential_evapotranspiration_thornthwaite(poly: Polygon, temp_data):
    """ calculates potential evapotranspiration (mm/yr) using the
    Thornwaite method. temp_data is in the format returned by the function `get_temperature`"""

    monthly_t = [x[2] for x in temp_data]
    cent = poly.centroid
    xy = cent.coords.xy
    _, latitude = xy
    latitude_r = latitude[0] * (math.pi / 180)

    mmdlh = monthly_mean_daylight_hours(latitude_r)

    pet_mm_month = thornthwaite(monthly_t, mmdlh)

    return sum(pet_mm_month)


def get_slope_elevation_aspect(polygon: MultiPolygon):
    """
    This calls the sea api with a polygon and receives back
    slope, elevation and aspect information.

    In case of an error in the external slope/elevation/aspect service,
    a tuple of (None, None, None) will be returned. Any code making
    use of this function should interpret None as "not available".
    """
    sea_url = "https://apps.gov.bc.ca/gov/sea/slopeElevationAspect/json"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    }

    exterior = extract_poly_coords(polygon)["exterior_coords"]
    coordinates = [[list(elem) for elem in exterior]]

    payload = "format=json&aoi={\"type\":\"Feature\",\"properties\":{},\"geometry\":{\"type\":\"MultiPolygon\", \"coordinates\":" \
        + str(coordinates) + \
        "},\"crs\":{\"type\":\"name\",\"properties\":{\"name\":\"urn:ogc:def:crs:EPSG:4269\"}}}"

    try:
        if WATERSHED_DEBUG:
            logger.warn("(SEA) Request Started")
        response = requests.post(sea_url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.warn("(SEA) Http Error:" + errh)
    except requests.exceptions.ConnectionError as errc:
        logger.warn("(SEA) Error Connecting:" + errc)
    except requests.exceptions.Timeout as errt:
        logger.warn("(SEA) Timeout Error:" + errt)
    except requests.exceptions.RequestException as err:
        logger.warn("(SEA) OOps: Something Else" + err)

    result = response.json()

    if WATERSHED_DEBUG:
        logger.warn(result)
        logger.warn("(SEA) Request Finished")

    if result["status"] != "SUCCESS":
        if WATERSHED_DEBUG:
            logger.warn("(SEA) Request Failed:" + result["message"])
        raise Exception

    # response object from sea example
    # {"status":"SUCCESS","message":"717 DEM points were used in the calculations.",
    # "SlopeElevationAspectResult":{"slope":44.28170006222049,
    # "minElevation":793.0,"maxElevation":1776.0,
    # "averageElevation":1202.0223152022315,"aspect":125.319019998603,
    # "confidenceIndicator":46.840837384501654}}
    sea = result["SlopeElevationAspectResult"]

    slope = sea["slope"]
    median_elev = sea["averageElevation"]
    aspect = sea["aspect"]

    return (slope, median_elev, aspect)


def get_hillshade(slope_rad: float, aspect_rad: float):
    """
    Calculates the percentage hillshade (solar_exposure) value
    based on the average slope and aspect of a point
    """

    if slope_rad is None or aspect_rad is None:
        return None

    azimuth = 180.0  # 0-360 we are using values from the scsb2016 paper
    altitude = 45.0  # 0-90 " "
    azimuth_rad = azimuth * math.pi / 2.
    altitude_rad = altitude * math.pi / 180.

    shade_value = math.sin(altitude_rad) * math.sin(slope_rad) \
        + math.cos(altitude_rad) * math.cos(slope_rad) \
        * math.cos((azimuth_rad - math.pi / 2.) - aspect_rad)

    return abs(shade_value)


def extract_poly_coords(geom):
    if geom.type == 'Polygon':
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for interior in geom.interiors:
            interior_coords += interior.coords[:]
    elif geom.type == 'MultiPolygon':
        exterior_coords = []
        interior_coords = []
        for part in geom:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc['exterior_coords']
            interior_coords += epc['interior_coords']
    else:
        raise ValueError('Unhandled geometry type: ' + repr(geom.type))
    return {'exterior_coords': exterior_coords,
            'interior_coords': interior_coords}


def export_summary_as_xlsx(data: dict):
    """ exports watershed summary data as an excel file
        using a template in the ./templates directory.
    """

    cur_date = datetime.datetime.now().strftime("%Y%m%d")

    ws_name = data.get("watershed_name", "Surface_Water")
    ws_name.replace(" ", "_")

    filename = f"{cur_date}_{ws_name}"

    excel_file = docgen_export_to_xlsx(
        data, SURFACE_WATER_XLSX_TEMPLATE, filename)

    return Response(
        content=excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}.xlsx"}
    )


def find_50k_watershed_codes(db: Session, geom: Polygon):
    """ returns an array of 50k watershed codes (older watershed codes) within the watershed area """

    ws_wkt = geom.wkt

    q = db.query(
        func.distinct(FreshwaterAtlasStreamNetworks.WATERSHED_CODE_50K)) \
        .filter(
            func.st_intersects(
                FreshwaterAtlasStreamNetworks.GEOMETRY,
                func.ST_GeomFromText(ws_wkt, 4326)
            )
    ).filter(FreshwaterAtlasStreamNetworks.WATERSHED_CODE_50K.isnot(None))

    codes = [code for sublist in q.all() for code in sublist]

    # the Stream Networks layer returns codes as one long number, but the proper legacy
    # format is 119-111111-22222-22222 .... (number of digits per segment: 3-6-5-5-5...)
    # use regex to format the number groups.
    # the last digit was arbitrarily set to 6 until documentation on the correct format for
    # these legacy codes is found.
    re_pattern = r"(\d{3})(\d{6})(\d{5})(\d{5})(\d{5})(\d{5})(\d{5})(\d{5})(\d{6})"

    formatted_codes = []

    for code in codes:
        segments = re.findall(re_pattern, code)[0]
        # truncate all-zero codes at end (e.g. 119-118400-00000-00000-00000 ....)
        fwa_20k_code = '-'.join([s for s in segments if s != len(s) * '0'])
        formatted_codes.append(fwa_20k_code)

    return sorted(formatted_codes, key=len)


def known_fish_observations(polygon: Polygon):
    """ returns fish observation data from within a watershed polygon"""
    fish_observations_layer = 'fish_observations'

    # search with a simplified rectangle representing the polygon.
    # we will do an intersection on the more precise polygon after
    polygon_rect = polygon.minimum_rotated_rectangle
    fish_observations = databc_feature_search(
        fish_observations_layer, search_area=polygon_rect)

    polygon_3005 = transform(transform_4326_3005, polygon)

    features_within_search_area = []
    # observation_count_by_species = {}
    # life_stages_by_species = {}
    # observation_date_by_species = {}

    fish_species_data = {}

    for feature in fish_observations.features:
        feature_shape = shape(feature.geometry)

        # skip observations outside search area
        if not feature_shape.within(polygon_3005):
            continue

        # skip point if not a direct observation
        # summary points are consolidated observations.
        if feature.properties['POINT_TYPE_CODE'] != 'Observation':
            continue

        species_name = feature.properties['SPECIES_NAME']
        life_stage = feature.properties['LIFE_STAGE']
        observation_date = datetime.datetime.strptime(feature.properties['OBSERVATION_DATE'], '%Y-%m-%dZ').date() \
            if feature.properties['OBSERVATION_DATE'] is not None else None  # 1997-02-01Z

        if species_name is not None:
            if not fish_species_data.get(species_name, None):
                fish_species_data[species_name] = {
                    'count': 0,
                    'life_stages': [],
                    'observation_date_min': None,
                    'observation_date_max': None
                }

            # add to observation count for this species
            fish_species_data[species_name]['count'] += 1

            # add life stage observed uniquely
            if life_stage is not None:
                if life_stage not in fish_species_data[species_name]['life_stages']:
                    fish_species_data[species_name]['life_stages'].append(
                        life_stage)

            # add oldest and latest observation of species within watershed
            if observation_date is not None:
                if fish_species_data[species_name]['observation_date_min'] is None:
                    fish_species_data[species_name]['observation_date_min'] = observation_date
                if fish_species_data[species_name]['observation_date_max'] is None:
                    fish_species_data[species_name]['observation_date_max'] = observation_date

                if observation_date < fish_species_data[species_name]['observation_date_min']:
                    fish_species_data[species_name]['observation_date_min'] = observation_date
                if observation_date > fish_species_data[species_name]['observation_date_max']:
                    fish_species_data[species_name]['observation_date_max'] = observation_date

        features_within_search_area.append(feature)

    # transform multi-dict to flat list
    fish_species_data_list = []
    for key, val in fish_species_data.items():
        fish_species_data_list.append({
            'species': key,
            'count': val['count'],
            'life_stages': parse_fish_life_stages(val['life_stages']),
            'observation_date_min': val['observation_date_min'],
            'observation_date_max': val['observation_date_max']
        })

    return FishObservationsDetails(
        fish_observations=FeatureCollection([
            Feature(
                geometry=transform(transform_3005_4326, shape(feat.geometry)),
                id=feat.id,
                properties=feat.properties
            ) for feat in features_within_search_area
        ]),
        fish_species_data=fish_species_data_list
    )


def get_stream_inventory_report_link_for_region(point: Point):
    """ Returns Fish Inventory Data Query (FIDQ) links for streams within this
        watershed area.
    """
    point_3005 = transform(transform_4326_3005, point)

    # look up region that this point is in
    cql_filter = f"""INTERSECTS(SHAPE, {point_3005.wkt})"""
    region = databc_feature_search(
        'WHSE_ADMIN_BOUNDARIES.ADM_NR_REGIONS_SPG', cql_filter=cql_filter)

    # a point in BC should match with a region.
    # We also expect any given point to be within at most 1 region.
    if len(region['features']) != 1:
        return None

    region_code = region['features'][0]['properties'].get('ORG_UNIT', None)

    if not region_code:
        return None

    # if reports need to be added or updated, a database table might be required.
    # for now, we only have to keep track of these 7 report links.
    report_map = {
        "RNO":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=48460",
             "Inventory of Streamflow in the Omineca and Northeast Regions"),
        "ROM":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=48460",
             "Inventory of Streamflow in the Omineca and Northeast Regions"),
        "RSC":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=53344",
             "Inventory of Streamflow in the South Coast and West Coast Regions"),
        "RWC":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=53344",
             "Inventory of Streamflow in the South Coast and West Coast Regions"),
        "RCB":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=52707",
             "Inventory of Streamflow in the Cariboo Region"),
        "RTO":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=58628",
             "Inventory of Streamflow in the Thompson Okanagan Region"),
        "RSK":
            ("https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=40801",
             "Inventory of Streamflow in the Skeena Region"),
    }

    return report_map.get(region_code, None)


def parse_fish_life_stages(stages):
    """ cleans up life stage strings such as 'egg,juvenile'"""

    split_list = [item.split(',') for item in stages]
    flat_list = [item for sublist in split_list for item in sublist]

    return list(set(flat_list))


def get_scsb2016_input_stats(db: Session):
    q = """
    select * from modeling.scsb2016_model_input_stats;
    """
    result = db.execute(q)
    stats = [dict(row) for row in result]
    return stats


def get_watershed_details(db: Session, watershed: Feature, use_sea: bool = True):
    """ returns watershed inputs variables used in modelling """

    if WATERSHED_DEBUG:
        logger.info("getting watershed details")

    watershed_poly = shape(watershed.geometry)
    watershed_area = transform(transform_4326_3005, watershed_poly).area
    watershed_rect = watershed_poly.minimum_rotated_rectangle

    if WATERSHED_DEBUG:
        logger.info("watershed area %s", watershed_area)

    # watershed characteristics lookups
    drainage_area = watershed_area / 1e6  # needs to be in km²
    glacial_area_m, glacial_coverage = calculate_glacial_area(
        db, watershed_rect)

    if WATERSHED_DEBUG:
        logger.info("glacial coverage %s", glacial_coverage)

    # precipitation values from prism raster
    annual_precipitation = mean_annual_precipitation(db, watershed_poly)
    if not annual_precipitation:
        # fall back on PCIC data
        annual_precipitation = get_annual_precipitation(watershed_poly)

    if WATERSHED_DEBUG:
        logger.info("annual precipitation %s", annual_precipitation)

    # temperature and potential evapotranspiration values
    try:
        temperature_data = get_temperature(watershed_poly)
        potential_evapotranspiration_hamon = calculate_potential_evapotranspiration_hamon(
            watershed_poly, temperature_data)
        potential_evapotranspiration_thornthwaite = calculate_potential_evapotranspiration_thornthwaite(
            watershed_poly, temperature_data
        )
    except Exception:
        temperature_data = None
        potential_evapotranspiration_hamon = None
        potential_evapotranspiration_thornthwaite = None

    if WATERSHED_DEBUG:
        logger.info("temperature data %s", temperature_data)

    # hydro zone dictates which model values to use
    hydrological_zone = get_hydrological_zone(watershed_poly.centroid)

    polygon_4140 = transform(transform_4326_4140, watershed_poly)
    area_cdem = CDEM(polygon_4140)

    elev_stats = area_cdem.get_raster_summary_stats()
    median_elev = area_cdem.get_median_elevation()
    avg_slope = area_cdem.get_average_slope()
    aspect = area_cdem.get_mean_aspect()

    slope_percent = math.tan(avg_slope) * 100
    slope_radians = avg_slope * (math.pi/180)
    solar_exposure = get_hillshade(slope_radians, aspect)

    if WATERSHED_DEBUG:
        logger.info("elevation stats %s", elev_stats)
        logger.info("median elevation %s", median_elev)
        logger.info("average slope %s", slope_percent)
        logger.info("aspect %s", aspect)
        logger.info("solar exposure %s", solar_exposure)

    data = {
        "watershed_id": watershed.id,
        "watershed_area": watershed_area,
        "drainage_area": drainage_area,
        "glacial_area": glacial_area_m,
        "glacial_coverage": glacial_coverage,
        "temperature_data": temperature_data,
        "annual_precipitation": annual_precipitation,
        "potential_evapotranspiration_hamon": potential_evapotranspiration_hamon,
        "potential_evapotranspiration_thornthwaite": potential_evapotranspiration_thornthwaite,
        "hydrological_zone": hydrological_zone,
        "average_slope": slope_percent,
        "solar_exposure": solar_exposure,
        "median_elevation": median_elev,
        "elevation_stats": elev_stats,
        "aspect": aspect
    }

    return data
