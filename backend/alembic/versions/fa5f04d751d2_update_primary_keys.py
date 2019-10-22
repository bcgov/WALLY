"""update primary keys

Revision ID: fa5f04d751d2
Revises: 30d75d8eb63d
Create Date: 2019-10-22 14:40:05.892774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa5f04d751d2'
down_revision = '30d75d8eb63d'
branch_labels = None
depends_on = None


def upgrade():
    # op.drop_constraint('PRIMARY', 'ecocat_water_related_reports', type_='primary')
    op.execute('ALTER TABLE ecocat_water_related_reports DROP CONSTRAINT ecocat_water_related_reports_pkey CASCADE')
    op.create_primary_key('ecocat_water_related_reports_pkey', 'ecocat_water_related_reports', ['REPORT_ID'])


def downgrade():
    pass
