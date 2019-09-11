"""add layer catalogue data

Revision ID: db674c5861c7
Revises: fc2537bad3fa
Create Date: 2019-09-11 15:34:58.155423

"""
import logging
import os
import json
import datetime
from app.db.session import db_session
from app.metadata.db_models import ApiCatalogue, WmsCatalogue, DataFormatCode, ComponentTypeCode, \
    DisplayCatalogue, VectorCatalogue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# revision identifiers, used by Alembic.
revision = 'db674c5861c7'
down_revision = 'fc2537bad3fa'
branch_labels = None
depends_on = None


def upgrade():
    # User file array to ensure loading order
    # File names must match class names for globals() to work
    files = ['ApiCatalogue.json', "WmsCatalogue.json", 'DisplayCatalogue.json',
             "DataFormatCode.json", "ComponentTypeCode.json", "VectorCatalogue.json"]
    directory = '/app/fixtures/'

    logger.info("Loading Initial Catalogue Information")

    for filename in files:
        with open(os.path.join(directory, filename)) as json_file:
            data = json.load(json_file)

        # Get class name from file name
        file = os.path.splitext(filename)[0]
        # Need imports at top even though linter says they are unused
        cls = globals()[file]

        logger.info(f"Loading Fixture: {filename}")
        # Create class instances
        instances = []
        for obj in data:
            logger.info(f"Object: {obj}")
            instance = cls(**{**obj, **get_audit_fields()})
            instances.append(instance)

        db_session.add_all(instances)

    logger.info("Loading Fixtures Complete")
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


def downgrade():
    pass
