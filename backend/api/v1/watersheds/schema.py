import json
from typing import List, Optional, Union
from pydantic import BaseModel
from geojson import Feature, FeatureCollection, Point


class WatershedDetails(BaseModel):
    """ info about a watershed"""
    potential_evapotranspiration_hamon: Optional[float]
    potential_evapotranspiration_thornthwaite: Optional[float]
    precipitation: Optional[dict]
    glacial_coverage: float
    glacial_area: float
    watershed_area: float
    precip_search_area: Optional[float]
    runoff_isoline_avg: Optional[float]
    hydrological_zone: Optional[str]


class LicenceDetails(BaseModel):
    """ statistics about licences in a given area """
    licences: FeatureCollection
    total_qty: float
    total_qty_by_purpose: List
    projected_geometry_area: Optional[float]
    projected_geometry_area_simplified: Optional[float]

    class Config:
        arbitrary_types_allowed = True


class SurficialGeologyTypeSummary(BaseModel):
    """ 
    Summary of features belonging to single type of surficial geology in a search area.
    e.g. summary of all bedrock features in a search area, with a FeatureCollection,
    total area, etc.
    """
    soil_type: str
    area_within_watershed: float
    geojson: FeatureCollection

    class Config:
        arbitrary_types_allowed = True


class SurficialGeologyDetails(BaseModel):
    """ statistics about surficial geology
    """
    summary_by_type: List
    coverage_area: Optional[float]
    projected_geometry_area: Optional[float]
    projected_geometry_area_simplified: Optional[float]


class FishObservationsDetails(BaseModel):
    """ statistics about fish observations in a given area """
    fish_observations: FeatureCollection
    fish_species_data: List

    class Config:
        arbitrary_types_allowed = True