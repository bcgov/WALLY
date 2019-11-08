"""add_layer_catalogue_cols

Revision ID: 5be35dfffc00
Revises: ab7b5daedfbd
Create Date: 2019-11-01 17:16:31.388055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

# revision identifiers, used by Alembic.
revision = '5be35dfffc00'
down_revision = 'ab7b5daedfbd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

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

    op.add_column('data_source',
                  sa.Column('source_object_id', sa.String, nullable=True,
                            comment='The ID on the upstream data source. This is specifically required for paging through the DataBC API. Note: do not rely on these IDs as permanent keys, only for sorting and paginating during queries (e.g. `sortBy=WLS_WRL_SYSID&startIndex=1000`)'))

    op.add_column('display_catalogue',
                  sa.Column('required_map_properties', ARRAY(TEXT), nullable=False, server_default="{}", comment='Properties that are required by the map for rendering markers/shapes, e.g. for colouring markers based on a value or property like POD_SUBTYPE'))
    op.add_column('display_catalogue',
                  sa.Column('mapbox_layer_id', sa.String, nullable=False, comment='The mapbox tileset ID used to upload and replace layer data via the mapbox api.'))

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

    op.execute("""
        UPDATE data_source AS ds SET source_object_id = CASE
        WHEN ds.data_source_id = 1  THEN 'SNOW_ASWS_STN_ID'
        WHEN ds.data_source_id = 2  THEN NULL
        WHEN ds.data_source_id = 3  THEN 'WTHR_STTNS'
        WHEN ds.data_source_id = 4  THEN 'PARCEL_FABRIC_POLY_ID'
        WHEN ds.data_source_id = 5  THEN 'CRITICAL_HABITAT_ID'
        WHEN ds.data_source_id = 6  THEN 'REPORT_ID'
        WHEN ds.data_source_id = 7  THEN NULL
        WHEN ds.data_source_id = 8  THEN NULL
        WHEN ds.data_source_id = 9  THEN 'AQ_TAG'
        WHEN ds.data_source_id = 10 THEN 'WELL_TAG_NO'
        WHEN ds.data_source_id = 11 THEN 'LINEAR_FEATURE_ID'
        WHEN ds.data_source_id = 12 THEN 'WLS_WRL_SYSID'
        WHEN ds.data_source_id = 13 THEN NULL
        ELSE NULL
        END
    """)

    # initial data for required_map_properties
    # these are the fields that we need for coloring markers on the map based on properties of the features
    op.execute("""
        UPDATE display_catalogue AS dc SET required_map_properties = CASE
            WHEN dc.display_data_name = 'water_rights_licences' THEN ARRAY['POD_SUBTYPE']
            WHEN dc.display_data_name = 'freshwater_atlas_stream_directions' THEN ARRAY['DOWNSTREAM_DIRECTION']
            WHEN dc.display_data_name = 'water_allocation_restrictions' THEN ARRAY['PRIMARY_RESTRICTION_CODE']
            ELSE ARRAY[]::text[]
        END
    """)

    # initial data for mapbox_layer_id's
    # these are the id's used to know which layers to replace in mapbox
    op.execute("""
        UPDATE display_catalogue AS dc SET mapbox_layer_id = CASE
            WHEN ds.display_data_name = 'automated_snow_weather_station_locations' THEN 'iit-water.2svbut5f'
            WHEN ds.display_data_name = 'bc_major_watersheds' THEN 'iit-water.0tsq064k'
            WHEN ds.display_data_name = 'bc_wildfire_active_weather_stations' THEN 'iit-water.2svbut5f'
            WHEN ds.display_data_name = 'cadastral' THEN 'iit-water.36r1x37x'
            WHEN ds.display_data_name = 'critical_habitat_species_at_risk' THEN 'iit-water.0tsq064k'
            WHEN ds.display_data_name = 'ecocat_water_related_reports' THEN 'iit-water.2svbut5f'
            WHEN ds.display_data_name = 'freshwater_atlas_stream_directions' THEN 'iit-water.7iwr3fo1'
            WHEN ds.display_data_name = 'freshwater_atlas_watersheds' THEN 'iit-water.7iwr3fo1'
            WHEN ds.display_data_name = 'ground_water_aquifers' THEN 'iit-water.0tsq064k'
            WHEN ds.display_data_name = 'groundwater_wells' THEN 'iit-water.2svbut5f'
            WHEN ds.display_data_name = 'water_allocation_restrictions' THEN 'iit-water.2ah76e1a'
            WHEN ds.display_data_name = 'water_rights_licenses' THEN 'iit-water.2svbut5f'
            WHEN ds.display_data_name = 'hydat.stations' THEN 'iit-water.2svbut5f'
            ELSE ''
        END
    """)

    op.alter_column('data_source', 'data_table_name', nullable=False)
    op.alter_column('data_source', 'source_object_name', nullable=False)
    op.execute('SET search_path TO public')


def downgrade():
    return
