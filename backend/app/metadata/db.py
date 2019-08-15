"""
Database tables and data access functions for Wally Data Layer Meta Information
"""
from sqlalchemy.orm import Session, load_only
from app.metadata.db_models import ContextData, DataSource, MapLayer, DataMart
import itertools


def get_map_layers(db: Session):
    """ Get all supported map layers"""
    return db.query(MapLayer).all()


def get_highlight_columns(db: Session, context_id: str):
    """ Get highlight columns for a map layer"""
    return db.query(ContextData).\
        filter(context_id=context_id).\
        options(load_only("highlight_fields")).\
        one_or_none()


def get_data_sources(db: Session):
    """ Get all data marts"""
    return db.query(DataSource).all()


def get_context_data(layer_names, db: Session):
    """ Get data fixtures by concatenated layer names """
    permutations = list(itertools.permutations(layer_names))
    results = []
    for perm in permutations:
        results += db.query(ContextData).filter(ContextData.context_name == perm)

    return results
