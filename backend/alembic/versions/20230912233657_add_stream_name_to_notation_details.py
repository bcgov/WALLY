"""add stream name to notation details

Revision ID: a147b403c0a6
Revises: fbd0db388b3e
Create Date: 2023-09-12 23:36:57.186164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a147b403c0a6'
down_revision = 'fbd0db388b3e'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
               update metadata.display_catalogue 
               set highlight_columns = highlight_columns || '{"STREAM_NAME"}' 
               where display_data_name = 'streams_with_water_allocation_notations'
    """)

def downgrade():
    op.execute("""
               update metadata.display_catalogue 
               set highlight_columns = array_remove ( highlight_columns, 'STREAM_NAME' ) 
               where display_data_name = 'streams_with_water_allocation_notations'
    """)
