"""update_search_view2

Revision ID: 56cd94a2e609
Revises: 978751d9a7f2
Create Date: 2019-09-20 19:51:05.531222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56cd94a2e609'
down_revision = '978751d9a7f2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP MATERIALIZED VIEW IF EXISTS geocode_lookup")
    op.execute("""
        CREATE MATERIALIZED VIEW geocode_lookup AS

        SELECT
        ST_AsText(stn.geom) AS center,
        stn.station_number AS primary_id,
        stn.station_name AS name,
        'Stream station' AS kind,
        'hydrometric_stream_flow' AS layer,
        to_tsvector(concat_ws(' ',stn.station_number, stn.station_name)) AS tsv
        FROM hydat.stations AS stn
        WHERE stn.prov_terr_state_loc = 'BC'

        UNION
        SELECT
        ST_AsText(ST_Centroid(cadastral."SHAPE")) AS center,
        coalesce(cadastral."PID", cadastral."PARCEL_NAME"::text) AS primary_id,
        NULL AS name,
        'Parcel' AS kind,
        'cadastral' AS layer,
        to_tsvector(coalesce(cadastral."PID"::text, cadastral."PARCEL_NAME"::text)) AS tsv
        FROM cadastral

        UNION
        SELECT
        ST_AsText(ST_Centroid(wrl."SHAPE")) AS center,
        concat(wrl."POD_NUMBER"::text, ' (', wrl."LICENCE_NUMBER"::text, ')') AS primary_id,
        wrl."SOURCE_NAME" AS name,
        'Water rights licence' AS kind,
        'water_rights_licences' AS layer,
        to_tsvector(concat_ws(' ', wrl."POD_NUMBER"::text, wrl."LICENCE_NUMBER"::text, wrl."SOURCE_NAME")) AS tsv
        FROM water_rights_licenses AS wrl
    """)
    # op.execute("""
    #     create index idx_geocode_tsv ON geocode_lookup USING GIN(tsv)
    # """)


def downgrade():
    pass
