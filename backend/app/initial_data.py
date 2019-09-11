import logging
import os
from app.db.session import db_session
from app.hydat.factory import StationFactory
from app.layers.parcel_factory import ParcelFactory

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


def create_parcels():
    # logger
    logger = logging.getLogger("fixtures")
    logger.info("Adding parcels")
    parcels = ParcelFactory.create_batch(5)
    for par in parcels:
        logger.info(
            f"Adding parcel {par.PARCEL_NAME}")
        db_session.add(par)
    db_session.commit()


def refresh_geocoder_view():
    db_session.execute("refresh materialized view geocode_lookup")


def main():
    # just another failsafe to prevent fixture data in production
    env = os.getenv('WALLY_ENV')
    if env == 'PROD' or env == 'PRODUCTION':
        logger.error(f"Skipping fixture data due to environment ({env})")
        return

    logger.info("Creating initial fixture data")
    create_hydat_data()
    create_parcels()
    logger.info("Initial data created")

    logger.info(
        "refreshing materialized views (cached list of features and locations)")
    refresh_geocoder_view()


if __name__ == "__main__":
    main()
