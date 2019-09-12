"""
Database queries for aggregating data from WMS layers and APIs
"""
from sqlalchemy.orm import Session
from typing import List
import logging
from app.metadata.db_models import DisplayCatalogue, ApiCatalogue, WmsCatalogue
from sqlalchemy.orm import joinedload

logger = logging.getLogger("api")


def get_display_catalogue(db: Session, display_data_names: List[str]):
    q = db.query(DisplayCatalogue).options(joinedload(DisplayCatalogue.wms_catalogue),
                                           joinedload(
                                               DisplayCatalogue.api_catalogue),
                                           joinedload(DisplayCatalogue.vector_catalogue))\
        .filter(DisplayCatalogue.display_data_name.in_(display_data_names))\
        .all()
    # [logger.info(vars(x)) for x in q]
    return q
