"""
Database tables and data access functions for Wally Data Layer Meta Information
"""
from sqlalchemy.orm import Session
from app.data.db_models import WmsLayer, ApiLayer, DataSource


def get_wms_layers(db: Session):
    """ Get all supported wms layers"""
    return db.query(WmsLayer).all()


def get_wms_layer_columns(db: Session, id: int):
    """ Get wms layer highlight columns"""
    return db.query()


def get_api_layers(db: Session):
    """ Get all supported api layers"""
    return db.query(ApiLayer).all()


def get_data_sources(db: Session):
    """ Get all data marts"""
    return db.query(DataSource).all()

def get_context(db: Session):
    return db.query