"""
Database queries for aggregating data from WMS layers and APIs
"""
from sqlalchemy.orm import Session
from typing import List
import logging
from app.metadata.db_models import ContextData

logger = logging.getLogger("api")


def get_context(db: Session, layer_id: str):
    return db.query(ContextData).filter(ContextData.context_id == layer_id).one_or_none()


def get_contexts(db: Session, layer_ids: List[str]):
    return db.query(ContextData).filter(ContextData.context_id.in_(layer_ids)).all()

