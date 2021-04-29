"""update_fwa_streams

Revision ID: e9e52d4b325d
Revises: 702efdc8f3fa
Create Date: 2021-04-26 15:10:20.681440

"""
from sqlalchemy.orm.session import Session
from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e9e52d4b325d'
down_revision = '702efdc8f3fa'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('freshwater_atlas_watersheds', 'GEOMETRY', existing_type=geoalchemy2.types.Geometry(),
                    type_=geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326),
                    postgresql_using='ST_Multi(ST_SetSRID("GEOMETRY", 4326))', existing_nullable=True)
    op.alter_column('freshwater_atlas_stream_networks', 'GEOMETRY',
                    existing_type=geoalchemy2.types.Geometry(
                        geometry_type='LINESTRINGZ', srid=4326),
                    type_=geoalchemy2.types.Geometry(
                        geometry_type='MULTILINESTRINGZ', srid=4326),
                    postgresql_using='ST_Multi("GEOMETRY")',
                    existing_nullable=True)


def downgrade():
    pass
