"""add water allocation notations tables

Revision ID: fbd0db388b3e
Revises: f5024174a526
Create Date: 2023-08-01 10:44:45.751704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd0db388b3e'
down_revision = 'f5024174a526'
branch_labels = None
depends_on = None


def upgrade():
   op.execute('SET search_path TO metadata')
   
   # Create tables for 'Streams with Water Allocation Notations' layer
   op.execute("""
        INSERT INTO metadata.mapbox_source (mapbox_source_id) VALUES ('iit-water.c3ufv733');
        WITH ds_id AS (
                INSERT INTO metadata.data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date, layer
                ) VALUES (
                    'json',
                    'Streams with Water Allocation Notations',
                    'This dataset displays streams that have water allocation notations on them.',
                    'https://catalogue.data.gov.bc.ca/dataset/streams-with-water-allocation-notations',
                    'WHSE_WATER_MANAGEMENT.WLS_WATER_NOTATION_STREAMS_SP',
                    'streams_with_water_allocation_notations', 
                    'LINEAR_FEATURE_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z', 'streams_with_water_allocation_notations'
                ) RETURNING data_source_id
        ),
        wms_id AS (
            INSERT INTO metadata.wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from metadata.wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Streams with Water Allocation Notations',
                    'WHSE_WATER_MANAGEMENT.WLS_WATER_NOTATION_STREAMS_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
        )
        INSERT INTO metadata.display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                wms_catalogue_id,
                layer_category_code,
                required_map_properties,
                mapbox_layer_id,
                mapbox_source_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) SELECT
                'streams_with_water_allocation_notations', 
                'Streams with Water Allocation Notations',
                'LINEAR_FEATURE_ID',
                'Feature Id',
                ARRAY['PRIMARY_NOTATION_TYPE', 'SECONDARY_NOTATION_TYPES', 'NOTATION_ID_LIST'],
                ds_id.data_source_id,
                wms_id.wms_catalogue_id,
                'WATER_ADMINISTRATION',
                '{PRIMARY_NOTATION_TYPE}',
                'iit-water.c3ufv733',
                'iit-water.c3ufv733',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM ds_id, wms_id ;
    """)
   
   # Create tables for 'Aquifers with Water Allocation Notations' layer
   op.execute("""
        INSERT INTO metadata.mapbox_source (mapbox_source_id) VALUES ('iit-water.cs8nith6');
        WITH ds_id AS (
            INSERT INTO metadata.data_source (
                data_format_code,
                name,
                description,
                source_url,
                source_object_name,
                data_table_name,
                source_object_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date, layer
            ) VALUES (
                'json',
                'Aquifers with Water Allocation Notations',
                'This dataset displays aquifers with water allocation notations on them.',
                'https://catalogue.data.gov.bc.ca/dataset/aquifers-with-water-allocation-notations',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_NOTATION_AQUIFERS_SP',
                'aquifers_with_water_allocation_notations', 
                'AQUIFER_ID',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z', 'aquifers_with_water_allocation_notations'
            ) RETURNING data_source_id
        ),
        wms_id AS (
            INSERT INTO metadata.wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                wms_style,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                (select wms_catalogue_id from metadata.wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                'Aquifers with Water Allocation Notations',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_NOTATION_AQUIFERS_SP',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        INSERT INTO metadata.display_catalogue (
            display_data_name,
            display_name,
            label_column,
            label,
            highlight_columns,
            data_source_id,
            wms_catalogue_id,
            layer_category_code,
            required_map_properties,
            mapbox_layer_id,
            mapbox_source_id,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) SELECT
            'aquifers_with_water_allocation_notations', 
            'Aquifers with Water Allocation Notations',
            'AQUIFER_ID',
            'Feature Id',
            ARRAY[ 'NOTATION_ID', 'NOTATION_DESCRIPTION', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M' ],
            ds_id.data_source_id,
            wms_id.wms_catalogue_id,
            'WATER_ADMINISTRATION',
            '{}',
            'iit-water.cs8nith6',
            'iit-water.cs8nith6',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM ds_id, wms_id ;
   """)

def downgrade():
    pass
