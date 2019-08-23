from typing import Optional, List
from pydantic import BaseModel, Schema


class Catalogue(BaseModel):
    """
    Map layer information
    """
    display_data_name: str
    wms_name: str
    wms_style: str
    url: str

    class Config:
        orm_mode = True
