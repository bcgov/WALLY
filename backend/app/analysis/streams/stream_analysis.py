import json
import logging
import requests
from sqlalchemy import func
from sqlalchemy.orm import Session
logger = logging.getLogger("api")

from app.aggregator.endpoints import API_DATASOURCES


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
