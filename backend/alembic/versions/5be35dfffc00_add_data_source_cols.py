"""add_layer_catalogue_cols

Revision ID: 5be35dfffc00
Revises: ab7b5daedfbd
Create Date: 2019-11-01 17:16:31.388055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5be35dfffc00'
down_revision = 'ab7b5daedfbd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')
    op.execute('SET CONSTRAINTS ALL DEFERRED')

    # add foreign key column relating to data source
    op.add_column('data_source',
                  sa.Column('source_object_name', sa.String, nullable=True,
                            comment='The object name reference at the external data source.  This is used to lookup datasets on directories like DataBC, e.g. WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW'))
    op.add_column('data_source',
                  sa.Column('data_table_name', sa.String, nullable=True,
                            comment='The table name where data for a map layer is stored. Used to help ogr2ogr and pgloader reference the correct table when processing new map layer data.'))
    op.add_column('data_source',
                  sa.Column('last_updated_data', sa.DateTime, server_default=sa.text('make_timestamp(2019, 1, 1, 1, 1, 1)'), nullable=False,
                            comment='The date the data for this map layer was last updated in the database.'))
    op.add_column('data_source',
                  sa.Column('last_updated_tiles', sa.DateTime, server_default=sa.text('make_timestamp(2019, 1, 1, 1, 1, 1)'), nullable=False,
                            comment='The date the tiles for this map layer were last re-generated and made available on the tile server. Should be as close as possible to last_updated_data, but differences are expected due to tile processing times.'))
    op.add_column('data_source',
                  sa.Column('direct_link', sa.String, nullable=True,
                            comment='A direct link to download the dataset from the source, if available.'))

    op.execute("""
        UPDATE data_source AS ds SET source_object_name = CASE
        WHEN ds.data_source_id = 1  THEN 'WHSE_WATER_MANAGEMENT.SSL_SNOW_ASWS_STNS_SP'
        WHEN ds.data_source_id = 2  THEN 'WHSE_BASEMAPPING.BC_MAJOR_WATERSHEDS'
        WHEN ds.data_source_id = 3  THEN 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_WEATHER_STATIONS_SP'
        WHEN ds.data_source_id = 4  THEN 'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW'
        WHEN ds.data_source_id = 5  THEN 'WHSE_WILDLIFE_MANAGEMENT.WCP_CRITICAL_HABITAT_SP'
        WHEN ds.data_source_id = 6  THEN 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW'
        WHEN ds.data_source_id = 7  THEN 'WHSE_BASEMAPPING.FWA_STREAM_DIRECTIONS_SP'
        WHEN ds.data_source_id = 8  THEN 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY'
        WHEN ds.data_source_id = 9  THEN 'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW'
        WHEN ds.data_source_id = 10 THEN 'WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW'
        WHEN ds.data_source_id = 11 THEN 'WHSE_WATER_MANAGEMENT.WLS_STREAM_RESTRICTIONS_SP'
        WHEN ds.data_source_id = 12 THEN 'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV'
        WHEN ds.data_source_id = 13 THEN 'Hydat_sqlite3_20191016.zip'
        ELSE NULL
        END
    """)

    op.execute("""
        UPDATE data_source AS ds SET data_table_name = CASE
        WHEN ds.data_source_id = 1  THEN 'automated_snow_weather_station_locations'
        WHEN ds.data_source_id = 2  THEN 'bc_major_watersheds'
        WHEN ds.data_source_id = 3  THEN 'bc_wildfire_active_weather_stations'
        WHEN ds.data_source_id = 4  THEN 'cadastral'
        WHEN ds.data_source_id = 5  THEN 'critical_habitat_species_at_risk'
        WHEN ds.data_source_id = 6  THEN 'ecocat_water_related_reports'
        WHEN ds.data_source_id = 7  THEN 'freshwater_atlas_stream_directions'
        WHEN ds.data_source_id = 8  THEN 'freshwater_atlas_watersheds'
        WHEN ds.data_source_id = 9  THEN 'ground_water_aquifers'
        WHEN ds.data_source_id = 10 THEN 'ground_water_wells'
        WHEN ds.data_source_id = 11 THEN 'water_allocation_restrictions'
        WHEN ds.data_source_id = 12 THEN 'water_rights_licenses'
        WHEN ds.data_source_id = 13 THEN 'hydat.stations'
        ELSE NULL
        END

    """)

    op.alter_column('data_source', 'data_table_name', nullable=False)
    op.alter_column('data_source', 'source_object_name', nullable=False)
    op.execute('SET search_path TO public')


def downgrade():
    return
