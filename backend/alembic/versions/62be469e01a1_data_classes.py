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
        'data_mart',
        sa.Column('id', sa.Integer, primary_key=True),
    )

    op.create_table(
        'data_store',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, comment='data store detail name'),
        sa.Column('description', sa.String, comment='explanation behind data store and use case'),
        sa.Column('time_relevance', sa.Integer,
                  comment='how long before this data store becomes stale, measured in DAYS'),
        sa.Column('last_updated', sa.DateTime, comment='last time data store was updated from sources'),
        sa.Column('data_mart_id', sa.Integer, ForeignKey('metadata.data_mart.id'), comment='parent data mart'),
    )

    op.create_table(
        'data_format_type',
        sa.Column('type', sa.String(50), primary_key=True,
                  comment='source data format - options: wms, csv, excel, sqlite, text, json'),
    )

    op.create_table(
        'data_source',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, comment='data source detail name'),
        sa.Column('description', sa.String, comment='explanation behind data source and use case'),
        sa.Column('source_url', sa.String, comment='root source url of data'),
        sa.Column('data_format_type_id', sa.String, ForeignKey('metadata.data_format_type.type'),
                  comment='data format type'),
        sa.Column('data_store_id', sa.Integer, ForeignKey('metadata.data_store.id'), comment='related data store'),
        sa.Column('data_mart_id', sa.Integer, ForeignKey('metadata.data_mart.id'), comment='parent data mart'),
    )

    op.create_table(
        'map_layer_type',
        sa.Column('type', sa.String(50), primary_key=True,
                  comment='type that defines where map layer data comes from - options: api, wms'),
    )

    op.create_table(
        'map_layer',
        sa.Column('layer_id', sa.String, primary_key=True,
                  comment='id used internally map context objects'),
        sa.Column('layer_name', sa.String, comment='name used to represent layer to users'),
        sa.Column('wms_name', sa.String, comment='wms layer id used in all async requests'),
        sa.Column('wms_style', sa.String,
                  comment='wms style identifier to view layer info with different visualizations'),
        sa.Column('api_url', sa.String, comment='api endpoint to get base geojson information'),
        sa.Column('map_layer_type_id', sa.String, ForeignKey('metadata.map_layer_type.type'),
                  comment='this layers source type'),
        sa.Column('data_mart_id', sa.Integer, ForeignKey('metadata.data_mart.id'), comment='parent data mart'),
    )

    op.create_table(
        'context_data',
        sa.Column('context_id', sa.String, primary_key=True,
                  comment='identifies which MapLayer(s) this fixtures belongs to by layer_name, '
                          'a ContextData can be the visualization of two merged MapLayers. '
                          'ex: MapLayer(layer_name=gwells) MapLayer(layer_name=hydat) context_name = gwellshydat'),
        sa.Column('context', sa.String,
                  comment='holds the fixtures schema for this singular or combination of layer(s)'),

        sa.Column('title_column', sa.String, comment='we use this column value as a title in the client'),
        sa.Column('title_label', sa.String, comment='label for title_column value'),

        sa.Column('chart_label_columns', sa.ARRAY(sa.String),
                  comment='column value that represents chart x axis labels'),
        sa.Column('chart_data_columns', sa.ARRAY(sa.String),
                  comment='column value that represents chart x axis values'),

        sa.Column('link_pattern', sa.String, comment='link pattern to source data'),
        sa.Column('link_columns', sa.ARRAY(sa.String),
                  comment='id value(s) to use with link column to reach source data'),

        sa.Column('image_url', sa.String, comment='image representing this context'),
        sa.Column('highlight_columns', sa.JSON,
                  comment='columns to use from the data source, ignore other columns'),
        sa.Column('highlight_descriptions', sa.JSON,
                  comment='explanations of each highlight column and their value'),
        sa.Column('data_mart_id', sa.Integer, ForeignKey('metadata.data_mart.id'), comment='parent data mart'),
    )

    op.execute('SET search_path TO public')


def downgrade():
    op.execute("drop schema metadata")
    pass
