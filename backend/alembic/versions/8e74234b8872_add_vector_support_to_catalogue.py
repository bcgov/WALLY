"""add vector support to catalogue

Revision ID: 8e74234b8872
Revises: 27df43577da2
Create Date: 2019-09-06 21:21:40.608660

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e74234b8872'
down_revision = '27df43577da2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('SET search_path TO metadata')
    op.create_table(
        'vector_catalogue',
        sa.Column('vector_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, comment='vector layer description'),
        sa.Column('vector_name', sa.String, comment='identifying vector layer name'),

        sa.Column('create_user', sa.String(100), comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime, comment='Date and time (UTC) when the physical record was '
                                                      'created in the database.'),
        sa.Column('update_user', sa.String(100), comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime, comment='Date and time (UTC) when the physical record was updated '
                                                      'in the database. It will be the same as the create_date until '
                                                      'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime, comment='The date and time that the code became valid '
                                                         'and could be used.'),
        sa.Column('expiry_date', sa.DateTime, comment='The date and time after which the code is no longer valid and '
                                                      'should not be used.')
    )

    op.add_column(
        'display_catalogue',
        sa.Column('vector_catalogue_id', sa.Integer, sa.ForeignKey('metadata.vector_catalogue.vector_catalogue_id'),
                  comment='reference to vector catalogue item'),
    )
    op.execute('SET search_path TO public')

def downgrade():
    pass
