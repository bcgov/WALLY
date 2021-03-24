"""add dem schema

Revision ID: c82f8499050e
Revises: 7a154ea3f123
Create Date: 2021-03-16 12:34:20.205965

"""
import os
from alembic import op
import sqlalchemy as sa
from api.config import ENV_DEV, WALLY_ENV


# revision identifiers, used by Alembic.
revision = 'c82f8499050e'
down_revision = '7a154ea3f123'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema if not exists dem")

    if WALLY_ENV == ENV_DEV:
        op.execute("""
          CREATE TABLE dem.cdem ("rid" serial PRIMARY KEY,"rast" raster);
          """)
        
        dirname = os.path.dirname(__file__)
        sql_file = open(dirname + "/sql/cdem_dev.sql")
        cdem_insert_dev_data = sql_file.read()
        op.execute(cdem_insert_dev_data)
        
        op.execute("""
          CREATE INDEX ON dem.cdem USING gist (st_convexhull("rast"));
        """)


def downgrade():
    op.execute("drop schema dem")
