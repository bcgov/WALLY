import logging
import os
import json
import datetime
from app.db.session import db_session
from app.hydat.factory import StationFactory
from app.metadata.db_models import ApiCatalogue, WmsCatalogue, DataFormatCode, ComponentTypeCode, \
    DisplayCatalogue, DisplayTemplate, ChartComponent, LinkComponent, ImageComponent, FormulaComponent, \
    DisplayTemplateDisplayCatalogueXref, VectorCatalogue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_hydat_data():
    """generate stream station and flow/level data"""

    # logger
    logger = logging.getLogger("hydat")
    logger.info("Stream Stations")
    stations = StationFactory.create_batch(3)
    for stn in stations:
        logger.info(f"Adding stream station {stn.station_number} - {stn.station_name}")
        db_session.add(stn)
    db_session.commit()


def load_fixtures():
    # User file array to ensure loading order
    # File names must match class names for globals() to work
    files = ['ApiCatalogue.json', "WmsCatalogue.json", 'DisplayCatalogue.json',
             "DataFormatCode.json",  "ComponentTypeCode.json", "VectorCatalogue.json"]
    directory = '/app/fixtures/'

    logger = logging.getLogger("metadata")
    logger.info("Loading Fixtures")

    for filename in files:
        with open(os.path.join(directory, filename)) as json_file:
            data = json.load(json_file)

        # Get class name from file name
        file = os.path.splitext(filename)[0]
        cls = globals()[file]  # Need imports at top even though linter says they are unused

        # Only add fixtures is no data exists in table
        if db_session.query(cls).first() is None:
            logger.info(f"Loading Fixture: {filename}")
            # Create class instances
            instances = []
            for obj in data:
                logger.info(f"Object: {obj}")
                instance = cls(**{**obj, **get_audit_fields()})
                instances.append(instance)

            db_session.add_all(instances)
        else:
            logger.info(f"Skipping: {filename} already imported")

    logger.info("Loading Fixtures Complete")
    db_session.commit()


def load_display_templates():
    directory = '/app/display_templates/'
    logger = logging.getLogger("display_templates")
    logger.info("Merging Display Templates")

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename)) as json_file:
                logger.info(f"Merging Template: {filename}")
                data = json.load(json_file)
                logger.info(data)

                # Merge any changes to display template components into database
                # Updates the audit logging information with current dates
                db_session.merge(DisplayTemplate(**{**data["display_template"], **get_audit_fields()}))
                [db_session.merge(ChartComponent(**{**chart, **get_audit_fields()})) for chart in data["charts"]]
                [db_session.merge(LinkComponent(**{**link, **get_audit_fields()})) for link in data["links"]]
                [db_session.merge(ImageComponent(**{**image, **get_audit_fields()})) for image in data["images"]]
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
    # just another failsafe to prevent fixture data in production
    env = os.getenv('WALLY_ENV')
    if env == 'PROD' or env == 'PRODUCTION':
        logger.error(f"Skipping fixture data due to environment ({env})")
        return

    logger.info("Creating initial fixture data")
    load_fixtures()
    create_hydat_data()
    load_display_templates()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
