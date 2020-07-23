"""fish obstacle layer

Revision ID: 00c94ea61cd1
Revises: 8f0eb2b03a97
Create Date: 2020-06-30 14:58:49.417417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00c94ea61cd1'
down_revision = '8f0eb2b03a97'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

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
                'Provincial Obstacles to Fish Passage',
                'The Provincial Obstacles to Fish Passage theme presents records of all known obstacles to fish passage from several fisheries datasets. Records from the following datasets have been included: The Fisheries Information Summary System (FISS); the Fish Habitat Inventory and Information Program (FHIIP); the Field Data Information System (FDIS) and the Resource Analysis Branch (RAB) inventory studies. The main intent of this layer is to have a single layer of all known obstacles to fish passage.',
                'https://catalogue.data.gov.bc.ca/dataset/provincial-obstacles-to-fish-passage',
                'WHSE_FISH.FISS_OBSTACLES_PNT_SP',
                'fish_obstacles',
                'FISH_OBSTACLE_POINT_ID',
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
                'Provincial Obstacles to Fish Passage',
                'WHSE_FISH.FISS_OBSTACLES_PNT_SP',
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
            'fish_obstacles',
            'Provincial Obstacles to Fish Passage',
            'FISH_OBSTACLE_POINT_ID',
            'Fish Obstacle Point Id',
            ARRAY[
                'OBSTACLE_NAME', 'SOURCE', 'SURVEY_DATE', 'AGENCY_NAME', 'HEIGHT', 'LENGTH', 'ACAT_REPORT_URL', 'UTM_EASTING', 'UTM_NORTHING', 'WATERBODY_TYPE'
            ],
            ds_id.data_source_id,
            wms_id.wms_catalogue_id,
            'FISH_WILDLIFE_PLANTS',
            'iit-water.448thhpa',
            'iit-water.448thhpa',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM ds_id, wms_id ;
    """)

    op.execute('SET search_path TO public')


def downgrade():
    pass
