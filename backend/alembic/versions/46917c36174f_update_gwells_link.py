"""update gwells link

Revision ID: 46917c36174f
Revises: 40a169a3bda1
Create Date: 2020-01-06 16:49:08.228883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46917c36174f'
down_revision = '40a169a3bda1'
branch_labels = None
depends_on = None


def upgrade():
    stmt = """
        update  metadata.data_source
        set     source_url = 'https://apps.nrs.gov.bc.ca/gwells/'
        where   source_url = 'https://catalogue.data.gov.bc.ca/dataset/ground-water-wells'
        and     name = 'Ground Water Wells';
    """
    op.execute(stmt)


def downgrade():
    pass
