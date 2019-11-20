import logging
import os
import json
from shapely.geometry import shape
import shapely.geometry
from app.db.session import db_session

from app.hydat.factory import StationFactory
from app.layers.water_rights_licences import WaterRightsLicenses
from app.layers.water_rights_applications import WaterRightsApplications
from app.layers.automated_snow_weather_station_locations import AutomatedSnowWeatherStationLocations
from app.layers.bc_wildfire_active_weather_stations import BcWildfireActiveWeatherStations
from app.layers.cadastral import Cadastral
from app.layers.critical_habitat_species_at_risk import CriticalHabitatSpeciesAtRisk
from app.layers.freshwater_atlas_stream_directions import FreshwaterAtlasStreamDirections
from app.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds
from app.layers.ground_water_wells import GroundWaterWells
from app.layers.bc_major_watersheds import BcMajorWatersheds
from app.layers.ecocat_water_related_reports import EcocatWaterRelatedReports
from app.layers.ground_water_aquifers import GroundWaterAquifers
from app.layers.water_allocation_restrictions import WaterAllocationRestrictions
from app.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_hydat_data():
    """generate stream station and flow/level data"""

    # logger
    logger = logging.getLogger("hydat")
    logger.info("Stream Stations")
    stations = StationFactory.create_batch(3)
    for stn in stations:
        logger.info(
            f"Adding stream station {stn.station_number} - {stn.station_name}")
        db_session.add(stn)
    db_session.commit()


def load_dev_data():
    directory = '/app/fixtures/layer_subsets/'

    for filename in os.listdir(directory):
        if filename.endswith(".geojson"):
            with open(os.path.join(directory, filename)) as json_file:
                data = json.load(json_file)

                # Get class name from file name
                file = os.path.splitext(filename)[0]
                cls = globals()[file]  # Need imports from app.layers even though linter says they are unused

                # Only add subset fixture if no data exists in table
                if db_session.query(cls).first() is None:
                    logger.info(f"Loading Subset: {filename}")

                    # Create class instances
                    instances = []
                    for feature in data["features"]:
                        params = {**feature["properties"]}
                        geom = shape(feature["geometry"]).wkt
                        geom_field = 'SHAPE' if cls.shape_column_exists() else 'GEOMETRY'
                        params[geom_field] = 'SRID=4326;' + geom
                        # str "None" is not compatible with field types other than str
                        # so we replace with proper None here
                        for k, v in params.items():
                            if v == "None":
                                params[k] = None
                        instance = cls(**params)
                        instances.append(instance)

                    db_session.add_all(instances)
                else:
                    logger.info(f"Skipping Subset: {filename} data already exists")

    logger.info("Subset Data Load - Complete")
    db_session.commit()


def refresh_geocoder_view():
    db_session.execute("refresh materialized view geocode_lookup")
    db_session.commit()


def main():
    # just another failsafe to prevent fixture data in production
    env = os.getenv('WALLY_ENV')
    if env == 'PROD' or env == 'PRODUCTION':
        logger.error(f"Skipping fixture data due to environment ({env})")
        return

    logger.info("Creating initial fixture data")
    create_hydat_data()
    load_dev_data()
    logger.info("Initial data created")

    logger.info(
        "refreshing materialized views (cached list of features and locations)")
    refresh_geocoder_view()


if __name__ == "__main__":
    main()
