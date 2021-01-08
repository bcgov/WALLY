"""
API data models for Projects.
"""
from pydantic import BaseModel
from typing import Optional


class Project(BaseModel):
    name: Optional[str]
    description: Optional[str]
