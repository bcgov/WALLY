import logging
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import Point, shape
from api.utils import normalize_quantity
from api.v1.aggregator.controller import DATABC_GEOMETRY_FIELD, databc_feature_search
from api.layers.water_rights_licences import WaterRightsLicenses
from api.layers.water_rights_applications import WaterRightsApplications
from api.v1.licences.schema import WaterRightsLicence
logger = logging.getLogger("api")


def get_surface_water_approval_points_databc(point: Point, radius: float):
    """ returns surface water approval points (section 11 approvals) """
    water_approval_layer = "WHSE_WATER_MANAGEMENT.WLS_WATER_APPROVALS_SVW"

    cql_filter = f"""DWITHIN({DATABC_GEOMETRY_FIELD.get(
        water_approval_layer, 'SHAPE')}, {point.wkt}, {radius}, meters)"""

    approvals_list = databc_feature_search(
        water_approval_layer, cql_filter=cql_filter)

    features_within_search_area = []

    for feat in approvals_list.features:

        if feat.properties.get('QUANTITY', None):
            try:
                qty = float(feat.properties['QUANTITY'])
            except:
                # if QUANTITY can't be converted to a float, treat it like a string.
                qty = feat.properties['QUANTITY']
            else:
                qty_unit = feat.properties.get('QUANTITY_UNITS', '').strip()
                feat.properties['qty_m3yr'] = normalize_quantity(qty, qty_unit)
        else:
            feat.properties['qty_m3yr'] = None

        feat.properties['usage'] = feat.properties.get(
            'WORKS_DESCRIPTION', '')
        feat.properties['status'] = feat.properties.get(
            'APPROVAL_STATUS', None)
        feat.properties['type'] = feat.properties.get('APPROVAL_TYPE',
                                                      'Water approval (no approval type listed)')
        feat.properties['distance'] = shape(feat.geometry).distance(point)
        features_within_search_area.append(feat)

    return features_within_search_area


def get_licences_by_distance_databc(point: Point, radius: float):
    water_licence_layer = "water_rights_licences"

    cql_filter = f"""DWITHIN({DATABC_GEOMETRY_FIELD.get(
        water_licence_layer, 'GEOMETRY')}, {point.wkt}, {radius}, meters)"""

    licences_list = databc_feature_search(
        water_licence_layer, cql_filter=cql_filter)

    features_within_search_area = []

    for feat in licences_list.features:

        if feat.properties.get('QUANTITY', None):
            qty = float(feat.properties['QUANTITY'])
            qty_unit = feat.properties.get('QUANTITY_UNITS', '').strip()

            feat.properties['qty_m3yr'] = normalize_quantity(qty, qty_unit)
        else:
            feat.properties['qty_m3yr'] = None

        feat.properties['usage'] = feat.properties.get(
            'PURPOSE_USE', '')
        feat.properties['status'] = feat.properties.get('LICENCE_STATUS', None)
        feat.properties['type'] = 'Licence'
        feat.properties['distance'] = shape(feat.geometry).distance(point)

        features_within_search_area.append(feat)

    return features_within_search_area


def get_applications_by_distance_databc(point: Point, radius: float):
    water_application_layer = "water_rights_applications"

    cql_filter = f"""DWITHIN({DATABC_GEOMETRY_FIELD.get(
        water_application_layer, 'GEOMETRY')}, {point.wkt}, {radius}, meters)"""

    applications_list = databc_feature_search(
        water_application_layer, cql_filter=cql_filter)

    features_within_search_area = []

    for feat in applications_list.features:

        if feat.properties.get('QUANTITY', None):
            qty = float(feat.properties['QUANTITY'])
            qty_unit = feat.properties.get('QUANTITY_UNITS', '').strip()

            feat.properties['qty_m3yr'] = normalize_quantity(qty, qty_unit)
        else:
            feat.properties['qty_m3yr'] = None

        feat.properties['status'] = feat.properties.get(
            'APPLICATION_STATUS', None)
        feat.properties['usage'] = feat.properties.get(
            'PURPOSE_USE', '')
        feat.properties['type'] = 'Application'
        feat.properties['distance'] = shape(feat.geometry).distance(point)
        features_within_search_area.append(feat)

    return features_within_search_area
