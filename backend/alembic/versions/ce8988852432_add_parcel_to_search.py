"""add parcel to search

Revision ID: ce8988852432
Revises: 97efdf3c7904
Create Date: 2019-09-09 06:32:16.481619

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ce8988852432'
down_revision = '97efdf3c7904'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW geocode_lookup AS

        SELECT
        ST_AsText(stn.geom) AS center,
        stn.station_number AS primary_id,
        stn.station_name AS name,
        'Stream station' AS kind,
        'hydrometric_stream_data' AS layer,
        to_tsvector(concat_ws(' ',stn.station_number, stn.station_name)) AS tsv
        FROM hydat.stations AS stn

        UNION
        SELECT
        ST_AsText(ST_Centroid(parcel.geom)) AS center,
        parcel."PID"::text AS primary_id,
        NULL AS name,
        'Parcel' AS kind,
        'parcel_fabric' AS layer,
        to_tsvector(concat_ws(' ',parcel."PID"::text, parcel."PARCEL_NAME"::text)) AS tsv
        FROM parcel
    """)
    op.execute("""
    create index idx_geocode_tsv ON geocode_lookup USING GIN(tsv)
    """)


def downgrade():
    return
