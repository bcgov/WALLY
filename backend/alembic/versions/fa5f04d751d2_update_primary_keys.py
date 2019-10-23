"""update primary keys

Revision ID: fa5f04d751d2
Revises: 30d75d8eb63d
Create Date: 2019-10-22 14:40:05.892774

"""
from alembic import op
from sqlalchemy import Integer

# revision identifiers, used by Alembic.
revision = 'fa5f04d751d2'
down_revision = '30d75d8eb63d'
branch_labels = None
depends_on = None


def upgrade():
    # op.drop_constraint('PRIMARY', 'ecocat_water_related_reports', type_='primary')
    op.execute('ALTER TABLE ecocat_water_related_reports DROP CONSTRAINT ecocat_water_related_reports_pkey CASCADE')
    op.create_primary_key('ecocat_water_related_reports_pkey', 'ecocat_water_related_reports', ['REPORT_ID'])
    
    op.alter_column('automated_snow_weather_station_locations', 'SNOW_ASWS_STN_ID', _type=Integer)
    op.alter_column('bc_major_watersheds', 'OBJECTID', _type=Integer)
    op.alter_column('bc_wildfire_active_weather_stations', 'WEATHER_STATIONS_ID', _type=Integer)
    op.alter_column('cadastral', 'PARCEL_FABRIC_POLY_ID', _type=Integer)
    op.alter_column('critical_habitat_species_at_risk', 'CRITICAL_HABITAT_ID', _type=Integer)
    op.alter_column('ecocat_water_related_reports', 'REPORT_ID', _type=Integer)
    op.alter_column('freshwater_atlas_stream_directions', 'OBJECTID', _type=Integer)
    op.alter_column('freshwater_atlas_watersheds', 'WATERSHED_FEATURE_ID', _type=Integer)
    op.alter_column('ground_water_aquifers', 'AQ_TAG', _type=Integer)
    op.alter_column('ground_water_wells', 'WELL_TAG_NO', _type=Integer)
    op.alter_column('water_allocation_restrictions', 'OBJECTID', _type=Integer)
    op.alter_column('water_rights_licenses', 'WLS_WRL_SYSID', _type=Integer)
    op.alter_column('hydat.stations', 'station_number', _type=Integer)
    

def downgrade():
    pass
