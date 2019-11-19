"""Renaming fwa_stream_networks table to freshwater_atlas_stream_networks

Revision ID: 05f3c648c825
Revises: 1d3a9bfe6150
Create Date: 2019-11-18 22:14:53.703451

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '05f3c648c825'
down_revision = '1d3a9bfe6150'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('fwa_stream_networks', 'freshwater_atlas_stream_networks')

    op.execute('ALTER SEQUENCE "fwa_stream_networks_OGC_FID_seq" '
               'RENAME TO "freshwater_atlas_stream_networks_OGC_FID_seq"')

    op.execute('ALTER INDEX fwa_stream_networks_pkey RENAME TO freshwater_atlas_stream_networks_pkey')
    op.execute('ALTER INDEX fwa_stream_networks_geom_geom_idx RENAME TO freshwater_atlas_stream_networks_geom_geom_idx')
    op.execute('ALTER INDEX "idx_fwa_stream_networks_GEOMETRY" '
               'RENAME TO "idx_freshwater_atlas_stream_networks_GEOMETRY"')

    op.execute('UPDATE metadata.data_source SET data_table_name=\'freshwater_atlas_stream_networks\' '
               'WHERE data_source_id=15 AND data_table_name=\'fwa_stream_networks\'')
    op.execute('UPDATE metadata.display_catalogue SET display_data_name=\'freshwater_atlas_stream_networks\' '
               'WHERE data_source_id=15 AND display_data_name=\'fwa_stream_networks\'')
    op.execute('UPDATE metadata.vector_catalogue SET vector_name=\'freshwater_atlas_stream_networks\' '
               'WHERE vector_catalogue_id=7 AND vector_name=\'fwa_stream_networks\'')


def downgrade():
    op.rename_table('freshwater_atlas_stream_networks', 'fwa_stream_networks')
    op.execute('ALTER SEQUENCE "freshwater_atlas_stream_networks_OGC_FID_seq" '
               'RENAME TO "fwa_stream_networks_OGC_FID_seq"')

    op.execute('ALTER INDEX freshwater_atlas_stream_networks_pkey RENAME TO fwa_stream_networks_pkey')
    op.execute('ALTER INDEX freshwater_atlas_stream_networks_geom_geom_idx RENAME TO fwa_stream_networks_geom_geom_idx')
    op.execute('ALTER INDEX "idx_freshwater_atlas_stream_networks_GEOMETRY" '
               'RENAME TO "idx_fwa_stream_networks_GEOMETRY"')

    op.execute('UPDATE metadata.data_source SET data_table_name=\'fwa_stream_networks\' '
               'WHERE data_source_id=15 AND data_table_name=\'freshwater_atlas_stream_networks\'')
    op.execute('UPDATE metadata.display_catalogue SET display_data_name=\'fwa_stream_networks\' '
               'WHERE data_source_id=15 AND display_data_name=\'freshwater_atlas_stream_networks\'')
    op.execute('UPDATE metadata.vector_catalogue SET vector_name=\'fwa_stream_networks\' '
               'WHERE vector_catalogue_id=7 AND vector_name=\'freshwater_atlas_stream_networks\'')
