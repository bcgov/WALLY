"""change project id primary key to uuid

Revision ID: 7a154ea3f123
Revises: 74ddceb41c46
Create Date: 2021-02-18 14:48:58.580550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text

# revision identifiers, used by Alembic.
revision = '7a154ea3f123'
down_revision = '74ddceb41c46'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('project_document', 'project_id')

    op.drop_column('saved_analysis', 'project_id')

    op.drop_column('project', 'project_id')

    op.drop_column('project_document', 'project_document_id')

    op.add_column('project_document', Column('project_document_uuid', UUID(),
             server_default=sa.text("uuid_generate_v4()"), primary_key=True,
             comment="Project document identifier"))

    op.add_column('project', Column('project_uuid', UUID(), primary_key=True,
                   server_default=sa.text("uuid_generate_v4()"), unique=True,
                   comment="Project identifier"))

    op.add_column('project_document',
                  Column('project_uuid', UUID(), ForeignKey('project.project_uuid'),
                         comment="Project that this document relates to"))

    op.add_column('saved_analysis',
                      Column('project_uuid', UUID(), ForeignKey('project.project_uuid'),
                             comment="Project that this saved_analysis relates to"))


def downgrade():
    op.add_column('project_document', Column('project_document_id', Integer,
                  primary_key=True, comment="Project document identifier"))

    op.add_column('project', Column('project_id', Integer, primary_key=True,
               comment="Project identifier"))

    op.drop_column('project_document', 'project_uuid')
    op.drop_column('saved_analysis', 'project_uuid')
    op.drop_column('project', 'project_uuid')

    op.add_column('project_document',
                  Column('project_id', Integer, ForeignKey('project.project_id'),
                         comment="Project that this document relates to"))

    op.add_column('saved_analysis',
              Column('project_id', Integer, ForeignKey('project.project_id'),
                     comment="Project that this saved_analysis relates to"))