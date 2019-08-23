"""
Database queries for aggregating data from WMS layers and APIs
"""
from sqlalchemy.orm import Session
from typing import List
import logging
from app.metadata.db_models import DisplayTemplate, DisplayCatalogue, \
    ChartComponent, FormulaComponent, ImageComponent, LinkComponent

logger = logging.getLogger("template_builder")


def get_display_templates(db: Session, display_data_name: str):
    """ Returns all display templates that are associated
    with the display catalogue with matching data_name """
    catalogue_entry = db.query(DisplayCatalogue)\
        .filter(display_data_name= display_data_name).one_or_none()

    if catalogue_entry is not None:
        display_templates = []

        templates = catalogue_entry.display_templates

        for template in templates:
            
            result = db.query(DisplayTemplate).join(ChartComponent).join(FormulaComponent)\
                .join(ImageComponent).join(LinkComponent).get(template.display_template_id)

            display_templates.append(result)

        return display_templates
    else:
        return []
