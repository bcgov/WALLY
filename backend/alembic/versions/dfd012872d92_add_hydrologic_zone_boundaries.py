"""add hydrologic zone boundaries

Revision ID: dfd012872d92
Revises: 8972e90a3cf4
Create Date: 2019-12-30 13:29:19.805579

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA

# revision identifiers, used by Alembic.
revision = 'dfd012872d92'
down_revision = '8972e90a3cf4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hydrologic_zone_boundaries',
                          
        sa.Column('HYDROLOGICZONE_SP_ID', sa.Integer, primary_key=True, autoincrement=False, comment='Primary unique numeric identifier for a Hydrological Zone Polygon.'),
        sa.Column('FEATURE_CODE', sa.String, comment='A standard numeric code to identify the type of feature represented by the spatial data.'),
        sa.Column('HYDROLOGICZONE_NO', sa.Integer, comment='A numeric identifier assigned to a zone that represents an area of homogenous hydrologic and geomorphological characteristics'),
        sa.Column('HYDROLOGICZONE_NAME', sa.String, comment='A descriptive name, assigned to a zone having a numeric identifier and that represents an area of homogenous hydrologic and geomorphological characteristics.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional polygon in square meters'),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a geometry in meters'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is the column used to reference the spatial coordinates defining the feature.'),
        sa.Column('OBJECTID', sa.Float, comment=''),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools'
                                'to store annotation, curve features and CAD data when using'
                                'the SDO_GEOMETRY storage data type.')
    )


def downgrade():
    pass
