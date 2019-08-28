"""
Database tables and data access functions for Wally Data Layer Meta Information
"""
from sqlalchemy.orm import Session, load_only
from app.metadata.db_models import DisplayCatalogue, DisplayTemplate, DataSource
import itertools
from logging import getLogger
from sqlalchemy.orm import joinedload

logger = getLogger("api")


def get_display_catalogue(db: Session):
    """ Get all supported catalogue layers"""
    q = db.query(DisplayCatalogue).options(joinedload(DisplayCatalogue.wms_catalogue),
                                           joinedload(DisplayCatalogue.api_catalogue))
                                           .all()
    return db.query(DisplayCatalogue).all()


def get_highlight_columns(db: Session, display_data_name: str):
    """ Get highlight columns for a catalogue layer"""
    return db.query(DisplayCatalogue).\
        filter(display_data_name=display_data_name).\
        options(load_only("highlight_fields")).\
        one_or_none()


def get_data_sources(db: Session):
    """ Get all data sources"""
    return db.query(DataSource).all()


def get_display_components(db: Session, display_data_name):
    """ Get display template data by display_data_name """

    catalogue = db.query(DisplayCatalogue)\
        .filter(display_data_name=display_data_name)\
        .one_or_none()

    if catalogue is not None:
        catalogue.display_components




# def get_context_data(layer_names, db: Session):
#     """ Get data fixtures by concatenated layer names """
#     permutations = list(itertools.permutations(layer_names))
#     results = []
#     for perm in permutations:
#         logger.info(perm)
#         results += db.query(ContextData).filter(ContextData.context_id == perm)
#
#     return results
