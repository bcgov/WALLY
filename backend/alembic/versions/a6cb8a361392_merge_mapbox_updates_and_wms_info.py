"""merge mapbox updates and wms info

Revision ID: a6cb8a361392
Revises: 368193bdec64, e57ae036b7d1
Create Date: 2020-05-20 14:20:58.169722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6cb8a361392'
down_revision = ('368193bdec64', 'e57ae036b7d1')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
