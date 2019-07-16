"""
API data models.
These are external facing data models/schemas that users see.
"""
from pydantic import BaseModel, Schema, UUID4


class Publisher(BaseModel):
    """
    API data model for a publisher (data owner).
    """
    id: UUID4
    name: str = Schema(
        ..., title="The name of the organization", max_length=300)
    description: str = Schema(
        None, title="The description of the organization", max_length=300)
