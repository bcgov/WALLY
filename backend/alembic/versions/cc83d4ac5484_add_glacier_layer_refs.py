"""add glacier layer refs

Revision ID: cc83d4ac5484
Revises: db6313a85cf5
Create Date: 2020-01-01 14:42:08.903465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc83d4ac5484'
down_revision = 'db6313a85cf5'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    op.execute("""
        INSERT INTO metadata.mapbox_source (mapbox_source_id, max_zoom) VALUES ('iit-water.glaciers', 9)
    """)   

    # populate freshwater_atlas_glaciers info
    op.execute("""
          WITH vc_id AS (
                INSERT INTO vector_catalogue (
                vector_catalogue_id,
                description, 
                vector_name,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                NEXTVAL(pg_get_serial_sequence('vector_catalogue','vector_catalogue_id')),
                'Freshwater Atlas Glaciers', 
                'freshwater_atlas_glaciers',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING vector_catalogue_id
        ),
        ds_id AS (
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
                'Freshwater Atlas Glaciers',
                'Glaciers and ice masses for the province of British Columbia.',
                'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-glaciers',
                'WHSE_BASEMAPPING.FWA_GLACIERS_POLY',
                'freshwater_atlas_glaciers',
                'WATERBODY_POLY_ID',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING data_source_id
        ),
        wms_id AS (
          INSERT INTO wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                NEXTVAL(pg_get_serial_sequence('wms_catalogue','wms_catalogue_id')),
                'Freshwater Atlas Glaciers', 
                'WHSE_BASEMAPPING.FWA_GLACIERS_POLY',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        INSERT INTO display_catalogue (
            display_data_name,
            display_name,
            label_column,
            label,
            highlight_columns,
            vector_catalogue_id,
            data_source_id,
            wms_catalogue_id,
            layer_category_code,
            mapbox_layer_id,
            mapbox_source_id,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) SELECT
            'freshwater_atlas_glaciers',
            'Freshwater Atlas Glaciers',
            'GNIS_NAME_1',
            'Name',
            ARRAY[
                'WATERBODY_TYPE', 'AREA_HA', 'GNIS_NAME_1', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M'
            ],
            vc_id.vector_catalogue_id,
            ds_id.data_source_id,
            wms_id.wms_catalogue_id,
            'FRESHWATER_MARINE',
            'iit-water.0tsq064k',
            'iit-water.0tsq064k',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM vc_id, ds_id, wms_id ;
    """)

    op.execute('SET search_path TO public') 


def downgrade():
    pass
