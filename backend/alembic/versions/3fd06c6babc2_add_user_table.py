"""add user table

Revision ID: 3fd06c6babc2
Revises: 00c94ea61cd1
Create Date: 2020-07-06 15:30:22.044190

"""
from alembic import op
from sqlalchemy import Column, String, ARRAY, TEXT


# revision identifiers, used by Alembic.
revision = '3fd06c6babc2'
down_revision = '00c94ea61cd1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        Column('uuid', String, primary_key=True),
        Column('default_map_layers', ARRAY(TEXT), nullable=True),
    )


def downgrade():
    op.drop_table('user')
