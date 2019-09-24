"""
Database queries for aggregating data from WMS layers and APIs
"""
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_
import logging
from app.metadata.db_models import DisplayTemplate, DisplayCatalogue, DisplayTemplateDisplayCatalogueXref, \
    ChartComponent, FormulaComponent, ImageComponent, LinkComponent
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR


logger = logging.getLogger("template_builder")


def get_display_templates(db: Session, display_data_names: List[str]):
    """ Returns all display templates that are associated
    with the display catalogue with matching data_name """
    templates = db.query(DisplayTemplate) \
        .filter(or_(*[DisplayTemplate.display_data_names == [name] for name in display_data_names]))\
        .all()

    # TODO Update query to handle multi-layer template requests, with below code starter
    # if len(display_data_names) > 1:
    #     multi_templates = db.query(DisplayTemplate) \
    #         .filter(display_data_names DisplayTemplate.display_data_names ()).all()
    #     templates.append(multi_templates)
    #     logger.info(multi_templates)

    # logger.info(templates)

    if templates is not None:
        display_templates = []

        for template in templates:
            charts = db.query(ChartComponent)\
                .filter(ChartComponent.display_template_id == template.display_template_id).all()
            links = db.query(LinkComponent)\
                .filter(LinkComponent.display_template_id == template.display_template_id).all()
            images = db.query(ImageComponent)\
                .filter(ImageComponent.display_template_id == template.display_template_id).all()
            formulas = db.query(FormulaComponent)\
                .filter(FormulaComponent.display_template_id == template.display_template_id).all()

            template_info = {
                "display_template": template,
                "charts": charts,
                "links": links,
                "images": images,
                "formulas": formulas
            }
            display_templates.append(template_info)

        # logger.info(display_templates)
        return display_templates
    else:
        return []
