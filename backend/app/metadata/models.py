from typing import Optional, List
from pydantic import BaseModel, Schema


class MapLayer(BaseModel):
    """
    Map layer information
    """

    layer_name: str
    map_layer_type_id: str
    wms_name: str
    wms_style: str
    api_url: str

    class Config:
        orm_mode = True
