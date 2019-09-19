import logging
import os
from app.db.session import db_session
from app.hydat.factory import StationFactory

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
    logger.info("Initial data created")

    logger.info(
        "refreshing materialized views (cached list of features and locations)")
    refresh_geocoder_view()


if __name__ == "__main__":
    main()
