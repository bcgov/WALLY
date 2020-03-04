"""
Functions for aggregating data from web requests and database records
"""
import logging
import requests
import geojson
import json

import math
from typing import Tuple
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from shapely.geometry import Point, Polygon, MultiPolygon, shape, box, mapping
from shapely.ops import transform
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds
from fastapi import HTTPException
from pyeto import thornthwaite, monthly_mean_daylight_hours, deg2rad
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326
from api.v1.models.isolines.controller import calculate_runoff_in_area

from api.v1.watersheds.schema import LicenceDetails, SurficialGeologyDetails

from api.v1.aggregator.controller import feature_search, databc_feature_search

logger = logging.getLogger('api')


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

    logger.info('pcic request: %s', req_url)

    try:
        resp = requests.get(req_url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return resp.json()


def surface_water_rights_licences(polygon: Polygon):
    """ returns surface water rights licences (filtered by POD subtype)"""
    water_rights_layer = 'water_rights_licences'

    # search with a simplified rectangle representing the polygon.
    # we will do an intersection on the more precise polygon after
    polygon_rect = polygon.minimum_rotated_rectangle
    licences = databc_feature_search(
        water_rights_layer, search_area=polygon_rect)

    total_licenced_qty_m3_yr = 0
    licenced_qty_by_use_type = {}

    polygon_3005 = transform(transform_4326_3005, polygon)

    features_within_search_area = []

    for lic in licences.features:
        feature_shape = shape(lic.geometry)

        # skip licences outside search area
        if not feature_shape.within(polygon_3005):
            continue

        # skip licence if not a surface water point of diversion (POD)
        # other pod_subtype codes are associated with groundwater.
        if lic.properties['POD_SUBTYPE'] != 'POD':
            continue

        features_within_search_area.append(lic)

        qty = lic.properties['QUANTITY']
        qty_unit = lic.properties['QUANTITY_UNITS'].strip()
        purpose = lic.properties['PURPOSE_USE']

        if qty_unit == 'm3/year':
            pass
        elif qty_unit == 'm3/day':
            qty = qty * 365
        elif qty_unit == 'm3/sec':
            qty = qty * 60 * 60 * 24 * 365
        else:
            qty = 0

        total_licenced_qty_m3_yr += qty
        lic.properties['qty_m3_yr'] = qty

        if purpose is not None:
            if not licenced_qty_by_use_type.get(purpose, None):
                licenced_qty_by_use_type[purpose] = 0
            licenced_qty_by_use_type[purpose] += qty

    licence_purpose_type_list = []

    for purpose, qty in licenced_qty_by_use_type.items():
        licence_purpose_type_list.append({
            "purpose": purpose,
            "qty": qty,
            "units": "m3/year"
        })

    return LicenceDetails(
        licences=FeatureCollection([
            Feature(
                geometry=transform(transform_3005_4326, shape(feat.geometry)),
                id=feat.id,
                properties=feat.properties
            ) for feat in features_within_search_area
        ]),
        total_qty=total_licenced_qty_m3_yr,
        total_qty_by_purpose=licence_purpose_type_list,
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

    # calculates an upstream catchment feature (see function docstring), and inserts it into
    # upstream_watershed_cache.
    # the first query in the coalesce function retrieves a cached geometry, if available.
    # the second query attempts method 1 (see docstring); the third attempts method 3.
    q = """
        with del_outdated as (
            delete from upstream_watershed_cache
            where expiry_date < now()
        ),
        feat as (
            select coalesce(
                (
                    select  geom
                    from    upstream_watershed_cache
                    where   watershed_feature_id = :watershed_feature_id
                    and     include_features is not distinct from (:include)::int
                    and     expiry_date >= now()
                    limit 1
                ),
                (
                    select  ST_Union(geom) as geom
                    from     calculate_upstream_catchment_starting_upstream(:watershed_feature_id, :include)
                ),
                (
                    select  ST_Union(geom) as geom
                    from    calculate_upstream_catchment(:watershed_feature_id))
            ) as geom
        ),
        ins_feat as (
            insert into upstream_watershed_cache
            (watershed_feature_id, include_features, geom, create_date, update_date, expiry_date)
            select 
                :watershed_feature_id,
                (:include)::int,
                feat.geom,
                now(), now(), now() + interval '10 min'
                from feat
            on conflict do nothing
        )
        select ST_AsGeojson(
            geom
        ) as geom from feat """

    res = db.execute(q, {"watershed_feature_id": watershed_feature_id,
                         "include": watershed_feature_id if include_self else None})

    record = res.fetchone()

    if not record or not record[0]:
        db.rollback()
        logger.warn(
            'unable to calculate watershed from watershed feature id %s', watershed_feature_id)
        return None

    db.commit()

    return Feature(
        geometry=shape(
            geojson.loads(record[0])
        ),
        id=f"generated.{watershed_feature_id}",
        properties={
            "name": "Estimated catchment area (Freshwater Atlas)"
        }
    )


def calculate_watershed(
    db: Session,
    point: Point,
    include_self: bool
):
    """ calculates watershed area upstream of a POI """

    q = db.query(FreshwaterAtlasWatersheds.WATERSHED_FEATURE_ID).filter(
        func.ST_Contains(
            FreshwaterAtlasWatersheds.GEOMETRY,
            func.ST_GeomFromText(point.wkt, 4326)
        )
    )

    watershed_id = q.first()

    if not watershed_id:
        logger.info(
            'watershed estimation: no watershed polygons available at this point')
        return None
    watershed_id = watershed_id[0]

    feature = get_upstream_catchment_area(
        db, watershed_id, include_self=include_self)

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

    cql_filter = f"{id_props[watershed_layer]}={watershed_feature}"

    watershed = databc_feature_search(watershed_layer, cql_filter=cql_filter)
    if len(watershed.features) != 1:
        raise HTTPException(
            status_code=404, detail=f"Watershed with id {watershed_id} not found")

    return watershed.features[0]


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


def get_watershed(db: Session, watershed_feature: str, include_self=False):
    """ finds a watershed by either generating it or looking it up in DataBC watershed datasets """
    watershed_layer = '.'.join(watershed_feature.split('.')[:-1])
    watershed_feature_id = watershed_feature.split('.')[-1:]
    watershed = None

    # basic method to lookup a cached watershed geometry, if one exists.
    # it first clears out outdated cached records.
    cache_q = """
    with del_outdated as (
        delete from upstream_watershed_cache
        where expiry_date < now()
    )
    select * from upstream_watershed_cache
    where watershed_feature_id = :watershed_feature
    and include_features = ARRAY[(:include_features)::int)
    
    """

    logger.info(watershed_feature_id)

    # if we generated this watershed, use the catchment area
    # generation function to get the shape.
    if watershed_layer == 'generated':
        watershed = get_upstream_catchment_area(db, watershed_feature_id[0])

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

    min_temp = pcic_data_request(poly, 'tasmin')
    max_temp = pcic_data_request(poly, 'tasmax')

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
        response = requests.post(sea_url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise HTTPException(
            status_code=error.response.status_code, detail=str(error))

    result = response.json()
    logger.warning("sea result")
    logger.warning(result)

    if result["status"] != "SUCCESS":
        raise HTTPException(204, detail=result["message"])

    # response object from sea example
    # {"status":"SUCCESS","message":"717 DEM points were used in the calculations.",
    # "SlopeElevationAspectResult":{"slope":44.28170006222049,
    # "minElevation":793.0,"maxElevation":1776.0,
    # "averageElevation":1202.0223152022315,"aspect":125.319019998603,
    # "confidenceIndicator":46.840837384501654}}
    sea = result["SlopeElevationAspectResult"]

    slope = sea["slope"]
    median_elevation = sea["averageElevation"]
    aspect = sea["aspect"]

    return (slope, median_elevation, aspect)


def get_hillshade(slope: float, aspect: float):
    """
    Calculates the percentage hillshade (solar_exposure) value
    based on the average slope and aspect of a point
    """
    azimuth = 180.0  # 0-360 we are using values from the scsb2016 paper
    altitude = 45.0  # 0-90 " "
    azimuth_rad = azimuth * math.pi / 2.
    altitude_rad = altitude * math.pi / 180.

    shade_value = math.sin(altitude_rad) * math.sin(slope) \
        + math.cos(altitude_rad) * math.cos(slope) \
        * math.cos((azimuth_rad - math.pi / 2.) - aspect)

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
