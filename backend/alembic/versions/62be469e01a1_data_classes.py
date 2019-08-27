"""data classes

Revision ID: 62be469e01a1
Revises: 88f4ca055ae7
Create Date: 2019-08-12 15:30:53.291713

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
import logging

# revision identifiers, used by Alembic.
revision = '62be469e01a1'
down_revision = '88f4ca055ae7'
branch_labels = None
depends_on = None

logger = logging.getLogger("alembic")


def upgrade():
    op.execute("create schema if not exists metadata")
    op.execute('SET search_path TO metadata')
    logger.info("creating metadata tables")

    op.create_table(
        'data_store',
        sa.Column('data_store_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, comment='data store detail name', index=True),
        sa.Column('description', sa.String, comment='explanation behind data store and use case'),
        sa.Column('time_relevance', sa.Integer,
                  comment='how long before this data store becomes stale, measured in DAYS'),
        sa.Column('last_updated', sa.DateTime, comment='last time data store was updated from sources'),

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

    op.create_table(
        'data_format_code',
        sa.Column('data_format_code', sa.String(50), primary_key=True,
                  comment='source data format - options: wms, csv, excel, sqlite, text, json'),
        sa.Column('description', sa.String, comment='code type description'),

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

    op.create_table(
        'data_source',
        sa.Column('data_source_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, comment='data source detail name', index=True),
        sa.Column('description', sa.String, comment='explanation behind data source and use case'),
        sa.Column('source_url', sa.String, comment='root source url of data'),
        sa.Column('data_format_code', sa.String, ForeignKey('metadata.data_format_code.data_format_code'),
                  comment='format type of the source information'),
        sa.Column('data_store_id', sa.Integer, ForeignKey('metadata.data_store.data_store_id'),
                  comment='related data store where this sources data is held after ETL'),

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

    op.create_table(
        'api_catalogue',
        sa.Column('api_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, comment='api endpoint description'),
        sa.Column('url', sa.String, comment='an internal api endpoint that serves all data points for a display layer'),

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

    op.create_table(
        'wms_catalogue',
        sa.Column('wms_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, comment='wms layer description'),
        sa.Column('wms_name', sa.String, comment='identifying layer name with the data bc wms server'),
        sa.Column('wms_style', sa.String, comment='style key to display data in different '
                                                  'visualizations for wms layer'),

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

    # op.create_table(
    #     'component_type_code',
    #     sa.Column('component_type_code', sa.String, primary_key=True,
    #               comment='components have many different types, which determines what business logic to use when '
    #                       'constructing the component.'),
    #     sa.Column('description', sa.String, comment='explanation of component type and use case'),
    #
    #     sa.Column('create_user', sa.String(100), comment='The user who created this record in the database.'),
    #     sa.Column('create_date', sa.DateTime, comment='Date and time (UTC) when the physical record was '
    #                                                   'created in the database.'),
    #     sa.Column('update_user', sa.String(100), comment='The user who last updated this record in the database.'),
    #     sa.Column('update_date', sa.DateTime, comment='Date and time (UTC) when the physical record was updated '
    #                                                   'in the database. It will be the same as the create_date until '
    #                                                   'the record is first updated after creation.'),
    #     sa.Column('effective_date', sa.DateTime, comment='The date and time that the code became valid '
    #                                                      'and could be used.'),
    #     sa.Column('expiry_date', sa.DateTime, comment='The date and time after which the code is no longer valid and '
    #                                                   'should not be used.')
    # )

    op.create_table(
        'display_catalogue',
        sa.Column('display_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('display_name', sa.String(200), comment='this is the public name of the display layer'),
        sa.Column('display_data_name', sa.String(200), unique=True, index=True,
                  comment='this is the main business key used throughout the application to identify data '
                          'layers and connect data to templates.'),
        sa.Column('label', sa.String, comment='label for label_column value'),
        sa.Column('label_column', sa.String, comment='we use this column value as a list item title in the client'),
        sa.Column('highlight_columns', sa.ARRAY(sa.String), comment='the key columns that have business value to '
                                                                    'the end user. We primarily will only show these '
                                                                    'columns in the client and report'),
        sa.Column('api_catalogue_id', sa.Integer, ForeignKey('metadata.api_catalogue.api_catalogue_id'),
                  comment='reference to api catalogue item'),
        sa.Column('wms_catalogue_id', sa.Integer, ForeignKey('metadata.wms_catalogue.wms_catalogue_id'),
                  comment='reference to wms catalogue item'),

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

    op.create_table(
        'display_template',
        sa.Column('display_template_id', sa.Integer, primary_key=True),

        sa.Column('title', sa.String, comment='title to be used for headers and labels for template'),
        sa.Column('display_order', sa.Integer, comment='determines which templates are shown first to last in 100s'),

        sa.Column('display_data_names', sa.ARRAY(sa.String), comment='unique business keys that represent the required '
                                                                     'layers used to hydrate this display template'),

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

    op.create_table(
        'display_template_display_catalogue_xref',
        # sa.Column('display_template_display_catalogue_xref_id', sa.Integer, primary_key=True),
        sa.Column('display_template_id', sa.Integer, ForeignKey('metadata.display_template.display_template_id'),
                  primary_key=True),
        sa.Column('display_catalogue_id', sa.Integer, ForeignKey('metadata.display_catalogue.display_catalogue_id'),
                  primary_key=True),

        sa.Column('create_user', sa.String(100), comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime, comment='Date and time (UTC) when the physical record was '
                                                      'created in the database.'),
        sa.Column('update_user', sa.String(100), comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime, comment='Date and time (UTC) when the physical record was updated '
                                                      'in the database. It will be the same as the create_date until '
                                                      'the record is first updated after creation.'),
    )

    op.create_table(
        'chart_component',
        sa.Column('chart_component_id', sa.Integer, primary_key=True),
        sa.Column('chart', sa.JSON, comment='this holds the chart js json schema to use '),
        sa.Column('title', sa.String, comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer, comment='determines which components are shown first to last in 100s'),
        sa.Column('labels_key', sa.String, comment='the key used to generate the labels array'),
        sa.Column('dataset_keys', sa.ARRAY(sa.String),
                  comment='the keys used to generate the raw data for chart datasets'),
        sa.Column('display_template_id', sa.Integer, ForeignKey('metadata.display_template.display_template_id')),

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

    op.create_table(
        'link_component',
        sa.Column('link_component_id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer, comment='determines which components are shown first to last in 100s'),
        sa.Column('link_pattern', sa.String, comment='url pattern to source document or webpage'),
        sa.Column('link_pattern_keys', sa.ARRAY(sa.String), comment='keys to plug into link pattern'),
        sa.Column('display_template_id', sa.Integer, ForeignKey('metadata.display_template.display_template_id')),

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

    op.create_table(
        'image_component',
        sa.Column('image_component_id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer, comment='determines which components are shown first to last in 100s'),
        sa.Column('width', sa.Integer, comment='x size of image'),
        sa.Column('height', sa.Integer, comment='y size of image'),
        sa.Column('url', sa.String, comment='source url to image source'),
        sa.Column('display_template_id', sa.Integer, ForeignKey('metadata.display_template.display_template_id')),

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

    op.create_table(
        'formula_component',
        sa.Column('formula_component_id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer, comment='determines which components are shown first to last in 100s'),
        sa.Column('formula_component', sa.JSON, comment='formula layout for calculation'),
        sa.Column('display_template_id', sa.Integer, ForeignKey('metadata.display_template.display_template_id')),

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

    op.execute('SET search_path TO public')


def downgrade():
    op.execute("drop schema metadata")
    pass
