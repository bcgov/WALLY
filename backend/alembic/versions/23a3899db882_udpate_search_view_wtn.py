"""udpate_search_view_wtn

Revision ID: 23a3899db882
Revises: eca0ac552803
Create Date: 2019-10-16 16:07:05.530381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23a3899db882'
down_revision = 'eca0ac552803'
branch_labels = None
depends_on = None


def upgrade():
    # replace materialized view with new view with extra records added.
    # note on table names: some layers like water_rights_licenses do not have
    # consistent spelling across
    # the application and in external resources.
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

        UNION
        SELECT
        ST_AsText(ST_Centroid(gww."GEOMETRY")) AS center,
        gww."WELL_TAG_NO"::text AS primary_id,
        gww."WELL_LOCATION" AS name,
        'Ground water well' AS kind,
        'ground_water_wells' AS layer,
        to_tsvector(concat_ws(' ', gww."WELL_TAG_NO"::text, gww."WELL_LOCATION")) AS tsv
        FROM ground_water_wells AS gww
    """)

    op.execute("""
        create index idx_geocode_tsv ON geocode_lookup USING GIN(tsv)
    """)


def downgrade():
    pass
