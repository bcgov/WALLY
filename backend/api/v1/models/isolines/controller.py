import logging
from sqlalchemy.orm import Session
from api.v1.aggregator.controller import feature_search
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
from api.v1.aggregator.helpers import transform_4326_3005

logger = logging.getLogger("isolines")


def calculate_runoff_in_area(db: Session, polygon: MultiPolygon):
    """
    Calculates the precipitation runoff using the area of `polygon`
    which intersects with features from the normal annual runoff
    isolines layer.
    """

    isolines_layer = 'normal_annual_runoff_isolines'

    features = feature_search(db, [isolines_layer], polygon)
    if features:
        isoline_features = features[0].geojson.features
    else:
        isoline_features = []

    area_total = 0
    avg_mm = 0
    runoff_total = 0

    for isoline in isoline_features:

        isoline_clipped = shape(isoline.geometry).intersection(polygon)
        isoline_clipped = transform(transform_4326_3005, isoline_clipped)

        if not isoline_clipped.area:
            logger.info('isoline outside search area')
            continue

        area_total += isoline_clipped.area
        runoff_total += isoline_clipped.area * \
            (float(isoline["properties"]["ANNUAL_RUNOFF_IN_MM"]) / 1000)

    if isoline_features:
        avg_mm = avg_mm / len(isoline_features)

    return {
        "area": area_total,
        "runoff": runoff_total,
        "avg_mm": (runoff_total / area_total) if area_total > 0 else 0
    }
