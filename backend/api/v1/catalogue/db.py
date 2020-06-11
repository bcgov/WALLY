"""
Database tables and data access functions for Wally Data Layer Meta Information
"""
from sqlalchemy import or_
from sqlalchemy.orm import Session, load_only
from api.v1.catalogue.db_models import (
    DisplayCatalogue,
    DisplayTemplate,
    DataSource,
    WmsCatalogue,
    LayerCategory,
    ApiCatalogue,
    VectorCatalogue)
import itertools
import operator
from logging import getLogger
from sqlalchemy.orm import joinedload, subqueryload

logger = getLogger("api")


def get_display_catalogue(db: Session):
    """ Get all supported catalogue layers"""
    wms_query = db.query(
        DisplayCatalogue.display_name,
        DisplayCatalogue.display_data_name,
        DisplayCatalogue.highlight_columns,
        DisplayCatalogue.label,
        DisplayCatalogue.label_column,
        DataSource.name,
        DataSource.description,
        DataSource.source_url,
        LayerCategory.display_order,
        DisplayCatalogue.layer_category_code,
        DisplayCatalogue.use_wms,
        WmsCatalogue.wms_name,
        WmsCatalogue.wms_style,)

    wms_result = wms_query.join(WmsCatalogue).join(LayerCategory).join(DataSource) \
        .filter(DisplayCatalogue.wms_catalogue_id == WmsCatalogue.wms_catalogue_id) \
        .filter(DisplayCatalogue.use_wms == True) \
        .all() \

    api_query = db.query(
        DisplayCatalogue.display_name,
        DisplayCatalogue.display_data_name,
        DisplayCatalogue.highlight_columns,
        DisplayCatalogue.layer_category_code,
        DisplayCatalogue.label,
        DisplayCatalogue.label_column,
        DataSource.name,
        DataSource.description,
        DataSource.source_url,
        LayerCategory.display_order,
        ApiCatalogue.url,)

    api_result = api_query.join(ApiCatalogue).join(LayerCategory).join(DataSource) \
        .filter(DisplayCatalogue.api_catalogue_id == ApiCatalogue.api_catalogue_id) \
        .all()

    vector_query = db.query(
        DisplayCatalogue.display_name,
        DisplayCatalogue.display_data_name,
        DisplayCatalogue.highlight_columns,
        DisplayCatalogue.layer_category_code,
        DisplayCatalogue.label,
        DisplayCatalogue.label_column,
        DataSource.name,
        DataSource.description,
        DataSource.source_url,
        LayerCategory.display_order,
        VectorCatalogue.vector_name,)

    vector_result = vector_query.join(VectorCatalogue).join(LayerCategory).join(DataSource) \
        .filter(DisplayCatalogue.vector_catalogue_id == VectorCatalogue.vector_catalogue_id) \
        .filter(DisplayCatalogue.use_wms == False) \
        .all()

    all_layers = wms_result + api_result + vector_result

    # Ideally, we would sort in the database, but because our tables have different columns
    # (for vector info, wms info etc.), we are using 3 queries.  As such, we sort them
    # after retrieving all 3 sets of layers. We could arguably consolidate the WMS, API and
    # VectorCatalogue tables and that would allow us to use an ORDER BY clause.
    return sorted(all_layers, key=operator.attrgetter('display_order', 'display_name'))


def get_layer_categories(db: Session):
    """ returns layer categories from the database """
    return db.query(LayerCategory).order_by(LayerCategory.display_order).all()


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
