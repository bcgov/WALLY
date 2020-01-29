import logging

from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import LineString, CAP_STYLE, JOIN_STYLE
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
    line = transform(transform_4326_3005, line)
    buf = line.buffer(distance, cap_style=CAP_STYLE.flat,
                      join_style=JOIN_STYLE.round)
    buf_simplified = buf.simplify(50, preserve_topology=False)

    buf_4326 = transform(transform_3005_4326, buf_simplified)

    features = feature_search(db, [layer], buf_4326)[0].geojson

    return [feature.properties for feature in features.features]
