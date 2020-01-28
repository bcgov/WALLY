import logging
from sqlalchemy.orm import Session
from api.v1.aggregator.controller import feature_search
from api.v1.aggregator.helpers import transform_4326_3005
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform

logger = logging.getLogger("isolines")


def calculate_runnoff_in_area(db: Session, polygon: MultiPolygon) -> float:
    """
    Calculates the precipitation runoff using the area of `polygon` which intersects with features from
    the normal annual runoff isolines layer.
    """

    isolines_layer = 'normal_annual_runoff_isolines'

    logger.info(polygon)

    isoline_features = feature_search(db, [isolines_layer], polygon)[
        0].geojson.features

    isoline_area = 0

    polygon = transform(transform_4326_3005, polygon)

    for isoline in isoline_features:
        isoline_clipped = shape(isoline.geometry).intersection(polygon)

        if not isoline_clipped.area:
            logger.info('isoline outside search area')
            continue

        logger.info('adding %s', str(isoline_clipped.area))

        isoline_area += isoline_clipped.area

    coverage = isoline_area / polygon.area

    return (isoline_area, coverage)