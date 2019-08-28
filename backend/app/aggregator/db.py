"""
Database queries for aggregating data from WMS layers and APIs
"""
from typing import List
import logging

logger = logging.getLogger("api")


def get_layers(layers: List[str]):
    """ placeholder for testing.  to be replaced with context metadata """
    valid_layers = []
    if "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW" in layers:
        valid_layers.append({
            "id": "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
            "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?",
            "type": "wms"
        })

    if "WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW" in layers:
        valid_layers.append({
            "id": "WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW",
            "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW/ows?",
            "type": "wms"
        })

    if "WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY" in layers:
        valid_layers.append({
            "id": "WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY",
            "api_url": "https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY/ows?",
            "type": "wms"
        })

    if "HYDAT" in layers:
        valid_layers.append({
            "id": "HYDAT",
            "api_url": "localhost:8000/api/v1/hydat",
            "type": "api"
        })

    return valid_layers
