"""
External API data models for Common Services Document Generator.
"""
from pydantic import BaseModel
from typing import List, Any, Optional
from geojson import Feature


class DocGenTemplateFile(BaseModel):
    """ the metadata and encoded file for
        a stream apportionment excel template.
        This is the format required by the Common Services
        Document Generator.
    """

    outputFileName: str
    contentEncodingType: str
    content: str  # base64 encoded
    contentFileType: str


class DocGenRequest(BaseModel):
    """ the request body for making document generator requests """

    contexts: list
    template: dict
