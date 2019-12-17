import logging
import os
import json
import datetime
from api.db.session import db_session
from api.metadata.db_models import DisplayTemplate, ChartComponent, LinkComponent, ImageComponent, FormulaComponent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def merge_display_templates():
    directory = '/app/display_templates/'

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename)) as json_file:
                logger.info(f"Merging Template: {filename}")
                data = json.load(json_file)

                # Merge any changes to display template components into database
                # Updates the audit loggi ng information with current dates
                db_session.merge(DisplayTemplate(
                    **{**data["display_template"], **get_audit_fields()}))
                [db_session.merge(ChartComponent(
                    **{**chart, **get_audit_fields()})) for chart in data["charts"]]
                [db_session.merge(LinkComponent(
                    **{**link, **get_audit_fields()})) for link in data["links"]]
                [db_session.merge(ImageComponent(
                    **{**image, **get_audit_fields()})) for image in data["images"]]
                [db_session.merge(FormulaComponent(**{**formula,
                                                      **get_audit_fields()})) for formula in data["formulas"]]

    logger.info("Merging Display Templates Complete")
    db_session.commit()


def get_audit_fields():
    current_date = datetime.datetime.now()
    return {
        "create_user": "ETL_USER",
        "create_date": current_date,
        "update_user": "ETL_USER",
        "update_date": current_date,
        "effective_date": current_date,
        "expiry_date": "9999-12-31T23:59:59Z"
    }


def main():
    logger.info("Merging display templates")
    merge_display_templates()
    logger.info("Display templates merging complete")


if __name__ == "__main__":
    main()
