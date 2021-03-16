"""add dem schema

Revision ID: c82f8499050e
Revises: 7a154ea3f123
Create Date: 2021-03-16 12:34:20.205965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c82f8499050e'
down_revision = '7a154ea3f123'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema if not exists dem")


def downgrade():
    op.execute("drop schema dem")
