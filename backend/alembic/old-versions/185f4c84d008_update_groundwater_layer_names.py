"""Update groundwater layer names

Revision ID: 185f4c84d008
Revises: 8d26b7e18b0f
Create Date: 2020-01-30 11:21:15.699842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '185f4c84d008'
down_revision = '8d26b7e18b0f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')
    op.execute("""
           UPDATE data_source AS ds SET name = 'Groundwater Wells' 
           WHERE data_table_name = 'ground_water_wells'
    """)
    op.execute("""
            UPDATE data_source AS ds SET name = 'Groundwater Aquifers' 
            WHERE data_table_name = 'ground_water_aquifers'
    """)
    op.execute('SET search_path TO public')


def downgrade():
    op.execute('SET search_path TO metadata')
    op.execute("""
           UPDATE data_source AS ds SET name = 'Ground Water Wells' 
           WHERE data_table_name = 'ground_water_wells'
    """)
    op.execute("""
            UPDATE data_source AS ds SET name = 'Ground Water Aquifers' 
            WHERE data_table_name = 'ground_water_aquifers'
    """)
    op.execute('SET search_path TO public')
