import logging

from app.db.session import db_session
from app.stream_levels.factory import StationFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_stream_levels_data():
    """generate stream station and flow/level data"""

    # logger
    logger = logging.getLogger("stream_levels")
    stations = StationFactory.create_batch(3)
    for stn in stations:
        logger.info(f"Adding stream station {stn.station_number} - {stn.station_name}")
        db_session.add(stn)
    db_session.commit()


def main():
    logger.info("Creating initial data")
    create_stream_levels_data()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
