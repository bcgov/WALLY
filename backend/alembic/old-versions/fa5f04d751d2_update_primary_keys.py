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
    # Ecocat's pk REPORT_POINT_ID was not unique so this changes it to REPORT_ID which is.
    op.execute('ALTER TABLE ecocat_water_related_reports DROP CONSTRAINT ecocat_water_related_reports_pkey CASCADE')
    op.create_primary_key('ecocat_water_related_reports_pkey', 'ecocat_water_related_reports', ['REPORT_ID'])
    
    # Change all Primary Key types from SERIAL to INTEGER to eliminate autoincrementing behaviour.
    op.execute('ALTER TABLE automated_snow_weather_station_locations ALTER COLUMN "SNOW_ASWS_STN_ID" TYPE INTEGER USING "SNOW_ASWS_STN_ID"::integer')
    op.execute('ALTER TABLE bc_major_watersheds ALTER COLUMN "OBJECTID" TYPE INTEGER USING "OBJECTID"::integer')
    op.execute('ALTER TABLE bc_wildfire_active_weather_stations ALTER COLUMN "WEATHER_STATIONS_ID" TYPE INTEGER USING "WEATHER_STATIONS_ID"::integer')
    op.execute('ALTER TABLE cadastral ALTER COLUMN "PARCEL_FABRIC_POLY_ID" TYPE INTEGER USING "PARCEL_FABRIC_POLY_ID"::integer')
    op.execute('ALTER TABLE critical_habitat_species_at_risk ALTER COLUMN "CRITICAL_HABITAT_ID" TYPE INTEGER USING "CRITICAL_HABITAT_ID"::integer')
    op.execute('ALTER TABLE ecocat_water_related_reports ALTER COLUMN "REPORT_ID" TYPE INTEGER USING "REPORT_ID"::integer')
    op.execute('ALTER TABLE freshwater_atlas_stream_directions ALTER COLUMN "OBJECTID" TYPE INTEGER USING "OBJECTID"::integer')
    op.execute('ALTER TABLE freshwater_atlas_watersheds ALTER COLUMN "WATERSHED_FEATURE_ID" TYPE INTEGER USING "WATERSHED_FEATURE_ID"::integer')
    # ground_water_aquifers has a String pk type so no need to alter
    # ground_water_wells has a String pk type so no need to alter
    op.execute('ALTER TABLE water_allocation_restrictions ALTER COLUMN "OBJECTID" TYPE INTEGER USING "OBJECTID"::integer')
    op.execute('ALTER TABLE water_rights_licenses ALTER COLUMN "WLS_WRL_SYSID" TYPE INTEGER USING "WLS_WRL_SYSID"::integer')
    # hydat.Station has a String pk type so no need to alter

def downgrade():
    pass
