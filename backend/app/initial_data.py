import logging

from app.db.session import db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    # use the db_session to populate fixture data
    pass


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
