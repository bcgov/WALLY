"""Change user id primary key to uuid
The current user table has a String primary key.
This migration creates a new user table with a UUID() primary key and preserves the data contained
in the old user table (just user IDIRs and their saved map layers) into a new table called
`user_map_layers`

Revision ID: 74ddceb41c46
Revises: 563750b4923c
Create Date: 2021-01-28 16:41:28.180248

"""
from alembic import op
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '74ddceb41c46'
down_revision = '563750b4923c'
branch_labels = None
depends_on = None


def upgrade():
    # Rename existing user table to `user_map_layer`
    op.rename_table('user', 'user_map_layer')

    # Create new user table
    op.create_table(
        'user',
        Column('user_uuid', UUID(),
               primary_key=True,
               comment=''),
        Column('user_idir', String, comment='The IDIR of the user'),
        Column('create_date', DateTime, nullable=False),
        Column('update_date', DateTime, nullable=False)
    )

    # Update referenced tables' user ids.
    # We're dropping the `user_id` idir column to avoid confusion and
    # replace them with the proper uuid
    op.add_column('project',
                  Column('user_uuid', UUID(), ForeignKey('user.user_uuid'),
                         comment="User who owns this project"))
    op.drop_column('project', 'user_id')

    op.add_column('saved_analysis',
                  Column('user_uuid', UUID(), ForeignKey('user.user_uuid'),
                         comment="User who owns this saved analysis"))
    op.drop_column('saved_analysis', 'user_id')

    # Rename the string uuid column to its more appropriate name, user_idir
    op.alter_column('user_map_layer', 'uuid', new_column_name='user_idir')


def downgrade():
    # Revert the changes done in upgrade
    op.alter_column('user_map_layer', 'user_idir', new_column_name='uuid')

    op.add_column('saved_analysis',
                  Column('user_id', String, ForeignKey('user_map_layer.uuid'),
                         comment="User who owns this saved analysis"))
    op.drop_column('saved_analysis', 'user_uuid')

    op.add_column('project',
                  Column('user_id', String, ForeignKey('user_map_layer.uuid'),
                         comment="User who owns this project"))
    op.drop_column('project', 'user_uuid')

    op.drop_table('user')
    op.rename_table('user_map_layer', 'user')
