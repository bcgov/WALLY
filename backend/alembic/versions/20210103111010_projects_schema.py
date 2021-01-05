"""projects_schema

Revision ID: b93cc797efe6
Revises: 72ed26845a6d
Create Date: 2021-01-03 11:10:10.127212

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


# revision identifiers, used by Alembic.
revision = 'b93cc797efe6'
down_revision = '72ed26845a6d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
          'project',
          Column('project_id', Integer, primary_key=True),
          Column('name', String),
          Column('description', String),
          Column('user_id', String, ForeignKey('user.uuid')),
          Column('create_date', DateTime, nullable=False),
          Column('update_date', DateTime, nullable=False)
      )


def downgrade():
    pass
