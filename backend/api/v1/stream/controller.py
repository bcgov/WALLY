import logging

import geojson
from geojson import Feature, FeatureCollection
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import LineString, CAP_STYLE, JOIN_STYLE, shape, mapping
from shapely.ops import transform
from api.v1.aggregator.controller import feature_search
from api.v1.aggregator.helpers import transform_3005_4326, transform_4326_3005
from api.v1.wells.controller import create_line_buffer
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks

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

    logger.warn('to_3005: from_proj must be either 4326 or 3005. Feature returned without transforming to 3005.')
    return feat


def get_features_within_buffer(db: Session, line, distance: float, layer: str) -> FeatureCollection:
    """ List features within a buffer zone from a geometry
    """

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
        Feature(geometry=feat['geometry'], properties=feat['properties']) for feat in features if to_3005(feat_proj, shape(feat['geometry'])).intersects(line_3005)
    ]

    return FeatureCollection(features_intersecting)
