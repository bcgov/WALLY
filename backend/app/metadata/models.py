from typing import Optional, List
from pydantic import BaseModel, Schema


class Catalogue(BaseModel):
    """
    Map layer information
    """
    display_name: str
    display_data_name: str
    label: str
    label_column: str
    highlight_columns: List[str]
    wms_name: str = ''
    wms_style: str = ''
    vector_name: str = ''
    layer_category_code: str = ''
    url: str = ''

    class Config:
        orm_mode = True


class MapConfig(BaseModel):
    """
    Client map config e.g. access tokens
    """
    mapbox_token: str


class LayerCategory(BaseModel):
    """ Layer categories """
    layer_category_code: str
    description: str
