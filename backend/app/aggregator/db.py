"""
Database queries for aggregating data from WMS layers and APIs
"""
from typing import List
import logging

logger = logging.getLogger("api")


def get_wms_layers(layers: List[str]):
    valid_layers = []
    if "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW" in layers:
        valid_layers.append({
            "id": "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
            "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?",
            "type": "wms"
        })
    return valid_layers
