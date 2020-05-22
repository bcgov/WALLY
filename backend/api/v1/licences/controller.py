import logging
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import Point, shape
from api.v1.aggregator.controller import DATABC_GEOMETRY_FIELD, databc_feature_search
from api.layers.water_rights_licences import WaterRightsLicenses
from api.layers.water_rights_applications import WaterRightsApplications
from api.v1.licences.schema import WaterRightsLicence
logger = logging.getLogger("api")


def normalize_quantity(qty, qty_unit: str):
    """ takes a qty and a unit (as a string) and returns the quantity in m3/year
        accepts:
        m3/sec
        m3/day
        m3/year
    """

    qty_unit = qty_unit.strip()

    if qty_unit == 'm3/year':
        return qty
    elif qty_unit == 'm3/day':
        return qty * 365
    elif qty_unit == 'm3/sec':
        return qty * 60 * 60 * 24 * 365
    else:
        return None


def get_surface_water_approval_points_databc(point: Point, radius: float):
    """ returns surface water approval points (section 11 approvals) """
    water_approval_layer = "WHSE_WATER_MANAGEMENT.WLS_WATER_APPROVALS_SVW"

    cql_filter = f"""DWITHIN({DATABC_GEOMETRY_FIELD.get(
        water_approval_layer, 'SHAPE')}, {point.wkt}, {radius}, meters)"""

    approvals_list = databc_feature_search(
        water_approval_layer, cql_filter=cql_filter)

    features_within_search_area = []

    for feat in approvals_list.features:

        if feat.properties['QUANTITY']:
            qty = float(feat.properties['QUANTITY'])
            qty_unit = feat.properties['QUANTITY_UNITS'].strip()

            feat.properties['qty_m3yr'] = normalize_quantity(qty, qty_unit)
        else:
            feat.properties['qty_m3yr'] = None

        feat.properties['status'] = feat.properties['APPROVAL_STATUS']
        feat.properties['type'] = 'Water approval'
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

        if feat.properties['QUANTITY']:
            qty = float(feat.properties['QUANTITY'])
            qty_unit = feat.properties['QUANTITY_UNITS'].strip()

            feat.properties['qty_m3yr'] = normalize_quantity(qty, qty_unit)
        else:
            feat.properties['qty_m3yr'] = None

        feat.properties['status'] = feat.properties['LICENCE_STATUS']
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

        if feat.properties['QUANTITY']:
            qty = float(feat.properties['QUANTITY'])
            qty_unit = feat.properties['QUANTITY_UNITS'].strip()

            feat.properties['qty_m3yr'] = normalize_quantity(qty, qty_unit)
        else:
            feat.properties['qty_m3yr'] = None

        feat.properties['status'] = feat.properties['APPLICATION_STATUS']
        feat.properties['type'] = 'Application'
        feat.properties['distance'] = shape(feat.geometry).distance(point)
        features_within_search_area.append(feat)

    return features_within_search_area


def get_licences_by_distance(db: Session, search_point: Point, radius: float) -> list:
    """ List water rights licences by distance from a point.
    """

    if radius > 10000:
        radius = 10000

    # search within a given radius, adding a distance column denoting
    # distance from the centre point in metres
    # geometry columns are cast to geography to use metres as the base unit.
    licences_q = db.query(
        WaterRightsLicenses,
        func.ST_Distance(func.Geography(WaterRightsLicenses.SHAPE),
                         func.ST_GeographyFromText(search_point.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(WaterRightsLicenses.SHAPE),
                            func.ST_GeographyFromText(search_point.wkt), radius)
    ) \
        .order_by('distance')

    licences_results = licences_q.all()

    licences = [WaterRightsLicence(
        **row[0].__dict__, distance=row[1]) for row in licences_results]

    applications_q = db.query(
        WaterRightsApplications,
        func.ST_Distance(func.Geography(WaterRightsApplications.SHAPE),
                         func.ST_GeographyFromText(search_point.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(WaterRightsApplications.SHAPE),
                            func.ST_GeographyFromText(search_point.wkt), radius)
    ) \
        .order_by('distance')

    applications_results = applications_q.all()

    applications = [WaterRightsLicence(
        **row[0].__dict__, distance=row[1]) for row in applications_results]

    return licences + applications
