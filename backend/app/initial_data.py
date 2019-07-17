import logging

from app.db.session import db_session
from app.stream_levels.factory import StationFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    # generate stream station and flow/level data
    stn = StationFactory()

    db_session.add(stn)
    db_session.commit()
    pass


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
