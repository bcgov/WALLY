"""add_source_layer_column

Revision ID: 72ed26845a6d
Revises: 3694e369419c
Create Date: 2020-11-04 00:16:39.719167

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '72ed26845a6d'
down_revision = '3694e369419c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    op.add_column('data_source',
                  sa.Column('layer', sa.String(length=200), nullable=True,
                            comment='Source layer used for mapbox style'), schema='metadata')

    # We are currently using the display_data_name to name our sources, so let's migrate them to the new column
    op.execute("""UPDATE data_source SET layer = display_catalogue.display_data_name
    FROM display_catalogue
    WHERE display_catalogue.data_source_id = data_source.data_source_id""")

    op.execute("""
    UPDATE display_catalogue
    SET display_name = 'Known Fish Observation Point'
    WHERE display_data_name = 'fish_observations'
    """)
    op.execute("""
    INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                wms_catalogue_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
               'fish_observations_summaries',
               'Known Fish Summary Point',
               label_column,
               label,
               highlight_columns,
               data_source_id,
               wms_catalogue_id,
               layer_category_code,
               mapbox_layer_id,
               mapbox_source_id,
               create_user, create_date, update_user, update_date, effective_date, expiry_date
            FROM display_catalogue WHERE display_data_name = 'fish_observations';
    """)
    op.execute('SET search_path TO public')


def downgrade():
    op.execute('SET search_path TO metadata')
    op.execute("""
    UPDATE display_catalogue SET display_name = 'Known BC Fish Observations & Distributions'
        WHERE display_data_name = 'fish_observations'
    """)
    op.execute(
        """DELETE FROM display_catalogue WHERE display_data_name = 'fish_observations_summaries'""")
    op.drop_column('data_source', 'source_name', schema='metadata')
    op.execute('SET search_path TO public')
