"""
External API data models for Common Services Document Generator.
"""
from pydantic import BaseModel


class DocGenTemplateFile(BaseModel):
    """ the metadata and encoded file for
        a stream  excel template.
        This is the format required by the Common Services
        Document Generator.
    """

    encodingType: str
    content: str  # base64 encoded
    fileType: str


class DocGenOptions(BaseModel):
    """ options for docgen requests """
    reportName: str
    overwrite: str = "true"


class DocGenRequest(BaseModel):
    """ the request body for making document generator requests """

    data: dict
    template: dict
    options: dict = {}
