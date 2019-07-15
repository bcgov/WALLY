"""stream stations

Revision ID: 88f4ca055ae7
Revises: 4375f087337e
Create Date: 2019-07-15 16:27:54.990523

"""
from alembic import op
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

# revision identifiers, used by Alembic.
revision = '88f4ca055ae7'
down_revision = '4375f087337e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stations',
        Column('station_number', String, primary_key=True),
        Column('station_name', String),
        Column('prov_terr_state_loc', String),
        Column('regional_office_id', String),
        Column('hyd_status', String),
        Column('sed_status', String),
        Column('latitude', DOUBLE_PRECISION),
        Column('longitude', DOUBLE_PRECISION),
        Column('drainage_area_gross', DOUBLE_PRECISION),
        Column('drainage_area_effect', DOUBLE_PRECISION),
        Column('rhbn', Integer),
        Column('real_time', Integer),
        Column('sed_status', Integer),
    )


def downgrade():
    pass
