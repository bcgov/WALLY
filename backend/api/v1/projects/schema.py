"""
API data models for Projects.
"""
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class ProjectDocument(BaseModel):
    project_document_uuid: UUID
    s3_path: Optional[str]
    filename: Optional[str]

    class Config:
        orm_mode = True


class Project(BaseModel):
    project_uuid: UUID
    name: Optional[str]
    description: Optional[str]
    children: Optional[List[ProjectDocument]]

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]
