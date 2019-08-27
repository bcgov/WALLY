"""
Database queries for aggregating data from WMS layers and APIs
"""
from sqlalchemy.orm import Session
from typing import List
import logging
from app.metadata.db_models import DisplayCatalogue, ApiCatalogue, WmsCatalogue
from sqlalchemy.orm import joinedload

logger = logging.getLogger("api")


def get_display_catalogue(db: Session, display_data_names: List[str]):
    q = db.query(DisplayCatalogue).options(joinedload(DisplayCatalogue.wms_catalogue),
                                           joinedload(DisplayCatalogue.api_catalogue))\
        .filter(DisplayCatalogue.display_data_name.in_(display_data_names))\
        .all()
    # [logger.info(vars(x)) for x in q]
    return q

    # """ placeholder for testing.  to be replaced with context metadata """
    # valid_layers = []
    # if "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW" in layers:
    #     valid_layers.append({
    #         "id": "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
    #         "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?",
    #         "type": "wms"
    #     })
    #
    # if "WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW" in layers:
    #     valid_layers.append({
    #         "id": "WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW",
    #         "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW/ows?",
    #         "type": "wms"
    #     })
    #
    # if "HYDAT" in layers:
    #     valid_layers.append({
    #         "id": "HYDAT",
    #         "api_url": "localhost:8000/api/v1/hydat",
    #         "type": "api"
    #     })
    #
    # return valid_layers
