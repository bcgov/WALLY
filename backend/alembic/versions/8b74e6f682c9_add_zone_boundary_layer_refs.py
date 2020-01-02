"""add zone boundary layer refs

Revision ID: 8b74e6f682c9
Revises: cc83d4ac5484
Create Date: 2020-01-01 15:16:06.088872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b74e6f682c9'
down_revision = 'cc83d4ac5484'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    # populate hydrologic_zone_boundaries info
    op.execute("""
    WITH vc_id AS (
                INSERT INTO vector_catalogue (
                vector_catalogue_id,
                description, 
                vector_name,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                NEXTVAL(pg_get_serial_sequence('vector_catalogue','vector_catalogue_id')),
                'Hydrologic Zone Boundaries of BC', 
                'hydrologic_zone_boundaries',
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
                'Hydrologic Zone Boundaries of BC',
                'Zones that represent areas of homogeneous hydrologic and geomorphological characteristics.',
                'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrologic-zone-boundaries-of-british-columbia',
                'WHSE_WATER_MANAGEMENT.HYDZ_HYDROLOGICZONE_SP',
                'hydrologic_zone_boundaries',
                'HYDROLOGICZONE_SP_ID',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING data_source_id
        )
        INSERT INTO display_catalogue (
            display_data_name,
            display_name,
            label_column,
            label,
            highlight_columns,
            vector_catalogue_id,
            data_source_id,
            layer_category_code,
            mapbox_layer_id,
            mapbox_source_id,
            required_map_properties,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) SELECT
            'hydrologic_zone_boundaries',
            'Hydrologic Zone Boundaries of BC',
            'HYDROLOGICZONE_NAME',
            'Name',
            ARRAY[
                'HYDROLOGICZONE_SP_ID', 'HYDROLOGICZONE_NO', 'HYDROLOGICZONE_NAME', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M'
            ],
            vc_id.vector_catalogue_id,
            ds_id.data_source_id,
            'FRESHWATER_MARINE',
            'iit-water.0tsq064k',
            'iit-water.0tsq064k',
            ARRAY[
                'HYDROLOGICZONE_NO'
            ],
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM vc_id, ds_id ;
    """)

    op.execute('SET search_path TO public') 


def downgrade():
    pass
