"""stream stations

Revision ID: 88f4ca055ae7
Revises: 4375f087337e
Create Date: 2019-07-15 16:27:54.990523

"""
from alembic import op
from sqlalchemy import Column, String, Integer, ForeignKey
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

    op.create_table(
        'dly_levels',
        Column('station_number', String, ForeignKey(
            'stations.station_number'), primary_key=True),
        Column('year', Integer, primary_key=True),
        Column('month', Integer, primary_key=True),
        Column('full_month', Integer),
        Column('no_days', Integer),
        Column('precision_code', Integer),
        Column('monthly_mean', DOUBLE_PRECISION),
        Column('monthly_total', DOUBLE_PRECISION),
        Column('min', DOUBLE_PRECISION),
        Column('max', DOUBLE_PRECISION),
    )

    op.create_table(
        'dly_flows',
        Column('station_number', String, ForeignKey(
            'stations.station_number'), primary_key=True),
        Column('year', Integer, primary_key=True),
        Column('month', Integer, primary_key=True),
        Column('full_month', Integer),
        Column('no_days', Integer),
        Column('monthly_mean', DOUBLE_PRECISION),
        Column('monthly_total', DOUBLE_PRECISION),
        Column('min', DOUBLE_PRECISION),
        Column('max', DOUBLE_PRECISION),
    )


def downgrade():
    pass
