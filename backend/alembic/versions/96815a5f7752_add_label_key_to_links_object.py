  """add label key to links object
Revision ID: 96815a5f7752
Revises: 73ffeef2cc38
Create Date: 2019-09-19 15:49:17.627612
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96815a5f7752'
down_revision = '516ece576828'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    alter table metadata.link_component add column
        link_label_key VARCHAR;
    """)


def downgrade():
    pass