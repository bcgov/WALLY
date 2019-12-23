"""
API data models.
These are external facing data models/schemas that users see.
"""
from pydantic import BaseModel


class Elevation(BaseModel):
    """ elevation data at a point """
    distance_from_origin: float
    elevation: float
