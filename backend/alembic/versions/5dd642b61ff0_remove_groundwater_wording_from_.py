"""Remove Groundwater wording from Groundwater Aquifers

Revision ID: 5dd642b61ff0
Revises: 6eccf085d7c7
Create Date: 2020-02-07 19:57:43.279440

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5dd642b61ff0'
down_revision = '6eccf085d7c7'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')
    op.execute("""
                UPDATE data_source AS ds SET name = 'Aquifers' 
                WHERE data_table_name = 'ground_water_aquifers'
        """)
    op.execute('SET search_path TO public')


def downgrade():
    op.execute('SET search_path TO metadata')
    op.execute("""
                UPDATE data_source AS ds SET name = 'Groundwater Aquifers' 
                WHERE data_table_name = 'ground_water_aquifers'
        """)
    op.execute('SET search_path TO public')
