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

    op.execute('alter table display_catalogue add column use_wms boolean default true')

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
                '1853',
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
        WITH wms_id AS (
            INSERT INTO wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                wms_style,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                'Ground Water Aquifers', 
                'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'aquifers';
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
                'Water Rights Applications - Public', 
                'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_APPLICTNS_SV',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'water_rights_applications';
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
                'First Nation Community Locations', 
                'WHSE_HUMAN_CULTURAL_ECONOMIC.FN_COMMUNITY_LOCATIONS_SP',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'fn_community_locations';
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
                'First Nations Treaty Areas', 
                'WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_AREA_SP',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'fn_treaty_areas';
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
                'First Nations Treaty Lands', 
                'WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_LAND_SP',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'fn_treaty_lands';
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
                'Water Rights Licences - Public', 
                'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'water_rights_licences';
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
                'Ground Water Wells', 
                'postgis_ftw.gwells_well_view',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'groundwater_wells';
    """)

    op.execute("""
        UPDATE display_catalogue set use_wms = false where display_data_name = 'hydrometric_stream_flow';
        UPDATE display_catalogue set use_wms = false where display_data_name = 'normal_annual_runoff_isolines';

        UPDATE wms_catalogue set wms_style = '719' where wms_name = 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY';
        UPDATE wms_catalogue set wms_style = '4883' where wms_name = 'WHSE_WILDLIFE_MANAGEMENT.WCP_CRITICAL_HABITAT_SP';
    """)

    op.execute('SET search_path TO public')



def downgrade():
    pass
