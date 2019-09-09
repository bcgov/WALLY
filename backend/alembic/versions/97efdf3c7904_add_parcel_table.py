"""add parcel table

Revision ID: 97efdf3c7904
Revises: 4afd09e628a3
Create Date: 2019-09-09 05:57:24.518281

"""
from geoalchemy2 import Geometry
from sqlalchemy import Column, Text, BigInteger
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '97efdf3c7904'
down_revision = '4afd09e628a3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "parcel",
        Column("geom", Geometry('MULTIPOLYGON', 4326)),
        Column("PARCEL_FABRIC_POLY_ID", BigInteger),
        Column("PIN", BigInteger),
        Column("PID", BigInteger),
        Column("PARCEL_NAME", BigInteger),
        Column("PLAN_NUMBER", BigInteger)
    )


def downgrade():
    return
