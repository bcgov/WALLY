"""
Database tables and data access functions for Wally Data Layer Meta Information
"""
from sqlalchemy.orm import Session
from app.meta.db_models import WmsLayer, ApiLayer, DataMart


def get_wms_layers(db: Session):
    """ Get all supported wms layers"""
    return db.query(WmsLayer).all()


def get_api_layers(db: Session):
    """ Get all supported api layers"""
    return db.query(ApiLayer).all()


def get_data_marts(db: Session):
    """ Get all data marts"""
    return db.query(DataMart).all()
