"""add fish observation layer

Revision ID: a803c45b7396
Revises: f2b445f6650c
Create Date: 2020-03-05 11:15:32.216909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a803c45b7396'
down_revision = 'f2b445f6650c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')

    op.execute("""
        INSERT INTO mapbox_source (mapbox_source_id, max_zoom) VALUES ('iit-water.448thhpa', 9)
    """)

    # need to update water_rights_licences display_catalogue
    # to share mapbox layer with fish_observations
    op.execute("""
           UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.448thhpa', mapbox_source_id = 'iit-water.448thhpa'
           WHERE display_data_name = 'water_rights_licences'
    """)

    # populate fish_observations info
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
                'Known BC Fish Observations & BC Fish Distributions',
                'This point location dataset of fish observations is a regularly updated compilation of BC fish distribution information taken from a combination of all the official provincial databases including the BC Fisheries Information Summary System (FISS). Fish occurrences in this dataset represent the most current and comprehensive information source on fish presence for the province.',
                'https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions',
                'WHSE_FISH.FISS_FISH_OBSRVTN_PNT_SP',
                'fish_observations',
                'FISH_OBSERVATION_POINT_ID',
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
                'Known BC Fish Observations and BC Fish Distributions',
                'WHSE_FISH.FISS_FISH_OBSRVTN_PNT_SP',
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
            'fish_observations',
            'Known BC Fish Observations and BC Fish Distributions',
            'SPECIES_NAME',
            'Species Name',
            ARRAY[
                'SPECIES_NAME', 'LIFE_STAGE', 'ACTIVITY', 'OBSERVATION_DATE', 'ACAT_REPORT_URL', 'POINT_TYPE_CODE', 'AGENCY_NAME', 'WATERBODY_TYPE'
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
