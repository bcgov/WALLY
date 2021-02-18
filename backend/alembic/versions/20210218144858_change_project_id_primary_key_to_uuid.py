"""change project id primary key to uuid

Revision ID: 7a154ea3f123
Revises: 74ddceb41c46
Create Date: 2021-02-18 14:48:58.580550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a154ea3f123'
down_revision = '74ddceb41c46'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column('project', 'project_id', existing_type=sa.Integer, type_=UUID())
    op.alter_column('project', 'project_id', new_column_name='project_uuid')

	op.alter_column('project_document', 'project_id', existing_type=sa.Integer, type_=UUID())
    op.alter_column('project_document', 'project_id', new_column_name='project_uuid')

	op.alter_column('project_document', 'project_document_id', existing_type=sa.Integer, type_=UUID())
    op.alter_column('project_document', 'project_document_id', new_column_name='project_document_uuid')


def downgrade():
	
	op.alter_column('project', 'project_id', existing_type=UUID(), type_=sa.Integer)
    op.alter_column('project', 'project_uuid', new_column_name='project_id')

	op.alter_column('project_document', 'project_id', existing_type=UUID(), type_=sa.Integer)
    op.alter_column('project_document', 'project_uuid', new_column_name='project_id')
    
	op.alter_column('project_document', 'project_document_id', existing_type=UUID(), type_=sa.Integer)
    op.alter_column('project_document', 'project_document_uuid', new_column_name='project_document_id')
