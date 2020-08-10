"""add licensed works layer

Revision ID: 369150228f9d
Revises: 603d93ba52ea
Create Date: 2020-08-10 02:52:28.638544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '369150228f9d'
down_revision = '603d93ba52ea'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    # populate water_licensed_works info
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
                'Water Licensed Works - Lines',
                'Province-wide SDE layer showing linear works associated with a Water Licence',
                'https://catalogue.data.gov.bc.ca/dataset/water-licensed-works-lines',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_LICENCED_WRK_LINE_SP',
                'water_licensed_works',
                'WATER_LICENCED_WORK_LINE_ID',
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
                'Water Licensed Works - Lines',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_LICENCED_WRK_LINE_SP',
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
            'water_licensed_works',
            'Water Licensed Works - Lines',
            'WATER_LICENCED_WORK_LINE_ID',
            'Work Line ID',
            ARRAY[
                'WORKS_ID', 'FEATURE_CODE', 'DISPLAY_COLOUR'
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
