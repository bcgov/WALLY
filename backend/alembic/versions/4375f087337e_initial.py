"""initial

Revision ID: 4375f087337e
Revises: 
Create Date: 2019-07-12 16:27:26.122759

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '4375f087337e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    op.create_table(
        'publisher',
        sa.Column('publisher_guid', UUID(as_uuid=True), primary_key=True,
                  index=True, default=uuid.uuid4()),
        sa.Column('name', sa.String, index=True, nullable=False),
        sa.Column('description', sa.String),
    )


def downgrade():
    pass
