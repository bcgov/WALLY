from pydantic import BaseModel
from pyparsing import Optional


class MapConfig(BaseModel):
    """
    Client map config e.g. access tokens
    """
    mapbox_token: str
    mapbox_style: str


class VersionConfig(BaseModel):
    """
    Client map config e.g. access tokens
    """
    wally_version: str
    wally_env: str
    api_version: str

