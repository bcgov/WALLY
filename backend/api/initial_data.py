import logging
import os
import json
from shapely.geometry import shape
import shapely.geometry
from api.db.session import db_session
from api.minio.client import s3_upload_file
from api.v1.hydat.db_models import Station
# Need imports from api.layers even though linter says they are unused
from api.layers.water_rights_licences import WaterRightsLicenses
from api.layers.water_rights_applications import WaterRightsApplications
from api.layers.automated_snow_weather_station_locations import AutomatedSnowWeatherStationLocations
from api.layers.bc_wildfire_active_weather_stations import BcWildfireActiveWeatherStations
from api.layers.cadastral import Cadastral
from api.layers.critical_habitat_species_at_risk import CriticalHabitatSpeciesAtRisk
from api.layers.freshwater_atlas_stream_directions import FreshwaterAtlasStreamDirections
from api.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds
from api.layers.ground_water_wells import GroundWaterWells
from api.layers.bc_major_watersheds import BcMajorWatersheds
from api.layers.ecocat_water_related_reports import EcocatWaterRelatedReports
from api.layers.ground_water_aquifers import GroundWaterAquifers
from api.layers.water_allocation_restrictions import WaterAllocationRestrictions
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.layers.first_nations import CommunityLocations, TreatyAreas, TreatyLands
from api.layers.normal_annual_runoff_isolines import NormalAnnualRunoffIsolines


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_hydat_data():
    """generate stream station and flow/level data"""
    logger = logging.getLogger("hydat")

    q = """select * from fasstr.fasstr_flows limit 1"""
    if db_session.execute(q).fetchone() is not None:
        # fasstr_flows table already has data.
        logger.info("FASSTR fasstr_flows table already contains data")
        return

    directory = '/app/fixtures/layer_subsets/hydat/'
    with open(os.path.join(directory, "hydat.sql"), "r") as sql_file:
        sql = sql_file.read()
    db_session.execute(sql)
    db_session.commit()
    logger.info("FASSTR data loaded")


def load_dev_raster_data():
    """ load raster data for dev envs """
    directory = '/app/fixtures/raster/'
    for filename in os.listdir(directory):
        if filename.endswith(".tif"):
            s3_upload_file(filename, os.path.join(directory, filename), "image/geotiff", "raster")


def load_dev_data():
    directory = '/app/fixtures/layer_subsets/'

    for filename in os.listdir(directory):
        if filename.endswith(".geojson"):
            with open(os.path.join(directory, filename)) as json_file:
                data = json.load(json_file)

                # Get class name from file name
                file = os.path.splitext(filename)[0]
                cls = globals()[file]

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

                        # remove values that can't be handled in this script.
                        params.pop('GEOMETRY.AREA', None)
                        params.pop('GEOMETRY.LEN', None)

                        instance = cls(**params)
                        instances.append(instance)

                    db_session.add_all(instances)
                else:
                    logger.info(
                        f"Skipping Subset: {filename} data already exists")

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
    load_dev_raster_data()
    logger.info("Raster data loaded")

    logger.info(
        "refreshing materialized views (cached list of features and locations)")


if __name__ == "__main__":
    main()
