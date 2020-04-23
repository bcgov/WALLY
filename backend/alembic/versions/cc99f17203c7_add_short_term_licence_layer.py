"""add short term licence layer

Revision ID: cc99f17203c7
Revises: 47f2e019d65d
Create Date: 2020-04-21 17:35:16.972644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc99f17203c7'
down_revision = '47f2e019d65d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    # populate water_approval_points info
    op.execute("""
          WITH ds_id AS (
            INSERT INTO data_source (
                data_source_id,
                data_format_code,
                name,
                description,
                source_url,
                source_object_name,
                data_table_name,
                source_object_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                NEXTVAL(pg_get_serial_sequence('data_source','data_source_id')),
                'json',
                'Water Approval Points',
                'The location (point) where an approval has been requested to conduct works in the vicinity of a water source.',
                'https://catalogue.data.gov.bc.ca/dataset/water-approval-points',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_APPROVALS_SVW',
                'water_approval_points',
                'WATER_APPROVAL_ID',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING data_source_id
        ),
        wms_id AS (
          INSERT INTO wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                wms_style,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                'Water Approval Points',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_APPROVALS_SVW',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
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
            'water_approval_points',
            'Water Approval Points',
            'FCBC_TRACKING_NUMBER',
            'FCBC Tracking Number',
            ARRAY[
                'WSD_REGION', 'APPROVAL_TYPE', 'APPROVAL_FILE_NUMBER', 'FCBC_TRACKING_NUMBER', 'SOURCE', 'WORKS_DESCRIPTION', 'QUANTITY', 'QUANTITY_UNITS', 'QTY_DIVERSION_MAX_RATE', 'QTY_UNITS_DIVERSION_MAX_RATE', 'WATER_DISTRICT', 'PRECINCT', 'APPROVAL_STATUS', 'APPLICATION_DATE', 'FCBC_ACCEPTANCE_DATE', 'APPROVAL_ISSUANCE_DATE', 'APPROVAL_START_DATE', 'APPROVAL_EXPIRY_DATE', 'APPROVAL_REFUSE_ABANDON_DATE'
            ],
            ds_id.data_source_id,
            wms_id.wms_catalogue_id,
            'WATER_ADMINISTRATION',
            'iit-water.448thhpa',
            'iit-water.448thhpa',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM ds_id, wms_id ;
    """)

    op.execute('SET search_path TO public')


def downgrade():
    pass
