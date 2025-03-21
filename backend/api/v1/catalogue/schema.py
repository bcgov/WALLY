from typing import Optional, List
from pydantic import BaseModel, Schema


class Layer(BaseModel):
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
    use_wms: bool = False
    source_name: str = ''
    source_description: str = ''
    source_layer: str = ''
    source_url: str = ''
    vector_name: str = ''
    layer_category_code: str = ''
    url: str = ''

    class Config:
        orm_mode = True


class LayerCategory(BaseModel):
    """ Layer categories """
    layer_category_code: str
    description: str
    display_order: int

    class Config:
        orm_mode = True


class Catalogue(BaseModel):
    """ catalogue of layers and other layer metadata """
    layers: List[Layer]
    categories: List[LayerCategory]
