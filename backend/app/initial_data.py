import logging
import os
import json
from app.db.session import db_session
from app.hydat.factory import StationFactory
from app.data.db_models import MapLayer, MapLayerType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_hydat_data():
    """generate stream station and flow/level data"""

    # logger
    logger = logging.getLogger("hydat")
    stations = StationFactory.create_batch(3)
    for stn in stations:
        logger.info(f"Adding stream station {stn.station_number} - {stn.station_name}")
        db_session.add(stn)
    db_session.commit()


def load_fixtures():
    # User file array to ensure loading order
    # File names must match class names for globals() to work
    files = ['MapLayerTypes.json', 'MapLayers.json']
    directory = os.path.dirname(__file__)

    for filename in files:
        with open(os.path.join(directory, filename)) as json_file:
            data = json.load(json_file)

        # Get class name from file name
        file = os.path.splitext(filename)[0]
        cls = globals()[file]

        # Create class instances
        instances = []
        for obj in data:
            instances.append(cls(**obj))

        db_session.add_all(instances)

    db_session.commit()

    # for filename in os.listdir(directory):
    #     if filename.endswith(".json"):
    #         with open(os.path.join(directory, filename)) as json_file:
    #             data = json.load(json_file)
    #
    #         # Get class name from file name
    #         file_name = os.path.splitext(filename)[0]
    #         cls = globals()[file_name]
    #
    #         # Create class instances
    #         instances = []
    #         for obj in data:
    #             instances.append(cls(**obj))
    #
    #         db_session.add_all(instances)
    # # Map Layer Types
    # with open('../fixtures/MapLayerTypes.json') as json_file:
    #     types = json.load(json_file)
    #
    # layer_types = []
    # for t in types:
    #     layer_types.append(MapLayerType(**t))
    #
    # db_session.add_all(layer_types)
    #
    # # Map Layers
    # with open('../fixtures/MapLayers.json') as json_file:
    #     layers = json.load(json_file)
    #
    # map_layers = []
    # for l in layers:
    #     map_layers.append(MapLayer(**l))
    #
    # db_session.add_all(map_layers)



def main():
    # just another failsafe to prevent fixture data in production
    env = os.getenv('WALLY_ENV')
    if env == 'PROD' or env == 'PRODUCTION':
        logger.error(f"Skipping fixture data due to environment ({env})")
        return

    logger.info("Creating initial fixture data")
    create_hydat_data()
    load_fixtures()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
