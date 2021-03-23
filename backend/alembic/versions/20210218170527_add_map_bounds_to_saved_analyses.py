"""add map bounds to saved analyses

Revision ID: 48ca44a2a61f
Revises: 74ddceb41c46
Create Date: 2021-02-10 17:05:27.383044

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision = '48ca44a2a61f'
down_revision = '7a154ea3f123'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('saved_analysis', Column('map_bounds', ARRAY(Float, dimensions=2),
      comment="Saved map bounds of analysis"))


def downgrade():
    op.drop_column('saved_analysis', 'map_bounds')
