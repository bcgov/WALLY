"""
Map layers (layers module) API endpoints/handlers.
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.layers.models import Publisher

router = APIRouter()


@router.get("/publishers", response_model=List[Publisher])
def get_publishers():
    """ returns available map layers """

    owner1 = Publisher(
        id=uuid.uuid4(),
        name="Environment Canada",
        description="The department of the Government of Canada with responsibility for coordinating " +
        "environmental policies and programs as well as preserving and enhancing the natural environment " +
        "and renewable resources."
    )

    owner2 = Publisher(
        id=uuid.uuid4(),
        name="Ministry of Environment and Climate Change",
        description="The British Columbia Ministry of Environment and Climate Change"
    )

    response = [owner1, owner2]

    return response
