"""
Functions for aggregating data from web requests and database records
"""
import logging
import requests
import geojson
from typing import Tuple
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from shapely.geometry import Polygon, MultiPolygon, shape, box
from shapely.ops import transform
from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326
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


def precipitation(
        polygon: Polygon,
        output_variable: str = 'pr',
        dataset: str = 'pr_mClim_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19810101-20101231_Canada'):
    """ Returns an average precipitation from the pacificclimate.org climate explorer service """

    pcic_url = "https://services.pacificclimate.org/pcex/api/timeseries?"

    params = {
        "id_": dataset,
        "variable": output_variable,
        "area": polygon.wkt
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
    """

    q = """
        select ST_AsGeojson(
            coalesce(
                (SELECT ST_Union(geom) as geom from calculate_upstream_catchment_starting_upstream(:watershed_feature_id, :include)),
                (SELECT ST_Union(geom) as geom from calculate_upstream_catchment(:watershed_feature_id))
            )
        ) as geom """

    logger.info(watershed_feature_id)

    res = db.execute(q, {"watershed_feature_id": watershed_feature_id,
                         "include": watershed_feature_id if include_self else None})

    one = res.fetchone()

    logger.info(one)
    return Feature(
        geometry=shape(
            geojson.loads(one[0])
        ),
        id=watershed_feature_id,
        properties={
            "name": "Estimated catchment area (Freshwater Atlas)"
        }
    )


def get_watershed(watershed_id: str):
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
