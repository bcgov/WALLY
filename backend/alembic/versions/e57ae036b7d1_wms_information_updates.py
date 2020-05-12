"""wms information updates

Revision ID: e57ae036b7d1
Revises: cc99f17203c7
Create Date: 2020-05-11 16:47:48.281211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e57ae036b7d1'
down_revision = 'cc99f17203c7'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    op.execute('alter table display_catalogue add column use_wms boolean default false')

    op.execute("""
        WITH wms_id AS (
            INSERT INTO wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                wms_style,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                'Freshwater Atlas Stream Networks', 
                'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'freshwater_atlas_stream_networks';
    """)

    op.execute("""
        WITH wms_id AS (
            INSERT INTO wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                wms_style,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                'ParcelMap BC Parcel Fabric', 
                'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'cadastral';
    """)

    op.execute("""
        UPDATE display_catalogue set use_wms = true where display_data_name = 'freshwater_atlas_stream_networks';
        UPDATE display_catalogue set use_wms = true where display_data_name = 'freshwater_atlas_stream_directions';
        UPDATE display_catalogue set use_wms = true where display_data_name = 'freshwater_atlas_watersheds';
        UPDATE display_catalogue set use_wms = true where display_data_name = 'water_allocation_restrictions';
        UPDATE display_catalogue set use_wms = true where display_data_name = 'critical_habitat_species_at_risk';
        UPDATE display_catalogue set use_wms = true where display_data_name = 'fish_observations';
        UPDATE display_catalogue set use_wms = true where display_data_name = 'cadastral';
    """)

    op.execute('SET search_path TO public')



def downgrade():
    pass
