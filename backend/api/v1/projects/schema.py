"""
API data models for Projects.
"""
from pydantic import BaseModel
from typing import Optional, List


class ProjectDocument(BaseModel):
    project_document_id: int
    s3_path: Optional[str]
    filename: Optional[str]

    class Config:
        orm_mode = True


class Project(BaseModel):
    project_id: int
    name: Optional[str]
    description: Optional[str]
    children: Optional[List[ProjectDocument]]

    class Config:
        orm_mode = True
