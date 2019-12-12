import json
import logging
import requests
from sqlalchemy import func
from sqlalchemy.orm import Session, load_only
from app.aggregator.endpoints import API_DATASOURCES
from app.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from geoalchemy2.shape import to_shape
from geojson import Feature
from shapely import wkb

logger = logging.getLogger("api")

def get_connected_streams(db: Session, outflowcode: str) -> list:

    q = db.query(FreshwaterAtlasStreamNetworks) \
        .filter(FreshwaterAtlasStreamNetworks.FWA_WATERSHED_CODE.startswith(outflowcode))

    results = q.all()

    feature_results = [FreshwaterAtlasStreamNetworks \
        .get_as_feature(row, FreshwaterAtlasStreamNetworks.GEOMETRY) for row in results]

    return feature_results


def get_features_within_buffer(db: Session, geometry, buffer: float, layer: str) -> list:
    """ List features within a buffer zone from a geometry
    """
    layer_class = API_DATASOURCES[layer]
    geom = layer_class.get_geom_column(db)

    feature_results = db.query(
        layer_class,
        func.ST_Distance(func.Geography(geom),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(geom),
                            func.ST_GeographyFromText(geometry.wkt), buffer)
    ) \
    .order_by('distance').all()

    features = [layer_class.get_as_properties(row[0]) for row in feature_results]

    return features
