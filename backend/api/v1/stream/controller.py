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


def get_features_within_buffer(db: Session, line, distance: float, layer: str) -> list:
    """ List features within a buffer zone from a geometry
    """

    buf_simplified = line.minimum_rotated_rectangle

    fc = feature_search(db, [layer], buf_simplified)[0].geojson
    features = fc.get('features')

    line_3005 = transform(transform_4326_3005, line)

    features_intersecting = [
        Feature(geometry=feat['geometry'], properties=feat['properties']) for feat in features if transform(transform_4326_3005, shape(feat['geometry'])).distance(line_3005) < distance
    ]

    return FeatureCollection(features_intersecting)
