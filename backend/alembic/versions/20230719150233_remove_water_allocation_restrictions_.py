"""remove water allocation restrictions layer

Revision ID: f5024174a526
Revises: e10c8d94b5ec
Create Date: 2023-07-18 15:02:33.194858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5024174a526'
down_revision = 'e10c8d94b5ec'
branch_labels = None
depends_on = None


def upgrade():

    op.execute('SET search_path TO metadata')
    op.execute("""DELETE FROM display_catalogue WHERE display_catalogue_id = 11""")
    op.execute("""DELETE FROM data_source WHERE data_source_id = 11""")
    op.execute("""DELETE FROM wms_catalogue WHERE wms_catalogue_id = 11""")

    op.execute('SET search_path TO public')
    op.execute("""DROP TABLE IF EXISTS water_allocation_restrictions""")

def downgrade():
    pass
