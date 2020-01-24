"""update glacier label column

Revision ID: 9ee500c7ad08
Revises: 40a169a3bda1
Create Date: 2020-01-21 13:33:28.212470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ee500c7ad08'
down_revision = '40a169a3bda1'
branch_labels = None
depends_on = None


def upgrade():
    q = """
        UPDATE  metadata.display_catalogue
        SET     label_column = 'WATERBODY_POLY_ID'
        WHERE   display_data_name = 'freshwater_atlas_glaciers'
    """
    op.execute(q)


def downgrade():
    pass
