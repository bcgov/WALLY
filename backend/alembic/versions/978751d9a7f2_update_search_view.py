"""update search view

Revision ID: 978751d9a7f2
Revises: 73ffeef2cc38
Create Date: 2019-09-18 19:36:46.534164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '978751d9a7f2'
down_revision = '73ffeef2cc38'
branch_labels = None
depends_on = None


def upgrade():
    # replace materialized view with new view with extra records added.
    # note on table names: some layers like water_rights_licenses do not have
    # consistent spelling across
    # the application and in external resources.
    op.execute("DROP MATERIALIZED VIEW geocode_lookup")
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
        concat_ws(wrl."POD_NUMBER"::text, ' (', wrl."LICENCE_NUMBER"::text, ')') AS primary_id,
        wrl."SOURCE_NAME" AS name,
        'Water rights licence' AS kind,
        'water_rights_licences' AS layer,
        to_tsvector(concat_ws(' ', wrl."POD_NUMBER"::text, wrl."LICENCE_NUMBER"::text, wrl."SOURCE_NAME")) AS tsv
        FROM water_rights_licenses AS wrl
    """)

    op.execute("""
    create index idx_geocode_tsv ON geocode_lookup USING GIN(tsv)
    """)


def downgrade():
    pass
