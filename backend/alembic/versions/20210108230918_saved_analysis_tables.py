"""Saved Analysis tables

Revision ID: 563750b4923c
Revises: b93cc797efe6
Create Date: 2021-01-08 23:09:18.641841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '563750b4923c'
down_revision = 'b93cc797efe6'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'saved_analysis',

        Column('saved_analysis_id', Integer, primary_key=True, comment='Primary key id for '
                                                                       'a saved analysis'),
        Column('description', String, comment='Description of the analysis'),
        Column('name', String, comment='Name of the custom analysis'),
        Column('geometry', String, comment='Geometry of the analysis'),
        Column('feature_type', String, comment='Feature used for analysis'),
        Column('zoom_level', String, comment='Starting zoom level'),
        Column('project_id', Integer, ForeignKey('project.project_id')),
        Column('user_id', String, ForeignKey('user.uuid')),
        Column('create_date', DateTime, nullable=False),
        Column('update_date', DateTime, nullable=False),


    )

    op.create_table(
        'saved_analysis_map_layer',
        Column('saved_analysis_id', Integer, ForeignKey('project.project_id')),
        Column('map_layer', String, ForeignKey('metadata.display_catalogue.display_data_name')),
        Column('create_date', DateTime, nullable=False),
        Column('update_date', DateTime, nullable=False),
        PrimaryKeyConstraint('saved_analysis_id', 'map_layer')
    )


def downgrade():

    op.drop_table('saved_analysis_map_layer')
    op.drop_table('saved_analysis')

