"""merge revisions 20191023

Revision ID: ab7b5daedfbd
Revises: 854b87855859, 30d75d8eb63d
Create Date: 2019-10-23 20:17:31.395366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab7b5daedfbd'
down_revision = ('854b87855859', '30d75d8eb63d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
