"""
API data models for Projects.
"""
from pydantic import BaseModel
from typing import Optional


class SavedAnalysis(BaseModel):
    name: Optional[str]
    description: Optional[str]
