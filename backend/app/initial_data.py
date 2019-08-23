import logging
import os
import json
from app.db.session import db_session
from app.hydat.factory import StationFactory
# from app.metadata.db_models import DataMart, DataFormatType, MapLayer, MapLayerType, ContextData

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
    files = ['DataMart.json', "DataFormatType.json", 'MapLayerType.json', 'MapLayer.json']
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
                instances.append(cls(**obj))

            db_session.add_all(instances)
        else:
            logger.info(f"Skipping: {filename} already imported")

    logger.info("Loading Fixtures Complete")
    db_session.commit()


def load_contexts():
    directory = '/app/contexts/'
    logger = logging.getLogger("contexts")
    logger.info("Merging Contexts")

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename)) as json_file:
                logger.info(f"Merging Context: {filename}")
                data = json.load(json_file)
                logger.info(data)
                # context_obj = ContextData(**data)
                # db_session.merge(context_obj)

    logger.info("Merging Contexts Complete")
    db_session.commit()


def main():
    # just another failsafe to prevent fixture data in production
    env = os.getenv('WALLY_ENV')
    if env == 'PROD' or env == 'PRODUCTION':
        logger.error(f"Skipping fixture data due to environment ({env})")
        return

    logger.info("Creating initial fixture data")
    # load_fixtures()
    # create_hydat_data()
    # load_contexts()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
