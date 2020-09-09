from pydantic import BaseModel
from pyparsing import Optional


class VersionConfig(BaseModel):
    """
    Client map config e.g. access tokens
    """
    wally_version: str
    wally_env: str
    api_version: str

