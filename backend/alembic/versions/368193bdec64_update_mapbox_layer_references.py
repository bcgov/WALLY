"""update mapbox layer references

Revision ID: 368193bdec64
Revises: cc99f17203c7
Create Date: 2020-05-01 09:00:32.398315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '368193bdec64'
down_revision = 'cc99f17203c7'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    op.execute("""
           UPDATE display_catalogue SET required_map_properties = ARRAY['APPROVAL_STATUS'] WHERE display_data_name = 'water_approval_points';
           UPDATE display_catalogue SET required_map_properties = ARRAY['LIFE_STAGE', 'SPECIES_NAME'] WHERE display_data_name = 'fish_observations';
           UPDATE display_catalogue SET required_map_properties = ARRAY['DOWNSTREAM_ROUTE_MEASURE', 'FWA_WATERSHED_CODE', 'LINEAR_FEATURE_ID', 'LOCAL_WATERSHED_CODE', 'STREAM_MAGNITUDE'] WHERE display_data_name = 'freshwater_atlas_stream_networks';
           UPDATE display_catalogue SET required_map_properties = ARRAY['station_number'] WHERE display_data_name = 'hydrometric_stream_flow';
           UPDATE display_catalogue SET required_map_properties = ARRAY['WATERSHED_FEATURE_ID'] WHERE display_data_name = 'freshwater_atlas_watersheds';
           UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.0tsq064k' WHERE display_data_name = 'aquifers';
           UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.31epl7h1' WHERE display_data_name = 'hydrometric_stream_flow';
           UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.56s6dyhu' WHERE display_data_name = 'freshwater_atlas_stream_directions';
           UPDATE data_source SET source_object_id = 'AQUIFER_ID' WHERE data_table_name = 'ground_water_aquifers';
           UPDATE data_source SET source_object_id = 'OBJECTID' WHERE data_table_name = 'bc_major_watersheds';
    """)

    op.execute('SET search_path TO public') 


def downgrade():
    pass
