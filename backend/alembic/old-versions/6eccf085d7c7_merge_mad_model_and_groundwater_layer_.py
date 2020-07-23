"""merge mad model and groundwater layer names

Revision ID: 6eccf085d7c7
Revises: 8c0ac4dc8ac2, 185f4c84d008
Create Date: 2020-02-03 13:40:30.902462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eccf085d7c7'
down_revision = ('8c0ac4dc8ac2', '185f4c84d008')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
