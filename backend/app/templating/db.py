"""
Database queries for aggregating data from WMS layers and APIs
"""
from sqlalchemy.orm import Session
from typing import List
import logging
from app.metadata.db_models import DisplayTemplate, DisplayCatalogue, DisplayTemplateDisplayCatalogueXref, \
    ChartComponent, FormulaComponent, ImageComponent, LinkComponent

logger = logging.getLogger("template_builder")


def get_display_templates(db: Session, display_data_names: List[str]):
    """ Returns all display templates that are associated
    with the display catalogue with matching data_name """
    templates = db.query(DisplayTemplate).join(DisplayCatalogue)\
        .filter(DisplayCatalogue.display_data_name.in_(display_data_names))\
        .all().distinct(DisplayTemplate.display_template_id)

    # if catalogue_entries is not None:
    #     for entry in catalogue_entries:
    #         display_templates = []
    #
    #         templates = catalogue_entry.display_templates

    if templates is not None:
        display_templates = []

        for template in templates:
            charts = db.query(ChartComponent).filter(display_template_id=template.id).all()
            links = db.query(LinkComponent).filter(display_template_id=template.id).all()
            images = db.query(ImageComponent).filter(display_template_id=template.id).all()
            formulas = db.query(FormulaComponent).filter(display_template_id=template.id).all()

            template_info = {
                "template": template,
                "charts": charts,
                "links": links,
                "images": images,
                "formulas": formulas
            }
            display_templates.append(template_info)

        return display_templates
    else:
        return []
