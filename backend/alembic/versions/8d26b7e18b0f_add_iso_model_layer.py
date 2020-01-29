"""add iso model layer

Revision ID: 8d26b7e18b0f
Revises: 9ee500c7ad08
Create Date: 2020-01-28 10:27:36.012094

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '8d26b7e18b0f'
down_revision = '9ee500c7ad08'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'normal_annual_runoff_isolines',
        sa.Column('id', sa.Integer, primary_key=True,
               comment='Arbitrary id to differentiate polygons.'),
        sa.Column('ANNUAL_RUNOFF_IN_MM', sa.Integer,
               comment='Annual runoff of precipitation in the area of the associated polygon. '
                       'Possible values in mm: 10 50 100 200 500 1000 1500 2000 3000 4000'),
        sa.Column('GEOMETRY', Geometry('POLYGON', 4326),
               comment='This geometry is the polygon associated with the isoline for this area.')
    )

    op.execute('SET search_path TO metadata')

    # populate normal_annual_runoff_isolines info
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
                'Normal Annual Runoff Isolines (1961 - 1990)',
                'Spatial layer intended to display normal annual runoff isolines, in millimetres, for 1961 -1990.',
                'https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical',
                'WHSE_WATER_MANAGEMENT.HYDZ_ANNUAL_RUNOFF_LINE',
                'normal_annual_runoff_isolines',
                'id',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING data_source_id
        ),
        vc_id AS (
                INSERT INTO vector_catalogue (
                vector_catalogue_id,
                description, 
                vector_name,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                NEXTVAL(pg_get_serial_sequence('vector_catalogue','vector_catalogue_id')),
                'Normal Annual Runoff Isolines (1961 - 1990)', 
                'normal_annual_runoff_isolines',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING vector_catalogue_id
        )
        INSERT INTO display_catalogue (
            display_data_name,
            display_name,
            label_column,
            label,
            highlight_columns,
            data_source_id,
            vector_catalogue_id,
            layer_category_code,
            mapbox_layer_id,
            mapbox_source_id,
            required_map_properties,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) SELECT
            'normal_annual_runoff_isolines',
            'Normal Annual Runoff Isolines (1961 - 1990) - Historical',
            'id',
            'Id',
            ARRAY[
                'id', 'ANNUAL_RUNOFF_IN_MM'
            ],
            ds_id.data_source_id,
            vc_id.vector_catalogue_id,
            'FRESHWATER_MARINE',
            'iit-water.0tsq064k',
            'iit-water.0tsq064k',
            ARRAY[
                'ANNUAL_RUNOFF_IN_MM'
            ],
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM ds_id, vc_id ;
    """)

    op.execute('SET search_path TO public')

def downgrade():
    pass
