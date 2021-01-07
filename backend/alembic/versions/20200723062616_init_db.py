"""Init db

Revision ID: 603d93ba52ea
Revises: 
Create Date: 2020-07-23 06:26:16.856955

"""
import logging
import uuid
import datetime
import os
import json

from alembic import op
from geoalchemy2 import Geometry

import sqlalchemy as sai
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import BigInteger, Column, DateTime, String, Integer, Float, Index, Table, Text, \
    PrimaryKeyConstraint, ForeignKey, ARRAY, TEXT
from sqlalchemy.dialects import postgresql
import geoalchemy2
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.dialects.postgresql import BYTEA
from api.config import ENV_DEV, ENV_STAGING, WALLY_ENV

import sqlalchemy as sa

logger = logging.getLogger("alembic")

# revision identifiers, used by Alembic.
revision = '603d93ba52ea'
down_revision = None
branch_labels = None
depends_on = None

Base = declarative_base()


# class DataFormatCode(Base):
#     __tablename__ = 'data_format_code'
#     data_format_code = Column(String, primary_key=True, comment='source data format, options: '
#                                                                 'wms, csv, excel, sqlite, text, json')
#     description = Column(String, comment='code type description')


class DataSource(Base):
    __tablename__ = 'data_source'

    data_source_id = Column(Integer, primary_key=True)
    name = Column(String, comment='data source detail name', index=True)
    description = Column(
        String, comment='explanation behind data source and use case')
    source_url = Column(String, comment='root source url of data')
    data_format_code = Column(String, ForeignKey('data_format_code.data_format_code'),
                              comment='format type of the source information')
    data_format = orm.relationship('DataFormatCode')
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


class DataFormatCode(Base):
    __tablename__ = 'data_format_code'
    data_format_code = Column(String, primary_key=True, comment='source data format, options: '
                                                                'wms, csv, excel, sqlite, text, json')
    description = Column(String, comment='code type description')
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


class ComponentTypeCode(Base):
    __tablename__ = 'component_type_code'
    component_type_code = Column(String, primary_key=True,
                                 comment='components have many different types, which determines what business '
                                         'logic to use when constructing the component.')
    description = Column(String, comment='explanation of component type and use case')
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


class ApiCatalogue(Base):
    __tablename__ = 'api_catalogue'
    api_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='api endpoint description')
    url = Column(String,
                 comment='an internal api endpoint that serves all data points for a display layer')
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


class WmsCatalogue(Base):
    __tablename__ = 'wms_catalogue'
    wms_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='wms layer description')
    wms_name = Column(String, comment='identifying layer name with the data bc wms server')
    wms_style = Column(String,
                       comment='style key to display data in different visualizations for wms layer')
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


class VectorCatalogue(Base):
    __tablename__ = 'vector_catalogue'
    vector_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='vector layer description')
    vector_name = Column(String, comment='identifying vector layer name')
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


class DisplayCatalogue(Base):
    __tablename__ = 'display_catalogue'
    display_catalogue_id = Column(Integer, primary_key=True)

    display_name = Column(String, comment='this is the public name of the display layer')
    display_data_name = Column(String(200), unique=True,
                               comment='this is the main business key used throughout the application to '
                                       'identify data layers and connect data to templates.')
    label = Column(String, comment='label for label_column value')
    label_column = Column(String,
                          comment='we use this column value as a list item label in the client')
    highlight_columns = Column(ARRAY(TEXT),
                               comment='the key columns that have business value to the end user. '
                                       'We primarily will only show these columns in the '
                                       'client and report')

    api_catalogue_id = Column(Integer, ForeignKey('api_catalogue.api_catalogue_id'),
                              comment='references api catalogue item')
    api_catalogue = orm.relationship("ApiCatalogue")

    wms_catalogue_id = Column(Integer, ForeignKey('wms_catalogue.wms_catalogue_id'),
                              comment='references wms catalogue item')
    wms_catalogue = orm.relationship("WmsCatalogue")

    vector_catalogue_id = Column(Integer, ForeignKey('vector_catalogue.vector_catalogue_id'),
                                 comment='references vector catalogue item')
    vector_catalogue = orm.relationship("VectorCatalogue")
    create_user = Column(String(100),
                         comment='The user who created this record in the database.')
    create_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100),
                         comment='The user who last updated this record in the database.')
    update_date = Column(DateTime,
                         comment='Date and time (UTC) when the physical record was updated in the database. '
                                 'It will be the same as the create_date until the record is first '
                                 'updated after creation.')
    effective_date = Column(DateTime,
                            comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime,
                         comment='The date and time after which the code is no longer valid and '
                                 'should not be used.')


def upgrade():
    op.execute("create schema if not exists public")
    if WALLY_ENV == ENV_DEV:
        logger.info("create extension")
        op.execute("CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public")
        op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.create_table(
        'publisher',
        sa.Column('publisher_guid', UUID(as_uuid=True), primary_key=True,
                  index=True, default=uuid.uuid4()),
        sa.Column('name', sa.String, index=True, nullable=False),
        sa.Column('description', sa.String),
    )

    op.execute("create  schema if not exists hydat")
    op.execute('SET search_path TO hydat')
    logger.info("creating table hydat.stations")

    op.create_table(
        'agency_list',
        Column('agency_id', BigInteger, unique=True, primary_key=True),
        Column('agency_en', Text),
        Column('agency_fr', Text),
    )

    op.create_table(
        'stations',
        Column('station_number', Text, unique=True, primary_key=True),
        Column('station_name', Text),
        Column('prov_terr_state_loc', Text),
        Column('regional_office_id', Text),
        Column('hyd_status', Text),
        Column('sed_status', Text),
        Column('latitude', DOUBLE_PRECISION),
        Column('longitude', DOUBLE_PRECISION),
        Column('drainage_area_gross', DOUBLE_PRECISION),
        Column('drainage_area_effect', DOUBLE_PRECISION),
        Column('rhbn', BigInteger),
        Column('real_time', BigInteger),
        Column('contributor_id', BigInteger),
        Column('operator_id', BigInteger, index=True),
        Column('datum_id', BigInteger),
    )

    op.create_table(
        'annual_instant_peaks',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('peak_code', Text, primary_key=True),
        Column('precision_code', BigInteger, index=True),
        Column('month', BigInteger),
        Column('day', BigInteger),
        Column('hour', BigInteger),
        Column('minute', BigInteger),
        Column('time_zone', Text),
        Column('peak', DOUBLE_PRECISION),
        Column('symbol', Text),
        Index('idx_20802_annual_instant_peaks___uniqueindex', 'station_number', 'data_type', 'year',
              'peak_code', unique=True),
    )

    op.create_table(
        'annual_statistics',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('mean', DOUBLE_PRECISION),
        Column('min_month', BigInteger),
        Column('min_day', BigInteger),
        Column('min', DOUBLE_PRECISION),
        Column('min_symbol', Text),
        Column('max_month', BigInteger),
        Column('max_day', BigInteger),
        Column('max', DOUBLE_PRECISION),
        Column('max_symbol', Text),
        Index('idx_20940_annual_statistics_primarykey', 'station_number', 'data_type', 'year',
              unique=True),
    )

    op.create_table(
        'concentration_symbols',
        Column('concentration_symbol', Text, unique=True, primary_key=True),
        Column('concentration_en', Text),
        Column('concentration_fr', Text),
    )

    op.create_table(
        'data_symbols',
        Column('symbol_id', Text, unique=True, primary_key=True),
        Column('symbol_en', Text),
        Column('symbol_fr', Text),
    )

    op.create_table(
        'data_types',
        Column('data_type', Text, unique=True, primary_key=True),
        Column('data_type_en', Text),
        Column('data_type_fr', Text),
    )

    op.create_table(
        'datum_list',
        Column('datum_id', BigInteger, unique=True, primary_key=True),
        Column('datum_en', Text),
        Column('datum_fr', Text),
    )

    op.create_table(
        'dly_flows',
        Column('station_number', Text, ForeignKey(
            'hydat.stations.station_number'), primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('month', BigInteger, primary_key=True),
        Column('full_month', BigInteger),
        Column('no_days', BigInteger),
        Column('monthly_mean', DOUBLE_PRECISION),
        Column('monthly_total', DOUBLE_PRECISION),
        Column('first_day_min', BigInteger),
        Column('min', DOUBLE_PRECISION),
        Column('first_day_max', BigInteger),
        Column('max', DOUBLE_PRECISION),
        Column('flow1', DOUBLE_PRECISION),
        Column('flow_symbol1', Text),
        Column('flow2', DOUBLE_PRECISION),
        Column('flow_symbol2', Text),
        Column('flow3', DOUBLE_PRECISION),
        Column('flow_symbol3', Text),
        Column('flow4', DOUBLE_PRECISION),
        Column('flow_symbol4', Text),
        Column('flow5', DOUBLE_PRECISION),
        Column('flow_symbol5', Text),
        Column('flow6', DOUBLE_PRECISION),
        Column('flow_symbol6', Text),
        Column('flow7', DOUBLE_PRECISION),
        Column('flow_symbol7', Text),
        Column('flow8', DOUBLE_PRECISION),
        Column('flow_symbol8', Text),
        Column('flow9', DOUBLE_PRECISION),
        Column('flow_symbol9', Text),
        Column('flow10', DOUBLE_PRECISION),
        Column('flow_symbol10', Text),
        Column('flow11', DOUBLE_PRECISION),
        Column('flow_symbol11', Text),
        Column('flow12', DOUBLE_PRECISION),
        Column('flow_symbol12', Text),
        Column('flow13', DOUBLE_PRECISION),
        Column('flow_symbol13', Text),
        Column('flow14', DOUBLE_PRECISION),
        Column('flow_symbol14', Text),
        Column('flow15', DOUBLE_PRECISION),
        Column('flow_symbol15', Text),
        Column('flow16', DOUBLE_PRECISION),
        Column('flow_symbol16', Text),
        Column('flow17', DOUBLE_PRECISION),
        Column('flow_symbol17', Text),
        Column('flow18', DOUBLE_PRECISION),
        Column('flow_symbol18', Text),
        Column('flow19', DOUBLE_PRECISION),
        Column('flow_symbol19', Text),
        Column('flow20', DOUBLE_PRECISION),
        Column('flow_symbol20', Text),
        Column('flow21', DOUBLE_PRECISION),
        Column('flow_symbol21', Text),
        Column('flow22', DOUBLE_PRECISION),
        Column('flow_symbol22', Text),
        Column('flow23', DOUBLE_PRECISION),
        Column('flow_symbol23', Text),
        Column('flow24', DOUBLE_PRECISION),
        Column('flow_symbol24', Text),
        Column('flow25', DOUBLE_PRECISION),
        Column('flow_symbol25', Text),
        Column('flow26', DOUBLE_PRECISION),
        Column('flow_symbol26', Text),
        Column('flow27', DOUBLE_PRECISION),
        Column('flow_symbol27', Text),
        Column('flow28', DOUBLE_PRECISION),
        Column('flow_symbol28', Text),
        Column('flow29', DOUBLE_PRECISION),
        Column('flow_symbol29', Text),
        Column('flow30', DOUBLE_PRECISION),
        Column('flow_symbol30', Text),
        Column('flow31', DOUBLE_PRECISION),
        Column('flow_symbol31', Text),
        Index('idx_20862_dly_flows_primarykey', 'station_number', 'year', 'month', unique=True),
    )

    op.create_table(
        'dly_levels',
        Column('station_number', Text, ForeignKey(
            'hydat.stations.station_number'), primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('month', BigInteger, primary_key=True),
        Column('precision_code', BigInteger),
        Column('full_month', BigInteger),
        Column('no_days', BigInteger),
        Column('monthly_mean', DOUBLE_PRECISION),
        Column('monthly_total', DOUBLE_PRECISION),
        Column('first_day_min', BigInteger),
        Column('min', DOUBLE_PRECISION),
        Column('first_day_max', BigInteger),
        Column('max', DOUBLE_PRECISION),
        Column('level1', DOUBLE_PRECISION),
        Column('level_symbol1', Text),
        Column('level2', DOUBLE_PRECISION),
        Column('level_symbol2', Text),
        Column('level3', DOUBLE_PRECISION),
        Column('level_symbol3', Text),
        Column('level4', DOUBLE_PRECISION),
        Column('level_symbol4', Text),
        Column('level5', DOUBLE_PRECISION),
        Column('level_symbol5', Text),
        Column('level6', DOUBLE_PRECISION),
        Column('level_symbol6', Text),
        Column('level7', DOUBLE_PRECISION),
        Column('level_symbol7', Text),
        Column('level8', DOUBLE_PRECISION),
        Column('level_symbol8', Text),
        Column('level9', DOUBLE_PRECISION),
        Column('level_symbol9', Text),
        Column('level10', DOUBLE_PRECISION),
        Column('level_symbol10', Text),
        Column('level11', DOUBLE_PRECISION),
        Column('level_symbol11', Text),
        Column('level12', DOUBLE_PRECISION),
        Column('level_symbol12', Text),
        Column('level13', DOUBLE_PRECISION),
        Column('level_symbol13', Text),
        Column('level14', DOUBLE_PRECISION),
        Column('level_symbol14', Text),
        Column('level15', DOUBLE_PRECISION),
        Column('level_symbol15', Text),
        Column('level16', DOUBLE_PRECISION),
        Column('level_symbol16', Text),
        Column('level17', DOUBLE_PRECISION),
        Column('level_symbol17', Text),
        Column('level18', DOUBLE_PRECISION),
        Column('level_symbol18', Text),
        Column('level19', DOUBLE_PRECISION),
        Column('level_symbol19', Text),
        Column('level20', DOUBLE_PRECISION),
        Column('level_symbol20', Text),
        Column('level21', DOUBLE_PRECISION),
        Column('level_symbol21', Text),
        Column('level22', DOUBLE_PRECISION),
        Column('level_symbol22', Text),
        Column('level23', DOUBLE_PRECISION),
        Column('level_symbol23', Text),
        Column('level24', DOUBLE_PRECISION),
        Column('level_symbol24', Text),
        Column('level25', DOUBLE_PRECISION),
        Column('level_symbol25', Text),
        Column('level26', DOUBLE_PRECISION),
        Column('level_symbol26', Text),
        Column('level27', DOUBLE_PRECISION),
        Column('level_symbol27', Text),
        Column('level28', DOUBLE_PRECISION),
        Column('level_symbol28', Text),
        Column('level29', DOUBLE_PRECISION),
        Column('level_symbol29', Text),
        Column('level30', DOUBLE_PRECISION),
        Column('level_symbol30', Text),
        Column('level31', DOUBLE_PRECISION),
        Column('level_symbol31', Text),
        Index('idx_20916_dly_levels_primarykey', 'station_number', 'year', 'month', unique=True),
    )

    op.create_table(
        'measurement_codes',
        Column('measurement_code', Text, unique=True, primary_key=True),
        Column('measurement_en', Text),
        Column('measurement_fr', Text),
    )

    op.create_table(
        'operation_codes',
        Column('operation_code', Text, unique=True, primary_key=True),
        Column('operation_en', Text),
        Column('operation_fr', Text),
    )

    op.create_table(
        'peak_codes',
        Column('peak_code', Text, unique=True, primary_key=True),
        Column('peak_en', Text),
        Column('peak_fr', Text),
    )

    op.create_table(
        'precision_codes',
        Column('precision_code', BigInteger, unique=True, primary_key=True),
        Column('precision_en', Text),
        Column('precision_fr', Text),
    )

    op.create_table(
        'regional_office_list',
        Column('regional_office_id', BigInteger, unique=True, primary_key=True),
        Column('regional_office_name_en', Text),
        Column('regional_office_name_fr', Text),
    )

    op.create_table(
        'sample_remark_codes',
        Column('sample_remark_code', BigInteger, unique=True, primary_key=True),
        Column('sample_remark_en', Text),
        Column('sample_remark_fr', Text),
    )

    op.create_table(
        'sed_data_types',
        Column('sed_data_type', Text, unique=True, primary_key=True),
        Column('sed_data_type_en', Text),
        Column('sed_data_type_fr', Text),
    )

    op.create_table(
        'sed_dly_loads',
        Column('station_number', Text, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('month', BigInteger, primary_key=True),
        Column('full_month', BigInteger),
        Column('no_days', BigInteger),
        Column('monthly_mean', DOUBLE_PRECISION),
        Column('monthly_total', DOUBLE_PRECISION),
        Column('first_day_min', BigInteger),
        Column('min', DOUBLE_PRECISION),
        Column('first_day_max', BigInteger),
        Column('max', DOUBLE_PRECISION),
        Column('load1', DOUBLE_PRECISION),
        Column('load2', DOUBLE_PRECISION),
        Column('load3', DOUBLE_PRECISION),
        Column('load4', DOUBLE_PRECISION),
        Column('load5', DOUBLE_PRECISION),
        Column('load6', DOUBLE_PRECISION),
        Column('load7', DOUBLE_PRECISION),
        Column('load8', DOUBLE_PRECISION),
        Column('load9', DOUBLE_PRECISION),
        Column('load10', DOUBLE_PRECISION),
        Column('load11', DOUBLE_PRECISION),
        Column('load12', DOUBLE_PRECISION),
        Column('load13', DOUBLE_PRECISION),
        Column('load14', DOUBLE_PRECISION),
        Column('load15', DOUBLE_PRECISION),
        Column('load16', DOUBLE_PRECISION),
        Column('load17', DOUBLE_PRECISION),
        Column('load18', DOUBLE_PRECISION),
        Column('load19', DOUBLE_PRECISION),
        Column('load20', DOUBLE_PRECISION),
        Column('load21', DOUBLE_PRECISION),
        Column('load22', DOUBLE_PRECISION),
        Column('load23', DOUBLE_PRECISION),
        Column('load24', DOUBLE_PRECISION),
        Column('load25', DOUBLE_PRECISION),
        Column('load26', DOUBLE_PRECISION),
        Column('load27', DOUBLE_PRECISION),
        Column('load28', DOUBLE_PRECISION),
        Column('load29', DOUBLE_PRECISION),
        Column('load30', DOUBLE_PRECISION),
        Column('load31', DOUBLE_PRECISION),
        Index('idx_20910_sed_dly_loads_primarykey', 'station_number', 'year', 'month', unique=True),
    )

    op.create_table(
        'sed_dly_suscon',
        Column('station_number', Text, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('month', BigInteger, primary_key=True),
        Column('full_month', BigInteger),
        Column('no_days', BigInteger),
        Column('monthly_total', DOUBLE_PRECISION),
        Column('first_day_min', BigInteger),
        Column('min', DOUBLE_PRECISION),
        Column('first_day_max', BigInteger),
        Column('max', DOUBLE_PRECISION),
        Column('suscon1', DOUBLE_PRECISION),
        Column('suscon_symbol1', Text),
        Column('suscon2', DOUBLE_PRECISION),
        Column('suscon_symbol2', Text),
        Column('suscon3', DOUBLE_PRECISION),
        Column('suscon_symbol3', Text),
        Column('suscon4', DOUBLE_PRECISION),
        Column('suscon_symbol4', Text),
        Column('suscon5', DOUBLE_PRECISION),
        Column('suscon_symbol5', Text),
        Column('suscon6', DOUBLE_PRECISION),
        Column('suscon_symbol6', Text),
        Column('suscon7', DOUBLE_PRECISION),
        Column('suscon_symbol7', Text),
        Column('suscon8', DOUBLE_PRECISION),
        Column('suscon_symbol8', Text),
        Column('suscon9', DOUBLE_PRECISION),
        Column('suscon_symbol9', Text),
        Column('suscon10', DOUBLE_PRECISION),
        Column('suscon_symbol10', Text),
        Column('suscon11', DOUBLE_PRECISION),
        Column('suscon_symbol11', Text),
        Column('suscon12', DOUBLE_PRECISION),
        Column('suscon_symbol12', Text),
        Column('suscon13', DOUBLE_PRECISION),
        Column('suscon_symbol13', Text),
        Column('suscon14', DOUBLE_PRECISION),
        Column('suscon_symbol14', Text),
        Column('suscon15', DOUBLE_PRECISION),
        Column('suscon_symbol15', Text),
        Column('suscon16', DOUBLE_PRECISION),
        Column('suscon_symbol16', Text),
        Column('suscon17', DOUBLE_PRECISION),
        Column('suscon_symbol17', Text),
        Column('suscon18', DOUBLE_PRECISION),
        Column('suscon_symbol18', Text),
        Column('suscon19', DOUBLE_PRECISION),
        Column('suscon_symbol19', Text),
        Column('suscon20', DOUBLE_PRECISION),
        Column('suscon_symbol20', Text),
        Column('suscon21', DOUBLE_PRECISION),
        Column('suscon_symbol21', Text),
        Column('suscon22', DOUBLE_PRECISION),
        Column('suscon_symbol22', Text),
        Column('suscon23', DOUBLE_PRECISION),
        Column('suscon_symbol23', Text),
        Column('suscon24', DOUBLE_PRECISION),
        Column('suscon_symbol24', Text),
        Column('suscon25', DOUBLE_PRECISION),
        Column('suscon_symbol25', Text),
        Column('suscon26', DOUBLE_PRECISION),
        Column('suscon_symbol26', Text),
        Column('suscon27', DOUBLE_PRECISION),
        Column('suscon_symbol27', Text),
        Column('suscon28', DOUBLE_PRECISION),
        Column('suscon_symbol28', Text),
        Column('suscon29', DOUBLE_PRECISION),
        Column('suscon_symbol29', Text),
        Column('suscon30', DOUBLE_PRECISION),
        Column('suscon_symbol30', Text),
        Column('suscon31', DOUBLE_PRECISION),
        Column('suscon_symbol31', Text),
        Index('idx_20886_sed_dly_suscon_primarykey', 'station_number', 'year', 'month',
              unique=True),
    )

    op.create_table(
        'sed_samples',
        Column('station_number', Text, primary_key=True),
        Column('sed_data_type', Text, primary_key=True),
        Column('date', DateTime(True), primary_key=True),
        Column('sample_remark_code', Text, index=True),
        Column('time_symbol', Text),
        Column('flow', DOUBLE_PRECISION),
        Column('flow_symbol', Text),
        Column('sampler_type', Text),
        Column('sampling_vertical_location', Text),
        Column('sampling_vertical_symbol', Text),
        Column('temperature', DOUBLE_PRECISION),
        Column('concentration', DOUBLE_PRECISION),
        Column('concentration_symbol', Text),
        Column('dissolved_solids', DOUBLE_PRECISION),
        Column('sample_depth', DOUBLE_PRECISION),
        Column('streambed', Text),
        Column('sv_depth1', DOUBLE_PRECISION),
        Column('sv_depth2', DOUBLE_PRECISION),
        Index('idx_20970_sed_samples_primarykey', 'station_number', 'sed_data_type', 'date',
              unique=True),
    )

    op.create_table(
        'sed_samples_psd',
        Column('station_number', Text, primary_key=True),
        Column('sed_data_type', Text, primary_key=True),
        Column('date', DateTime(True), primary_key=True),
        Column('particle_size', DOUBLE_PRECISION, primary_key=True),
        Column('percent', BigInteger),
        Index('idx_20796_sed_samples_psd_primarykey', 'station_number', 'sed_data_type', 'date',
              'particle_size', unique=True),
    )

    op.create_table(
        'sed_vertical_location',
        Column('sampling_vertical_location_id', Text, unique=True, primary_key=True),
        Column('sampling_vertical_location_en', Text),
        Column('sampling_vertical_location_fr', Text),
    )

    op.create_table(
        'sed_vertical_symbols',
        Column('sampling_vertical_symbol', Text, unique=True, primary_key=True),
        Column('sampling_vertical_en', Text),
        Column('sampling_vertical_fr', Text),
    )

    op.create_table(
        'stn_data_collection',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('year_from', BigInteger, primary_key=True),
        Column('year_to', BigInteger),
        Column('measurement_code', Text),
        Column('operation_code', Text),
        Index('idx_20826_stn_data_collection___uniqueindex', 'station_number', 'data_type',
              'year_from', unique=True),
    )

    op.create_table(
        'stn_data_range',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('sed_data_type', Text, primary_key=True),
        Column('year_from', BigInteger),
        Column('year_to', BigInteger),
        Column('record_length', BigInteger),
        Index('idx_20898_stn_data_range_primarykey', 'station_number', 'data_type', 'sed_data_type',
              unique=True),
    )

    op.create_table(
        'stn_datum_conversion',
        Column('station_number', Text, primary_key=True),
        Column('datum_id_from', BigInteger, primary_key=True),
        Column('datum_id_to', BigInteger, primary_key=True),
        Column('conversion_factor', DOUBLE_PRECISION),
        Index('idx_20874_stn_datum_conversion_primarykey', 'station_number', 'datum_id_from',
              'datum_id_to', unique=True),
    )

    op.create_table(
        'stn_datum_unrelated',
        Column('station_number', Text, primary_key=True),
        Column('datum_id', BigInteger, primary_key=True),
        Column('year_from', DateTime(True)),
        Column('year_to', DateTime(True)),
        Index('idx_20808_stn_datum_unrelated_primarykey', 'station_number', 'datum_id',
              unique=True),
    )

    op.create_table(
        'stn_operation_schedule',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('month_from', Text),
        Column('month_to', Text),
        Index('idx_20892_stn_operation_schedule___uniqueindex', 'station_number', 'data_type',
              'year', unique=True),
    )

    op.create_table(
        'stn_regulation',
        Column('station_number', Text, unique=True, primary_key=True),
        Column('year_from', BigInteger),
        Column('year_to', BigInteger),
        Column('regulated', BigInteger),
    )

    op.create_table(
        'stn_remark_codes',
        Column('remark_type_code', BigInteger, unique=True, primary_key=True),
        Column('remark_type_en', Text),
        Column('remark_type_fr', Text),
    )

    op.create_table(
        'stn_remarks',
        Column('station_number', Text, primary_key=True),
        Column('remark_type_code', BigInteger, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('remark_en', Text),
        Column('remark_fr', Text),
        Index('idx_20868_stn_remarks___uniqueindex', 'station_number', 'remark_type_code', 'year',
              unique=True),
    )

    op.create_table(
        'stn_status_codes',
        Column('status_code', Text, unique=True, primary_key=True),
        Column('status_en', Text),
        Column('status_fr', Text),
    )

    op.create_table(
        'version',
        Column('version', Text, primary_key=True),
        Column('date', DateTime(True)),
    )

    op.execute('SET search_path TO public')

    # Add Geom column
    op.execute("""
    alter table hydat.stations add column
        geom geometry('POINT', 4326);
    """)
    op.execute("""
        CREATE INDEX stations_geom_idx ON hydat.stations USING GIST (geom);
    """)

    # Data classes
    op.execute("create schema if not exists metadata")
    op.execute('SET search_path TO metadata')
    logger.info("creating metadata tables")

    op.create_table(
        'data_store',
        sa.Column('data_store_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, comment='data store detail name',
                  index=True),
        sa.Column('description', sa.String, comment='explanation behind data store and use case'),
        sa.Column('time_relevance', sa.Integer,
                  comment='how long before this data store becomes stale, measured in DAYS'),
        sa.Column('last_updated', sa.DateTime,
                  comment='last time data store was updated from sources'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'data_format_code',
        sa.Column('data_format_code', sa.String(50), primary_key=True,
                  comment='source data format - options: wms, csv, excel, sqlite, text, json'),
        sa.Column('description', sa.String, comment='code type description'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'data_source',
        sa.Column('data_source_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, comment='data source detail name',
                  index=True),
        sa.Column('description', sa.String, comment='explanation behind data source and use case'),
        sa.Column('source_url', sa.String, comment='root source url of data'),
        sa.Column('data_format_code', sa.String,
                  ForeignKey('metadata.data_format_code.data_format_code'),
                  comment='format type of the source information'),
        sa.Column('data_store_id', sa.Integer, ForeignKey('metadata.data_store.data_store_id'),
                  comment='related data store where this sources data is held after ETL'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'api_catalogue',
        sa.Column('api_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, comment='api endpoint description'),
        sa.Column('url', sa.String,
                  comment='an internal api endpoint that serves all data points for a display layer'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'wms_catalogue',
        sa.Column('wms_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, comment='wms layer description'),
        sa.Column('wms_name', sa.String,
                  comment='identifying layer name with the data bc wms server'),
        sa.Column('wms_style', sa.String, comment='style key to display data in different '
                                                  'visualizations for wms layer'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'component_type_code',
        sa.Column('component_type_code', sa.String, primary_key=True,
                  comment='components have many different types, which determines what business logic to use when '
                          'constructing the component.'),
        sa.Column('description', sa.String, comment='explanation of component type and use case'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'display_catalogue',
        sa.Column('display_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('display_name', sa.String(200),
                  comment='this is the public name of the display layer'),
        sa.Column('display_data_name', sa.String(200), unique=True, index=True,
                  comment='this is the main business key used throughout the application to identify data '
                          'layers and connect data to templates.'),
        sa.Column('label', sa.String, comment='label for label_column value'),
        sa.Column('label_column', sa.String,
                  comment='we use this column value as a list item title in the client'),
        sa.Column('highlight_columns', ARRAY(TEXT),
                  comment='the key columns that have business value to '
                          'the end user. We primarily will only show these '
                          'columns in the client and report'),
        sa.Column('api_catalogue_id', sa.Integer,
                  ForeignKey('metadata.api_catalogue.api_catalogue_id'),
                  comment='reference to api catalogue item'),
        sa.Column('wms_catalogue_id', sa.Integer,
                  ForeignKey('metadata.wms_catalogue.wms_catalogue_id'),
                  comment='reference to wms catalogue item'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'display_template',
        sa.Column('display_template_id', sa.Integer, primary_key=True),

        sa.Column('title', sa.String,
                  comment='title to be used for headers and labels for template'),
        sa.Column('display_order', sa.Integer,
                  comment='determines which templates are shown first to last in 100s'),

        sa.Column('display_data_names', ARRAY(TEXT),
                  comment='unique business keys that represent the required '
                          'layers used to hydrate this display template'),
        sa.Column('override_key', sa.String, unique=True,
                  comment='unique business key that is used to override '
                          'default builder method during template hydration.'
                          'optional field, if null then use default builder'),
        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'display_template_display_catalogue_xref',
        # sa.Column('display_template_display_catalogue_xref_id', sa.Integer, primary_key=True),
        sa.Column('display_template_id', sa.Integer,
                  ForeignKey('metadata.display_template.display_template_id'),
                  primary_key=True),
        sa.Column('display_catalogue_id', sa.Integer,
                  ForeignKey('metadata.display_catalogue.display_catalogue_id'),
                  primary_key=True),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'chart_component',
        sa.Column('chart_component_id', sa.Integer, primary_key=True),
        sa.Column('chart', sa.JSON, comment='this holds the chart js json schema to use '),
        sa.Column('chart_title', sa.String,
                  comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer,
                  comment='determines which components are shown first to last in 100s'),
        sa.Column('labels_key', sa.String, comment='the key used to generate the labels array'),
        sa.Column('dataset_keys', ARRAY(TEXT),
                  comment='the keys used to generate the raw data for chart datasets'),
        sa.Column('display_template_id', sa.Integer,
                  ForeignKey('metadata.display_template.display_template_id')),
        sa.Column('component_type_code', sa.String,
                  ForeignKey('metadata.component_type_code.component_type_code'),
                  comment='component type used for rendering functionality'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'link_component',
        sa.Column('link_component_id', sa.Integer, primary_key=True),
        sa.Column('link_title', sa.String,
                  comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer,
                  comment='determines which components are shown first to last in 100s'),
        sa.Column('link_pattern', sa.String, comment='url pattern to source document or webpage'),
        sa.Column('link_pattern_keys', ARRAY(TEXT), comment='keys to plug into link pattern'),
        sa.Column('display_template_id', sa.Integer,
                  ForeignKey('metadata.display_template.display_template_id')),
        sa.Column('component_type_code', sa.String,
                  ForeignKey('metadata.component_type_code.component_type_code'),
                  comment='component type used for rendering functionality'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'image_component',
        sa.Column('image_component_id', sa.Integer, primary_key=True),
        sa.Column('image_title', sa.String,
                  comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer,
                  comment='determines which components are shown first to last in 100s'),
        sa.Column('width', sa.Integer, comment='x size of image'),
        sa.Column('height', sa.Integer, comment='y size of image'),
        sa.Column('url', sa.String, comment='source url to image source'),
        sa.Column('display_template_id', sa.Integer,
                  ForeignKey('metadata.display_template.display_template_id')),
        sa.Column('component_type_code', sa.String,
                  ForeignKey('metadata.component_type_code.component_type_code'),
                  comment='component type used for rendering functionality'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.create_table(
        'formula_component',
        sa.Column('formula_component_id', sa.Integer, primary_key=True),
        sa.Column('formula_title', sa.String,
                  comment='title to be used for headers and labels for components'),
        sa.Column('display_order', sa.Integer,
                  comment='determines which components are shown first to last in 100s'),
        sa.Column('formula_component', sa.JSON, comment='formula layout for calculation'),
        sa.Column('component_type_code', sa.String,
                  ForeignKey('metadata.component_type_code.component_type_code'),
                  comment='component type used for rendering functionality'),
        sa.Column('display_template_id', sa.Integer,
                  ForeignKey('metadata.display_template.display_template_id')),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.execute('SET search_path TO public')

    # add vector support to catalogue
    op.execute('SET search_path TO metadata')
    op.create_table(
        'vector_catalogue',
        sa.Column('vector_catalogue_id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, comment='vector layer description'),
        sa.Column('vector_name', sa.String, comment='identifying vector layer name'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was '
                          'created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated '
                          'in the database. It will be the same as the create_date until '
                          'the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid '
                          'and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and '
                          'should not be used.')
    )

    op.add_column(
        'display_catalogue',
        sa.Column('vector_catalogue_id', sa.Integer,
                  sa.ForeignKey('metadata.vector_catalogue.vector_catalogue_id'),
                  comment='reference to vector catalogue item'),
    )
    op.execute('SET search_path TO public')

    # add parcel table
    op.create_table(
        "parcel",
        Column("geom", Geometry('MULTIPOLYGON', 4326)),
        Column("PARCEL_FABRIC_POLY_ID", BigInteger,
               unique=True, primary_key=True),
        Column("PIN", BigInteger),
        Column("PID", Text),
        Column("PID_NUMBER", BigInteger),
        Column("PARCEL_NAME", Text),
        Column("PLAN_NUMBER", BigInteger)
    )

    # add parcel to search
    op.execute("""
        CREATE MATERIALIZED VIEW geocode_lookup AS

        SELECT
        ST_AsText(stn.geom) AS center,
        stn.station_number AS primary_id,
        stn.station_name AS name,
        'Stream station' AS kind,
        'hydrometric_stream_data' AS layer,
        to_tsvector(concat_ws(' ',stn.station_number, stn.station_name)) AS tsv
        FROM hydat.stations AS stn

        UNION
        SELECT
        ST_AsText(ST_Centroid(parcel.geom)) AS center,
        coalesce(parcel."PID", parcel."PARCEL_NAME"::text) AS primary_id,
        NULL AS name,
        'Parcel' AS kind,
        'parcel_fabric' AS layer,
        to_tsvector(coalesce(parcel."PID"::text, parcel."PARCEL_NAME"::text)) AS tsv
        FROM parcel
    """)
    op.execute("""
    create index idx_geocode_tsv ON geocode_lookup USING GIN(tsv)
    """)

    # Added wms db layer tables
    logger.info("creating wms data tables")

    op.create_table(
        'automated_snow_weather_station_locations',

        sa.Column('SNOW_ASWS_STN_ID', sa.Integer, primary_key=True,
                  comment='SNOW_ASWS_STN_ID is a system generated unique '
                          'identification number.'),
        sa.Column('LOCATION_ID', sa.String,
                  comment='LOCATION_ID is the unique identifier of the snow weather station, '
                          'e.g. 1C41P.'),
        sa.Column('LOCATION_NAME', sa.String,
                  comment='LOCATION_NAME is the name of the snow weather station, e.g. Yanks Peak.'),
        sa.Column('ELEVATION', sa.Float,
                  comment='ELEVATION the elevation of the snow weather station in metres, e.g. 1670.'),
        sa.Column('STATUS', sa.String,
                  comment='STATUS is the operational status of the snow station, e.g. Active, Inactive.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the '
                          'location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='	LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), of '
                          'the location of the feature as measured from the prime meridian, '
                          'e.g., -123.093544.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates defining '
                          'the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a column required by spatial layers that '
                          'interact with ESRI ArcSDE. It is populated with unique '
                          'values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
    )

    op.create_table(
        'bc_major_watersheds',

        sa.Column('AREA', sa.Float, comment=''),
        sa.Column('PERIMETER', sa.Float, comment=''),
        sa.Column('MAJOR_WATERSHED_CODE', sa.String, comment=''),
        sa.Column('MAJOR_WATERSHED_SYSTEM', sa.String, comment=''),
        sa.Column('FCODE', sa.String, comment=''),
        sa.Column('GEOMETRY', Geometry,
                  comment='GEOMETRY is the column used to reference the spatial coordinates '
                          'defining the feature.'),
        sa.Column('OBJECTID', sa.String, primary_key=True,
                  comment='OBJECTID is a required attribute of feature classes and '
                          'object classes in a geodatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float,
                  comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional '
                          'polygon in square meters'),
        sa.Column('FEATURE_LENGTH_M', sa.Float,
                  comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a '
                          'geometry in meters'),
    )

    op.create_table(
        'bc_wildfire_active_weather_stations',

        sa.Column('WEATHER_STATIONS_ID', sa.Integer, primary_key=True,
                  comment='WEATHER STATION ID is a system generated '
                          'unique identifier number.'),
        sa.Column('STATION_CODE', sa.Integer,
                  comment='STATION_CODE is the internal unique number assigned to this weather '
                          'station, e.g., 67 .'),
        sa.Column('STATION_NAME', sa.String,
                  comment='STATION_NAME is a derived name of a weather station based on geographic '
                          'significance, e.g. HAIG CAMP.'),
        sa.Column('STATION_ACRONYM', sa.String,
                  comment='STATION_ACRONYM is a 4 character airport code for the closest airport to '
                          'the station. This is used for weather forecasting software. This is not '
                          'populated for all weather stations. The leading "C" may be dropped from '
                          'most of the values, e.g.,CYYJ, YVR.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the '
                          'location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), '
                          'of the location of the feature as measured from the prime meridian, '
                          'e.g., -123.093544.'),
        sa.Column('ELEVATION', sa.Float,
                  comment='ELEVATION is the elevation of the weather station in metres above sea level as '
                          'derived from the TRIM DEM.'),
        sa.Column('INSTALL_DATE', sa.DateTime,
                  comment='INSTALL_DATE is the date when the weather station was '
                          'physically installed.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates '
                          'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a column required by spatial layers that interact with '
                          'ESRI ArcSDE. It is populated with '
                          'unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
    )

    op.create_table(
        'cadastral',

        sa.Column('PARCEL_FABRIC_POLY_ID', sa.Integer, primary_key=True,
                  comment='PARCEL_FABRIC_POLY_ID is a system generated '
                          'unique identification number.'),
        sa.Column('PARCEL_NAME', sa.String,
                  comment='PARCEL_NAME is the same as the PID, if there is one. If there is a '
                          'PIN but no PID, then PARCEL_NAME is the PIN. If there is no PID nor '
                          'PIN, then PARCEL_NAME is the parcel class value, e.g., COMMON OWNERSHIP, '
                          'BUILDING STRATA, AIR SPACE, ROAD, PARK.'),
        sa.Column('PLAN_NUMBER', sa.String,
                  comment='PLAN_NUMBER is the Land Act, Land Title Act, or Strata Property Act Plan '
                          'Number for the land survey plan that corresponds to this parcel, e.g., '
                          'VIP1632, NO_PLAN.'),
        sa.Column('PIN', sa.Integer,
                  comment='PIN is the Crown Land Registry Parcel Identifier, if applicable.'),
        sa.Column('PID', sa.String,
                  comment='PID is the Land Title Register parcel identifier, an up-to nine-digit text number '
                          'with leading zeros that uniquely identifies a parcel in the land title register '
                          'of in British Columbia. The registrar assigns PID numbers to parcels for which a '
                          'title is being entered as a registered title. The Land Title Act refers to the '
                          'PID as the permanent parcel identifier.'),
        sa.Column('PID_NUMBER', sa.Integer,
                  comment='PID_NUMBER is the Land Title Register parcel identifier, an up-to nine-digit '
                          'number without leading zeros that uniquely identifies a parcel in the land '
                          'title register of in British Columbia. The registrar assigns PID numbers '
                          'to parcels for which a title is being entered as a registered title. The '
                          'Land Title Act refers to the PID as the permanent parcel identifier.'),
        sa.Column('PARCEL_STATUS', sa.String,
                  comment='PARCEL_STATUS is the status of the parcel, according to the Land Title '
                          'Register or Crown Land Registry, as appropriate, '
                          'i.e., ACTIVE, CANCELLED, INACTIVE, PENDING.'),
        sa.Column('PARCEL_CLASS', sa.String,
                  comment='PARCEL_CLASS is the Parcel classification for maintenance, mapping, '
                          'publishing and analysis, i.e., PRIMARY, SUBDIVISION, PART OF PRIMARY, '
                          'BUILDING STRATA, BARE LAND STRATA, AIR SPACE, ROAD, HIGHWAY, PARK, '
                          'INTEREST, COMMON OWNERSHIP, ABSOLUTE FEE BOOK, CROWN SUBDIVISION, '
                          'RETURN TO CROWN.'),
        sa.Column('OWNER_TYPE', sa.String,
                  comment='OWNER_TYPE is the general ownership category, e.g., PRIVATE, CROWN '
                          'PROVINCIAL, MUNICIPAL. For more information, '
                          'see https://help.ltsa.ca/parcelmap-bc/owner-types-parcelmap-bc'),
        sa.Column('PARCEL_START_DATE', sa.DateTime,
                  comment='PARCEL_START_DATE is the date of the legal event that created '
                          'the parcel, i.e., the date the plan was filed.'),
        sa.Column('MUNICIPALITY', sa.String,
                  comment='MUNICIPALITY is the municipal area within which the parcel is located. '
                          'The value is either RURAL (for parcels in unincorporated regions) or '
                          'the name of a BC municipality.'),
        sa.Column('REGIONAL_DISTRICT', sa.String,
                  comment='REGIONAL_DISTRICT is the name of the regional district in which '
                          'the parcel is located, e.g., CAPITAL REGIONAL DISTRICT.'),
        sa.Column('WHEN_UPDATED', sa.DateTime,
                  comment='WHEN_UPDATED is the date and time the record was last modified.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float,
                  comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional '
                          'polygon in square meters.'),
        sa.Column('FEATURE_LENGTH_M', sa.Float,
                  comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a '
                          'geometry in meters.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates defining '
                          'the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a column required by spatial layers that interact with ESRI '
                          'ArcSDE. It is populated with unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='	SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
    )

    op.create_table(
        'ecocat_water_related_reports',

        sa.Column('REPORT_POINT_ID', sa.Integer, primary_key=True, comment=''),
        sa.Column('FEATURE_CODE', sa.String, comment=''),
        sa.Column('REPORT_ID', sa.Integer, comment=''),
        sa.Column('TITLE', sa.String, comment=''),
        sa.Column('SHORT_DESCRIPTION', sa.String, comment=''),
        sa.Column('AUTHOR', sa.String, comment=''),
        sa.Column('DATE_PUBLISHED', sa.DateTime, comment=''),
        sa.Column('WATERSHED_CODE', sa.String, comment=''),
        sa.Column('WATERBODY_IDENTIFIER', sa.String, comment=''),
        sa.Column('LONG_DESCRIPTION', sa.String, comment=''),
        sa.Column('REPORT_AUDIENCE', sa.String, comment=''),
        sa.Column('GEOMETRY', Geometry, comment=''),
        sa.Column('OBJECTID', sa.Integer, comment=''),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment=''),
    )

    op.create_table(
        'freshwater_atlas_stream_directions',

        sa.Column('STREAM_DIRECTION_ID', sa.Integer,
                  comment='STREAM DIRECTION ID is a surrogate key for the'
                          ' STREAM DIRECTION SP record. i.e. 1'),
        sa.Column('LINEAR_FEATURE_ID', sa.Integer,
                  comment='The LINEAR FEATURE ID is a unique numeric identifier used to '
                          'identify the STREAM NETWORKS SP spatial line that this '
                          'STREAM DIRECTION provides direction for. i.e 7209923'),
        sa.Column('DOWNSTREAM_DIRECTION', sa.Float,
                  comment='DOWNSTREAM DIRECTION is the direction in decimal degrees, '
                          'counterclockwise from east, where east is 0, north is '
                          '90, west is 180, and south is 270, e.g., 179.227053, '
                          'which indicates almost due west.'),
        sa.Column('FEATURE_CODE', sa.String,
                  comment='FEATURE CODE contains a value based on the Canadian Council of Surveys'
                          ' and Mappings (CCSM) system for classification of geographic features.'),
        sa.Column('GEOMETRY', Geometry,
                  comment='GEOMETRY is the column used to reference the spatial coordinates '
                          'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, primary_key=True,
                  comment='OBJECTID is a required attribute of feature classes and '
                          'object classes in a geodatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools '
                          'to store annotation, curve features and CAD data when using '
                          'the SDO_GEOMETRY storage data type.'),
    )

    op.create_table(
        'freshwater_atlas_watersheds',

        sa.Column('WATERSHED_FEATURE_ID', sa.Integer, primary_key=True,
                  comment='A unique identifier for each watershed '
                          'in the layer.'),
        sa.Column('WATERSHED_GROUP_ID', sa.Integer,
                  comment='An automatically generate id that uniquely identifies '
                          'the watershed group feature.'),
        sa.Column('WATERSHED_TYPE', sa.String,
                  comment='The type of watershed. This has yet to be determined for FWA '
                          'version 2.0.0, but possible values may include: R - real '
                          'watershed, F - face unit watershed, '
                          'W - waterbody watershed, etc.'),
        sa.Column('GNIS_ID_1', sa.Integer,
                  comment='The first BCGNIS (BC Geographical Names Information System) feature id '
                          'associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_NAME_1', sa.String,
                  comment='The first BCGNIS (BC Geographical Names Information System) name '
                          'associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_ID_2', sa.Integer,
                  comment='The second BCGNIS (BC Geographical Names Information System) feature '
                          'id associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_NAME_2', sa.String,
                  comment='The second BCGNIS (BC Geographical Names Information System) name '
                          'associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_ID_3', sa.Integer,
                  comment='The third BCGNIS (BC Geographical Names Information System) feature '
                          'id associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_NAME_3', sa.String,
                  comment='The third BCGNIS (BC Geographical Names Information System) name '
                          'associated with the watershed key of the principal watershed.'),
        sa.Column('WATERBODY_ID', sa.Integer,
                  comment='If the principal watershed is made up of a lake or river, this '
                          'field will contain the waterbody id associated with that '
                          'waterbody, otherwise it will be null.'),
        sa.Column('WATERBODY_KEY', sa.Integer,
                  comment='If the principal watershed is made up of a lake or river, this '
                          'field will contain the waterbody key associated with that '
                          'waterbody, otherwise it will be null.'),
        sa.Column('WATERSHED_KEY', sa.Integer,
                  comment='The watershed key associated with the watershed polygon '
                          '(and watershed code).'),
        sa.Column('FWA_WATERSHED_CODE', sa.String,
                  comment='The 143 character watershed code associated with '
                          'the watershed polygon.'),
        sa.Column('LOCAL_WATERSHED_CODE', sa.String,
                  comment='A 143 character code similar to the fwa watershed code '
                          'that further subdivides remnant polygons to provide an '
                          'approximate location along the mainstem.'),
        sa.Column('WATERSHED_GROUP_CODE', sa.String,
                  comment='The watershed group code associated with the polygon.'),
        sa.Column('LEFT_RIGHT_TRIBUTARY', sa.String,
                  comment='A value attributed via the watershed code to all watersheds '
                          'indicating on what side of the watershed they drain into.'),
        sa.Column('WATERSHED_ORDER', sa.Integer,
                  comment='The maximum order of the watershed key associated with the '
                          'principal watershed polygon.'),
        sa.Column('WATERSHED_MAGNITUDE', sa.Integer,
                  comment='The maximum magnitude of the watershed key associated with '
                          'the principal watershed.'),
        sa.Column('LOCAL_WATERSHED_ORDER', sa.Integer,
                  comment='The order associated with the local watershed code.'),
        sa.Column('LOCAL_WATERSHED_MAGNITUDE', sa.Integer,
                  comment='The magnitude associated with the local watershed code.'),
        sa.Column('AREA_HA', sa.Float, comment='Area of the watershed, in hectares.'),
        sa.Column('RIVER_AREA', sa.Float,
                  comment='Area of double line rivers within the watershed, in hectares.'),
        sa.Column('LAKE_AREA', sa.Float,
                  comment='Area of lakes within the watershed, in hectares.'),
        sa.Column('WETLAND_AREA', sa.Float,
                  comment='Area of wetland features within the watershed, in hectares.'),
        sa.Column('MANMADE_AREA', sa.Float,
                  comment='Area of manmade features within the watershed, in hectares.'),
        sa.Column('GLACIER_AREA', sa.Float,
                  comment='Area of glacier features within the watershed, in hectares.'),
        sa.Column('AVERAGE_ELEVATION', sa.Float,
                  comment='The average elevation of the watershed, in meters.'),
        sa.Column('AVERAGE_SLOPE', sa.Float, comment='The average slope of the watershed.'),
        sa.Column('ASPECT_NORTH', sa.Float,
                  comment='The percentage of the watershed that has an aspect within '
                          '45 degrees of north, ie. an aspect between 315 and 45 degrees.'),
        sa.Column('ASPECT_SOUTH', sa.Float,
                  comment='The percentage of the watershed that has an aspect within '
                          '45 degrees of south, ie. an aspect between 135 and 225 degrees.'),
        sa.Column('ASPECT_WEST', sa.Float,
                  comment='The percentage of the watershed that has an aspect within '
                          '45 degrees of west, ie. an aspect between 225 and 315 degrees.'),
        sa.Column('ASPECT_EAST', sa.Float,
                  comment='The percentage of the watershed that has an aspect within '
                          '45 degrees of east, ie. an aspect between 45 and 135 degrees.'),
        sa.Column('ASPECT_FLAT', sa.Float,
                  comment='The percentage of the watershed with no discernable aspect, '
                          'ie. the flat land.'),
        sa.Column('FEATURE_CODE', sa.String,
                  comment='FEATURE CODE contains a value based on the Canadian Council '
                          'of Surveys and Mappings (CCSM) system for classification of '
                          'geographic features.'),
        sa.Column('GEOMETRY', Geometry, comment=''),
        sa.Column('OBJECTID', sa.Integer, comment=''),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment=''),
        sa.Column('FEATURE_AREA_SQM', sa.Float,
                  comment='FEATURE_AREA_SQM is the system calculated area of a '
                          'two-dimensional polygon in square meters'),
        sa.Column('FEATURE_LENGTH_M', sa.Float,
                  comment='FEATURE_LENGTH_M is the system calculated length or perimeter '
                          'of a geometry in meters'),
    )

    op.create_table(
        'ground_water_aquifers',

        sa.Column('AQ_TAG', sa.String, primary_key=True,
                  comment='The AQ TAG is an alpha-numeric code assigned to the aquifer to '
                          'uniquely identify it.'),
        sa.Column('FCODE', sa.String,
                  comment='10	FCODE is a feature code is most importantly a means of linking a feature to '
                          'its name and definition. For example, the code GB15300120 on a digital geographic '
                          'feature links it to the name "Lake - Dry" with the definition '
                          '"A lake bed from which '
                          'all water has drained or evaporated." The feature code does NOT mark when it was '
                          'digitized, what dataset it belongs to, how accurate it is, what it should look '
                          'like when plotted, or who is responsible for updating it. It only says what it '
                          'represents in the real world. It also doesnt even matter how the lake is '
                          'represented. If it is a very small lake, it may be stored as a point feature. '
                          'If it is large enough to have a shape at the scale of data capture, it may be '
                          'stored as an outline, or a closed polygon. The same feature code still links it '
                          'to the same definition.'),
        sa.Column('PERIMETER', sa.Float,
                  comment='PERIMETER is the outside perimeter of the aquifer measured in metres.'),
        sa.Column('AQNAME', sa.String, comment='AQNAME is the name of the aquifer.'),
        sa.Column('AREA', sa.Float,
                  comment='AREA is the area of the aquifer measured in square metres.'),
        sa.Column('AQUIFER_NUMBER', sa.String,
                  comment='AQUIFER NUMBER is a text field created from the AQUIFER_ID corresponding '
                          'to the Aquifer Tag in GW_AQUIFERS.'),
        sa.Column('AQUIFER_MATERIALS', sa.String,
                  comment='AQUIFER MATERIALS is a broad grouping of '
                          'geologic material found in the '
                          'aquifer. Acceptable values are "Sand and Gravel", "Sand", '
                          '"Gravel" or "Bedrock".'),
        sa.Column('PRODUCTIVITY', sa.String,
                  comment='PRODUCTIVITY represents an aquifers ability to transmit '
                          'and yield groundwater '
                          'and is inferred from any combination of: the aquifer’s '
                          'transmissivity values, '
                          'specific capacity of wells, well yields, description of '
                          'aquifer materials, '
                          'and sources of recharge (such as rivers or lakes), '
                          'or a combination. '
                          'Acceptable values are "Low", "Moderate", "High".'),
        sa.Column('VULNERABILITY', sa.String,
                  comment='VVULNERABILITY of an aquifer to contamination indicates the aquifer’s '
                          'relative intrinsic vulnerability to impacts from human activities at the '
                          'land surface. Vulnerability is based on: the type, '
                          'thickness, and extent of '
                          'geologic materials above the aquifer, depth to water table (or to top of '
                          'confined aquifer), and type of aquifer materials. Acceptable values are '
                          '"Low", "Moderate", and "High".'),
        sa.Column('DEMAND', sa.String,
                  comment='DEMAND describes the level of groundwater use and represents '
                          'the level of reliance '
                          'on the resource for supply at the time of mapping. Demand may be '
                          '"Low", "Moderate", or "High".'),
        sa.Column('AQUIFER_CLASSIFICATION', sa.String,
                  comment='AQUIFER CLASSIFICATION categorizes an aquifer based on its level '
                          'of development (groundwater use) and '
                          'vulnerability to contamination, '
                          'at the time of mapping. For more information see J. Berardinucci '
                          'and K. Ronneseth. 2002: Guide to Using '
                          'The BC Aquifer Classification '
                          'Maps For The Protection And Management Of Groundwater. Level of '
                          'development of an aquifer is described as: "High" (I), "Moderate" '
                          '(II), "Low" (III). Vulnerability is '
                          'coded as "High" (A), "Moderate" '
                          '(B), or "Low" (C) . For example, a class IA aquifer would be '
                          'heavily developed with high vulnerability to contamination, while '
                          'a IIIC would be lightly developed with low vulnerability.'),
        sa.Column('ADJOINING_MAPSHEET', sa.String,
                  comment='ADJOINING MAPSHEET denotes if the spatial '
                          'extent of the aquifer extends '
                          'over more than one BC Geographic Series '
                          '(BCGS) 1:20,000 scale mapsheet. '
                          'Acceptable values are "Yes" and "No".'),
        sa.Column('AQUIFER_NAME', sa.String,
                  comment='AQUIFER NAME for a specific aquifer is typically '
                          'derived from geographic names'
                          ' or names in common use, but may also be lithologic or '
                          'litho-stratigraphic '
                          'units, e.g., ''Abbotsford-Sumas'', ''McDougall Creek Deltaic''.'),
        sa.Column('AQUIFER_RANKING_VALUE', sa.Float,
                  comment='AQUIFER RANKING VALUE is a points based numerical value used to '
                          'determine an aquifers priority in terms of the level of development '
                          'of ground water use. For more information '
                          'see J. Berardinucci and K. '
                          'Ronneseth. 2002: Guide to Using The BC Aquifer Classification Maps '
                          'For The Protection And Management Of Groundwater. The ranking is '
                          'the sum of the point values for each of the following physical '
                          'criteria: productivity, size, vulnerability, demand, type of use, '
                          'and documented quality concerns and quantity '
                          'concerns. Ranking scores '
                          'range from "Low" (5) to "High" (21).'),
        sa.Column('DESCRIPTIVE_LOCATION', sa.String,
                  comment='DESCRIPTIVE LOCATION is a brief description of the geographic '
                          'location of the aquifer. The description is usually referenced to a '
                          'nearby major natural geographic area or '
                          'community, e.g., "Grand Forks".'),
        sa.Column('LITHO_STRATOGRAPHIC_UNIT', sa.String,
                  comment='LITHO STRATOGRAPHIC UNIT is the named permeable geologic unit '
                          '(where available) that comprises the aquifer. It is typically '
                          'either; the era of deposition, the name of a specific formation '
                          'and or the broad material types, '
                          'e.g., "Paleozoic to Mesozoic Era"'
                          ', "Cache Creek Complex", "Intrusive Rock".'),
        sa.Column('QUALITY_CONCERNS', sa.String,
                  comment='QUALITY CONCERNS is the extent of documented '
                          'concerns within the aquifer '
                          'at the time of mapping. Quality concerns such as '
                          'contaminants may be '
                          '"Isolated", "Local", or "Regional" in extent. It is '
                          'possible to have no '
                          'quality concerns documented for a given aquifer.'),
        sa.Column('AQUIFER_DESCRIPTION_RPT_URL', sa.String,
                  comment='AQUIFER DESCRIPTION RPT URL is the Uniform Resource Locator '
                          '(URL) for the Aquifer Description '
                          'report available in Portable '
                          'Document Format (PDF). The date-stamped report describes '
                          'characteristics of the aquifer such '
                          'as: location, vulnerability, '
                          'lithology and hydrological parameters.'),
        sa.Column('AQUIFER_STATISTICS_RPT_URL', sa.String,
                  comment='AQUIFER STATISTICS RPT URL is the Uniform Resource Locator '
                          '(URL) for the Aquifer Summary Statistics report available in '
                          'Comma Separated Value (CSV) format. The date-stamped report '
                          'provides a statistical summary outlining the characteristics '
                          'of all wells associated within the aquifer, including average '
                          'well depth and maximum rate of flow.'),
        sa.Column('AQUIFER_SUBTYPE_CODE', sa.String, comment='AQUIFER SUBTYPE CODE specifies a '
                                                             'standardized code which categorizes '
                                                             'an aquifer based on how it was formed '
                                                             'geologically (depositional '
                                                             'description). Understanding of how aquifers '
                                                             'were formed governs '
                                                             'important attributes such as their productivity, '
                                                             'vulnerability to '
                                                             'contamination as well as proximity and likelihood '
                                                             'of hydraulic '
                                                             'connection to streams. Aquifer sub-type differs from '
                                                             'AQUIFER CLASSIFICATION in that the later system '
                                                             'classifies aquifers '
                                                             'based on their level of development and '
                                                             'vulnerability. Further '
                                                             'details on aquifer sub-types can '
                                                             'be found in Wei et al., 2009: '
                                                             'Streamline Watershed Management '
                                                             'Bulletin Vol. 13/No. 1.The code '
                                                             'value is a combination of an aquifer'
                                                             ' type represented by a '
                                                             'number and an optional letter '
                                                             'representing a more specific aquifer '
                                                             'sub-type. For example aquifer sub-type '
                                                             'code 6b is a comprised of '
                                                             'the aquifer type number (6: Crystalline '
                                                             'bedrock aquifers) and '
                                                             'subtype letter (b) specifically described '
                                                             'as: Fractured crystalline '
                                                             '(igneous intrusive or metamorphic,'
                                                             ' meta-sedimentary, meta-volcanic, '
                                                             'volcanic) rock aquifers. Initial code '
                                                             'values range from 1a to 6b.'),
        sa.Column('QUANTITY_CONCERNS', sa.String,
                  comment='QUANTITY CONCERNS is the extent of documented concerns '
                          'within the aquifer '
                          'at the time of mapping. Quantity concerns such as '
                          'dry wells may be '
                          '"Isolated", "Local", or "Regional" in extent. It is '
                          'possible to have '
                          'no quantity concerns documented for a given aquifer.'),
        sa.Column('SIZE_KM2', sa.Float,
                  comment='SIZE KM2 is the approximate size of the aquifer in square kilometers.'),
        sa.Column('TYPE_OF_WATER_USE', sa.String,
                  comment='TYPE OF WATER USE describes the type of known water use at the '
                          'time of mapping which indicates the variability or diversity of the '
                          'resource as a supply source. Water use categories include: 1) '
                          '"Potential Domestic" may not be primarily used as a source of '
                          'drinking water but has the potential to be in the future and should '
                          'be protected for such use; 2) "Domestic" used primarily as a '
                          'source of drinking water; and 3) "Multiple" used as a source of '
                          'drinking water, plus extensively for other uses such as irrigation.'),
        sa.Column('PRODUCTIVITY_CODE', sa.String,
                  comment='PRODUCTIVITY CODE is a description of the relative volume of water '
                          'being produced by the aquifer.'),
        sa.Column('DEMAND_CODE', sa.String,
                  comment='DEMAND CODE is a code used to classify the demand.'),
        sa.Column('VULNERABILITY_CODE', sa.String,
                  comment='VULNERABILITY CODE is a code used to identify the vulnerability.'),
        sa.Column('CLASSIFICATION_CODE', sa.String,
                  comment='CLASSIFICATION CODE is the aquifer classification system has two '
                          'components: 1) a classification component to categorize aquifers '
                          'based on their current level of development, (use) and vulnerability '
                          'to contamination, and 2) a ranking component to indicate '
                          'the relative '
                          'importance of an aquifer. The classification component categorizes '
                          'aquifers according to level of development and vulnerability to '
                          'contamination: Level of Development and Vulnerability subclasses '
                          'are designated. The composite of these two subclasses is the Aquifer '
                          'Class (Table 1). Development subclass: The level of development of '
                          'an aquifer is determined by assessing demand verses the aquifers '
                          'yield or productivity. A high (I), moderate (II), or low (III) '
                          'level of development can be designated. Vulnerability subclass: '
                          'The vulnerability of an aquifer to contamination '
                          'from surface sources '
                          'is assessed based on: type, thickness and extent '
                          'of geologic materials '
                          'overlying the aquifer, depth to water (or top of confined aquifers), '
                          'and the type of aquifer materials. A high '
                          '(A),moderate (B), or low (C) '
                          'vulnerability can be designated. Aquifer Class: '
                          'The combination of the '
                          'three development and three vulnerability subclasses results in nine '
                          'aquifer classes (Table 1). For example, a class IA aquifer would be '
                          'heavily developed with high vulnerability to contamination, while a '
                          'IIIC would be lightly developed with low vulnerability.'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is a ArcSDE spatial column.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment=''),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment=''),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a required attribute of feature classes and object classes in a '
                          'GeoDatabase. This attribute is added to a SDE layer that was not previously '
                          'created as part of a GeoDatabase but is now '
                          'being registered with a GeoDatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment=''),
    )

    op.create_table(
        'ground_water_wells',

        sa.Column('WELL_TAG_NO', sa.String, primary_key=True,
                  comment='WELL TAG NO is the unique number of the '
                          'groundwater well as assigned '
                          'by the Province of British Columbia'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a required attribute of feature classes and object classes in '
                          'a GeoDatabase. This attribute is added to a SDE layer that was not previously '
                          'created as part of a GeoDatabase but is now being registered '
                          'with a GeoDatabase.'),
        sa.Column('SOURCE_ACCURACY', sa.String,
                  comment='SOURCE ACCURACY is a groundwater well locations are identified '
                          'onto well cards by well drillersas part of the drilling process. '
                          'There is no statutory requirement for welldrillers to submit these '
                          'records to the Government of British Columbia,therefore not all '
                          'groundwater wells are represented in this dataset. It isuncertain '
                          'the percentage of wells that are represented, but the bestestimate '
                          'is around 50%. The dataset is in a constant state of update anddoes '
                          'not stay static for any length of time. Accuracy is defined by one '
                          'offive codes, as indicated here:A - digitized from well cards with '
                          'well defined cadastre onto IntegratedCadastral Initiative mapping. '
                          'Accuracy is +/- 10 metres.B - digitized from 1:5,000 cadastral mapping. '
                          'Accuracy is +/- 20 metresC - digitized from 1:20,000 cadastral mapping. '
                          'Accuracy is +/- 50 metresD - digitized from old Lands, Forests and '
                          'Water Resources mapping (variousscales) or from well cards with no '
                          'cadastral information. Accuracy is +/-100 metres.E - digitized from '
                          '1:50,000 NTS mapping. Accuracy is +/- 200 metres.'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is a ArcSDE spatial column.'),
        sa.Column('FCODE', sa.String,
                  comment='FCODE feature code is most importantly a means of linking a feature to its '
                          'name and definition. For example, the code GB15300120 on a digital geographic '
                          'feature links it to the name "Lake - Dry" with the definition "A lake bed from '
                          'which all water has drained or evaporated." The feature code does NOT mark when '
                          'it was digitized, what dataset it belongs to, how accurate it is, what it '
                          'should look like when plotted, or who is responsible for updating it. It '
                          'only says what it represents in the real world. It also doesnt even matter '
                          'how the lake is represented. If it is a very small lake, it may be stored as '
                          'a point feature. If it is large enough to have a shape at the scale of data '
                          'capture, it may be stored as an outline, or a closed polygon. The same feature '
                          'code still links it to the same definition.'),
        sa.Column('WELL_ID', sa.Integer, comment='WELL ID is a unique identifier for the table.'),
        sa.Column('WELL_LOCATION', sa.String,
                  comment='WELL LOCATION is a location description used in the MS-Access application.'),
        sa.Column('WELL_SEQUENCE_NO', sa.Integer,
                  comment='WELL SEQUENCE NO is a number which describes the order a '
                          'particular well islocated in a particular BCGS grid square. '
                          'For example the well 082L042321 #1is the '
                          'first well located in '
                          'BCGS grid 082L042321. Before a system'
                          ' generatednon-intelligent '
                          'WELL TAG NUMBER was in use this is how'
                          ' particular wells werenamed.'),
        sa.Column('WELL_IDENTIFICATION_PLATE_NO', sa.Integer,
                  comment='The Groundwater Protection Regulation of the Water Act '
                          'requires a WELL IDENTIFICATION PLATE NO for water supply '
                          'system wells and new and altered water supply wells.'
                          ' WLAP produces these aluminum plates with a unique number '
                          'for each plate. These plates are attached to the pump'
                          ' house or well by the drillers. Existing wells can have '
                          'these plates attached after the fact, especially if any'
                          ' lab samples or other information is being collected '
                          'about the well.'),
        sa.Column('WATER_UTILITY_FLAG', sa.String,
                  comment='WATER UTILITY FLAG is some wells belong to water utilities for '
                          'provision of water to their.'),
        sa.Column('WATER_SUPPLY_WELL_NAME', sa.String,
                  comment='The WATER SUPPLY WELL NAME is the Utilitys name for this well. '
                          'This is used when the well is owned by a Utility under the '
                          'Water Act. The Utility has applied and been granted a licence '
                          'to be a Water Supply Purveyor. This data is only filled in '
                          'when the well is owned by a Utility. E.g. Parksville Water '
                          'Utility calls one of its wells "Roberts Road Well No. 5"'),
        sa.Column('WELL_TAG_NUMBER', sa.Integer,
                  comment='WELL TAG NUMBER is an unique business well identifier.'),
        sa.Column('WATER_SUPPLY_SYSTEM_NAME', sa.String,
                  comment='The WATER SUPPLY SYSTEM NAME is the name of a Utility '
                          'under the Water Act. The Utility has applied and been '
                          'granted a licence to be a Water Supply Purveyor. This data'
                          ' is only filled in when the well is owned by a Utility.'
                          ' E.g. Parksville Water Utility.'),
        sa.Column('OBSERVATION_WELL_NUMBER', sa.Integer,
                  comment='The OBSERVATION WELL NUMBER exists when a well has been '
                          'selected for monitoring. An Observation well will have water '
                          'level readings recorded to track groundwater levels.'),
        sa.Column('AQUIFER_LITHOLOGY_CODE', sa.String,
                  comment='AQUIFER LITHOLOGY CODE is an aquifer lithology identifier, '
                          'enables lithology layers to be indentified by a short reference.'),
        sa.Column('WATER_DEPTH', sa.Integer,
                  comment='WATER DEPTH, how far down the well before water is reached.'),
        sa.Column('ARTESIAN_FLOW_VALUE', sa.Integer,
                  comment='The ARTESIAN FLOW VALUE is the Artesian water flow measurement of'
                          ' the flow that occurs naturally due to inherent water pressure'
                          ' in the WELL. The measurement is in ARTESIAN FLOW UNITS.'),
        sa.Column('BCGS_ID', sa.Integer,
                  comment='BCGS ID is an internal ID to track creation of unique business BCGS number.'),
        sa.Column('WATERSHED_CODE', sa.String,
                  comment='WATERSHED CODE is a watershed identifier, uniquely identifies '
                          'a water shed.'),
        sa.Column('BCGS_NUMBER', sa.String,
                  comment='The BCGS NUMBER is used by the Mapsheets which are based on the British'
                          ' Columbia Geographic System (BCGS) number scheme. The mapsheet number '
                          'is added to the well record after the well record has been added '
                          'in the system.'),
        sa.Column('BEDROCK_DEPTH', sa.Integer,
                  comment='The BEDROCK DEPTH captures the depth at which bedrock starts.'),
        sa.Column('CERTIFICATION', sa.String,
                  comment='CERTIFICATION can be used to collect water WELL certificate information.'
                          ' Not currently being used.'),
        sa.Column('CHEMISTRY_LAB_DATA', sa.String,
                  comment='Chemistry lab data exists. (flag), lab data exists usually tied '
                          'to chemistry site id.'),
        sa.Column('CHEMISTRY_SITE_ID', sa.String,
                  comment='Chemistry site ID number, assigned by water EMS (environmental '
                          'managment ssytem)'),
        sa.Column('CLASS_OF_WELL', sa.String,
                  comment='The CLASS OF WELL is a classification defined in the Groundwater '
                          'Protection Regulation of the Water Act. The classes are : Water Supply,'
                          ' Monitoring, Recharge / Injection, Dewatering / Drainage,'
                          ' Remediation, Geotechnical.'),
        sa.Column('UTM_NORTH', sa.Float,
                  comment='The UTM NORTH attribute stored in the spatial database and associated '
                          'with the WELL TAG NUMBER coordinated.'),
        sa.Column('CONSTRUCTION_END_DATE', sa.DateTime,
                  comment='CONSTRUCTION END DATE is the date when WELL construction'
                          ' was complete, defaults to date the well record was'
                          ' added to the system.'),
        sa.Column('CONSTRUCTION_METHOD_CODE', sa.String,
                  comment='The WELL CONSTRUCTION METHOD is the method of drilling '
                          'the Well.The construction methods are :'
                          ' DUG, DRILLED, DRIVING, JETTING, SPRING or OTHER.'),
        sa.Column('CONSTRUCTION_METHOD_NAME', sa.String,
                  comment='The CONSTRUCTION METHOD NAME is the method of '
                          'constructing the well. Example DRILLED '
                          'indicates a drill'
                          ' rig was used to construct the well. '
                          'Indicates the industry '
                          'trends in well construction methods.'),
        sa.Column('CONSTRUCTION_START_DATE', sa.DateTime,
                  comment='CONSTRUCTION START DATE is the date when WELL'
                          ' construction was started.'),
        sa.Column('CONSULTANT_COMPANY', sa.String,
                  comment='CONSULTANT COMPANY is a description of consulting company '
                          'hired by owner to locate well site.'),
        sa.Column('CONTRACTOR_INFO_1', sa.String,
                  comment='CONTRACTOR_ INFO 1 is MS Access Support for information field.'),
        sa.Column('CONTRACTOR_INFO_2', sa.String,
                  comment='CONTRACTOR_ INFO 2 is MS Access Support for information field.'),
        sa.Column('CONTRACTOR_WELL_PLATE_NMBR', sa.String,
                  comment='CONTRACTOR WELL PLATE NMBR is that the Contractor '
                          'may assign well plate number to a WELL. If the'
                          ' driller uses one of the WLAP identification plate,'
                          ' then this number may be the same as the '
                          'WELL_IDENTIFICATION_PLATE_NO. '
                          'Sometimes drillers have their '
                          'own plates made up and this number is different.'),
        sa.Column('COORDINATE_X', sa.String,
                  comment='COORDINATE X is an old three parameter coordinate system (arbitraty)'
                          ' supported for old maps with well data.'),
        sa.Column('COORDINATE_Y', sa.String,
                  comment='COORDINATE Y is an old three parameter coordinate system (arbitraty)'
                          ' supported for old maps with well data.'),
        sa.Column('COORDINATE_Z', sa.String,
                  comment='COORDINATE Z is an old three parameter coordinate system (arbitraty) '
                          'supported for old maps with well data.'),
        sa.Column('CREW_DRILLER_NAME', sa.String,
                  comment='The CREW DRILLER NAME is the first and last name of a certified '
                          'water well Driller.'),
        sa.Column('UTM_EAST', sa.Float,
                  comment='The UTM EAST attribute stored in the spatial database and associated with '
                          'the WELL TAG NUMBER coordinated.'),
        sa.Column('CREW_HELPER_NAME', sa.String,
                  comment='CREW HELPER NAME is the name of Driller Helper.'),
        sa.Column('DATE_ENTERED', sa.DateTime,
                  comment='DATE ENTERED is automatically updated when a new well record is '
                          'added to the system.'),
        sa.Column('DEPTH_WELL_DRILLED', sa.Integer,
                  comment='DEPTH WELL DRILLED is the finished Well depth, represented '
                          'in units of feet bgl (below ground level).'),
        sa.Column('DEVELOPMENT_HOURS', sa.Integer,
                  comment='DEVELOPMENT HOURS is the total hours devoted to develop WELL '
                          '(develop in this means enabling production of water).'),
        sa.Column('DEVELOPMENT_NOTES', sa.String,
                  comment='DEVELOPMENT NOTES is the additional notes regarding well'
                          ' development effort.'),
        sa.Column('DIAMETER', sa.String,
                  comment='DIAMETER is a well diameter, represented in units of inches.'),
        sa.Column('DRILLER_COMPANY_CODE', sa.String,
                  comment='DRILLER COMPANY CODE is a numeric code for identified'
                          ' driller company name.'),
        sa.Column('DRILLER_COMPANY_NAME', sa.String,
                  comment='The DRILLER COMPANY NAME is the compant Drillers work'
                          ' for, if they work for a company.'),
        sa.Column('DRILLER_WELL_ID', sa.Integer,
                  comment='MS-Access defined WATER WELL ID, used during upload into '
                          'MS-Access application'),
        sa.Column('ELEVATION', sa.Integer,
                  comment='The ELEVATION is the elevation above sea level in feet of the'
                          ' ground surface at the WELL.'),
        sa.Column('FIELD_LAB_DATA', sa.String,
                  comment='The FIELD LAB DATA indicates there is Chemistry field data '
                          '(flag), field chemistry information kept in a paper copy. '
                          'Y - yes there is field data. N - No there is no field data.'),
        sa.Column('GENERAL_REMARKS', sa.String,
                  comment='GENERAL REMARKS is the general water well comment.'),
        sa.Column('GRAVEL_PACKED_FLAG', sa.String,
                  comment='GRAVEL PACKED FLAG indicated whether or not a gravel pack'
                          ' was applied during the creation of the WELL.'),
        sa.Column('GRAVEL_PACKED_FROM', sa.Integer,
                  comment='GRAVEL PACKED FROM indicates whether or not degree gravel'
                          ' dispersed around WELL site.'),
        sa.Column('GRAVEL_PACKED_TO', sa.Integer,
                  comment='GRAVEL PACKED TO indicates whether or not degree gravel '
                          'dispersed around WELL site.'),
        sa.Column('GROUND_WATER_FLAG', sa.String,
                  comment='GROUND WATER FLAG indicates if a ground water report exists or not.'),
        sa.Column('INDIAN_RESERVE', sa.String,
                  comment='INDIAN RESERVE is the additional parcels identifiers for land '
                          'in B.C. include Legal Indian Reserve.'),
        sa.Column('INFO_OTHER', sa.String,
                  comment='INFO OTHER is the additional information has been captured about '
                          'this WELL that is significant.'),
        sa.Column('INFO_SITE', sa.String,
                  comment='The INFO SITE is additional site information, backward compatible'
                          ' attribute to capture legacy site information.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='Latitude coordinate, used to locate a WELL, alternative location method to UTM.'),
        sa.Column('LEGAL_BLOCK', sa.String,
                  comment='LEGAL BLOCK is the additional parcels identifiers for land in B.C. '
                          'include Legal block.'),
        sa.Column('LEGAL_DISTRICT_LOT', sa.String,
                  comment='The LEGAL DISTRICT LOT is part of the legal description of'
                          ' the land the well is located on. Example 2514S'),
        sa.Column('LEGAL_LAND_DISTRICT_CODE', sa.String,
                  comment='The LEGAL_LAND_DISTRICT_CODE represent Parcels of land '
                          'in B.C. can be identifed by the combination of Lot, Legal '
                          'Land District and Map # identifiers. This attribute consists'
                          ' of the Legal Land District to help identify the property '
                          'where the WELL is located.Code District1 Alberni 2 Barclay '
                          '3 Bright 4 Cameron 5 Cariboo 6 Cassiar 7 Cedar 8 Chemainus '
                          '9 Clayoquot 10 Coast Range 1 11 Coast Range 2 12 Coast Range '
                          '3 13 Coast Range 4 14 Coast Range 5 15 Comiaken 16 Comox 17 '
                          'Cowichan 18 Cowichan Lake 19 Cranberry 20 Douglas 21 Dunsmuir '
                          '22 Esquimalt 23 Goldstream 24 Helmcken 25 Highland 26 Kamloops '
                          '(KDYD) 27 Kootenay 28 Lake 29 Lillooet 30 Malahat 31 '
                          'Metchosin 32 Mountain 33 Nanaimo 34 Nanoose 35 Nelson 36 '
                          'Newcastle 37 New Westminster 38 Nootka 39 North Saanich 40 '
                          'Osoyoos (ODYD) 41 Otter 42 Oyster 43 Peace River 44 Quamichan '
                          '45 Queen Charlotte 46 Renfrew 47 Rupert 48 Sahtlam 49'
                          ' Sayward 50 Seymour 51 Shawnigan 52 Similkameen 53 Somenos'
                          ' 54 Sooke 55 South Saanich 56 Texada Island 57 Victoria '
                          '58 Wellington 59 Yale (YDYD).'),
        sa.Column('LEGAL_LAND_DISTRICT_NAME', sa.String,
                  comment='The LEGAL LAND DISTRICT NAME is part of the legal description'
                          ' of the land the well is located on. Example CHEMAINUS.Alberni '
                          'Barclay Bright Cameron Cariboo Cassiar Cedar Chemainus '
                          'Clayoquot Coast Range 1 Coast Range 2 Coast Range 3 Coast'
                          ' Range 4 Coast Range 5 Comiaken Comox Cowichan Cowichan Lake'
                          ' Cranberry Douglas Dunsmuir Esquimalt Goldstream Helmcken'
                          ' Highland Kamloops (KDYD) Kootenay Lake Lillooet Malahat '
                          'Metchosin Mountain Nanaimo Nanoose Nelson Newcastle New '
                          'Westminster Nootka North Saanich Osoyoos (ODYD) Otter Oyster'
                          ' Peace River Quamichan Queen Charlotte Renfrew Rupert Sahtlam '
                          'Sayward Seymour Shawnigan Similkameen Somenos Sooke South '
                          'Saanich Texada Island Victoria Wellington Yale (YDYD)'),
        sa.Column('UTM_ACCURACY_CODE', sa.String,
                  comment='UTM ACCURACY CODE is a description of how accurate the UTM coordinate '
                          'position is. Also implies scale to the coordinate.Codes are numeric '
                          '01 etc.... 01 - less than 3 metres margin of error 02 - 3-10 metres'
                          ' margin of error 03 - 10-30 metres margin of error 04 - 30-100 '
                          'metres margin of error 1:25 000 scale 05 - 100-300 metres margin '
                          'of error 1:50 000 scale 06 - 300-1000 metres margin of error '
                          '1:125 000 scale 07 - 1000-3000 metres margin of error 1:250 000 '
                          'scale 08 - 3000-10 000 metres margin of error 09 - well location '
                          'is unknown 10 - UTM Zone 10 from 1:50 000 scale 30-100 metres moe.'
                          ' 11 - UTM Zone 11 from 1:50 000 scale 30-100 metres.'),
        sa.Column('LEGAL_MISCELLANEOUS', sa.String,
                  comment='LEGAL MISCELLANEOUS is the additional legal land information.'),
        sa.Column('LEGAL_PLAN', sa.String,
                  comment='LEGAL PLAN is the parcels of land in B.C. can be identifed by the '
                          'combination of Lot, Legal Land District and '
                          'Plan # identifiers. This '
                          'attribute consists of the Legal Plan to help'
                          ' identify the property where '
                          'the WELL is located.'),
        sa.Column('LEGAL_RANGE', sa.String,
                  comment='LEGAL RANGE is the additional parcels identifiers for land in B.C. '
                          'include legal range.'),
        sa.Column('LEGAL_SECTION', sa.String,
                  comment='LEGAL SECTION is the additional parcels identifiers for land in '
                          'B.C. include Legal section.'),
        sa.Column('LEGAL_TOWNSHIP', sa.String,
                  comment='LEGAL TOWNSHIP is the additional parcels identifiers for land in'
                          ' B.C. include Legal township.'),
        sa.Column('LITHOLOGY_DESCRIPTION_COUNT', sa.String,
                  comment='LITHOLOGY DESCRIPTION COUNT is the number of'
                          ' Lithology layers identified.'),
        sa.Column('LITHOLOGY_FLAG', sa.String,
                  comment='The LITHOLOGY FLAG indictates if there is Lithology data '
                          'available for the well. Y - yes the soil and subsurface '
                          'material types have been documented.N - the lithology is '
                          'not documented.'),
        sa.Column('LITHOLOGY_MEASURMENT_UNIT', sa.String,
                  comment='LITHOLOGY MEASURMENT UNIT is the aquifer '
                          'lithology measurement units (inches,, feet) used to '
                          'refence the lithology layers '
                          'associated with the WELL.'),
        sa.Column('LOCATION_ACCURACY', sa.String,
                  comment='LOCATION ACCURACY is the estimated location accuracy. '
                          'The values for this field range from '
                          '1 through 5. The number '
                          '5 represents the most accurate estimate.'
                          ' The LOC ACCURACY CODE'
                          ' is a number 1 to 5 that indicates the '
                          'scale of map the location '
                          'is derived from. Example, 5 is a 1:50,000 '
                          'map. There is another '
                          'scale that is used, with values A - well '
                          'cards to cadastre or'
                          ' GPS +- 10m; B - 1:5000 maps +- 20m; '
                          'C - 1:20,000 maps +-50m; '
                          'D-old Dept of L,F WR maps or well cards without cadastre +-'
                          ' 100m; E - 1:50,000 maps +- 200m;'
                          'F - CDGPS differential GPS +- 1m.'),
        sa.Column('LOC_ACCURACY_CODE', sa.String,
                  comment='The LOC ACCURACY CODE is a number that indicates the scale of '
                          'map the location is derived from. Example, 5 is a 1:50,000 map. '
                          'There is another scale that is used, with values A - well cards '
                          'to cadastre or GPS +- 10m; B - 1:5000 maps +- 20m; C - 1:20,000 '
                          'maps +-50m; D-old Dept of L,F WR maps or well cards without'
                          ' cadastre +- 100m; E - 1:50,000 maps +- 200m;F - CDGPS '
                          'differential GPS +- 1m. Accuracy Codes for Horizontal'
                          ' Coordinates.1 < 3 metres margin of error. Differential GPS'
                          ' or location measured in field from known benchmarks.2 3-10'
                          ' metres margin of error. location measured in field from mapped '
                          'features. 3 10-30 metres margin of error. location measured in '
                          'field from mapped features. points plotted in field on topographic'
                          ' maps of 1:10 000 scale or larger single GPS measurement. '
                          '4 30-100 metres margin of error. points plotted in field on '
                          'topographic maps of 1:25 000 scale. 5 100-300 metres margin of error.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='Longitude coordinate, used to locate a WELL, alternative '
                          'location method to UTM.'),
        sa.Column('LOT_NUMBER', sa.String,
                  comment='LOT NUMBER is the parcels of land in B.C. can be identifed by the '
                          'combination of Lot, Legal Land District and Map # identifiers. '
                          'This attribute consists of the Lot to help identify the property '
                          'where the WELL is located.'),
        sa.Column('MERIDIAN', sa.String,
                  comment='The MERIDIAN indicates if the location of the well is east or west of '
                          'the 6th meridian which runs North-South.The meridian is part of a legal'
                          ' description for land in British Columbia. Example W6TH - the well is west '
                          'of the 6th meridian.'),
        sa.Column('MINISTRY_OBSERVATION_WELL_STAT', sa.String,
                  comment='MINISTRY OBSERVATION WELL STAT is the ministry of'
                          ' Water Land and Air Protection, formerly (Ministry '
                          'of Environment) observation.'),
        sa.Column('MS_ACCESS_NUM_OF_WELL', sa.String,
                  comment='The MS ACCESS NUM OF WELL is the sequence of the wells '
                          'entered by a driller in the MS Access Drilling '
                          'Data Capture System.'),
        sa.Column('OLD_MAPSHEET', sa.String,
                  comment='OLD_MAPSHEET is an identifer, used to track changes to the well location.'),
        sa.Column('OLD_WELL_NUMBER', sa.String,
                  comment='Old well number, used to track wells on old-style well maps '
                          'using X,,Y,Z and old three parameter arbritrary coordinate '
                          'system. (required to support old maps with well data)'),
        sa.Column('OTHER_CHEMISTRY_DATA', sa.String,
                  comment='OTHER CHEMISTRY DATA is the reference for additional '
                          'sources of chemistry data.'),
        sa.Column('OTHER_EQUIPMENT', sa.String,
                  comment='OTHER EQUIPMENT is the description of other equipment used '
                          'to create the WELL.'),
        sa.Column('OTHER_INFORMATION', sa.String,
                  comment='OTHER INFORMATION is the brief description of other well '
                          'data available.'),
        sa.Column('OWNERS_WELL_NUMBER', sa.String,
                  comment='OWNERS WELL NUMBER is the local WELL number applied by '
                          'owner for internal tracking.'),
        sa.Column('OWNER_ID', sa.Integer,
                  comment='OWNER ID is an owner Identification, uniqely identifies a WELL owner.'),
        sa.Column('SURNAME', sa.String, comment='SURNAME is the last Name of WELL owner.'),
        sa.Column('PERFORATION_FLAG', sa.String,
                  comment='The PERFORATION FLAG indicates if the steel casing has been '
                          'perforated by a hydraulic shear.'
                          ' Perforations improve flow to '
                          'the bottom of the well. Some wells '
                          'have been perforated rather '
                          'than having a screen installed. Perforations do not consider '
                          'soil size. Y- yes there are holes in the casing.'
                          ' N- no additional holes in casing.'),
        sa.Column('PERMIT_NUMBER', sa.String,
                  comment='The PERMIT NUMBER is used if permit numbers are issued to drill a WELL.'),
        sa.Column('PID', sa.Integer,
                  comment='PID is a parcel Identifier, identifes parcel where well is located.'),
        sa.Column('PLATE_ATTACHED_BY', sa.String,
                  comment='The PLATE ATTACHED BY is the name of the person who attached '
                          'the WELL IDENTIFICATION PLATE. The Groundwater Protection '
                          'Regulation of the Water Act requires this information for water'
                          ' supply system wells and new and altered water supply wells.'),
        sa.Column('PRODUCTION_TIDAL_FLAG', sa.String,
                  comment='PRODUCTION TIDAL FLAG indicates if production well rates are'
                          ' influenced by tidal activity or not.'),
        sa.Column('PUMP_DESCRIPTION', sa.String,
                  comment='PUMP DESCRIPTION is an information, including if a pump exists or not.'),
        sa.Column('PUMP_FLAG', sa.String,
                  comment='PUMP FLAG indicates if a pump is being used on the WELL or not.'),
        sa.Column('REPORTS_FLAG', sa.String,
                  comment='The REPORTS FLAG indicates if there is a report on the National '
                          'Topographical System (NTS) filing system '
                          'or the utility files(which '
                          'are reports submitted in support of an '
                          'application for a certificate '
                          'of PUBLIC CONVENIENCE AND NECESSITY). '
                          'Y yes Well Report(s) Exist . '
                          'N - no reports exist'),
        sa.Column('RIG_NUMBER', sa.String,
                  comment='RIG NUMBER is the number asscociated with the drilling rig. '
                          'Supplied by the Driller.'),
        sa.Column('QUARTER', sa.String,
                  comment='QUARTER is the additional parcels identifiers for land in B.C. '
                          'include Legal quarter.'),
        sa.Column('SCREEN_FLAG', sa.String,
                  comment='SCREEN FLAG depicts the use of a screen(s) in a WELL. Indicates '
                          'at least 1 SCREEN record is associated with the WELL record.'),
        sa.Column('SCREEN_INFORMATION_TEXT', sa.String,
                  comment='SCREEN INFORMATION TEXT is the additional information '
                          'regarding the screen.'),
        sa.Column('SCREEN_LENGTH', sa.String,
                  comment='The SCREEN LENGTH is the total length of the screen assembly, '
                          'including blanks and risers. (feet) . Most screens are '
                          'cylindrical in shape.'),
        sa.Column('SCREEN_MANUFACTURER', sa.String,
                  comment='The SCREEN MANUFACTURER identifies who made the screen.'),
        sa.Column('SCREEN_WIRE', sa.String,
                  comment='The SCREEN WIRE is the type of screen wire. The wire has different'
                          ' cross sections - like WIRE WOUND (round) or '
                          'V WIRE WOUND (triangular). '
                          'The wire is what some screens are made of.'),
        sa.Column('SEQUENCE_NO', sa.Float,
                  comment='SEQUENCE_NO is a number which describes the order a particular well '
                          'islocated in a particular BCGS grid square. For example the well'
                          ' 082L042321 #1is the first well located in BCGS grid 082L042321. '
                          'Before a system generatednon-intelligent WELL TAG NUMBER was in use'
                          ' this is how particular wells werenamed.'),
        sa.Column('SIEVE_FLAG', sa.String,
                  comment='SIEVE FLAG indicates if Sieve Analysis was done or not, default was'
                          ' blank field for No.'),
        sa.Column('SITE_AREA', sa.String,
                  comment='The SITE AREA is the town or nearest describable geogropahic area.'),
        sa.Column('SITE_FLAG', sa.String,
                  comment='SITE_FLAG indicated whether site inspection was done or not.'),
        sa.Column('SITE_ISLAND', sa.String,
                  comment='The SITE ISLAND is the island name, if the well is located on an Island.'),
        sa.Column('SITE_STREET', sa.String,
                  comment='The SITE STREET is the Well location, address (well) description of '
                          'where well is outside additional well information'),
        sa.Column('SURFACE_SEAL_DEPTH', sa.Integer,
                  comment='The SURFACE SEAL DEPTH indicates depth of surface seal which '
                          'is depth in feet below ground surface to bottom of Surface Seal.'),
        sa.Column('SURFACE_SEAL_FLAG', sa.String,
                  comment='The SURFACE SEAL FLAG indicates if a surface seal was applied '
                          'upon completion of WELL.Y- yes surface seal was constructed. N- '
                          'no surface seal was applied. Blank is unknown'),
        sa.Column('SURFACE_SEAL_THICKNESS', sa.Integer,
                  comment='The SURFACE SEAL THICKNESS is the thickness of the '
                          '"surface seal" which is a '
                          'sealant placed in the annular '
                          'space around the outside of '
                          'the outermost well casing and '
                          'between multiple well casings '
                          'and extending to or just below '
                          'the ground surface. Good practice '
                          'is a sealant with a minimum '
                          'thickness of 1 inch, minumum'
                          ' length of 15 feet and extending '
                          'a minimum of 3 feet into bedrock.'),
        sa.Column('TYPE_OF_RIG', sa.String,
                  comment='Type of RIG (drilling hardware) used during the creation of the WELL.'),
        sa.Column('TYPE_OF_WORK', sa.String,
                  comment='TYPE OF WORK is the legacy attribute contained in MS-Access application. '
                          'Values include NEW or DPD.'),
        sa.Column('WELL_USE_CODE', sa.String,
                  comment='WELL USE CODE is three letter character unique code to identify code.'),
        sa.Column('WELL_USE_NAME', sa.String,
                  comment='The WELL USE NAME is the long well use name. Examples may include '
                          'private, commercial, domestic.'),
        sa.Column('WHEN_CREATED', sa.DateTime,
                  comment='WHEN CREATED is the date and time the entry was created.'),
        sa.Column('WHEN_UPDATED', sa.DateTime,
                  comment='WHEN UPDATED is the date and time the entry was last modified.'),
        sa.Column('WHERE_PLATE_ATTACHED', sa.String,
                  comment='The WHERE PLATE ATTACHED is a description of where the '
                          'indentification plate has been attached. The Groundwater '
                          'Protection Regulation of the Water Act'
                          ' requires this information'
                          ' for water supply system wells and new and altered '
                          'water supply wells.'),
        sa.Column('WHO_CREATED', sa.String,
                  comment='WHO CREATED is the unique id of the user who created this entry.'),
        sa.Column('WHO_UPDATED', sa.String,
                  comment='WHO UPDATED is the unique id of the user who last modified this entry.'),
        sa.Column('YIELD_UNIT_CODE', sa.String,
                  comment='YIELD UNIT CODE is the yield unit of measure, unique code. '
                          'The MS-Access database expects flow rates to'
                          ' be entered as USgpm.'),
        sa.Column('YIELD_UNIT_DESCRIPTION', sa.String,
                  comment='YIELD UNIT DESCRIPTION is the yield measurement description, '
                          'if other yield units become supported or if a conversion factor '
                          'is required it could be entered in this attribute.'),
        sa.Column('YIELD_VALUE', sa.Float,
                  comment='YIELD VALUE is the well yield value, measured water yield ammount, '
                          'estimate how much water flow a WELL is capable of sustaining.'),
        sa.Column('WELL_LICENCE_GENERAL_STATUS', sa.String,
                  comment='A text value reflects the generalized status of '
                          'authorizations on the given well. '
                          'It value will be '
                          'set based on the contents of the '
                          'AUTHORIZATION STATUS '
                          'attribute coming from eLicensing '
                          'application via a trigger'
                          ' implemented on WELL_LICENCE Table.Acceptable '
                          'Values are:a) UNLICENSEDb) '
                          'LICENSEDc) HISTORICAL.'),
        sa.Column('WELL_DETAIL_URL', sa.String,
                  comment='A HTTP URL link value that contains the Well Tag Number, specifying'
                          ' a direct link to the WELL record in WELLS Public application.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to '
                          'store annotation, curve features and CAD data when using the '
                          'SDO_GEOMETRY storage data type.'),
    )

    op.create_table(
        'water_allocation_restrictions',

        sa.Column('LINEAR_FEATURE_ID', sa.Integer,
                  comment='LINEAR FEATURE ID is a primary Key to link to stream segments in '
                          'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP as a one to one join. This '
                          'is maintained by business users. E.g., 831792750'),
        sa.Column('RESTRICTION_ID_LIST', sa.String,
                  comment='RESTRICTION ID LIST is a list of one or more restriction IDs of '
                          'stream restriction points downstream from the stream segment. The '
                          'RESTRICTION_IDs correspond with RESTRICTION_IDs in '
                          'WHSE_WATER_MANAGEMENT.WLS_WATER_RESTRICTION_LOC_SVW. E.g., RS34144'),
        sa.Column('PRIMARY_RESTRICTION_CODE', sa.String,
                  comment='PRIMARY RESTRICTION CODE indicates the type of restriction '
                          'point downstream from the stream segment. E.g., FR - '
                          'Fully Recorded; FR_EXC - Fully Recorded Except; PWS - '
                          'Possible Water Shortage; RNW - Refused No Water; OR - '
                          'Office Reserve; UNSPECIFIED - type of '
                          'restriction not specified.'),
        sa.Column('SECONDARY_RESTRICTION_CODES', sa.String,
                  comment='SECONDARY RESTRICTION CODES is a list of additional '
                          'types of water restrictions downstream from the stream'
                          ' segment. E.g., FR - Fully Recorded; FR_EXC - '
                          'Fully Recorded Except; PWS - Possible Water Shortage; '
                          'RNW - Refused No Water; OR - Office Reserve; '
                          'UNSPECIFIED - type of restriction not specified.'),
        sa.Column('FWA_WATERSHED_CODE', sa.String,
                  comment='FWA WATERSHED CODE is a 143 character code derived using a '
                          'hierarchy coding scheme. Approximately identifies where a '
                          'particular stream is located within the province.'),
        sa.Column('WATERSHED_GROUP_CODE', sa.String,
                  comment='WATERSHED GROUP CODE is the watershed group code '
                          'associated with the polygon.'),
        sa.Column('GNIS_NAME', sa.String,
                  comment='GNIS NAME is the BCGNIS (BC Geographical Names Information System) '
                          'name associated with the GNIS feature id (an English name was used '
                          'where available, otherwise another language was selected).'),
        sa.Column('STREAM_ORDER', sa.Float,
                  comment='STREAM ORDER is the calculated modified Strahler order.'),
        sa.Column('STREAM_MAGNITUDE', sa.Float,
                  comment='STREAM MAGNITUDE is the calculated magnitude.'),
        sa.Column('FEATURE_CODE', sa.String,
                  comment='FEATURE CODE contains a value based on the Canadian Council of'
                          ' Surveys and Mappings (CCSM) system for classification of '
                          'geographic features.'),
        sa.Column('GEOMETRY', Geometry,
                  comment='GEOMETRY is the column used to reference the spatial coordinates '
                          'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, primary_key=True,
                  comment='OBJECTID is a required attribute of feature classes and '
                          'object classes in a geodatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to '
                          'store annotation, curve features and CAD data when using the '
                          'SDO_GEOMETRY storage data type.'),
        sa.Column('FEATURE_LENGTH_M', sa.Float,
                  comment='FEATURE_LENGTH_M is the system calculated length or perimeter '
                          'of a geometry in meters'),
    )

    op.create_table(
        'water_rights_licenses',

        sa.Column('WLS_WRL_SYSID', sa.Integer, primary_key=True,
                  comment='WLS WRL SYSID is a system generated unique '
                          'identification number.'),
        sa.Column('POD_NUMBER', sa.String,
                  comment='POD NUMBER is the unique identifier for a Point of Diversion, e.g., PW189413. '
                          'Each POD can have multiple licences associated with it.'),
        sa.Column('POD_SUBTYPE', sa.String,
                  comment='POD SUBTYPE distinguishes the different POD types, i.e., POD (a surface '
                          'water point of diversion), PWD (a point of well diversion that diverts '
                          'groundwater), or PG (a point of groundwater diversion that diverts '
                          'groundwater such as a dugout, ditch or quarry).'),
        sa.Column('POD_DIVERSION_TYPE', sa.String,
                  comment='POD_DIVERSION_TYPE is the type of diversion for a point of '
                          'groundwater diversion (PG subtype), i.e., '
                          'Dugout, Ditch, Quarry. '
                          'Since this only applies to PG subtypes,'
                          ' other subypes (POD or PWD)'
                          ' will be left blank (null value).'),
        sa.Column('POD_STATUS', sa.String,
                  comment='POD STATUS is the status of the Point of Diversion. Each POD can have '
                          'multiple licences, e.g., Active (one or more active licences associated), '
                          'Inactive (only historical inactive licences associated).'),
        sa.Column('FILE_NUMBER', sa.String,
                  comment='FILE NUMBER is the water business file number, assigned during the '
                          'application phase, e.g., 0321048. A file may hold one or more licences.'),
        sa.Column('WELL_TAG_NUMBER', sa.Integer,
                  comment='WELL TAG NUMBER is a unique well identifier for either registered '
                          'or licensed wells, e.g., 12345.'),
        sa.Column('LICENCE_NUMBER', sa.String,
                  comment='LICENCE NUMBER is the authorization number referenced in the water '
                          'licence document, e.g., 121173.'),
        sa.Column('LICENCE_STATUS', sa.String,
                  comment='LICENCE STATUS represents the existing status of licence, e.g., '
                          'Current, Cancelled, Pending.'),
        sa.Column('LICENCE_STATUS_DATE', sa.DateTime,
                  comment='LICENCE STATUS DATE indicates the last time the '
                          'licence status changed.'),
        sa.Column('PRIORITY_DATE', sa.DateTime,
                  comment='PRIORITY DATE is the date from which the precedence of the '
                          'licence is established within the first in time first '
                          'in right framework.'),
        sa.Column('EXPIRY_DATE', sa.DateTime,
                  comment='EXPIRY DATE is the date the licence expires.'),
        sa.Column('PURPOSE_USE_CODE', sa.String,
                  comment='PURPOSE USE CODE is the use of water authorized by the licence, '
                          'identified as a code, e.g., 02I.'),
        sa.Column('PURPOSE_USE', sa.String,
                  comment='PURPOSE USE is the use of water authorized by the licence, e.g. Industrial.'),
        sa.Column('SOURCE_NAME', sa.String,
                  comment='SOURCE NAME is the aquifer or body of surface water from which '
                          'the licence is authorized to extract water. A surface water body '
                          'can be a lake, river, creek or any other '
                          'surface water source e.g., '
                          'Skaha Lake or Kokanee Creek. For a known '
                          'aquifer that has been mapped, '
                          'the aquifer name is the BC Governments '
                          'Aquifer ID number, e.g., 1137. '
                          'For an unmapped aquifer, the aquifer '
                          'name is derived from water precincts '
                          'names in common use, and lithologic or litho-stratigraphic units,'
                          ' e.g., Nelson Unconsolidated; Nelson Bedrock.'),
        sa.Column('REDIVERSION_IND', sa.String,
                  comment='REDIVERSION IND is an indicator of whether the Point of Well '
                          'Diversion is, for the particular '
                          'licence, used to divert water '
                          'from another water source, i.e., Y or N.'),
        sa.Column('QUANTITY', sa.Float,
                  comment='QUANTITY is the maximum quantity of water that is authorized to be '
                          'diverted for the purpose use, e.g., 500.'),
        sa.Column('QUANTITY_UNITS', sa.String,
                  comment='QUANTITY UNITS is the units of measurement for the quantity of '
                          'water authorized in the licence, e.g., m3 / year.'),
        sa.Column('QUANTITY_FLAG', sa.String,
                  comment='QUANTITY FLAG is the code used to identify how the total quantity '
                          'is assigned across multiple Points of Well Diversion (PWD) for a '
                          'particular licence and purpose use, i.e., T, M, D, or P.'),
        sa.Column('QUANTITY_FLAG_DESCRIPTION', sa.String,
                  comment='QUANTITY FLAG DESCRIPTION is a description of the '
                          'QUANTITY FLAG code used to'
                          ' identify how the total quantity '
                          'is assigned across multiple '
                          'Points of Well Diversion (PWD) '
                          'for a particular licence and '
                          'purpose use, i.e., T (Total '
                          'demand for purpose, one PWD); '
                          'M (Maximum licensed demand '
                          'for purpose, multiple PWDs, '
                          'quantity at each PWD unknown); '
                          'D (Multiple PWDs for purpose, '
                          'quantities at each are known, '
                          'PWDs on different aquifers); '
                          'P (Multiple PWDs for purpose, '
                          'quantities at each are known, '
                          'PWDs on same aquifer).'),
        sa.Column('QTY_DIVERSION_MAX_RATE', sa.Float,
                  comment='QTY DIVERSION MAX RATE is the maximum authorized diversion '
                          'rate of water within a second, minute or day up to the total '
                          'licensed quantity per year, e.g, 0.006, 2000'),
        sa.Column('QTY_UNITS_DIVERSION_MAX_RATE', sa.String,
                  comment='QTY UNITS DIVERSION MAX RATE are the units of '
                          'measurement for the maximum '
                          'diversion rate of water '
                          'authorized in the licence, e.g., m3/second, '
                          'm3/minute, m3/day, m3/year.'),
        sa.Column('HYDRAULIC_CONNECTIVITY', sa.String,
                  comment='HYDRAULIC CONNECTIVITY is an indicator of whether the '
                          'licensed aquifer diversion '
                          '(PWD or PG) may be hydraulically '
                          'connected to one or more surface'
                          ' water sources (stream or '
                          'lake), i.e., Likely, Unknown.'),
        sa.Column('PERMIT_OVER_CROWN_LAND_NUMBER', sa.String,
                  comment='PERMIT OVER CROWN LAND NUMBER is an Internal number'
                          ' assigned to a Permit over Crown Land '
                          '(PCL), e.g., 12345.'),
        sa.Column('PRIMARY_LICENSEE_NAME', sa.String,
                  comment='PRIMARY LICENSEE NAME is the primary contact for the licence, '
                          'co-licensees will be displayed as et al.'),
        sa.Column('ADDRESS_LINE_1', sa.String,
                  comment='ADDRESS LINE 1 is the first line of the licensees mailing address.'),
        sa.Column('ADDRESS_LINE_2', sa.String,
                  comment='ADDRESS LINE 2 is the second line of the licensees mailing address.'),
        sa.Column('ADDRESS_LINE_3', sa.String,
                  comment='ADDRESS LINE 3 is the third line of the licensees mailing address.'),
        sa.Column('ADDRESS_LINE_4', sa.String,
                  comment='ADDRESS LINE 4 is the fourth line of the licensees mailing address.'),
        sa.Column('COUNTRY', sa.String, comment='COUNTRY is the licensees country.'),
        sa.Column('POSTAL_CODE', sa.String, comment='POSTAL CODE is the licensees postal code.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), '
                          'of the location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), '
                          'of the location of the feature as measured from the prime meridian, '
                          'e.g., -123.093544.'),
        sa.Column('DISTRICT_PRECINCT_NAME', sa.String,
                  comment='DISTRICT PRECINCT NAME is a jurisdictional area within a '
                          'Water District. It is a combination of District and Precinct '
                          'codes and names, e.g., New Westminster / Coquitlam. Not all '
                          'Water Districts contain Precincts.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates '
                          'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a column required by spatial layers that interact with '
                          'ESRI ArcSDE. It is populated with '
                          'unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE ANNO CAD DATA is a binary column used by spatial tools to '
                          'store annotation, curve features and CAD data when using '
                          'the SDO GEOMETRY storage data type.'),
    )

    # added habitat layer
    op.create_table(
        'critical_habitat_species_at_risk',

        sa.Column('CRITICAL_HABITAT_ID', sa.Integer, primary_key=True,
                  comment='CRITICAL_HABITAT_ID: is a system generated '
                          'unique identification number. This is the '
                          'primary key of this table. e.g., 1'),
        sa.Column('COSEWIC_SPECIES_ID', sa.String,
                  comment='COSEWIC_SPECIES_ID is a unique identification number assigned to '
                          'the species or taxa (including, if applicable, sub species and'
                          ' population) assessed by the Committee on the Status of Endangered '
                          'Wildlife in Canada (COSEWIC) and currently listed on SARA '
                          'Schedule 1; e.g., 1086.'),
        sa.Column('SCIENTIFIC_NAME', sa.String,
                  comment='SCIENTIFIC_NAME is the standard scientific name for the'
                          ' SARA-listed species or taxa, and can include subspecies;'
                          ' e.g., Oreoscoptes montanus.'),
        sa.Column('COMMON_NAME_ENGLISH', sa.String,
                  comment='COMMON_NAME_ENGLISH is the English name of the species'
                          ' or taxa listed on SARA Schedule 1; e.g., Sage Thrasher.'),
        sa.Column('COMMON_NAME_FRENCH', sa.String,
                  comment='COMMON_NAME_FRENCH is the French name of the species or taxa'
                          ' listed on SARA Schedule 1; e.g., Moqueur des armoises.'),
        sa.Column('COSEWIC_POPULATION', sa.String,
                  comment='COSEWIC_POPULATION is the population name of the species'
                          ' or taxa assessed by the Committee on '
                          'the Status of Endangered'
                          ' Wildlife in Canada (COSEWIC) and currently listed on SARA'
                          ' Schedule 1; e.g., Southern Mountain population.'),
        sa.Column('CRITICAL_HABITAT_STATUS', sa.String,
                  comment='CRITICAL_HABITAT_STATUS is the stage of development'
                          ' of the critical habitat polygon; '
                          'e.g., Final or Candidate'),
        sa.Column('CRITICAL_HABITAT_REGION', sa.String,
                  comment='CRITICAL_HABITAT_REGION is a regional identifier '
                          'optionally used to group critical habitat polygons;'
                          ' e.g. "Southeastern BC".'),
        sa.Column('CRITICAL_HABITAT_SITE_ID', sa.String,
                  comment='CRITICAL_HABITAT_SITE_ID is the alphanumeric code of a '
                          'critical habitat site as defined in the federal '
                          'recovery document; e.g., 937_5.'),
        sa.Column('CRITICAL_HABITAT_SITE_NAME', sa.String,
                  comment='CRITICAL_HABITAT_SITE_NAME is the name of a critical '
                          'habitat site as defined in the federal recovery document; '
                          'e.g., Kilpoola.'),
        sa.Column('CRITICAL_HABITAT_DETAIL', sa.String,
                  comment='CRITICAL_HABITAT_DETAIL is the level of detail of critical'
                          ' habitat polygon; e.g., Detailed polygon or Grid square. '
                          'Grid squares are used when detailed polygons contain '
                          'sensitive information that cannot be released.'),
        sa.Column('CRITICAL_HABITAT_VARIANT', sa.String,
                  comment='CRITICAL_HABITAT_VARIANT is the sub-type of critical'
                          ' habitat, if applicable; e.g. Regeneration.'),
        sa.Column('CRITICAL_HABITAT_APPROACH', sa.String,
                  comment='CRITICAL_HABITAT_APPROACH is the scale at which the '
                          'polygons were defined and refers'
                          ' to processes within '
                          'the Critical Habitat Toolbox policy; e.g.,'
                          ' Landscape, Area or Site.'),
        sa.Column('CRITICAL_HABITAT_METHOD', sa.String,
                  comment='CRITICAL_HABITAT_METHOD is a broad description of how '
                          'the critical habitat was identified and'
                          ' refers to processes '
                          'within the Critical Habitat Toolbox policy; e.g.,'
                          ' Critical Function Zone.'),
        sa.Column('AREA_HECTARES', sa.Float,
                  comment='AREA_HECTARES is the area calculated in hectares at source data'
                          ' which is in Lambert Conic Conformal. E.g., 14430833.7926'),
        sa.Column('LAND_TENURE', sa.String,
                  comment='LAND_TENURE is the status of federal crown ownership of the land;'
                          ' e.g., Federal or Non-federal.'),
        sa.Column('CRITICAL_HABITAT_COMMENTS', sa.String,
                  comment='CRITICAL_HABITAT_COMMENTS are notes about the critical'
                          ' habitat or specific polygon; e.g., Polygons were '
                          'identified as part of a multispecies recovery plan.'),
        sa.Column('CRITICAL_HABITAT_DATE_EDITED', sa.DateTime,
                  comment='CRITICAL_HABITAT_DATE_EDITED is the date that '
                          'the polygon was last edited; e.g., 8/21/2014.'),
        sa.Column('PROVINCE_TERRITORY', sa.String,
                  comment='PROVINCE_TERRITORY is the province or territory in which'
                          ' the critical habitat occurs; e.g., British Columbia.'),
        sa.Column('FEDERAL_DEPARTMENT_NAME', sa.String,
                  comment='FEDERAL_DEPARTMENT_NAME is the Federal department or '
                          'agency that published the recovery strategy or action'
                          ' plan in which the critical habitat is identified,'
                          ' and maintains the data; e.g., '
                          'Canadian Wildlife Service, '
                          '‘Parks Canada Agency’.'),
        sa.Column('UTM_ZONE', sa.Float,
                  comment='UTM_ZONE is a segment of the Earths surface 6 degrees of longitude '
                          'in width. The zones are numbered eastward starting at the meridian '
                          '180 degrees from the prime meridian at Greenwich. There are five zones'
                          ' numbered 7 through 11 that cover British Columbia,'
                          ' e.g., Zone 10 with '
                          'a central meridian at -123 degrees.'),
        sa.Column('UTM_EASTING', sa.Float,
                  comment='UTM EASTING is the distance in meters of the polygon centroid '
                          'eastward to or from the central meridian of a UTM zone with a '
                          'false easting of 500000 meters. E.g., 532538'),
        sa.Column('UTM_NORTHING', sa.Float,
                  comment='UTM NORTHING is the distance in meters of the polygon '
                          'centroidnorthward from the equator. e.g., 5747966'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees '
                          '(dd.dddddd), of the location of the feature as measured from '
                          'the equator, e.g., 55.323653'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='LONGITUDE is the geographic coordinate, in decimal degrees'
                          ' (ddd.dddddd), of the location of the feature as measured from '
                          'the prime meridian, e.g., -123.093544'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the sa.column used to reference the spatial coordinates'
                          ' defining the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a sa.column required by spatial layers that interact'
                          ' with ESRI ArcSDE. It is populated with unique '
                          'values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE ANNO CAD DATA is a binary sa.column used by spatial tools '
                          'to store annotation, curve features and CAD data when using the '
                          'SDO_GEOMETRY storage data type.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment=''),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment='')
    )

    # add layer catalogue data

    def get_audit_fields():
        current_date = datetime.datetime.now()
        return {
            "create_user": "ETL_USER",
            "create_date": current_date,
            "update_user": "ETL_USER",
            "update_date": current_date,
            "effective_date": current_date,
            "expiry_date": "9999-12-31T23:59:59Z"
        }

    op.execute('SET search_path TO metadata')
    logger.info("Loading Initial Catalogue Information")

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # User file array to ensure loading order
    # File names must match class names for globals() to work
    files = ['ApiCatalogue.json', "WmsCatalogue.json", 'DisplayCatalogue.json',
             "DataFormatCode.json", "ComponentTypeCode.json", "VectorCatalogue.json"]
    directory = '/app/fixtures/'

    for filename in files:
        with open(os.path.join(directory, filename)) as json_file:
            data = json.load(json_file)

        # Get class name from file name
        file = os.path.splitext(filename)[0]
        # Need imports at top even though linter says they are unused
        cls = globals()[file]

        logger.info(f"Loading Fixture: {filename}")
        # Create class instances
        instances = []
        for obj in data:
            logger.info(f"Object: {obj}")
            instance = cls(**{**obj, **get_audit_fields()})
            instances.append(instance)

        session.add_all(instances)

    logger.info("Loading Fixtures Complete")
    session.commit()
    op.execute('SET search_path TO public')

    # add label key to links object
    op.execute("""
    alter table metadata.link_component add column
        link_label_key VARCHAR;
    """)

    # add layer categories
    op.execute('SET search_path TO metadata')

    op.create_table('layer_category',
                    sa.Column('create_user', sa.String(length=100), nullable=True,
                              comment='The user who created this record in the database.'),
                    sa.Column('create_date', sa.DateTime(
                    ), nullable=True,
                              comment='Date and time (UTC) when the physical record was created in the database.'),
                    sa.Column('update_user', sa.String(length=100), nullable=True,
                              comment='The user who last updated this record in the database.'),
                    sa.Column('update_date', sa.DateTime(), nullable=True,
                              comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
                    sa.Column('effective_date', sa.DateTime(), nullable=True,
                              comment='The date and time that the code became valid and could be used.'),
                    sa.Column('expiry_date', sa.DateTime(), nullable=True,
                              comment='The date and time after which the code is no longer valid and should not be used.'),
                    sa.Column('layer_category_code',
                              sa.String(), nullable=False),
                    sa.Column('description',
                              sa.String(length=255), nullable=False),
                    sa.Column('display_order',
                              sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('layer_category_code'),
                    schema='metadata'
                    )

    op.add_column('display_catalogue',
                  sa.Column('layer_category_code', sa.String(),
                            sa.ForeignKey('metadata.layer_category.layer_category_code'),
                            nullable=True, comment='references a layer category'))

    # add starting codes into code table
    op.execute("""
        INSERT INTO layer_category (layer_category_code, description, display_order) VALUES
        ('LAND_TENURE', 'Land Tenure and Administrative Boundaries', 10),
        ('FISH_WILDLIFE_PLANTS', 'Fish, Wildlife, and Plant Species', 20),
        ('FRESHWATER_MARINE', 'Freshwater and Marine', 30),
        ('WATER_ADMINISTRATION','Water Administration', 40),
        ('REPORTS', 'Reports', 50),
        ('FORESTS', 'Forests, Grasslands and Wetlands', 60),
        ('AIR_CLIMATE', 'Air and Climate', 70)
    """)

    # one time command to populate the new column.
    # these categories are from https://apps.nrs.gov.bc.ca/int/jira/browse/WATER-417
    # if we need to modify/add columns regularly, we will need to build an admin page
    # for managing layers.
    op.execute("""
        UPDATE display_catalogue AS dc
        SET layer_category_code = CASE
            WHEN dc.display_data_name = 'water_rights_licences' THEN 'WATER_ADMINISTRATION'
            WHEN dc.display_data_name = 'groundwater_wells' THEN 'FRESHWATER_MARINE'
            WHEN dc.display_data_name = 'freshwater_atlas_watersheds' THEN 'FRESHWATER_MARINE'
            WHEN dc.display_data_name = 'bc_major_watersheds' THEN 'FRESHWATER_MARINE'
            WHEN dc.display_data_name = 'cadastral' THEN 'LAND_TENURE'
            WHEN dc.display_data_name = 'automated_snow_weather_station_locations' THEN 'FRESHWATER_MARINE'
            WHEN dc.display_data_name = 'freshwater_atlas_stream_directions' THEN 'FRESHWATER_MARINE'
            WHEN dc.display_data_name = 'bc_wildfire_active_weather_stations' THEN 'FORESTS'
            WHEN dc.display_data_name = 'ecocat_water_related_reports' THEN 'REPORTS'
            WHEN dc.display_data_name = 'aquifers' THEN 'FRESHWATER_MARINE'
            WHEN dc.display_data_name = 'water_allocation_restrictions' THEN 'WATER_ADMINISTRATION'
            WHEN dc.display_data_name = 'critical_habitat_species_at_risk' THEN 'FISH_WILDLIFE_PLANTS'
            WHEN dc.display_data_name = 'hydrometric_stream_flow' THEN 'FRESHWATER_MARINE'
            ELSE NULL
            END
        WHERE layer_category_code IS NULL
    """)

    op.execute('SET search_path TO public')

    # add data sources
    op.execute('SET search_path TO metadata')

    # add foreign key column relating to data source
    op.add_column('display_catalogue',
                  sa.Column('data_source_id', sa.Integer(),
                            sa.ForeignKey('metadata.data_source.data_source_id'), nullable=True,
                            comment='references a data source'))

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # add data source information
    session.add_all([
        DataSource(**{
            'data_source_id': 1,
            'data_format_code': 'json',
            'name': 'Automated Snow Weather Station Locations',
            'description': 'Locations of automated snow weather stations, active and inactive. Automated snow weather stations are components of the BC snow survey network.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/automated-snow-weather-station-locations',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 2,
            'data_format_code': 'json',
            'name': 'BC Major Watersheds',
            'description': 'Major watersheds of BC tagged with the first 3 digits of the Watershed Code (e.g.: 920)',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/bc-major-watersheds',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 3,
            'data_format_code': 'json',
            'name': 'BC Wildfire Active Weather Stations',
            'description': 'This dataset contains point locations for actively reporting BC Wildfire Service (BCWS) weather stations. BCWS operates a network of automated hourly reporting weather stations to support all aspects of fire management. The data are used as input to the Canadian Forest Fire Danger Rating System, as a basis for weather forecasting and for climate monitoring. Sensors at the weather stations monitor temperature, relative humidity, wind speed and direction and rainfall. In a collaborative project with other government agencies and the private sector, select sites are being upgraded for year round operation by the addition of snow measurement gauges.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-active-weather-stations',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 4,
            'data_format_code': 'json',
            'name': 'ParcelMap BC Parcel Fabric',
            'description': 'ParcelMap BC is the single, complete, trusted and sustainable electronic map of active titled parcels and surveyed provincial Crown land parcels in British Columbia. This particular dataset is a subset of the complete ParcelMap BC data and is comprised of the parcel fabric and attributes for over two million parcels published under the Open Government License - British Columbia.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/parcelmap-bc-parcel-fabric',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 5,
            'data_format_code': 'json',
            'name': 'Critical Habitat federally-listed species at risk',
            'description': 'This dataset displays the geographic areas within which critical habitat for species at risk listed on Schedule 1 of the federal Species at Risk Act (SARA) occurs in British Columbia. However, not all of the area within these boundaries is necessarily critical habitat. To precisely define what constitutes critical habitat for a particular species it is essential that this geo-spatial information be considered in conjunction with complementary information in a species’ recovery document. Recovery documents are available from the Species at Risk (SAR) Public Registry (http://www.sararegistry.gc.ca). The recovery documents contain important information about the interpretation of the geo-spatial information, especially regarding the biological and environmental features (“biophysical attributes”) that complete the definition of a species’ critical habitat.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/critical-habitat-for-federally-listed-species-at-risk-posted-',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 6,
            'data_format_code': 'json',
            'name': 'Ecological Catalogue (formerly AquaCat)',
            'description': 'A compendium of reports that provide information about aquatic and terrestrial animals and plants, soils, surface water, groundwater and their accompanying data files and maps',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/ecological-catalogue-formerly-aquacat',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 7,
            'data_format_code': 'json',
            'name': 'Freshwater Atlas Stream Directions',
            'description': 'Points with rotations that indicate downstream flow direction. Can be displayed with arrow symbols to show flow direction. There is one point at the upstream end for each stream network feature',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-directions',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 8,
            'data_format_code': 'json',
            'name': 'Freshwater Atlas Watersheds',
            'description': 'All fundamental watershed polygons generated from watershed boundary lines, bank edges, delimiter edges, coastline edges, and administrative boundary edges',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-watersheds',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 9,
            'data_format_code': 'json',
            'name': 'Ground Water Aquifers',
            'description': 'Polygon features represent developed ground water aquifers in BC (that have been mapped). Most aquifer boundaries are delineated based on geology, hydrology and topographic information. Some aquifer boundaries stop at the border of BC mapsheet boundaries due to resource or data constraints at the time of mapping.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/ground-water-aquifers',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 10,
            'data_format_code': 'json',
            'name': 'Ground Water Wells',
            'description': 'Point features showing the location of groundwater wells in BC joined with attributes and information from the WELLS database. NOTE: Artesian wells are flowing wells at the time of drilling.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/ground-water-wells',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 11,
            'data_format_code': 'json',
            'name': 'Streams with Water Allocation Restrictions',
            'description': 'This dataset displays streams that have water allocation restrictions on them.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/streams-with-water-allocation-restrictions',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 12,
            'data_format_code': 'json',
            'name': 'Water Rights Licences - Public',
            'description': 'This is a province-wide SDE spatial layer displaying water rights licence data administrated under the Water Sustainability Act which includes data for both surface water and groundwater Points of Diversions. Point of Diversion types include Surface water Points of Diversion (PDs) Groundwater Points of Well Diversion (PWDs) as well as points of Groundwater diversion (PGs), non-well groundwater diversion points such as dugouts, ditches and quarries. This layer contains a record for each water licence on each POD type that exists in the province (each POD can have multiple licences). For each record, some basic information about the water licence is included.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public',
            **get_audit_fields()
        }),
        DataSource(**{
            'data_source_id': 13,
            'data_format_code': 'sqlite',
            'name': 'National Water Data Archive: HYDAT',
            'description': 'Hydrometric data are collected and compiled by Water Survey of Canada’s eight regional offices. The information is housed in two centrally-managed databases: HYDEX and HYDAT. HYDEX is the relational database that contains inventory information on the various streamflow, water level, and sediment stations (both active and discontinued) in Canada. This database contains information about the stations themselves such as; location, equipment, and type(s) of data collected. HYDAT is a relational database that contains the actual computed data for the stations listed in HYDEX. These data include: daily and monthly means of flow, water levels and sediment concentrations (for sediment sites). For some sites, peaks and extremes are also recorded.WSC now offers hydrometric data and station information in a single downloadable file, either in Microsoft Access Database format or in SQLite format, updated on a quarterly basis.',
            'source_url': 'http://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/',
            **get_audit_fields()
        })
    ])

    session.commit()

    op.execute("""
        UPDATE display_catalogue AS dc
        SET data_source_id = CASE
            WHEN dc.display_data_name = 'automated_snow_weather_station_locations' THEN 1
            WHEN dc.display_data_name = 'bc_major_watersheds' THEN 2
            WHEN dc.display_data_name = 'bc_wildfire_active_weather_stations' THEN 3
            WHEN dc.display_data_name = 'cadastral' THEN 4
            WHEN dc.display_data_name = 'critical_habitat_species_at_risk' THEN 5
            WHEN dc.display_data_name = 'ecocat_water_related_reports' THEN 6
            WHEN dc.display_data_name = 'freshwater_atlas_stream_directions' THEN 7
            WHEN dc.display_data_name = 'freshwater_atlas_watersheds' THEN 8
            WHEN dc.display_data_name = 'aquifers' THEN 9
            WHEN dc.display_data_name = 'groundwater_wells' THEN 10
            WHEN dc.display_data_name = 'water_allocation_restrictions' THEN 11
            WHEN dc.display_data_name = 'water_rights_licences' THEN 12
            WHEN dc.display_data_name = 'hydrometric_stream_flow' THEN 13
            ELSE NULL
            END
        WHERE data_source_id IS NULL
    """)

    op.execute('SET search_path TO public')

    # update primary keys
    # Ecocat's pk REPORT_POINT_ID was not unique so this changes it to REPORT_ID which is.
    op.execute(
        'ALTER TABLE ecocat_water_related_reports DROP CONSTRAINT ecocat_water_related_reports_pkey CASCADE')
    op.create_primary_key('ecocat_water_related_reports_pkey', 'ecocat_water_related_reports',
                          ['REPORT_ID'])

    # Change all Primary Key types from SERIAL to INTEGER to eliminate autoincrementing behaviour.
    op.execute(
        'ALTER TABLE automated_snow_weather_station_locations ALTER COLUMN "SNOW_ASWS_STN_ID" TYPE INTEGER USING "SNOW_ASWS_STN_ID"::integer')
    op.execute(
        'ALTER TABLE bc_major_watersheds ALTER COLUMN "OBJECTID" TYPE INTEGER USING "OBJECTID"::integer')
    op.execute(
        'ALTER TABLE bc_wildfire_active_weather_stations ALTER COLUMN "WEATHER_STATIONS_ID" TYPE INTEGER USING "WEATHER_STATIONS_ID"::integer')
    op.execute(
        'ALTER TABLE cadastral ALTER COLUMN "PARCEL_FABRIC_POLY_ID" TYPE INTEGER USING "PARCEL_FABRIC_POLY_ID"::integer')
    op.execute(
        'ALTER TABLE critical_habitat_species_at_risk ALTER COLUMN "CRITICAL_HABITAT_ID" TYPE INTEGER USING "CRITICAL_HABITAT_ID"::integer')
    op.execute(
        'ALTER TABLE ecocat_water_related_reports ALTER COLUMN "REPORT_ID" TYPE INTEGER USING "REPORT_ID"::integer')
    op.execute(
        'ALTER TABLE freshwater_atlas_stream_directions ALTER COLUMN "OBJECTID" TYPE INTEGER USING "OBJECTID"::integer')
    op.execute(
        'ALTER TABLE freshwater_atlas_watersheds ALTER COLUMN "WATERSHED_FEATURE_ID" TYPE INTEGER USING "WATERSHED_FEATURE_ID"::integer')
    # ground_water_aquifers has a String pk type so no need to alter
    # ground_water_wells has a String pk type so no need to alter
    op.execute(
        'ALTER TABLE water_allocation_restrictions ALTER COLUMN "OBJECTID" TYPE INTEGER USING "OBJECTID"::integer')
    op.execute(
        'ALTER TABLE water_rights_licenses ALTER COLUMN "WLS_WRL_SYSID" TYPE INTEGER USING "WLS_WRL_SYSID"::integer')
    # hydat.Station has a String pk type so no need to alter

    # update_search_view_pks
    op.execute("DROP MATERIALIZED VIEW IF EXISTS geocode_lookup")

    # since we can't change geometry properties when the materialized view is referencing
    # these columns, this is an opportune time to update these columns.
    op.execute(
        """SELECT UpdateGeometrySRID('bc_major_watersheds', 'GEOMETRY', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('bc_wildfire_active_weather_stations', 'SHAPE', 4326)""")
    op.execute("""SELECT UpdateGeometrySRID('cadastral', 'SHAPE', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('ecocat_water_related_reports', 'GEOMETRY', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('freshwater_atlas_stream_directions', 'GEOMETRY', 4326)""")
    # op.execute("""SELECT UpdateGeometrySRID('freshwater_atlas_watersheds', 'GEOMETRY', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('ground_water_aquifers', 'GEOMETRY', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('ground_water_wells', 'GEOMETRY', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('water_allocation_restrictions', 'GEOMETRY', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('water_rights_licenses', 'SHAPE', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('critical_habitat_species_at_risk', 'SHAPE', 4326)""")
    op.execute(
        """SELECT UpdateGeometrySRID('automated_snow_weather_station_locations', 'SHAPE', 4326)""")
    op.execute("""
        CREATE MATERIALIZED VIEW geocode_lookup AS

        SELECT
        ST_AsText(stn.geom) AS center,
        stn.station_number AS primary_id,
        stn.station_name AS name,
        'Stream station' AS kind,
        'hydrometric_stream_flow' AS layer,
        to_tsvector(concat_ws(' ',stn.station_number, stn.station_name)) AS tsv
        FROM hydat.stations AS stn
        WHERE stn.prov_terr_state_loc = 'BC'

        UNION
        SELECT
        ST_AsText(ST_Centroid(cadastral."SHAPE")) AS center,
        cadastral."PID"::text AS primary_id,
        NULL AS name,
        'Parcel' AS kind,
        'cadastral' AS layer,
        to_tsvector(coalesce(cadastral."PID"::text, cadastral."PARCEL_NAME"::text)) AS tsv
        FROM cadastral

        UNION
        SELECT
        ST_AsText(ST_Centroid(wrl."SHAPE")) AS center,
        wrl."LICENCE_NUMBER"::text AS primary_id,
        wrl."SOURCE_NAME" AS name,
        'Water rights licence' AS kind,
        'water_rights_licences' AS layer,
        to_tsvector(concat_ws(' ', wrl."POD_NUMBER"::text, wrl."LICENCE_NUMBER"::text, wrl."SOURCE_NAME")) AS tsv
        FROM water_rights_licenses AS wrl

        UNION
        SELECT
        ST_AsText(gww."GEOMETRY") AS center,
        LTRIM(gww."WELL_TAG_NO"::text, '0') AS primary_id,
        NULL AS name,
        'Well' AS kind,
        'groundwater_wells' AS layer,
        to_tsvector(LTRIM(gww."WELL_TAG_NO"::text, '0')) AS tsv
        FROM ground_water_wells AS gww

        UNION SELECT
        ST_AsText(ST_Centroid(aq."GEOMETRY")) AS center,
        LTRIM(aq."AQ_TAG"::text, '0') AS primary_id,
        aq."DESCRIPTIVE_LOCATION" AS name,
        'Aquifer' AS kind,
        'aquifers' AS layer,
        to_tsvector(concat_ws(' ', LTRIM(aq."AQ_TAG"::text, '0'), aq."AQUIFER_NAME", aq."DESCRIPTIVE_LOCATION")) AS tsv
        FROM ground_water_aquifers AS aq

        UNION SELECT
        ST_AsText(ecocat."GEOMETRY") AS center,
        ecocat."REPORT_ID"::text AS primary_id,
        ecocat."TITLE" AS name,
        'Report' AS kind,
        'ecocat_water_related_reports' AS layer,
        to_tsvector(concat_ws(' ', ecocat."REPORT_ID"::text, ecocat."TITLE", ecocat."SHORT_DESCRIPTION", ecocat."AUTHOR")) AS tsv
        FROM ecocat_water_related_reports as ecocat
    """)

    op.execute("""
        create index idx_geocode_tsv ON geocode_lookup USING GIN(tsv)
    """)

    # add_layer_catalogue_cols
    op.execute('SET search_path TO metadata')

    # add foreign key column relating to data source
    op.add_column('data_source',
                  sa.Column('source_object_name', sa.String, nullable=True,
                            comment='The object name reference at the external data source.  This is used to lookup datasets on directories like DataBC, e.g. WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW'))
    op.add_column('data_source',
                  sa.Column('data_table_name', sa.String, nullable=True,
                            comment='The table name where data for a map layer is stored. Used to help ogr2ogr and pgloader reference the correct table when processing new map layer data.'))
    op.add_column('data_source',
                  sa.Column('last_updated_data', sa.DateTime,
                            server_default=sa.text('make_timestamp(2019, 1, 1, 1, 1, 1)'),
                            nullable=False,
                            comment='The date the data for this map layer was last updated in the database.'))
    op.add_column('data_source',
                  sa.Column('last_updated_tiles', sa.DateTime,
                            server_default=sa.text('make_timestamp(2019, 1, 1, 1, 1, 1)'),
                            nullable=False,
                            comment='The date the tiles for this map layer were last re-generated and made available on the tile server. Should be as close as possible to last_updated_data, but differences are expected due to tile processing times.'))
    op.add_column('data_source',
                  sa.Column('direct_link', sa.String, nullable=True,
                            comment='A direct link to download the dataset from the source, if available.'))

    op.add_column('data_source',
                  sa.Column('source_object_id', sa.String, nullable=True,
                            comment='The ID on the upstream data source. This is specifically required for paging through the DataBC API. Note: do not rely on these IDs as permanent keys, only for sorting and paginating during queries (e.g. `sortBy=WLS_WRL_SYSID&startIndex=1000`)'))

    op.add_column('display_catalogue',
                  sa.Column('required_map_properties', ARRAY(TEXT), nullable=False,
                            server_default="{}",
                            comment='Properties that are required by the map for rendering markers/shapes, e.g. for colouring markers based on a value or property like POD_SUBTYPE'))
    op.add_column('display_catalogue',
                  sa.Column('mapbox_layer_id', sa.String, nullable=True,
                            comment='The mapbox tileset ID used to upload and replace layer data via the mapbox api.'))

    op.execute("""
        UPDATE data_source AS ds SET source_object_name = CASE
        WHEN ds.data_source_id = 1  THEN 'WHSE_WATER_MANAGEMENT.SSL_SNOW_ASWS_STNS_SP'
        WHEN ds.data_source_id = 2  THEN 'WHSE_BASEMAPPING.BC_MAJOR_WATERSHEDS'
        WHEN ds.data_source_id = 3  THEN 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_WEATHER_STATIONS_SP'
        WHEN ds.data_source_id = 4  THEN 'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW'
        WHEN ds.data_source_id = 5  THEN 'WHSE_WILDLIFE_MANAGEMENT.WCP_CRITICAL_HABITAT_SP'
        WHEN ds.data_source_id = 6  THEN 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW'
        WHEN ds.data_source_id = 7  THEN 'WHSE_BASEMAPPING.FWA_STREAM_DIRECTIONS_SP'
        WHEN ds.data_source_id = 8  THEN 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY'
        WHEN ds.data_source_id = 9  THEN 'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW'
        WHEN ds.data_source_id = 10 THEN 'WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW'
        WHEN ds.data_source_id = 11 THEN 'WHSE_WATER_MANAGEMENT.WLS_STREAM_RESTRICTIONS_SP'
        WHEN ds.data_source_id = 12 THEN 'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV'
        WHEN ds.data_source_id = 13 THEN 'Hydat_sqlite3_20191016.zip'
        ELSE NULL
        END
    """)

    op.execute("""
        UPDATE data_source AS ds SET data_table_name = CASE
        WHEN ds.data_source_id = 1  THEN 'automated_snow_weather_station_locations'
        WHEN ds.data_source_id = 2  THEN 'bc_major_watersheds'
        WHEN ds.data_source_id = 3  THEN 'bc_wildfire_active_weather_stations'
        WHEN ds.data_source_id = 4  THEN 'cadastral'
        WHEN ds.data_source_id = 5  THEN 'critical_habitat_species_at_risk'
        WHEN ds.data_source_id = 6  THEN 'ecocat_water_related_reports'
        WHEN ds.data_source_id = 7  THEN 'freshwater_atlas_stream_directions'
        WHEN ds.data_source_id = 8  THEN 'freshwater_atlas_watersheds'
        WHEN ds.data_source_id = 9  THEN 'ground_water_aquifers'
        WHEN ds.data_source_id = 10 THEN 'ground_water_wells'
        WHEN ds.data_source_id = 11 THEN 'water_allocation_restrictions'
        WHEN ds.data_source_id = 12 THEN 'water_rights_licenses'
        WHEN ds.data_source_id = 13 THEN 'hydat.stations'
        ELSE NULL
        END
    """)

    op.execute("""
        UPDATE data_source AS ds SET source_object_id = CASE
        WHEN ds.data_source_id = 1  THEN 'SNOW_ASWS_STN_ID'
        WHEN ds.data_source_id = 2  THEN NULL
        WHEN ds.data_source_id = 3  THEN 'WEATHER_STATIONS_ID'
        WHEN ds.data_source_id = 4  THEN 'PARCEL_FABRIC_POLY_ID'
        WHEN ds.data_source_id = 5  THEN 'CRITICAL_HABITAT_ID'
        WHEN ds.data_source_id = 6  THEN 'REPORT_ID'
        WHEN ds.data_source_id = 7  THEN NULL
        WHEN ds.data_source_id = 8  THEN NULL
        WHEN ds.data_source_id = 9  THEN 'AQ_TAG'
        WHEN ds.data_source_id = 10 THEN 'WELL_TAG_NO'
        WHEN ds.data_source_id = 11 THEN 'LINEAR_FEATURE_ID'
        WHEN ds.data_source_id = 12 THEN 'WLS_WRL_SYSID'
        WHEN ds.data_source_id = 13 THEN NULL
        ELSE NULL
        END
    """)

    # initial data for required_map_properties
    # these are the fields that we need for coloring markers on the map based on properties of the features
    op.execute("""
        UPDATE display_catalogue AS dc SET required_map_properties = CASE
            WHEN dc.display_data_name = 'water_rights_licences' THEN ARRAY['POD_SUBTYPE', 'LICENCE_NUMBER']
            WHEN dc.display_data_name = 'freshwater_atlas_stream_directions' THEN ARRAY['DOWNSTREAM_DIRECTION']
            WHEN dc.display_data_name = 'water_allocation_restrictions' THEN ARRAY['PRIMARY_RESTRICTION_CODE']
            ELSE ARRAY[]::text[]
        END
    """)

    # initial data for mapbox_layer_id's
    # these are the id's used to know which layers to replace in mapbox
    op.execute("""
        UPDATE display_catalogue AS dc SET mapbox_layer_id = CASE
            WHEN dc.display_data_name = 'automated_snow_weather_station_locations' THEN 'iit-water.2svbut5f'
            WHEN dc.display_data_name = 'bc_major_watersheds' THEN 'iit-water.0tsq064k'
            WHEN dc.display_data_name = 'bc_wildfire_active_weather_stations' THEN 'iit-water.2svbut5f'
            WHEN dc.display_data_name = 'cadastral' THEN 'iit-water.36r1x37x'
            WHEN dc.display_data_name = 'critical_habitat_species_at_risk' THEN 'iit-water.0tsq064k'
            WHEN dc.display_data_name = 'ecocat_water_related_reports' THEN 'iit-water.2svbut5f'
            WHEN dc.display_data_name = 'freshwater_atlas_stream_directions' THEN 'iit-water.7iwr3fo1'
            WHEN dc.display_data_name = 'freshwater_atlas_watersheds' THEN 'iit-water.7iwr3fo1'
            WHEN dc.display_data_name = 'ground_water_aquifers' THEN 'iit-water.0tsq064k'
            WHEN dc.display_data_name = 'groundwater_wells' THEN 'iit-water.2svbut5f'
            WHEN dc.display_data_name = 'water_allocation_restrictions' THEN 'iit-water.2ah76e1a'
            WHEN dc.display_data_name = 'water_rights_licenses' THEN 'iit-water.2svbut5f'
            WHEN dc.display_data_name = 'hydat.stations' THEN 'iit-water.2svbut5f'
            ELSE ''
        END
    """)

    op.alter_column('data_source', 'data_table_name', nullable=False)
    op.alter_column('data_source', 'source_object_name', nullable=False)
    op.alter_column('display_catalogue', 'mapbox_layer_id', nullable=False)
    op.execute('SET search_path TO public')

    # add water applications
    op.create_table(
        'water_rights_applications',

        sa.Column('WLS_WRA_SYSID', sa.Integer,
                  comment='WLS WRA SYSID is a system generated unique identification number.'),
        sa.Column('APPLICATION_JOB_NUMBER', sa.String, primary_key=True,
                  comment='APPLICATION JOB NUMBER is a unique identifier for a ground water licence application, e.g. 1003202.'),
        sa.Column('POD_NUMBER', sa.String,
                  comment='POD NUMBER is the unique identifier for a Point of Diversion, e.g., PW189413. Each POD can have multiple licences associated with it.'),
        sa.Column('POD_SUBTYPE', sa.String,
                  comment='POD SUBTYPE distinguishes the different POD types, i.e., POD (a surface water point of diversion), PWD (a point of well diversion that diverts groundwater), or PG (a point of groundwater diversion that diverts grounwater such as a dugout, ditch or quarry).'),
        sa.Column('POD_DIVERSION_TYPE', sa.String,
                  comment='POD_DIVERSION_TYPE is the type of diversion for a point of groundwater diversion (PG subtype), i.e., Dugout, Ditch, Quarry. Since this only applies to PG subtypes, other subypes (POD or PWD) will be left blank (null value).'),
        sa.Column('FILE_NUMBER', sa.String,
                  comment='FILE NUMBER is the water business file number, assigned during the application phase, e.g., 0321048. A file may hold one or more applications.'),
        sa.Column('APPLICATION_STATUS', sa.String,
                  comment='APPLICATION STATUS is the status of the water rights application submitted by the applicant. There are two possible statuses: Active Application, if the application is undergoing adjudication; or Refused, if the application is complete but no licence was granted. When an application is granted as a licence it is removed from the applications dataset and added to the licences dataset.'),
        sa.Column('WELL_TAG_NUMBER', sa.Integer,
                  comment='WELL TAG NUMBER is a unique well identifier for either registered or licensed wells, e.g., 12345.'),
        sa.Column('PURPOSE_USE_CODE', sa.String,
                  comment='PURPOSE USE CODE is the use of water authorized by the licence, identified as a code, e.g., 02I.'),
        sa.Column('PURPOSE_USE', sa.String,
                  comment='PURPOSE USE is the use of water authorized by the licence, e.g., Industrial.'),
        sa.Column('QTY_DIVERSION_MAX_RATE', sa.Float,
                  comment='QTY DIVERSION MAX RATE is the maximum authorized diversion rate of water within a second, minute or day up to the total licensed quantity per year, e.g, 0.006, 2000'),
        sa.Column('QTY_UNITS_DIVERSION_MAX_RATE', sa.String,
                  comment='QTY UNITS DIVERSION MAX RATE are the units of measurement for the maximum diversion rate of water authorized in the licence, e.g., m3/second, m3/minute, m3/day, m3/year.'),
        sa.Column('PRIMARY_APPLICANT_NAME', sa.String,
                  comment='PRIMARY APPLICANT NAME is the primary contact for the application, co-applicants will be displayed as et al.'),
        sa.Column('ADDRESS_LINE_1', sa.String,
                  comment='ADDRESS LINE 1 is the first line of the applicant\'s mailing address.'),
        sa.Column('ADDRESS_LINE_2', sa.String,
                  comment='ADDRESS LINE 2 is the second line of the applicant\'s mailing address.'),
        sa.Column('ADDRESS_LINE_3', sa.String,
                  comment='ADDRESS LINE 3 is the third line of the applicant\'s mailing address.'),
        sa.Column('ADDRESS_LINE_4', sa.String,
                  comment='ADDRESS LINE 4 is the fourth line of the applicant\'s mailing address.'),
        sa.Column('COUNTRY', sa.String, comment='COUNTRY is the applicant\'s country.'),
        sa.Column('POSTAL_CODE', sa.String, comment='POSTAL CODE is the applicant\'s postal code.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.String,
                  comment='	LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), of the location of the feature as measured from the prime meridian, e.g., -123.093544.'),
        sa.Column('DISTRICT_PRECINCT_NAME', sa.String,
                  comment='DISTRICT PRECINCT NAME is a jurisdictional area within a Water District. It is a combination of District and Precinct codes and names, e.g., New Westminster / Coquitlam. Not all Water Districts contain Precincts.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates defining the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='	OBJECTID is a column required by spatial layers that interact with ESRI ArcSDE. It is populated with unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE ANNO CAD DATA is a binary sa.column used by spatial tools '
                          'to store annotation, curve features and CAD data when using the '
                          'SDO GEOMETRY storage data type.')
    )

    op.execute('SET search_path TO metadata')

    op.execute("""
        INSERT INTO vector_catalogue (
            vector_catalogue_id,
            description,
            vector_name,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES (
            (SELECT MAX(vector_catalogue_id) FROM vector_catalogue) + 1,
            'Water Rights Applications',
            'water_rights_applications',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        );

        INSERT INTO data_source (
            data_source_id,
            data_format_code,
            name,
            description,
            source_url,
            source_object_name,
            data_table_name,
            source_object_id,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES (
            (SELECT MAX(data_source_id) FROM data_source) + 1,
            'json',
            'Water Rights Applications - Public',
            'This is a province-wide SDE spatial layer displaying water rights licence application data, administrated under the Water Sustainability Act which includes application data for both surface water and groundwater Points of Diversions. Point of Diversion types include surface water Points of Diversion (PDs) groundwater Points of Well Diversion (PWDs) as well as Points of Groundwater diversion (PGs), non-well groundwater diversion points such as dugouts, ditches and quarries. This layer contains a record for each water licence application that has been both received and reviewed by FrountcounterBC. This layer contains a record of each current water licence application in the province which includes each POD type that exists in the province (each POD can have multiple licences). For each record, some basic information about the water licence application is included.',
            'https://catalogue.data.gov.bc.ca/dataset/water-rights-applications-public#edc-pow',
            'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_APPLICTNS_SV',
            'water_rights_applications',
            'APPLICATION_JOB_NUMBER',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        );

        INSERT INTO display_catalogue (
            display_data_name,
            display_name,
            label_column,
            label,
            highlight_columns,
            vector_catalogue_id,
            data_source_id,
            layer_category_code,
            mapbox_layer_id,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES (
            'water_rights_applications',
            'Water Rights Applications',
            'APPLICATION_JOB_NUMBER',
            'Application Job Number',
            ARRAY[
                'APPLICATION_JOB_NUMBER',
                'POD_NUMBER',
                'POD_SUBTYPE',
                'POD_DIVERSION_TYPE',
                'FILE_NUMBER',
                'APPLICATION_STATUS',
                'WELL_TAG_NUMBER',
                'PURPOSE_USE_CODE',
                'PURPOSE_USE',
                'QTY_DIVERSION_MAX_RATE',
                'QTY_UNITS_DIVERSION_MAX_RATE',
                'PRIMARY_APPLICANT_NAME',
                'ADDRESS_LINE_1',
                'POSTAL_CODE',
                'DISTRICT_PRECINCT_NAME'
            ],
            (SELECT MAX(vector_catalogue_id) FROM vector_catalogue),
            (SELECT MAX(data_source_id) FROM data_source),
            'WATER_ADMINISTRATION',
            'iit-water.2svbut5f',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        );
    """)

    op.execute('SET search_path TO public')

    # add stream table2
    op.create_table(
        'fwa_stream_networks',
        sa.Column('OGC_FID', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('LINEAR_FEATURE_ID', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('WATERSHED_GROUP_ID', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('EDGE_TYPE', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('BLUE_LINE_KEY', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('WATERSHED_KEY', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('FWA_WATERSHED_CODE', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('LOCAL_WATERSHED_CODE', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('WATERSHED_GROUP_CODE', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('DOWNSTREAM_ROUTE_MEASURE', postgresql.DOUBLE_PRECISION(precision=53),
                  autoincrement=False, nullable=True),
        sa.Column('LENGTH_METRE', postgresql.DOUBLE_PRECISION(precision=53),
                  autoincrement=False, nullable=True),
        sa.Column('FEATURE_SOURCE', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('GNIS_ID', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('GNIS_NAME', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('LEFT_RIGHT_TRIBUTARY', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('STREAM_ORDER', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('STREAM_MAGNITUDE', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('WATERBODY_KEY', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('BLUE_LINE_KEY_50K', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('WATERSHED_CODE_50K', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('WATERSHED_KEY_50K', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('WATERSHED_GROUP_CODE_50K', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('GRADIENT', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('FEATURE_CODE', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('OBJECTID', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('SE_ANNO_CAD_DATA', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            'FEATURE_LENGTH_M', postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False, nullable=True),
        sa.Column('GEOMETRY.LEN', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('fme_feature_type', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('GEOMETRY', geoalchemy2.types.Geometry(
            geometry_type='LINESTRINGZ',
            srid=4326), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('OGC_FID', name='fwa_stream_networks_pkey')
    )
    op.create_index('fwa_stream_networks_geom_geom_idx', 'fwa_stream_networks',
                    ['GEOMETRY'], unique=False, postgresql_using="gist")

    # add metadata for this layer.
    op.execute('SET search_path TO metadata')

    # add sequences to columns that are missing them.
    op.execute("""
            CREATE SEQUENCE vector_catalogue_id_seq;
            CREATE SEQUENCE data_source_id_seq;

            SELECT setval('vector_catalogue_id_seq',
                            COALESCE((SELECT MAX(vector_catalogue_id)+1 FROM vector_catalogue), 1),
                            false);
            SELECT setval('data_source_id_seq',
                            COALESCE((SELECT MAX(data_source_id)+1 FROM data_source), 1),
                            false);

            ALTER TABLE vector_catalogue
                ALTER COLUMN vector_catalogue_id SET DEFAULT NEXTVAL('vector_catalogue_id_seq');
            ALTER TABLE data_source
                ALTER COLUMN data_source_id SET DEFAULT NEXTVAL('data_source_id_seq');

            ALTER SEQUENCE vector_catalogue_id_seq OWNED BY vector_catalogue.vector_catalogue_id;
            ALTER SEQUENCE data_source_id_seq OWNED BY data_source.data_source_id;
        """)

    # populate stream layer info
    op.execute("""
        WITH vc_id AS (
                    INSERT INTO vector_catalogue (
                    description,
                    vector_name,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'Freshwater Atlas Stream Networks',
                    'fwa_stream_networks',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING vector_catalogue_id
            ),

            ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'Freshwater Atlas Stream Networks',
                    'Flow network arcs (observed, inferred and constructed). Contains no banks, coast or watershed bourdary arcs. Directionalized and connected. Contains heirarchial key and route identifier.',
                    'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-network',
                    'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP',
                    'fwa_stream_networks',
                    'LINEAR_FEATURE_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            )

            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                vector_catalogue_id,
                data_source_id,
                layer_category_code,
                mapbox_layer_id,
                required_map_properties,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'fwa_stream_networks',
                'Freshwater Atlas Stream Networks',
                'LINEAR_FEATURE_ID',
                'Feature ID',
                ARRAY[
                    'STREAM_ORDER', 'STREAM_MAGNITUDE', 'FEATURE_LENGTH_M', 'WATERSHED_GROUP_ID'
                ],
                vc_id.vector_catalogue_id,
                ds_id.data_source_id,
                'FRESHWATER_MARINE',
                'iit-water.fwa-streams',
                ARRAY[
                    'LINEAR_FEATURE_ID', 'FWA_WATERSHED_CODE', 'LOCAL_WATERSHED_CODE'
                ],
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM vc_id, ds_id ;
        """)

    op.execute('SET search_path TO public')

    # Renaming fwa_stream_networks table to freshwater_atlas_stream_networks
    op.rename_table('fwa_stream_networks', 'freshwater_atlas_stream_networks')

    op.execute('ALTER SEQUENCE "fwa_stream_networks_OGC_FID_seq" '
               'RENAME TO "freshwater_atlas_stream_networks_OGC_FID_seq"')

    op.execute(
        'ALTER INDEX fwa_stream_networks_pkey RENAME TO freshwater_atlas_stream_networks_pkey')
    op.execute(
        'ALTER INDEX fwa_stream_networks_geom_geom_idx RENAME TO freshwater_atlas_stream_networks_geom_geom_idx')
    op.execute('ALTER INDEX "idx_fwa_stream_networks_GEOMETRY" '
               'RENAME TO "idx_freshwater_atlas_stream_networks_GEOMETRY"')

    op.execute(
        'UPDATE metadata.data_source SET data_table_name=\'freshwater_atlas_stream_networks\' '
        'WHERE data_source_id=15 AND data_table_name=\'fwa_stream_networks\'')
    op.execute(
        'UPDATE metadata.display_catalogue SET display_data_name=\'freshwater_atlas_stream_networks\' '
        'WHERE data_source_id=15 AND display_data_name=\'fwa_stream_networks\'')
    op.execute(
        'UPDATE metadata.vector_catalogue SET vector_name=\'freshwater_atlas_stream_networks\' '
        'WHERE vector_catalogue_id=7 AND vector_name=\'fwa_stream_networks\'')

    # change pk for applications
    op.execute("""
    alter table water_rights_applications drop constraint water_rights_applications_pkey;
    alter table water_rights_applications alter column "WLS_WRA_SYSID" set data type varchar;
    alter table water_rights_applications add constraint water_rights_applications_pkey primary key ("WLS_WRA_SYSID");
    """)

    op.execute(
        """
        SELECT UpdateGeometrySRID('water_rights_applications', 'SHAPE', 4326);
        SELECT UpdateGeometrySRID('automated_snow_weather_station_locations', 'SHAPE', 4326);""")

    # add table for mapbox sources
    op.create_table('mapbox_source',
                    sa.Column('create_user', sa.String(length=100), nullable=True,
                              comment='The user who created this record in the database.'),
                    sa.Column('create_date', sa.DateTime(
                    ), nullable=True,
                              comment='Date and time (UTC) when the physical record was created in the database.'),
                    sa.Column('update_user', sa.String(length=100), nullable=True,
                              comment='The user who last updated this record in the database.'),
                    sa.Column('update_date', sa.DateTime(), nullable=True,
                              comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
                    sa.Column('effective_date', sa.DateTime(
                    ), nullable=True,
                              comment='The date and time that the code became valid and could be used.'),
                    sa.Column('expiry_date', sa.DateTime(
                    ), nullable=True,
                              comment='The date and time after which the code is no longer valid and should not be used.'),
                    sa.Column('mapbox_source_id', sa.String(), nullable=False),
                    sa.Column('max_zoom', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('mapbox_source_id'),
                    schema='metadata'
                    )
    op.add_column('display_catalogue',
                  sa.Column('mapbox_source_id', sa.String(), nullable=True),
                  schema='metadata'
                  )
    op.create_foreign_key(
        'fk_display_catalogue_mapbox_source_id',
        'display_catalogue', 'mapbox_source',
        ['mapbox_source_id'], ['mapbox_source_id'], source_schema="metadata",
        referent_schema="metadata"
    )

    op.execute("""
        INSERT INTO metadata.mapbox_source (mapbox_source_id, max_zoom) VALUES
        ('iit-water.2svbut5f', 9),
        ('iit-water.7iwr3fo1', NULL),
        ('iit-water.0tsq064k', NULL),
        ('iit-water.36r1x37x', NULL),
        ('iit-water.2ah76e1a', NULL),
        ('iit-water.6q8q0qac', NULL);
    """)

    op.execute("""
        UPDATE metadata.display_catalogue SET mapbox_layer_id='iit-water.6q8q0qac' WHERE mapbox_layer_id='iit-water.fwa-streams';
        UPDATE metadata.display_catalogue SET mapbox_source_id=mapbox_layer_id WHERE mapbox_layer_id != '';
    """)

    # add 3 First Nations layers
    op.create_table('fn_treaty_lands',
                    sa.Column('ogc_fid', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('TREATY_LAND_ID', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('TREATY', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('EFFECTIVE_DATE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('FIRST_NATION_NAME', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('LAND_TYPE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('CHAPTER_REFERENCE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('APPENDIX_REFERENCE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('COMMENTS', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('FEATURE_CODE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('OBJECTID', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('SE_ANNO_CAD_DATA', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column(
                        'FEATURE_AREA_SQM', postgresql.DOUBLE_PRECISION(precision=53),
                        autoincrement=False, nullable=True),
                    sa.Column(
                        'FEATURE_LENGTH_M', postgresql.DOUBLE_PRECISION(precision=53),
                        autoincrement=False, nullable=True),
                    sa.Column('GEOMETRY.area', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('GEOMETRY.len', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('fme_feature_type', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('SHAPE', geoalchemy2.types.Geometry(srid=4326), autoincrement=False,
                              nullable=True),
                    sa.PrimaryKeyConstraint('ogc_fid', name='fn_treaty_lands_pkey')
                    )
    op.create_index(
        'fn_treaty_lands_shape_geom_idx', 'fn_treaty_lands',
        ['SHAPE'], unique=False, postgresql_using="gist")

    op.create_table('fn_community_locations',
                    sa.Column('ogc_fid', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('COMMUNITY_LOCATION_ID', sa.INTEGER(), autoincrement=False,
                              nullable=True),
                    sa.Column('FIRST_NATION_BC_NAME', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('FIRST_NATION_FEDERAL_NAME', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('FIRST_NATION_FEDERAL_ID', sa.INTEGER(), autoincrement=False,
                              nullable=True),
                    sa.Column('URL_TO_BC_WEBSITE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('URL_TO_FEDERAL_WEBSITE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('URL_TO_FIRST_NATION_WEBSITE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('MEMBER_ORGANIZATION_NAMES', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('LANGUAGE_GROUP', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('BC_REGIONAL_OFFICE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('MAPSHEET_NUMBER', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('PREFERRED_NAME', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('ALTERNATIVE_NAME_1', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('ALTERNATIVE_NAME_2', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('ADDRESS_LINE1', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('ADDRESS_LINE2', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('OFFICE_CITY', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('OFFICE_PROVINCE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('OFFICE_POSTAL_CODE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('LOCATION_DESCRIPTION', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('SITE_NAME', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('SITE_NUMBER', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('COMMENTS', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('OBJECTID', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('SE_ANNO_CAD_DATA', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('fme_feature_type', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column(
                        'SHAPE', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326),
                        autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('ogc_fid', name='fn_community_locations_pkey')
                    )
    op.create_index(
        'fn_community_locations_shape_geom_idx',
        'fn_community_locations', ['SHAPE'], unique=False, postgresql_using="gist")

    op.create_table('fn_treaty_areas',
                    sa.Column('ogc_fid', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('TREATY_AREA_ID', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('TREATY', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('EFFECTIVE_DATE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('FIRST_NATION_NAME', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('AREA_TYPE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('LAND_TYPE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('GEOGRAPHIC_LOCATION', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('CHAPTER_REFERENCE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('APPENDIX_REFERENCE', sa.VARCHAR(), autoincrement=False,
                              nullable=True),
                    sa.Column('COMMENTS', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('FEATURE_CODE', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('SE_ANNO_CAD_DATA', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('OBJECTID', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column(
                        'FEATURE_AREA_SQM',
                        postgresql.DOUBLE_PRECISION(precision=53),
                        autoincrement=False, nullable=True),
                    sa.Column(
                        'FEATURE_LENGTH_M', postgresql.DOUBLE_PRECISION(precision=53),
                        autoincrement=False, nullable=True),
                    sa.Column('GEOMETRY.AREA', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('GEOMETRY.LEN', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('fme_feature_type', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('SHAPE', geoalchemy2.types.Geometry(srid=4326), autoincrement=False,
                              nullable=True),
                    sa.PrimaryKeyConstraint('ogc_fid', name='fn_treaty_areas_pkey')
                    )
    op.create_index(
        'fn_treaty_areas_shape_geom_idx',
        'fn_treaty_areas', ['SHAPE'], unique=False, postgresql_using="gist")

    op.execute('SET search_path TO metadata')

    # add metadata for this layer.

    op.execute("""
            INSERT INTO metadata.mapbox_source (mapbox_source_id, max_zoom) VALUES ('iit-water.first-nations', 9)
        """)

    # populate fn_community_locations info
    op.execute("""
        WITH vc_id AS (
                    INSERT INTO vector_catalogue (
                    description,
                    vector_name,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'First Nations Community Locations',
                    'fn_community_locations',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING vector_catalogue_id
            ),
            ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'First Nation Community Locations',
                    'This spatial dataset contains the approximate locations of First Nations in British Columbia. Locations are based on the location of the main community, as obtained from Aboriginal Affairs and Northern Development Canada (AANDC). This data includes 6 Yukon or NWT bands that have parts of their traditional territories in B.C. and have been accepted into the BC treaty process. This is a multipoint feature. LIMITATONS: Although every attempt has been made to ensure that this data is accurate and complete, some First Nations may be missing or inaccurately positioned. The First Nations themselves should be contacted for the definitive locations.',
                    'https://catalogue.data.gov.bc.ca/dataset/first-nation-community-locations',
                    'WHSE_HUMAN_CULTURAL_ECONOMIC.FN_COMMUNITY_LOCATIONS_SP',
                    'fn_community_locations',
                    'COMMUNITY_LOCATION_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                vector_catalogue_id,
                data_source_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'fn_community_locations',
                'First Nation Community Locations',
                'FIRST_NATION_BC_NAME',
                'Name of Band or First Nation',
                ARRAY[
                    'FIRST_NATION_BC_NAME', 'URL_TO_BC_WEBSITE', 'PREFERRED_NAME', 'LANGUAGE_GROUP'
                ],
                vc_id.vector_catalogue_id,
                ds_id.data_source_id,
                'LAND_TENURE',
                'iit-water.first-nations',
                'iit-water.first-nations',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM vc_id, ds_id ;
        """)

    # populate fn_treaty_areas info
    op.execute("""
        WITH vc_id AS (
                    INSERT INTO vector_catalogue (
                    description,
                    vector_name,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'First Nations Treaty Areas',
                    'fn_treaty_areas',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING vector_catalogue_id
            ),
            ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'First Nation Treaty Areas',
                    'This layer contains the areas within which the First Nation has a role (as described in the treaty) related to economic activities, governance activities and cultural activities.',
                    'https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-areas',
                    'WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_AREA_SP',
                    'fn_treaty_areas',
                    'TREATY_AREA_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                vector_catalogue_id,
                data_source_id,
                layer_category_code,
                mapbox_layer_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'fn_treaty_areas',
                'First Nations Treaty Areas',
                'TREATY',
                'First Nation or First Nations Organization',
                ARRAY[
                    'TREATY', 'FIRST_NATION_NAME', 'LAND_TYPE', 'GEOGRAPHIC_LOCATION', 'AREA_TYPE', 'EFFECTIVE_DATE', 'COMMENTS'
                ],
                vc_id.vector_catalogue_id,
                ds_id.data_source_id,
                'LAND_TENURE',
                'iit-water.first-nations',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM vc_id, ds_id ;
        """)

    # populate fn_treaty_lands info
    op.execute("""
        WITH vc_id AS (
                    INSERT INTO vector_catalogue (
                    description,
                    vector_name,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'First Nations Treaty Lands',
                    'fn_treaty_lands',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING vector_catalogue_id
            ),
            ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'First Nations Treaty Lands',
                    'This layer shows the lands that are owned by the First Nation as a result of the treaty and over which the First Nation has governance as described in the treaty. These boundaries should be treated as cartographic representations only. The official versions of these boundaries are contained within the treaty documents.',
                    'https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-lands',
                    'WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_LAND_SP',
                    'fn_treaty_lands',
                    'TREATY_LAND_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                vector_catalogue_id,
                data_source_id,
                layer_category_code,
                mapbox_layer_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'fn_treaty_lands',
                'First Nations Treaty Lands',
                'TREATY',
                'First Nation or First Nations Organization',
                ARRAY[
                    'TREATY', 'FIRST_NATION_NAME', 'LAND_TYPE', 'EFFECTIVE_DATE', 'COMMENTS'
                ],
                vc_id.vector_catalogue_id,
                ds_id.data_source_id,
                'LAND_TENURE',
                'iit-water.first-nations',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM vc_id, ds_id ;
        """)

    op.execute('SET search_path TO public')

    # add glacier layer refs
    op.execute('SET search_path TO metadata')

    op.execute("""
            INSERT INTO metadata.mapbox_source (mapbox_source_id, max_zoom) VALUES ('iit-water.glaciers', 9)
        """)

    # populate freshwater_atlas_glaciers info
    op.execute("""
              WITH ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'Freshwater Atlas Glaciers',
                    'Glaciers and ice masses for the province of British Columbia.',
                    'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-glaciers',
                    'WHSE_BASEMAPPING.FWA_GLACIERS_POLY',
                    'freshwater_atlas_glaciers',
                    'WATERBODY_POLY_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            ),
            wms_id AS (
              INSERT INTO wms_catalogue (
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'Freshwater Atlas Glaciers',
                    'WHSE_BASEMAPPING.FWA_GLACIERS_POLY',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                wms_catalogue_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'freshwater_atlas_glaciers',
                'Freshwater Atlas Glaciers',
                'GNIS_NAME_1',
                'Name',
                ARRAY[
                    'WATERBODY_TYPE', 'AREA_HA', 'GNIS_NAME_1', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M'
                ],
                ds_id.data_source_id,
                wms_id.wms_catalogue_id,
                'FRESHWATER_MARINE',
                'iit-water.0tsq064k',
                'iit-water.0tsq064k',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM ds_id, wms_id ;
        """)

    op.execute('SET search_path TO public')

    # add zone boundary layer refs
    op.execute('SET search_path TO metadata')

    # populate hydrologic_zone_boundaries info
    op.execute("""
        WITH ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'Hydrologic Zone Boundaries of BC',
                    'Zones that represent areas of homogeneous hydrologic and geomorphological characteristics.',
                    'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrologic-zone-boundaries-of-british-columbia',
                    'WHSE_WATER_MANAGEMENT.HYDZ_HYDROLOGICZONE_SP',
                    'hydrologic_zone_boundaries',
                    'HYDROLOGICZONE_SP_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            ),
            wms_id AS (
              INSERT INTO wms_catalogue (
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'Hydrologic Zone Boundaries of BC',
                    'WHSE_WATER_MANAGEMENT.HYDZ_HYDROLOGICZONE_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                wms_catalogue_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                required_map_properties,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'hydrologic_zone_boundaries',
                'Hydrologic Zone Boundaries of BC',
                'HYDROLOGICZONE_NAME',
                'Name',
                ARRAY[
                    'HYDROLOGICZONE_SP_ID', 'HYDROLOGICZONE_NO', 'HYDROLOGICZONE_NAME', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M'
                ],
                ds_id.data_source_id,
                wms_id.wms_catalogue_id,
                'FRESHWATER_MARINE',
                'iit-water.0tsq064k',
                'iit-water.0tsq064k',
                ARRAY[
                    'HYDROLOGICZONE_NO'
                ],
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM ds_id, wms_id ;
        """)

    op.execute('SET search_path TO public')

    # add allocation coefficient tables
    op.execute("create schema if not exists modeling")
    op.execute('SET search_path TO modeling')

    op.create_table(
        'water_allocation_coefficients',
        Column('water_allocation_coefficients_id', sa.Integer, primary_key=True),
        Column('economic_region_name', sa.String,
               comment='The BC economic region name that these co-efficients are used as standard values for water calculations.'),
        Column('purpose_use_code', sa.String, comment='The code representing the purpose use.'),
        Column('purpose_use', sa.String, comment='The english written purpose use.'),
        Column('rationale', sa.String,
               comment='The rationale behind where these coefficients were derived from.'),
        Column('monthly_coefficients', ARRAY(sa.Float), nullable=False, server_default="{}",
               comment='Co-efficient values for each month in order from January to Decemeber.'),

        Column('create_user', sa.String(100),
               comment='The user who created this record in the database.'),
        Column('create_date', sa.DateTime,
               comment='Date and time (UTC) when the physical record was created in the database.'),
        Column('update_user', sa.String(100),
               comment='The user who last updated this record in the database.'),
        Column('update_date', sa.DateTime,
               comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        Column('effective_date', sa.DateTime,
               comment='The date and time that the code became valid and could be used.'),
        Column('expiry_date', sa.DateTime,
               comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.create_table(
        'water_return_coefficients',
        Column('water_return_coefficients_id', sa.Integer, primary_key=True),
        Column('economic_region_name', sa.String,
               comment='The BC economic region name that these co-efficients are used as standard values for water calculations.'),
        Column('purpose_use_code', sa.String, comment='The code representing the purpose use.'),
        Column('purpose_use', sa.String, comment='The english written purpose use.'),
        Column('rationale', sa.String,
               comment='The rationale behind where these coefficients were derived from.'),
        Column('annual_coefficient', sa.Float,
               comment='The coefficient for annual water return for this water rights purpose.'),
        Column('monthly_coefficients', ARRAY(sa.Float), nullable=False, server_default="{}",
               comment='Co-efficient values for each month in order from January to Decemeber.'),

        Column('create_user', sa.String(100),
               comment='The user who created this record in the database.'),
        Column('create_date', sa.DateTime,
               comment='Date and time (UTC) when the physical record was created in the database.'),
        Column('update_user', sa.String(100),
               comment='The user who last updated this record in the database.'),
        Column('update_date', sa.DateTime,
               comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        Column('effective_date', sa.DateTime,
               comment='The date and time that the code became valid and could be used.'),
        Column('expiry_date', sa.DateTime,
               comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.execute("""
            INSERT INTO water_allocation_coefficients (
                purpose_use_code,
                purpose_use,
                monthly_coefficients,
                rationale,
                economic_region_name,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES
                ('02I28', 'Indl Waste Mgmt: Sewage Disposal', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('11C', 'Conservation: Construct Works', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('01A01', 'Incidental - Domestic', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I07', 'Indl Waste Mgmt: Effluent', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I32', 'Swimming Pool', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'same as industrial because that is the category that hotels fall under', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02HU', 'Marine Export - Used (Inactive)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I43', 'Transport Mgmt: Tunnelling/Well Drilling', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I35', 'Waterworks: Water Delivery', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'use same as residential', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('09B', 'Mineralized Water: Comm. Pool', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I01', 'Vehicle & Eqpt: Brake Cooling', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I23', 'O&G: Oil Fld Inject (non-deep GW)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05E', 'O & G: Hydrlc Frctrg (non-deep GW)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('09A', 'Mineralized Water: Bottling & Dist', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05H', 'O & G: Drilling', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA06', 'Ice & Snow Making', ARRAY[ 0.25,0.25,0,0,0,0,0,0,0,0,0.25,0.25 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA04', 'Crop Harvest, Protect & Compost', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02E', 'Pond & Aquaculture', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I27', 'Misc Indl: Sediment Control', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'summer heavy', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I40', 'Comm. Enterprise: Amusement Park', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'use same as residential - land and garden', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('04B', 'Land Improve: Indl for Rehab/Remed', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('07B', 'Power: Commercial', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I02', 'Camps & Pub Facil: Non-Work Camps', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I17', 'Grnhouse & Nursery: Grnhouse', ARRAY[ 0,0.01,0.01,0.02,0.1,0.14,0.24,0.24,0.17,0.06,0.01,0 ], 'actual use data from Dave Woodske, P.Ag. | Industry Specialist, Orname', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02H', 'Bulk Shipment for Marine Trans', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I03', 'Camps & Pub Facil: Church/Com Hall', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I12', 'Misc Indl: Fire Protection', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I', 'Industrial - Misc (Inactive)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('01A', 'Domestic', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05F', 'O & G: Hydrlc Frctrg  (deep GW)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02G', 'Fresh Water Bottling', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('07C', 'Power: General', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I31', 'Livestock & Animal: Stockwatering', ARRAY[ 0.07,0.07,0.07,0.07,0.07,0.12,0.15,0.1,0.07,0.07,0.07,0.07 ], 'from BC Ministry of Agriculture Livestock watering factsheets', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05A', 'Mining: Hydraulic', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I21', 'Camps & Pub Facil: Institutions', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I37', 'Camps & Pub Facil: Work Camps', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('00A', 'Waterworks: Local Provider', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I29', 'Processing & Mfg: Shipyard', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I05', 'Crops: Crop Suppression', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA09', 'Processing & Manufacturing', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I26', 'River Improvement', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02C', 'Cooling', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I15', 'Livestock & Animal: Game Farm', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I22', 'Grnhouse & Nursery: Nursery', ARRAY[ 0,0.01,0.01,0.02,0.1,0.14,0.24,0.24,0.17,0.06,0.01,0 ], 'actual use data from Dave Woodske, P.Ag. | Industry Specialist, Orname', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02D', 'Comm. Enterprise: Enterprise', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I08', 'Transport Mgmt: Dust Control', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'summer heavy', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA13', 'Industrial Waste Mgmt', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA01', 'Domestic (WSA01)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I18', 'Heat Exchanger', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05C', 'Mining: Processing Ore', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I20', 'Ice & Snow Making: Ice', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05B', 'Mining: Washing Coal', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05D', 'Mining: Placer', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I33', 'Vehicle & Eqpt: Truck & Eqp Wash', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02A', 'Pulp Mill', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('07A', 'Power: Residential', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I41', 'Livestock & Animal: Kennel', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I14', 'Crops: Frost Protection', ARRAY[ 0,0.5,0.5,0,0,0,0,0,0,0,0,0 ], 'Carolyn Teasdale, Berry Specialist, Ministry of Agriculture', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA10', 'Well Drill/Transprt Mgmt', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I16', 'Indl Waste Mgmt: Garbage Dump', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I46', 'Transport Mgmt: Road Maint.', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'only has units in MD so no coefficient required', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I13', 'Crops: Flood Harvesting', ARRAY[ 0,0,0,0,0,0,0,0,0.25,0.5,0.25,1 ], 'Carolyn Teasdale, Berry Specialist, Ministry of Agriculture', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I42', 'Lwn, Fairway & Grdn: Res L/G', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I39', 'Vehicle & Eqpt: Mine & Quarry', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA11', 'Lawn, Fairway & Garden', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('00C', 'Waterworks: Sales', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('08A', 'Stream Storage: Non-Power', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I36', 'Processing & Mfg: Wharves', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I47', 'Heat Exchanger, Residential', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA08', 'Livestock & Animal', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I34', 'Indl Waste Mgmt: Intake Wash', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA03', 'Commercial Enterprise', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('04A', 'Land Improve: General', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I19', 'Hydraulicking (Inactive)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('03A', 'Irrigation: Local Provider', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('00B', 'Waterworks (other than LP)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I38', 'Fish Hatchery', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA02', 'Camps & Public Facilities', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('11B', 'Conservation: Use of Water', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I24', 'Misc Indl: Overburden Disposal', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I30', 'Ice & Snow Making: Snow', ARRAY[ 0.25,0.25,0,0,0,0,0,0,0,0,0.25,0.25 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA05', 'Greenhouse & Nursery', ARRAY[ 0,0.01,0.01,0.02,0.1,0.14,0.24,0.24,0.17,0.06,0.01,0 ], 'actual use data from Dave Woodske, P.Ag. | Industry Specialist, Orname', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I23', 'O & G: Oil Fld Inject. (non-deep GW)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA07', 'Misc Indust', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I11', 'Processing & Mfg: Fire Prevention', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 'same as fire protection (1/12) because it is used consistently', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('08B', 'Aquifer Storage: NP', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I06', 'Misc Indl: Dewatering', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'only quantity=0 - one time extractions', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I09', 'Camps & Pub Facil: Exhibition Grnds', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('11A', 'Conservation: Storage', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'assume flow returned', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('03B', 'Irrigation: Private', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05E', 'O & G: Hydrlc Frctrg (non-deep GW)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA12', 'Vehicle & Equipment', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02B', 'Processing & Mfg: Processing', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('12A', 'Stream Storage: Power', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02F', 'Lwn, Fairway & Grdn: Watering', ARRAY[ 0,0,0,0.1,0.2,0.2,0.2,0.2,0.1,0,0,0 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I04', 'Conveying (Inactive)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
            ;
            INSERT INTO water_return_coefficients (
                purpose_use_code,
                purpose_use,
                monthly_coefficients,
                annual_coefficient,
                rationale,
                economic_region_name,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES
                ('02I28', 'Indl Waste Mgmt: Sewage Disposal', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('11C', 'Conservation: Construct Works', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('01A01', 'Incidental - Domestic', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I07', 'Indl Waste Mgmt: Effluent', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I32', 'Swimming Pool', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'same as industrial because that is the category that hotels fall under', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02HU', 'Marine Export - Used (Inactive)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I43', 'Transport Mgmt: Tunnelling/Well Drilling', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I35', 'Waterworks: Water Delivery', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'assume fully consumptive', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('09B', 'Mineralized Water: Comm. Pool', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I01', 'Vehicle & Eqpt: Brake Cooling', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I23', 'O&G: Oil Fld Inject (non-deep GW)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05E', 'O & G: Hydrlc Frctrg (non-deep GW)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('09A', 'Mineralized Water: Bottling & Dist', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05H', 'O & G: Drilling', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA06', 'Ice & Snow Making', ARRAY[ 0,0,0.25,0.25,0.25,0.25,0,0,0,0,0,0 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA04', 'Crop Harvest, Protect & Compost', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02E', 'Pond & Aquaculture', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I27', 'Misc Indl: Sediment Control', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'assume fully consumptive', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I40', 'Comm. Enterprise: Amusement Park', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'use same as residential - land and garden', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('04B', 'Land Improve: Indl for Rehab/Remed', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('07B', 'Power: Commercial', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I02', 'Camps & Pub Facil: Non-Work Camps', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I17', 'Grnhouse & Nursery: Grnhouse', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'assume fully consumptive', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02H', 'Bulk Shipment for Marine Trans', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I03', 'Camps & Pub Facil: Church/Com Hall', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I12', 'Misc Indl: Fire Protection', ARRAY[ 0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333,0.02083333 ], 0.5, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I', 'Industrial - Misc (Inactive)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('01A', 'Domestic', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05F', 'O & G: Hydrlc Frctrg  (deep GW)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02G', 'Fresh Water Bottling', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('07C', 'Power: General', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I31', 'Livestock & Animal: Stockwatering', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from BC Ministry of Agriculture Livestock watering factsheets', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05A', 'Mining: Hydraulic', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I21', 'Camps & Pub Facil: Institutions', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I37', 'Camps & Pub Facil: Work Camps', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('00A', 'Waterworks: Local Provider', ARRAY[ 0,0,0,0.01,0.01,0.015,0.015,0.02,0.02,0.01,0,0 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I29', 'Processing & Mfg: Shipyard', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I05', 'Crops: Crop Suppression', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA09', 'Processing & Manufacturing', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I26', 'River Improvement', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02C', 'Cooling', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I15', 'Livestock & Animal: Game Farm', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I22', 'Grnhouse & Nursery: Nursery', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'assume fully consumptive', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02D', 'Comm. Enterprise: Enterprise', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I08', 'Transport Mgmt: Dust Control', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'summer heavy', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA13', 'Industrial Waste Mgmt', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA01', 'Domestic (WSA01)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I18', 'Heat Exchanger', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05C', 'Mining: Processing Ore', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I20', 'Ice & Snow Making: Ice', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05B', 'Mining: Washing Coal', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05D', 'Mining: Placer', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I33', 'Vehicle & Eqpt: Truck & Eqp Wash', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from BC Ministry of Agriculture Livestock watering factsheets', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02A', 'Pulp Mill', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('07A', 'Power: Residential', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I41', 'Livestock & Animal: Kennel', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I14', 'Crops: Frost Protection', ARRAY[ 0,0,0.025,0.025,0.02,0.01,0,0,0,0,0,0 ], 0.1, 'Carolyn Teasdale, Berry Specialist, Ministry of Agriculture', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA10', 'Well Drill/Transprt Mgmt', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I16', 'Indl Waste Mgmt: Garbage Dump', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I46', 'Transport Mgmt: Road Maint.', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'only has units in MD so no coefficient required', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I13', 'Crops: Flood Harvesting', ARRAY[ 0.01,0,0,0,0,0,0,0,0.02,0.04,0.03,0.02 ], 0.1, 'Carolyn Teasdale, Berry Specialist, Ministry of Agriculture', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I42', 'Lwn, Fairway & Grdn: Res L/G', ARRAY[ 0,0,0,0.01,0.01,0.015,0.015,0.02,0.02,0.01,0,0 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I39', 'Vehicle & Eqpt: Mine & Quarry', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA11', 'Lawn, Fairway & Garden', ARRAY[ 0,0,0,0.01,0.01,0.015,0.015,0.02,0.02,0.01,0,0 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('00C', 'Waterworks: Sales', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('08A', 'Stream Storage: Non-Power', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I36', 'Processing & Mfg: Wharves', ARRAY[ 0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25 ], 0.25, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I47', 'Heat Exchanger, Residential', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA08', 'Livestock & Animal', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I34', 'Indl Waste Mgmt: Intake Wash', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA03', 'Commercial Enterprise', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('04A', 'Land Improve: General', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I19', 'Hydraulicking (Inactive)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('03A', 'Irrigation: Local Provider', ARRAY[ 0.005,0.005,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005,0.005 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('00B', 'Waterworks (other than LP)', ARRAY[ 0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I38', 'Fish Hatchery', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA02', 'Camps & Public Facilities', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('11B', 'Conservation: Use of Water', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I24', 'Misc Indl: Overburden Disposal', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I30', 'Ice & Snow Making: Snow', ARRAY[ 0,0,0.25,0.25,0.25,0.25,0,0,0,0,0,0 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA05', 'Greenhouse & Nursery', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'assume fully consumptive', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I23', 'O & G: Oil Fld Inject. (non-deep GW)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA07', 'Misc Indust', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I11', 'Processing & Mfg: Fire Prevention', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'same as fire protection (1/12) because it is used consistently', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('08B', 'Aquifer Storage: NP', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I06', 'Misc Indl: Dewatering', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'only quantity=0 - one time extractions', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I09', 'Camps & Pub Facil: Exhibition Grnds', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('11A', 'Conservation: Storage', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('03B', 'Irrigation: Private', ARRAY[ 0.005,0.005,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005,0.005 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('05E', 'O & G: Hydrlc Frctrg (non-deep GW)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('WSA12', 'Vehicle & Equipment', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02B', 'Processing & Mfg: Processing', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('12A', 'Stream Storage: Power', ARRAY[ 0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333,0.0833333 ], 1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02F', 'Lwn, Fairway & Grdn: Watering', ARRAY[ 0,0,0,0.01,0.01,0.015,0.015,0.02,0.02,0.01,0,0 ], 0.1, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('02I04', 'Conveying (Inactive)', ARRAY[ 0,0,0,0,0,0,0,0,0,0,0,0 ], 0, 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
            ;
        """)

    op.execute('SET search_path TO public')

    # set wms_style to non nullable
    op.execute("""
        update metadata.wms_catalogue set wms_style='' where wms_style is null;
        alter table metadata.wms_catalogue alter column wms_style set not null;
        alter table metadata.wms_catalogue alter column wms_style set default '';
    """)

    # update gwells link
    stmt = """
            update  metadata.data_source
            set     source_url = 'https://apps.nrs.gov.bc.ca/gwells/'
            where   source_url = 'https://catalogue.data.gov.bc.ca/dataset/ground-water-wells'
            and     name = 'Ground Water Wells';
        """
    op.execute(stmt)

    # update wells metadata
    q = """
        UPDATE  metadata.display_catalogue
        SET     label_column = 'well_tag_number'
        WHERE   display_data_name = 'groundwater_wells'
    """
    op.execute(q)

    # update glacier label column
    q = """
        UPDATE  metadata.display_catalogue
        SET     label_column = 'WATERBODY_POLY_ID'
        WHERE   display_data_name = 'freshwater_atlas_glaciers'
    """
    op.execute(q)

    # add iso model layer
    op.create_table(
        'normal_annual_runoff_isolines',
        sa.Column('id', sa.Integer, primary_key=True,
                  comment='Arbitrary id to differentiate polygons.'),
        sa.Column('ANNUAL_RUNOFF_IN_MM', sa.Integer,
                  comment='Annual runoff of precipitation in the area of the associated polygon. '
                          'Possible values in mm: 10 50 100 200 500 1000 1500 2000 3000 4000'),
        sa.Column('GEOMETRY', Geometry('POLYGON', 4326),
                  comment='This geometry is the polygon associated with the isoline for this area.')
    )

    op.execute('SET search_path TO metadata')

    # populate normal_annual_runoff_isolines info
    op.execute("""
        WITH ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'Normal Annual Runoff Isolines (1961 - 1990)',
                    'Spatial layer intended to display normal annual runoff isolines, in millimetres, for 1961 -1990.',
                    'https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical',
                    'WHSE_WATER_MANAGEMENT.HYDZ_ANNUAL_RUNOFF_LINE',
                    'normal_annual_runoff_isolines',
                    'id',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            ),
            vc_id AS (
                    INSERT INTO vector_catalogue (
                    description,
                    vector_name,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'Normal Annual Runoff Isolines (1961 - 1990)',
                    'normal_annual_runoff_isolines',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING vector_catalogue_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                vector_catalogue_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                required_map_properties,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'normal_annual_runoff_isolines',
                'Normal Annual Runoff Isolines (1961 - 1990) - Historical',
                'id',
                'Id',
                ARRAY[
                    'id', 'ANNUAL_RUNOFF_IN_MM'
                ],
                ds_id.data_source_id,
                vc_id.vector_catalogue_id,
                'FRESHWATER_MARINE',
                'iit-water.0tsq064k',
                'iit-water.0tsq064k',
                ARRAY[
                    'ANNUAL_RUNOFF_IN_MM'
                ],
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM ds_id, vc_id ;
        """)

    op.execute('SET search_path TO public')

    # Update groundwater layer names
    op.execute('SET search_path TO metadata')
    op.execute("""
               UPDATE data_source AS ds SET name = 'Groundwater Wells'
               WHERE data_table_name = 'ground_water_wells'
        """)
    op.execute("""
                UPDATE data_source AS ds SET name = 'Groundwater Aquifers'
                WHERE data_table_name = 'ground_water_aquifers'
        """)
    op.execute('SET search_path TO public')

    # add mad model coefficients
    op.execute("create schema if not exists modeling")
    op.execute('SET search_path TO modeling')

    op.create_table(
        'model_output_type_code',
        sa.Column('model_output_type_code', sa.String, primary_key=True,
                  comment='The output type that this regression model outputs. Possible values: MAR, 7Q2, S-7Q10, MD'),
        sa.Column('description', sa.String,
                  comment='Description of the model output type.'),
        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was created in the database.'),
        sa.Column('update_user', sa.String(
            100), comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.create_table(
        'mad_model_coefficients',
        sa.Column('mad_model_coefficients_id', sa.Integer, primary_key=True),
        sa.Column('hydrologic_zone_id', sa.Integer,
                  comment='TA numeric identifier assigned to a zone that represents an area of homogenous hydrologic and geomorphological characteristics.'),
        sa.Column('model_output_type', sa.String,
                  sa.ForeignKey('modeling.model_output_type_code.model_output_type_code'),
                  comment='The resulting value that this multivariate model outputs. Possible values: MAR, 7Q2, S-7Q10, MD'),
        sa.Column('month', sa.Integer,
                  comment='The month of the year represented as an integer from 1-12 (0 if annual ouput)'),
        sa.Column('reference_model_id', sa.Integer,
                  comment='The model used for this zone in South Coast Stewardship Baseline (Brem, Fraser Valley South, Toba, Upper Lillooet)'),
        sa.Column('intercept_co', sa.Numeric,
                  comment='Intercept coefficient for the multi-variate model.'),
        sa.Column('median_elevation_co', sa.Numeric,
                  comment='Median elevation of the selected watershed area measured in meters (m).'),
        sa.Column('glacial_coverage_co', sa.Numeric,
                  comment='The amount of glacial coverage over the selected watershed area measured as a percentage (0.0-1.0).'),
        sa.Column('precipitation_co', sa.Numeric,
                  comment='The annual precipitation of the selected watershed area measured in milimeters per year (mm/year).'),
        sa.Column('potential_evapo_transpiration_co', sa.Numeric,
                  comment='A measure of the ability of the atmosphere to remove water through Evapo-Transpiration (ET) processes. A reference crop under optimal conditions, having the characteristics of well-watered grass with an assumed height of 12 centimeters, a fixed surface resistance of 70 seconds per meter and an albedo of 0.23.'),
        sa.Column('drainage_area_co', sa.Numeric,
                  comment='The drainage area of the selected watershed area measured in kilometers squared (km^2)'),
        sa.Column('solar_exposure_co', sa.Numeric,
                  comment='a surrogate variable in order to capture the effect of shadows, slope, and aspect together, a hillshade image was derived with shadows. The azimuth setting was 180° (due south) and the elevation was 45°. This roughly corresponds to noon on the 49th parallel in early summer.'),
        sa.Column('average_slope_co', sa.Numeric,
                  comment='The measure of rise over run (rise/run) of the selected watershed area.'),
        sa.Column('lake_coverage_co', sa.Numeric,
                  comment='The amount of lake coverage over the selected watershed area measured as a percentage (0.0-1.0).'),
        sa.Column('r2', sa.Float,
                  comment='The proportion of the variance for a dependent variable thats explained by an independent variable or variables in a regression model'),
        sa.Column('adjusted_r2', sa.Float,
                  comment='The correlation strength of additional variables.'),
        sa.Column('steyx', sa.Float,
                  comment='Standard error in the estimate of the hydrological variable (Y) as a function of the regression model (X).'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was created in the database.'),
        sa.Column('update_user', sa.String(
            100), comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.execute("""
            INSERT INTO model_output_type_code (
                model_output_type_code,
                description,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES
                ('MAR', 'Mean annual unit-area runoff measured in mm/year.', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('7Q2', '2-year return period Annual 7-day low flow (7Q2), which was adopted as replacement for the MALF7d, chosen to represent typical low flows of interest.', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('S-7Q10', 'the 10-year dry return period 7day late summer (Jun-Sep) low flow divided by the estimated MAD at the site: S-7Q10/MAD). A useful variable for characterizing the vulnerability of a watershed to summer low flows.', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('MD', 'Mean distribution of flow for the month calculated measured as a percent of the annual total.', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
            ;
        """)

    op.execute("""
            INSERT INTO mad_model_coefficients (
                hydrologic_zone_id,
                model_output_type,
                month,
                reference_model_id,
                intercept_co,
                median_elevation_co,
                glacial_coverage_co,
                precipitation_co,
                potential_evapo_transpiration_co,
                drainage_area_co,
                solar_exposure_co,
                average_slope_co,
                r2,
                adjusted_r2,
                steyx,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES
                (25, 'MAR', 0, 12, -30.05, 0, 0, 0.0162, 0, 0.00369, 0, 1.39, 0.97, 0.96, 4.16, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, '7Q2', 0, 12, 0.81, 0, -0.057, 0, -0.00102, -0.000006, 0, 0, 0.63, 0.52, 0.032, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'S-7Q10', 0, 12, 1.90, 0.000314, 0.685, 0, -0.0032, 0, 0, 0, 0.88, 0.83, 0.04, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 1, 13, 0.04, 0, -0.0512, 0.00000453, -0.0000216, 0, 0, 0, 0.62, 0.49, 0.001, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 2, 13, 0.00, 0, -0.0388, 0.00000342, 0.0000338, 0, 0, 0, 0.68, 0.58, 0.003, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 3, 13, -0.05, 0, -0.0475, 0.00000490, 0.000120, 0, 0, 0, 0.86, 0.81, 0.004, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 4, 13, -0.30, 0, -0.146, 0.00000433, 0.000578, 0, 0, 0, 0.94, 0.92, 0.012, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 5, 13, -0.58, 0, -0.600, -0.0000127, 0.00129, 0, 0, 0, 0.95, 0.93, 0.025, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 6, 13, 0.12, 0, -0.434, -0.00000682, 0.000205, 0, 0, 0, 0.84, 0.78, 0.023, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 7, 13, 0.66, 0, 0.381, 0.00000808, -0.000842, 0, 0, 0, 0.86, 0.81, 0.036, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 8, 13, 0.57, 0, 0.670, -0.00000763, -0.000778, 0, 0, 0, 0.96, 0.94, 0.021, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 9, 13, 0.33, 0, 0.369, -0.00000622, -0.000446, 0, 0, 0, 0.96, 0.95, 0.012, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 10, 13, 0.22, 0, 0.0931, -0.000000490, -0.000273, 0, 0, 0, 0.83, 0.77, 0.010, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 11, 13, 0.07, 0, -0.0676, 0.0000129, -0.0000620, 0, 0, 0, 0.66, 0.55, 0.008, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (25, 'MD', 12, 13, 0.04, 0, -0.0708, 0.00000628, -0.0000275, 0, 0, 0, 0.61, 0.48, 0.005, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),

                (26, 'MAR', 0, 13, -83.53, 0, 124, 0.0246, 0.121, 0, 0, 0, 0.70, 0.65, 13.8, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, '7Q2', 0, 12, 0.53, 0, -0.692, 0, -0.000478, 0.0000198, 0, 0, 0.61, 0.54, 0.043, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'S-7Q10', 0, 12, 1.15, 0, 0.717, 0, -0.00143, 0.0000314, 0, 0, 0.86, 0.83, 0.053, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 1, 12, 0.02, 0.0000141, -0.219, 0.00000788, 0, 0, 0, 0, 0.88, 0.85, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 2, 13, 0.02, -0.0000181, -0.125, 0, 0.0000875, 0, 0, 0, 0.78, 0.72, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 3, 13, -0.02, -0.0000237, -0.101, 0, 0.000161, 0, 0, 0, 0.83, 0.79, 0.008, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 4, 13, -0.06, -0.0000375, -0.0359, 0, 0.000276, 0, 0, 0, 0.76, 0.70, 0.011, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 5, 13, -0.10, -0.0000212, -0.0199, 0, 0.000420, 0, 0, 0, 0.51, 0.38, 0.021, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 6, 12, 0.14, 0.0000440, 0.00498, -0.0000122, 0, 0, 0, 0, 0.71, 0.63, 0.011, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 7, 12, 0.05, 0.0000697, 0.306, -0.00000988, 0, 0, 0, 0, 0.85, 0.81, 0.014, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 8, 13, 0.11, 0.0000916, 0.342, 0, -0.000255, 0, 0, 0, 0.91, 0.88, 0.016, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 9, 13, 0.24, 0.000000849, 0.184, 0, -0.000307, 0, 0, 0, 0.85, 0.81, 0.012, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 10, 13, 0.33, -0.0000778, 0.105, 0, -0.000261, 0, 0, 0, 0.83, 0.78, 0.006, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 11, 12, 0.08, -0.00000985, -0.169, 0.00000881, 0, 0, 0, 0, 0.87, 0.83, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (26, 'MD', 12, 12, 0.07, -0.00000255, -0.249, 0.00000412, 0, 0, 0, 0, 0.86, 0.82, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),

                (27, 'MAR', 0, 12, -13.24, -0.00421, 0, 0.0248, 0, 0, 0, 1.36, 0.90, 0.89, 13, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, '7Q2', 0, 12, 0.49, 0, 0, 0, -0.0000649, 0, -0.556, 0.00228, 0.52, 0.44, 0.04, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'S-7Q10', 0, 12, 0.40, 0, 0, 0, -0.0000303, 0, -0.484, 0.00191, 0.48, 0.39, 0.037, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 1, 12, 0.18, -0.0000690, 0, -0.00000613, 0, -0.0000251, 0, 0, 0.94, 0.92, 0.025, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 2, 13, 0.13, 0, 0, -0.0000244, 0, -0.0000305, 0.0589, 0, 0.93, 0.91, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 3, 12, 0.15, 0.0000125, 0, -0.0000205, 0, -0.0000359, 0, 0, 0.83, 0.78, 0.005, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 4, 12, 0.10, 0.0000507, 0, -0.0000138, 0, -0.00000758, 0, 0, 0.54, 0.42, 0.004, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 5, 12, 0.02, 0.0000457, 0, 0.0000135, 0, 0.0000770, 0, 0, 0.86, 0.83, 0.01, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 6, 13, 0.15, 0, 0, 0.0000320, 0, 0.0000847, -0.253, 0, 0.90, 0.87, 0.006, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 7, 12, -0.04, -0.0000403, 0, 0.0000335, 0, 0.0000992, 0, 0, 0.90, 0.88, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 8, 12, -0.01, -0.0000230, 0, 0.0000153, 0, 0.0000435, 0, 0, 0.81, 0.75, 0.003, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 9, 12, 0.01, 0.00000639, 0, 0.00000368, 0, 0.0000123, 0, 0, 0.61, 0.50, 0.005, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 10, 13, -0.06, 0, 0, 0.0000178, 0, 0.0000332, 0.100, 0, 0.88, 0.85, 0.004, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 11, 13, 0.05, 0, 0, -0.00000842, 0, -0.0000575, 0.157, 0, 0.42, 0.26, 0.011, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                (27, 'MD', 12, 13, 0.14, 0, 0, -0.0000321, 0, -0.0000955, 0.120, 0, 0.94, 0.92, 0.010, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
            ;
        """)

    op.execute('SET search_path TO public')

    # TODO: FIX ABOVE
    # Remove Groundwater wording from Groundwater Aquifers
    op.execute('SET search_path TO metadata')
    op.execute("""
                UPDATE data_source AS ds SET name = 'Aquifers'
                WHERE data_table_name = 'ground_water_aquifers'
        """)
    op.execute('SET search_path TO public')

    # add watershed function
    # note on the WHERE clause in the following query:
    # the comparison between split_part functions is important.
    # to start at the first stream downstream from the source polygon,
    # use >=.  To start at the first stream upstream from the source polygon,
    # use >.  Starting at the first stream downstream will include that stream's
    # catchment area, but starting at the first stream upstream may not work when
    # close to the "headwaters" of a river. Both versions are included below.
    op.execute("""
    CREATE OR REPLACE
    FUNCTION public.calculate_upstream_catchment(upstream_from INTEGER default NULL)
    RETURNS TABLE(
        geom Geometry(Polygon, 4326),
        area float
    )
    AS $$
        SELECT
            "GEOMETRY" as geom,
            "FEATURE_AREA_SQM" as area
        FROM    freshwater_atlas_watersheds
        WHERE   "FWA_WATERSHED_CODE" ilike (
            SELECT  left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code
            FROM    freshwater_atlas_watersheds fwa2
            WHERE   "WATERSHED_FEATURE_ID" = upstream_from
        )
        AND split_part("LOCAL_WATERSHED_CODE", '-', (
                SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                FROM freshwater_atlas_watersheds
                WHERE   "WATERSHED_FEATURE_ID" = upstream_from
            )::int
        )::int >= split_part((
                SELECT "LOCAL_WATERSHED_CODE"
                FROM freshwater_atlas_watersheds
                WHERE "WATERSHED_FEATURE_ID" = upstream_from
            ), '-', (
                SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                FROM freshwater_atlas_watersheds
                WHERE "WATERSHED_FEATURE_ID" = upstream_from
            )::int
        )::int
    $$
    LANGUAGE 'sql'
    STABLE
    ;

    CREATE OR REPLACE
    FUNCTION public.calculate_upstream_catchment_starting_upstream(upstream_from INTEGER default NULL, include INTEGER default NULL)
    RETURNS TABLE(
        geom Geometry(Polygon, 4326),
        area float
    )  
    AS $$
        SELECT
            "GEOMETRY" as geom,
            "FEATURE_AREA_SQM" as area
        FROM    freshwater_atlas_watersheds
        WHERE   "FWA_WATERSHED_CODE" ilike (
            SELECT  left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code
            FROM    freshwater_atlas_watersheds fwa2
            WHERE   "WATERSHED_FEATURE_ID" = upstream_from
        )
        AND split_part("LOCAL_WATERSHED_CODE", '-', (
                SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                FROM freshwater_atlas_watersheds
                WHERE   "WATERSHED_FEATURE_ID" = upstream_from
            )::int
        )::int > split_part((
                SELECT "LOCAL_WATERSHED_CODE"
                FROM freshwater_atlas_watersheds
                WHERE "WATERSHED_FEATURE_ID" = upstream_from
            ), '-', (
                SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                FROM freshwater_atlas_watersheds
                WHERE "WATERSHED_FEATURE_ID" = upstream_from
            )::int
        )::int
        OR "WATERSHED_FEATURE_ID" = include
    $$
    LANGUAGE 'sql'
    STABLE
    ;


    """)

    # add fish observation layer
    op.execute('SET search_path TO metadata')

    op.execute("""
            INSERT INTO mapbox_source (mapbox_source_id, max_zoom) VALUES ('iit-water.448thhpa', 9)
        """)

    # need to update water_rights_licences display_catalogue
    # to share mapbox layer with fish_observations
    op.execute("""
               UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.448thhpa', mapbox_source_id = 'iit-water.448thhpa'
               WHERE display_data_name = 'water_rights_licences'
        """)

    # populate fish_observations info
    op.execute("""
              WITH ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'Known BC Fish Observations & BC Fish Distributions',
                    'This point location dataset of fish observations is a regularly updated compilation of BC fish distribution information taken from a combination of all the official provincial databases including the BC Fisheries Information Summary System (FISS). Fish occurrences in this dataset represent the most current and comprehensive information source on fish presence for the province.',
                    'https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions',
                    'WHSE_FISH.FISS_FISH_OBSRVTN_PNT_SP',
                    'fish_observations',
                    'FISH_OBSERVATION_POINT_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            ),
            wms_id AS (
              INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Known BC Fish Observations and BC Fish Distributions',
                    'WHSE_FISH.FISS_FISH_OBSRVTN_PNT_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                wms_catalogue_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'fish_observations',
                'Known BC Fish Observations and BC Fish Distributions',
                'SPECIES_NAME',
                'Species Name',
                ARRAY[
                    'SPECIES_NAME', 'LIFE_STAGE', 'ACTIVITY', 'OBSERVATION_DATE', 'ACAT_REPORT_URL', 'POINT_TYPE_CODE', 'AGENCY_NAME', 'WATERBODY_TYPE'
                ],
                ds_id.data_source_id,
                wms_id.wms_catalogue_id,
                'FISH_WILDLIFE_PLANTS',
                'iit-water.448thhpa',
                'iit-water.448thhpa',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM ds_id, wms_id ;
        """)

    op.execute('SET search_path TO public')

    # hydrometric_test_data_whistler
    if WALLY_ENV == ENV_DEV or WALLY_ENV == ENV_STAGING:
        op.execute('SET search_path TO hydat')

        # Add two stream stations in Whistler
        op.execute("""INSERT INTO stations
        (station_number, station_name, prov_terr_state_loc, regional_office_id, hyd_status, sed_status,
        latitude, longitude, drainage_area_gross, drainage_area_effect, rhbn, real_time,
        contributor_id, operator_id, datum_id, geom)
        VALUES ('08MG021', 'TWENTYONE MILE CREEK AT 670 M CONTOUR', 'BC', '2', 'D', NULL,
        50.1305618286132812, -122.986106872558594, 28.2000007629394531, NULL, 0, 0, NULL, NULL, 10,
        '0101000020E6100000000000601CBF5EC000000040B6104940')
        ON CONFLICT (station_number) DO NOTHING;
        """)

        op.execute("""INSERT INTO stations
        (station_number, station_name, prov_terr_state_loc, regional_office_id, hyd_status, sed_status,
        latitude, longitude, drainage_area_gross, drainage_area_effect, rhbn, real_time,
        contributor_id, operator_id, datum_id, geom)
        VALUES ('08MG026', 'FITZSIMMONS CREEK BELOW BLACKCOMB CREEK', 'BC', '2', 'A', NULL,
        50.1202507019042969, -122.948806762695327, 89.6999969482421875, NULL, 0, 1, 906, 647, 10,
        '0101000020E610000001000040B9BC5EC000000060640F4940')
        ON CONFLICT (station_number) DO NOTHING;""")

        op.execute("""INSERT INTO dly_flows
        (station_number, year, month, full_month, no_days, monthly_mean, monthly_total, first_day_min, min, first_day_max, max, flow1, flow_symbol1, flow2, flow_symbol2, flow3, flow_symbol3, flow4, flow_symbol4, flow5, flow_symbol5, flow6, flow_symbol6, flow7, flow_symbol7, flow8, flow_symbol8, flow9, flow_symbol9, flow10, flow_symbol10, flow11, flow_symbol11, flow12, flow_symbol12, flow13, flow_symbol13, flow14, flow_symbol14, flow15, flow_symbol15, flow16, flow_symbol16, flow17, flow_symbol17, flow18, flow_symbol18, flow19, flow_symbol19, flow20, flow_symbol20, flow21, flow_symbol21, flow22, flow_symbol22, flow23, flow_symbol23, flow24, flow_symbol24, flow25, flow_symbol25, flow26, flow_symbol26, flow27, flow_symbol27, flow28, flow_symbol28, flow29, flow_symbol29, flow30, flow_symbol30, flow31, flow_symbol31)
     VALUES
     ('08MG021', 1974, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3.78999996185302734, 'B', 9.97000026702880859, 'B', 7.15999984741210938, 'E', 3.33999991416931152, NULL, 1.75999999046325684, NULL, 1.28999996185302712, NULL, 0.987999975681304821, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1974, 3, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.767000019550323486, 'A', 0.745000004768371582, NULL, 0.648000001907348633, NULL, 0.606000006198883057, NULL),
     ('08MG021', 1974, 4, 1, 30, 0.856000006198883057, 25.6930007934570312, 4, 0.486999988555908203, 30, 2.97000002861022905, 0.565999984741210938, NULL, 0.518000006675720215, NULL, 0.509999990463256836, NULL, 0.486999988555908203, NULL, 0.537999987602233887, NULL, 0.676999986171722412, NULL, 0.620000004768371582, NULL, 0.574999988079071045, NULL, 0.572000026702880859, NULL, 0.648000001907348633, NULL, 0.727999985218048096, NULL, 0.643000006675720215, NULL, 0.60000002384185791, NULL, 0.611999988555908203, NULL, 0.648000001907348633, NULL, 0.637000024318695068, NULL, 0.643000006675720215, NULL, 0.755999982357025146, NULL, 0.843999981880187988, NULL, 0.837999999523162842, NULL, 0.866999983787536621, NULL, 0.799000024795532227, NULL, 0.847000002861022949, NULL, 1.22000002861022949, NULL, 1.61000001430511475, NULL, 1.33000004291534424, NULL, 1.0700000524520874, NULL, 1.08000004291534424, NULL, 1.24000000953674316, NULL, 2.97000002861022905, NULL, NULL, NULL),
     ('08MG021', 1974, 5, 1, 31, 2.90000009536743208, 90.0400009155273438, 16, 1.02999997138977051, 26, 10.1000003814697283, 3.40000009536743208, NULL, 2.17000007629394531, NULL, 1.6799999475479126, NULL, 1.80999994277954102, NULL, 2.8900001049041748, NULL, 3.65000009536743208, NULL, 5.03999996185302734, NULL, 3.48000001907348633, NULL, 2.52999997138977051, NULL, 1.89999997615814209, NULL, 1.61000001430511475, NULL, 1.49000000953674316, NULL, 1.33000004291534424, NULL, 1.20000004768371582, NULL, 1.10000002384185791, NULL, 1.02999997138977051, NULL, 1.02999997138977051, NULL, 1.14999997615814209, NULL, 1.41999995708465576, NULL, 1.63999998569488525, NULL, 1.75, NULL, 2.22000002861022905, NULL, 2.59999990463256836, NULL, 3.1400001049041748, NULL, 8.94999980926513672, 'E', 10.1000003814697283, 'E', 5.15000009536743164, NULL, 3.61999988555908203, NULL, 3.74000000953674316, NULL, 3.68000006675720215, NULL, 3.53999996185302779, NULL),
     ('08MG021', 1974, 6, 1, 30, 8.48999977111816406, 254.660003662109347, 5, 2.66000008583068848, 19, 14.8000001907348633, 5.30000019073486328, NULL, 9.51000022888183594, 'E', 5.78000020980834961, 'E', 3.25999999046325684, NULL, 2.66000008583068848, NULL, 2.68000006675720215, NULL, 2.72000002861022905, NULL, 2.75, NULL, 2.8900001049041748, NULL, 4.07999992370605469, NULL, 7.25, 'E', 10, 'E', 11.8000001907348633, 'E', 12.8999996185302717, 'E', 14, 'E', 14.6000003814697283, 'E', 13.8999996185302717, 'E', 14.6000003814697283, 'E', 14.8000001907348633, 'E', 14, 'E', 13.1999998092651367, 'E', 13.3999996185302717, 'E', 12.1999998092651367, 'E', 8.64000034332275391, 'E', 6.63000011444091797, 'E', 4.5, NULL, 3.43000006675720215, NULL, 5.96999979019165039, 'E', 5.40999984741210938, NULL, 11.8000001907348633, 'E', NULL, NULL),
     ('08MG021', 1974, 7, 1, 31, 9.63000011444091797, 298.470001220703125, 13, 6.11999988555908203, 18, 14.3999996185302717, 11.1999998092651367, 'E', 8.35000038146972656, 'E', 8.82999992370605469, 'E', 9.63000011444091797, 'E', 8.23999977111816406, 'E', 7.78999996185302734, 'E', 8.13000011444091797, 'E', 7.65000009536743164, 'E', 10.5, 'E', 9.36999988555908203, 'E', 8.15999984741210938, 'E', 6.59999990463256836, 'E', 6.11999988555908203, 'E', 7.59000015258789062, 'E', 7.86999988555908203, 'E', 6.23000001907348633, 'E', 13, 'E', 14.3999996185302717, 'E', 12.5, 'E', 9.93999958038330078, 'E', 9.68000030517577947, 'E', 11.6000003814697283, 'E', 10.3000001907348633, 'E', 9.26000022888183594, 'E', 9.31999969482422053, 'E', 9.71000003814697266, 'E', 10.1000003814697283, 'E', 11, 'E', 11.8999996185302717, 'E', 11.6999998092651367, 'E', 11.8000001907348633, 'E'),
     ('08MG021', 1974, 8, 1, 31, 6.26999998092651367, 194.3800048828125, 23, 3.1400001049041748, 2, 12, 11.3999996185302717, 'E', 12, 'E', 11.8999996185302717, 'E', 11.8999996185302717, 'E', 11.1999998092651367, 'E', 9.65999984741210938, 'E', 7.73000001907348633, 'E', 6.57000017166137695, 'E', 6.36999988555908203, 'E', 7.15999984741210938, 'E', 7.84000015258789062, 'E', 7.69999980926513672, 'E', 6.96999979019165039, 'E', 6.09000015258789062, 'E', 5.6399998664855957, NULL, 5.55000019073486328, NULL, 5.55000019073486328, NULL, 5.46999979019165039, NULL, 4.96000003814697266, NULL, 4.30000019073486328, NULL, 3.65000009536743208, NULL, 3.33999991416931152, NULL, 3.1400001049041748, NULL, 3.43000006675720215, NULL, 3.61999988555908203, NULL, 3.53999996185302779, NULL, 3.45000004768371582, NULL, 3.74000000953674316, NULL, 3.74000000953674316, NULL, 3.50999999046325684, NULL, 3.25999999046325684, NULL),
     ('08MG021', 1974, 9, 1, 30, 1.37999999523162842, 41.4860000610351634, 30, 0.653999984264373779, 1, 3, 3, NULL, 2.66000008583068848, NULL, 2.32999992370605469, NULL, 2.08999991416931152, NULL, 1.88999998569488525, NULL, 1.83000004291534402, NULL, 1.75, NULL, 1.5700000524520874, NULL, 2.31999993324279785, NULL, 2.28999996185302779, NULL, 1.79999995231628418, NULL, 1.37999999523162842, NULL, 1.16999995708465576, NULL, 1.10000002384185791, NULL, 1.08000004291534424, NULL, 1.01999998092651367, NULL, 0.967999994754791149, NULL, 0.93199998140335083, NULL, 0.915000021457672008, NULL, 0.936999976634979248, NULL, 1.01999998092651367, NULL, 1, NULL, 0.915000021457672008, NULL, 0.869000017642974854, NULL, 0.855000019073486328, NULL, 0.864000022411346436, NULL, 0.813000023365020752, NULL, 0.764999985694885254, NULL, 0.699000000953674316, NULL, 0.653999984264373779, NULL, NULL, NULL),
     ('08MG021', 1974, 10, 1, 31, 0.555000007152557373, 17.2180004119873047, 25, 0.317000001668930054, 3, 1.15999996662139893, 0.676999986171722412, NULL, 1.11000001430511475, NULL, 1.15999996662139893, NULL, 0.973999977111816406, NULL, 0.787000000476837158, NULL, 0.676999986171722412, NULL, 0.595000028610229492, NULL, 0.565999984741210938, NULL, 0.53200000524520874, NULL, 0.504000008106231689, NULL, 0.449999988079071045, NULL, 0.412999987602233887, NULL, 0.393999993801116943, NULL, 0.379000008106231689, NULL, 0.36500000953674322, NULL, 0.416000008583068903, NULL, 0.493000000715255682, NULL, 0.456000000238418579, NULL, 0.472999989986419678, NULL, 0.708000004291534424, NULL, 0.50700002908706665, NULL, 0.418999999761581421, NULL, 0.360000014305114746, NULL, 0.319999992847442627, NULL, 0.317000001668930054, NULL, 0.351000010967254639, NULL, 0.875, NULL, 0.694000005722045898, NULL, 0.469999998807907104, NULL, 0.377000004053115845, NULL, 0.398999989032745361, NULL),
     ('08MG021', 1974, 11, 1, 30, 0.455000013113021851, 13.6350002288818359, 3, 0.289000004529953003, 25, 1.1799999475479126, 0.411000013351440374, NULL, 0.340000003576278687, NULL, 0.289000004529953003, NULL, 0.291999995708465576, NULL, 0.463999986648559626, NULL, 0.783999979496002197, NULL, 0.476000010967254583, NULL, 0.405000001192092896, NULL, 0.402000010013580322, NULL, 0.36500000953674322, NULL, 0.351000010967254639, NULL, 0.551999986171722412, NULL, 0.481000006198883112, NULL, 0.425000011920928955, NULL, 0.381999999284744263, NULL, 0.370999991893768311, NULL, 0.36500000953674322, NULL, 0.38499999046325678, NULL, 0.374000012874603271, NULL, 0.381999999284744263, NULL, 0.370999991893768311, NULL, 0.289000004529953003, NULL, 0.328000009059906006, NULL, 1.04999995231628418, NULL, 1.1799999475479126, NULL, 0.56099998950958252, NULL, 0.449999988079071045, NULL, 0.393999993801116943, NULL, 0.36500000953674322, NULL, 0.351000010967254639, NULL, NULL, NULL),
     ('08MG021', 1974, 12, 1, 31, 0.492000013589859009, 15.2519998550415039, 31, 0.282999992370605469, 16, 1.40999996662139893, 0.340000003576278687, NULL, 0.328000009059906006, NULL, 0.379000008106231689, NULL, 0.49000000953674322, NULL, 0.497999995946884155, NULL, 0.428000003099441528, NULL, 0.395999997854232788, NULL, 0.377000004053115845, NULL, 0.391000002622604426, NULL, 0.391000002622604426, NULL, 0.395999997854232788, NULL, 0.34299999475479126, NULL, 0.344999998807907104, NULL, 0.340000003576278687, NULL, 0.31400001049041748, NULL, 1.40999996662139893, NULL, 1.37999999523162842, NULL, 0.790000021457672119, NULL, 0.620000004768371582, NULL, 0.572000026702880859, NULL, 0.739000022411346436, NULL, 0.500999987125396729, NULL, 0.481000006198883112, 'B', 0.453000009059906006, 'B', 0.43900001049041748, NULL, 0.412999987602233887, NULL, 0.395999997854232788, 'B', 0.368000000715255682, 'B', 0.340000003576278687, 'B', 0.31099998950958252, 'B', 0.282999992370605469, 'B'),
     ('08MG021', 1975, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 0.277999997138977051, 'B', 0.268999993801116943, 'B', 0.275000005960464478, 'B', 0.261000007390975952, 'B', 0.254999995231628418, 'B', 0.252000004053115845, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1975, 5, 1, 31, 2.74000000953674316, 84.970001220703125, 1, 0.792999982833862305, 31, 9.28999996185302734, 0.792999982833862305, 'E', 1.10000002384185791, 'E', 1.52999997138977051, 'E', 1.15999996662139893, 'E', 1.09000003337860107, 'E', 1.00999999046325684, 'E', 0.936999976634979248, 'A', 1.21000003814697288, NULL, 2.33999991416931152, NULL, 3.61999988555908203, NULL, 4.69999980926513672, NULL, 3.50999999046325684, NULL, 3, NULL, 4.98000001907348633, NULL, 5.80000019073486328, 'E', 3.71000003814697266, NULL, 3.17000007629394531, NULL, 2.54999995231628418, NULL, 1.76999998092651367, NULL, 1.40999996662139893, NULL, 1.39999997615814209, NULL, 1.3200000524520874, NULL, 1.3200000524520874, NULL, 1.13999998569488525, NULL, 1.16999995708465576, NULL, 1.44000005722045898, NULL, 2.07999992370605469, NULL, 3.1099998950958252, NULL, 5.46999979019165039, NULL, 7.84000015258789062, 'E', 9.28999996185302734, 'E'),
     ('08MG021', 1975, 6, 1, 30, 7.32000017166137695, 219.580001831054688, 29, 2.94000005722045898, 1, 11, 11, 'E', 10.3999996185302717, 'E', 7.61999988555908203, 'E', 8.92000007629394531, 'E', 9.97000026702880859, 'E', 7.07999992370605469, 'E', 4.46999979019165039, NULL, 3.96000003814697266, NULL, 5.48999977111816406, NULL, 8.64000034332275391, 'E', 10.6000003814697283, 'E', 10.3000001907348633, 'E', 10.1999998092651367, 'E', 8.64000034332275391, 'E', 8.85999965667724609, 'E', 6.71000003814697266, 'E', 6.57000017166137695, 'E', 8.06999969482421875, 'E', 10.3999996185302717, 'E', 10.8000001907348633, 'E', 9.39999961853027166, 'E', 6.57000017166137695, 'E', 4.6399998664855957, NULL, 5.40999984741210938, NULL, 6.46000003814697266, 'E', 4.55999994277954102, NULL, 3.40000009536743208, NULL, 3.48000001907348633, NULL, 2.94000005722045898, NULL, 4.01999998092651367, NULL, NULL, NULL),
     ('08MG021', 1975, 7, 1, 31, 5.59999990463256836, 173.520004272460938, 31, 1.15999996662139893, 7, 12, 6.40000009536743164, 'E', 8.77999973297119141, 'E', 10.8000001907348633, 'E', 10.8000001907348633, 'E', 11.3999996185302717, 'E', 11.6000003814697283, 'E', 12, 'E', 11.8999996185302717, 'E', 11.6000003814697283, 'E', 11.6000003814697283, 'E', 9.73999977111816406, 'E', 8.47000026702880859, 'E', 5.57999992370605469, NULL, 4.28000020980834961, NULL, 4.28000020980834961, NULL, 3.20000004768371582, NULL, 2.56999993324279785, NULL, 2.33999991416931152, NULL, 2.33999991416931152, NULL, 2.52999997138977051, NULL, 2.29999995231628418, NULL, 2.05999994277954102, NULL, 2.06999993324279785, NULL, 2.56999993324279785, NULL, 2.28999996185302779, NULL, 1.92999994754791282, NULL, 2.21000003814697266, NULL, 2.08999991416931152, NULL, 1.45000004768371582, NULL, 1.1799999475479126, NULL, 1.15999996662139893, NULL),
     ('08MG021', 1975, 8, 1, 31, 1.37999999523162842, 42.6689987182617188, 25, 0.518000006675720215, 27, 5.13000011444091797, 1.26999998092651367, NULL, 1.5, NULL, 1.53999996185302712, NULL, 1.25999999046325684, NULL, 1.24000000953674316, NULL, 1.04999995231628418, NULL, 1.1799999475479126, NULL, 1.03999996185302712, NULL, 0.81800001859664917, NULL, 0.783999979496002197, NULL, 0.764999985694885254, NULL, 0.769999980926513672, NULL, 0.776000022888183594, NULL, 0.908999979496002197, NULL, 0.857999980449676514, NULL, 1.02999997138977051, NULL, 0.934000015258789174, NULL, 0.804000020027160645, NULL, 0.792999982833862305, NULL, 0.773000001907348633, NULL, 0.736000001430511475, NULL, 0.78200000524520874, NULL, 0.680000007152557373, NULL, 0.549000024795532227, NULL, 0.518000006675720215, NULL, 1.96000003814697288, NULL, 5.13000011444091797, NULL, 3.76999998092651367, NULL, 4.96000003814697266, NULL, 2.18000006675720215, NULL, 1.30999994277954102, NULL),
     ('08MG021', 1975, 9, 1, 30, 0.527000010013580322, 15.8159999847412127, 30, 0.328000009059906006, 1, 1.03999996185302712, 1.03999996185302712, NULL, 0.922999978065490834, NULL, 0.776000022888183594, NULL, 0.680000007152557373, NULL, 0.630999982357025146, NULL, 0.620000004768371582, NULL, 0.648000001907348633, NULL, 0.625999987125396729, NULL, 0.569000005722045898, NULL, 0.56400001049041748, NULL, 0.574999988079071045, NULL, 0.56400001049041748, NULL, 0.544000029563903809, NULL, 0.537999987602233887, NULL, 0.565999984741210938, NULL, 0.535000026226043701, NULL, 0.479000002145767212, NULL, 0.425000011920928955, NULL, 0.398999989032745361, NULL, 0.388000011444091797, NULL, 0.416000008583068903, NULL, 0.418999999761581421, NULL, 0.411000013351440374, NULL, 0.407999992370605524, NULL, 0.368000000715255682, NULL, 0.34299999475479126, NULL, 0.331000000238418579, NULL, 0.368000000715255682, NULL, 0.333999991416931152, NULL, 0.328000009059906006, NULL, NULL, NULL),
     ('08MG021', 1975, 10, 1, 31, 1.71000003814697288, 52.9560012817382812, 1, 0.328000009059906006, 17, 17, 0.328000009059906006, NULL, 0.337000012397766113, NULL, 1.10000002384185791, NULL, 1.0700000524520874, NULL, 1.14999997615814209, NULL, 0.800999999046325684, NULL, 0.595000028610229492, NULL, 0.529999971389770508, NULL, 0.820999979972839355, NULL, 0.815999984741210938, NULL, 0.72500002384185791, NULL, 0.704999983310699463, NULL, 0.732999980449676514, NULL, 1.39999997615814209, NULL, 1.60000002384185791, NULL, 3.74000000953674316, NULL, 17, 'E', 4.1100001335144043, NULL, 3, NULL, 1.96000003814697288, NULL, 1.44000005722045898, NULL, 1.1799999475479126, NULL, 1.01999998092651367, NULL, 0.950999975204467773, NULL, 0.94300001859664917, NULL, 0.871999979019165039, NULL, 0.847000002861022949, NULL, 0.783999979496002197, NULL, 0.787000000476837158, NULL, 0.792999982833862305, NULL, 0.81800001859664917, NULL),
     ('08MG021', 1975, 11, 1, 30, 3.51999998092651367, 105.602996826171875, 30, 0.820999979972839355, 4, 31.399999618530277, 1.94000005722045898, NULL, 1.73000001907348633, NULL, 11.3000001907348633, 'E', 31.399999618530277, 'E', 18.5, 'E', 3.96000003814697266, NULL, 2.44000005722045898, NULL, 2.46000003814697266, NULL, 2.13000011444091797, NULL, 1.82000005245208762, NULL, 1.66999995708465576, NULL, 1.64999997615814209, NULL, 1.88999998569488525, NULL, 2.07999992370605469, NULL, 2.26999998092651367, NULL, 1.77999997138977051, NULL, 1.5, NULL, 1.30999994277954102, NULL, 1.25, 'B', 1.1799999475479126, 'B', 1.10000002384185791, 'B', 1.08000004291534424, 'B', 1.13999998569488525, NULL, 1.60000002384185791, NULL, 1.33000004291534424, NULL, 1.23000001907348633, NULL, 1.12000000476837158, 'B', 1.02999997138977051, 'B', 0.892000019550323486, 'B', 0.820999979972839355, 'B', NULL, NULL),
     ('08MG021', 1976, 2, 0, 29, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.393999993801116943, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1976, 4, 1, 30, 0.551999986171722412, 16.5590000152587891, 2, 0.28600001335144043, 30, 1.3200000524520874, 0.303000003099441584, NULL, 0.28600001335144043, NULL, 0.293999999761581421, NULL, 0.323000013828277588, NULL, 0.402000010013580322, NULL, 0.58899998664855957, NULL, 0.527000010013580322, NULL, 0.537999987602233887, NULL, 0.634000003337860107, NULL, 0.699000000953674316, NULL, 0.755999982357025146, NULL, 0.702000021934509277, NULL, 0.667999982833862305, NULL, 0.648000001907348633, NULL, 0.583000004291534424, NULL, 0.509999990463256836, NULL, 0.481000006198883112, NULL, 0.458999991416931208, NULL, 0.43900001049041748, NULL, 0.425000011920928955, NULL, 0.407999992370605524, NULL, 0.407999992370605524, NULL, 0.412999987602233887, NULL, 0.421999990940093994, NULL, 0.411000013351440374, NULL, 0.446999996900558472, NULL, 0.578000009059906006, NULL, 0.815999984741210938, NULL, 1.0700000524520874, NULL, 1.3200000524520874, NULL, NULL, NULL),
     ('08MG021', 1976, 5, 1, 31, 3.75, 116.379997253417955, 3, 1.15999996662139893, 27, 7.15999984741210938, 1.33000004291534424, NULL, 1.20000004768371582, NULL, 1.15999996662139893, NULL, 1.15999996662139893, NULL, 1.25, NULL, 1.25, NULL, 1.25, NULL, 2.97000002861022905, NULL, 2.97000002861022905, NULL, 6.96999979019165039, 'A', 5.69000005722045898, NULL, 4.6399998664855957, NULL, 4.80999994277954102, NULL, 4.55999994277954102, NULL, 4.3600001335144043, NULL, 4.46999979019165039, NULL, 4.67000007629394531, NULL, 4.32999992370605469, NULL, 4.30000019073486328, NULL, 4.19000005722045898, NULL, 4.13000011444091797, NULL, 4.01999998092651367, NULL, 3.96000003814697266, NULL, 3.81999993324279785, NULL, 3.88000011444091797, NULL, 3.81999993324279785, NULL, 7.15999984741210938, NULL, 5.34999990463256836, NULL, 4.53000020980834961, NULL, 4.19000005722045898, NULL, 3.99000000953674316, NULL),
     ('08MG021', 1976, 6, 1, 30, 6.71999979019165039, 201.710006713867188, 3, 3.68000006675720215, 19, 11.3999996185302717, 3.84999990463256792, NULL, 3.76999998092651367, NULL, 3.68000006675720215, NULL, 3.76999998092651367, NULL, 3.84999990463256792, NULL, 4.19000005722045898, NULL, 4.92999982833862305, NULL, 5.51999998092651367, NULL, 6.09000015258789062, NULL, 6.28999996185302734, NULL, 5.57999992370605469, NULL, 5.55000019073486328, NULL, 4.92999982833862305, NULL, 5.17999982833862305, NULL, 6.96999979019165039, NULL, 8.68999958038330078, 'E', 9.09000015258789062, 'E', 9.90999984741210938, 'E', 11.3999996185302717, 'E', 8.32999992370605469, 'E', 7.69999980926513672, 'E', 9.77000045776367188, 'E', 7.59000015258789062, 'E', 7.01999998092651367, NULL, 6.80000019073486328, NULL, 6.46000003814697266, NULL, 6.57000017166137695, NULL, 7.82000017166137695, 'E', 9.90999984741210938, 'E', 10.5, 'E', NULL, NULL),
     ('08MG021', 1976, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 5.96999979019165039, NULL, 4.90000009536743164, NULL, 4.59000015258789062, NULL, 3.76999998092651367, NULL, 5.15000009536743164, NULL, 4.6399998664855957, NULL, 3.53999996185302779, NULL, 3.68000006675720215, NULL, 4.53000020980834961, NULL, 3.50999999046325684, NULL, 3.43000006675720215, NULL, 3.59999990463256836, NULL),
     ('08MG021', 1976, 9, 1, 30, 2.61999988555908203, 78.5, 30, 1.21000003814697288, 5, 9.82999992370605646, 3.68000006675720215, NULL, 3.45000004768371582, NULL, 3.36999988555908203, NULL, 6.03000020980834961, NULL, 9.82999992370605646, 'E', 4.21999979019165039, NULL, 2.92000007629394531, NULL, 2.63000011444091797, NULL, 2.3599998950958252, NULL, 2.3599998950958252, NULL, 2.31999993324279785, NULL, 2.40000009536743208, NULL, 2.24000000953674316, NULL, 3.53999996185302779, NULL, 2.38000011444091797, NULL, 2.25999999046325684, NULL, 2.17000007629394531, NULL, 2.11999988555908203, NULL, 2.04999995231628418, NULL, 1.99000000953674316, NULL, 1.89999997615814209, NULL, 1.75, NULL, 1.52999997138977051, NULL, 1.37000000476837158, NULL, 1.36000001430511475, NULL, 1.30999994277954102, NULL, 1.25999999046325684, NULL, 1.22000002861022949, NULL, 1.26999998092651367, NULL, 1.21000003814697288, NULL, NULL, NULL),
     ('08MG021', 1976, 10, 1, 31, 0.874000012874603271, 27.0890007019042969, 23, 0.453000009059906006, 28, 2.68000006675720215, 1.05999994277954102, NULL, 0.957000017166137584, NULL, 0.843999981880187988, NULL, 0.739000022411346436, NULL, 0.857999980449676514, NULL, 0.759000003337860107, NULL, 0.690999984741210938, NULL, 0.690999984741210938, NULL, 0.916999995708465576, NULL, 1.64999997615814209, NULL, 1.21000003814697288, NULL, 0.987999975681304821, NULL, 0.866999983787536621, NULL, 0.753000020980834961, NULL, 0.667999982833862305, NULL, 0.614000022411346436, NULL, 0.544000029563903809, NULL, 0.518000006675720215, NULL, 0.50700002908706665, NULL, 0.497999995946884155, NULL, 0.483999997377395574, NULL, 0.469999998807907104, NULL, 0.453000009059906006, NULL, 0.56400001049041748, NULL, 0.776000022888183594, NULL, 0.759000003337860107, NULL, 1.36000001430511475, NULL, 2.68000006675720215, NULL, 1.11000001430511475, NULL, 0.89999997615814209, NULL, 1.20000004768371582, NULL),
     ('08MG021', 1976, 11, 1, 30, 1.28999996185302712, 38.7649993896484375, 30, 0.614000022411346436, 17, 9.68000030517577947, 1.08000004291534424, NULL, 0.902999997138977051, NULL, 1.02999997138977051, NULL, 1.23000001907348633, NULL, 1.78999996185302712, NULL, 1.27999997138977051, NULL, 1.23000001907348633, NULL, 1.28999996185302712, NULL, 1.12000000476837158, NULL, 1.04999995231628418, NULL, 0.945999979972839355, NULL, 0.861000001430511475, NULL, 0.755999982357025146, NULL, 0.736000001430511475, NULL, 0.861000001430511475, NULL, 1.51999998092651367, NULL, 9.68000030517577947, 'E', 1.45000004768371582, NULL, 0.980000019073486439, NULL, 0.824000000953674316, NULL, 0.778999984264373779, NULL, 0.71399998664855957, NULL, 0.769999980926513672, NULL, 1.62000000476837158, NULL, 1.00999999046325684, NULL, 0.704999983310699463, NULL, 0.665000021457672119, NULL, 0.648000001907348633, 'E', 0.623000025749206543, 'E', 0.614000022411346436, 'E', NULL, NULL),
     ('08MG021', 1976, 12, 1, 31, 1.09000003337860107, 33.8899993896484375, 5, 0.565999984741210938, 16, 6.71000003814697266, 0.606000006198883057, 'E', 0.595000028610229492, 'E', 0.586000025272369385, 'E', 0.578000009059906006, 'E', 0.565999984741210938, 'E', 0.565999984741210938, 'E', 0.699000000953674316, NULL, 1.02999997138977051, NULL, 0.722000002861022949, NULL, 0.643000006675720215, NULL, 0.799000024795532227, NULL, 0.697000026702880859, NULL, 0.643000006675720215, NULL, 0.595000028610229492, NULL, 1.92999994754791282, NULL, 6.71000003814697266, NULL, 4.32999992370605469, NULL, 1.53999996185302712, NULL, 1.11000001430511475, NULL, 0.922999978065490834, NULL, 0.820999979972839355, NULL, 0.759000003337860107, NULL, 0.676999986171722412, NULL, 0.667999982833862305, NULL, 0.660000026226043701, NULL, 1.0700000524520874, NULL, 0.824000000953674316, NULL, 0.702000021934509277, NULL, 0.662999987602233887, NULL, 0.606000006198883057, NULL, 0.572000026702880859, NULL),
     ('08MG021', 1977, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1.19000005722045898, 'B', 0.934000015258789174, 'B', 0.75, 'B', 0.708000004291534424, 'B', 0.651000022888183594, 'B', 0.623000025749206543, 'B', 0.597000002861022949, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1977, 2, 0, 28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.03999996185302779, 'B', 1.12999999523162842, 'B', 0.990999996662140004, 'B', 0.892000019550323486, 'B', 0.820999979972839355, 'B', 0.764999985694885254, 'B', 0.722000002861022949, 'B', 0.688000023365020752, 'B', 0.708000004291534424, 'B', 0.651000022888183594, 'B', 0.623000025749206543, 'B', 0.60000002384185791, 'B', 0.583000004291534424, 'B', 0.565999984741210938, 'B', 0.549000024795532227, 'B', 0.523999989032745361, 'B', 0.495999991893768311, 'B', NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1977, 3, 1, 31, 0.347000002861022894, 10.7720003128051758, 26, 0.282999992370605469, 1, 0.462000012397766113, 0.462000012397766113, 'B', 0.444999992847442627, 'B', 0.430000007152557373, 'B', 0.425000011920928955, 'B', 0.416000008583068903, 'B', 0.411000013351440374, 'B', 0.402000010013580322, 'B', 0.395999997854232788, 'B', 0.388000011444091797, 'B', 0.381999999284744263, 'B', 0.368000000715255682, 'B', 0.361999988555908203, 'B', 0.360000014305114746, 'B', 0.354000002145767212, 'B', 0.347999989986419678, 'B', 0.34299999475479126, 'B', 0.337000012397766113, 'B', 0.331000000238418579, 'B', 0.317000001668930054, 'B', 0.31099998950958252, 'B', 0.305999994277954102, 'B', 0.303000003099441584, 'B', 0.296999990940093994, 'B', 0.293999999761581421, 'B', 0.28600001335144043, 'B', 0.282999992370605469, 'B', 0.282999992370605469, 'B', 0.282999992370605469, 'B', 0.282999992370605469, 'B', 0.282999992370605469, 'B', 0.282999992370605469, 'B'),
     ('08MG021', 1977, 4, 1, 30, 2.42000007629394531, 72.5059967041015625, 1, 0.282999992370605469, 25, 5.13000011444091797, 0.282999992370605469, 'B', 0.291999995708465576, 'B', 0.31099998950958252, 'B', 1.49000000953674316, NULL, 2.26999998092651367, NULL, 2.8900001049041748, NULL, 3.45000004768371582, NULL, 3.88000011444091797, NULL, 3.1400001049041748, NULL, 2.53999996185302779, NULL, 2.11999988555908203, NULL, 1.97000002861022927, NULL, 1.97000002861022927, NULL, 1.62000000476837158, NULL, 1.47000002861022949, NULL, 1.37000000476837158, NULL, 1.24000000953674316, NULL, 1.19000005722045898, NULL, 1.05999994277954102, NULL, 1.01999998092651367, NULL, 1.03999996185302712, NULL, 1.85000002384185791, NULL, 3.30999994277954102, NULL, 4.3899998664855957, NULL, 5.13000011444091797, NULL, 5.09999990463256836, NULL, 4.07999992370605469, NULL, 3.96000003814697266, NULL, 4.01999998092651367, NULL, 4.05000019073486328, NULL, NULL, NULL),
     ('08MG021', 1977, 5, 1, 31, 2.54999995231628418, 79.19000244140625, 15, 1.63999998569488525, 2, 4.53000020980834961, 4.25, NULL, 4.53000020980834961, NULL, 4.3899998664855957, NULL, 3.91000008583068892, NULL, 3.1099998950958252, NULL, 2.54999995231628418, NULL, 2.53999996185302779, NULL, 2.34999990463256836, NULL, 2.5, NULL, 2.43000006675720215, NULL, 2.31999993324279785, NULL, 2.16000008583068848, NULL, 2.03999996185302779, NULL, 1.78999996185302712, NULL, 1.63999998569488525, NULL, 1.6799999475479126, NULL, 2, NULL, 2.25, NULL, 2.3599998950958252, NULL, 2.38000011444091797, NULL, 3.65000009536743208, NULL, 2.78999996185302779, NULL, 2.44000005722045898, NULL, 2.31999993324279785, NULL, 2.28999996185302779, NULL, 2.25, NULL, 1.95000004768371604, NULL, 1.83000004291534402, NULL, 1.87000000476837203, NULL, 2.03999996185302779, NULL, 2.57999992370605469, NULL),
     ('08MG021', 1977, 6, 1, 30, 3.43000006675720215, 102.790000915527344, 30, 1.82000005245208762, 7, 8.67000007629394531, 3.25999999046325684, NULL, 2.47000002861022905, NULL, 2.23000001907348633, NULL, 2.69000005722045898, NULL, 3.59999990463256836, NULL, 7.19000005722045898, NULL, 8.67000007629394531, NULL, 5.13000011444091797, NULL, 2.79999995231628418, NULL, 3.1099998950958252, NULL, 3.56999993324279785, NULL, 4.13000011444091797, NULL, 4.01999998092651367, NULL, 3.71000003814697266, NULL, 3.45000004768371582, NULL, 3.50999999046325684, NULL, 4.15999984741210938, NULL, 4.42000007629394531, NULL, 3.74000000953674316, NULL, 2.71000003814697266, NULL, 3.48000001907348633, NULL, 3.25999999046325684, NULL, 2.29999995231628418, NULL, 3.43000006675720215, NULL, 2.34999990463256836, NULL, 1.91999995708465598, NULL, 1.83000004291534402, NULL, 1.98000001907348633, NULL, 1.85000002384185791, NULL, 1.82000005245208762, NULL, NULL, NULL),
     ('08MG021', 1977, 7, 1, 31, 1.46000003814697288, 45.2000007629394531, 30, 1.08000004291534424, 16, 2.03999996185302779, 2.01999998092651367, NULL, 1.78999996185302712, NULL, 1.64999997615814209, NULL, 1.53999996185302712, NULL, 1.49000000953674316, NULL, 1.39999997615814209, NULL, 1.36000001430511475, NULL, 1.44000005722045898, NULL, 1.5, NULL, 1.47000002861022949, NULL, 1.70000004768371582, NULL, 1.6799999475479126, NULL, 1.49000000953674316, NULL, 1.37999999523162842, NULL, 1.41999995708465576, NULL, 2.03999996185302779, NULL, 1.85000002384185791, NULL, 1.51999998092651367, NULL, 1.23000001907348633, NULL, 1.1799999475479126, NULL, 1.23000001907348633, NULL, 1.22000002861022949, NULL, 1.16999995708465576, NULL, 1.25, NULL, 1.41999995708465576, NULL, 1.41999995708465576, NULL, 1.47000002861022949, NULL, 1.41999995708465576, NULL, 1.22000002861022949, NULL, 1.08000004291534424, NULL, 1.14999997615814209, NULL),
     ('08MG021', 1977, 8, 1, 31, 0.944000005722046009, 29.2759990692138672, 27, 0.558000028133392334, 4, 1.20000004768371582, 1.12000000476837158, NULL, 1.10000002384185791, NULL, 1.1799999475479126, NULL, 1.20000004768371582, NULL, 1.10000002384185791, NULL, 1.02999997138977051, NULL, 0.996999979019165039, NULL, 0.950999975204467773, NULL, 0.925999999046325573, NULL, 0.922999978065490834, NULL, 0.915000021457672008, NULL, 0.916999995708465576, NULL, 0.949000000953674427, NULL, 0.980000019073486439, NULL, 0.916999995708465576, NULL, 0.834999978542327881, NULL, 0.834999978542327881, NULL, 0.815999984741210938, NULL, 0.855000019073486328, NULL, 0.878000020980834961, NULL, 0.883000016212463379, NULL, 0.815999984741210938, NULL, 1.16999995708465576, NULL, 1.1799999475479126, NULL, 0.949000000953674427, NULL, 0.680000007152557373, NULL, 0.558000028133392334, NULL, 1.03999996185302712, NULL, 1.1799999475479126, NULL, 0.778999984264373779, NULL, 0.616999983787536621, NULL),
     ('08MG021', 1977, 9, 1, 30, 1.04999995231628418, 31.3680000305175746, 18, 0.541000008583068848, 20, 2.78999996185302779, 0.565999984741210938, NULL, 0.71399998664855957, NULL, 1.05999994277954102, NULL, 1.62000000476837158, NULL, 1.30999994277954102, NULL, 0.985000014305114746, NULL, 0.916999995708465576, NULL, 0.843999981880187988, NULL, 0.731000006198883057, NULL, 0.646000027656555176, NULL, 0.630999982357025146, NULL, 0.660000026226043701, NULL, 0.685000002384185791, NULL, 0.824000000953674316, NULL, 0.813000023365020752, NULL, 0.616999983787536621, NULL, 0.565999984741210938, NULL, 0.541000008583068848, NULL, 1.79999995231628418, NULL, 2.78999996185302779, NULL, 1.72000002861022949, NULL, 1.29999995231628418, NULL, 1.74000000953674316, NULL, 1.69000005722045898, NULL, 1.35000002384185791, NULL, 1.12999999523162842, NULL, 0.959999978542327992, NULL, 0.824000000953674316, NULL, 0.711000025272369385, NULL, 0.623000025749206543, NULL, NULL, NULL),
     ('08MG021', 1977, 10, 1, 31, 1.24000000953674316, 38.4970016479492188, 5, 0.407999992370605524, 23, 7.76000022888183594, 0.583000004291534424, NULL, 0.537999987602233887, NULL, 0.469999998807907104, NULL, 0.430000007152557373, NULL, 0.407999992370605524, NULL, 0.43900001049041748, NULL, 0.458999991416931208, NULL, 1.01999998092651367, NULL, 0.71399998664855957, NULL, 0.544000029563903809, NULL, 0.486999988555908203, NULL, 0.892000019550323486, NULL, 0.892000019550323486, NULL, 0.623000025749206543, NULL, 0.639999985694885254, NULL, 0.736000001430511475, NULL, 0.551999986171722412, NULL, 0.500999987125396729, NULL, 0.458999991416931208, NULL, 0.407999992370605524, NULL, 0.421999990940093994, NULL, 1.14999997615814209, NULL, 7.76000022888183594, 'A', 2.8900001049041748, NULL, 2.53999996185302779, NULL, 2.25999999046325684, NULL, 1.87999999523162842, NULL, 2, NULL, 2.24000000953674316, NULL, 1.90999996662139893, NULL, 1.64999997615814209, NULL),
     ('08MG021', 1977, 11, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 1.59000003337860107, 'A', 2.75999999046325684, 'A', 2.15000009536743208, NULL, 1.82000005245208762, NULL, 1.64999997615814209, NULL, 1.61000001430511475, NULL, 1.46000003814697288, NULL, 1.36000001430511475, NULL, 1.38999998569488525, NULL, 1.87000000476837203, NULL, 2.46000003814697266, NULL, 2.29999995231628418, NULL, 2.15000009536743208, NULL, 1.95000004768371604, NULL, 1.70000004768371582, NULL, 1.54999995231628418, NULL, 1.36000001430511475, 'B', 1.12999999523162842, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1978, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.215000003576278687, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1978, 2, 0, 28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.221000000834465027, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1978, 3, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.296999990940093994, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1978, 4, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.716000020503997803, 'A', 0.623000025749206543, NULL, 0.569000005722045898, NULL, 0.555000007152557373, NULL, 0.595000028610229492, NULL, 0.697000026702880859, NULL, 1.12999999523162842, NULL, 1.54999995231628418, NULL, 1.02999997138977051, NULL, 0.883000016212463379, NULL, 0.762000024318695068, NULL, 0.667999982833862305, NULL, 0.634000003337860107, NULL, 0.595000028610229492, NULL, 0.58899998664855957, NULL, 0.767000019550323486, NULL, 0.985000014305114746, NULL, 0.908999979496002197, NULL, 0.80699998140335083, NULL, 0.732999980449676514, NULL, 0.674000024795532227, NULL, 0.748000025749206543, NULL, 1.54999995231628418, NULL, 2.59999990463256836, NULL, 2.75999999046325684, NULL, 2.77999997138977051, NULL, 2.59999990463256836, NULL, NULL, NULL),
     ('08MG021', 1978, 5, 1, 31, 2.79999995231628418, 86.69000244140625, 5, 1.79999995231628418, 20, 6.26000022888183594, 2.41000008583068848, NULL, 2.6099998950958252, NULL, 2.53999996185302779, NULL, 2.19000005722045898, NULL, 1.79999995231628418, NULL, 1.82000005245208762, NULL, 2.23000001907348633, NULL, 2.66000008583068848, NULL, 2.92000007629394531, NULL, 2.94000005722045898, NULL, 2.76999998092651367, NULL, 2.44000005722045898, NULL, 2.34999990463256836, NULL, 2.52999997138977051, NULL, 2.44000005722045898, NULL, 2.55999994277954102, NULL, 2.8599998950958252, NULL, 2.97000002861022905, NULL, 3.81999993324279785, NULL, 6.26000022888183594, NULL, 5.65999984741210938, NULL, 2.77999997138977051, NULL, 2.41000008583068848, NULL, 2.21000003814697266, NULL, 2.23000001907348633, NULL, 2.27999997138977051, NULL, 2.55999994277954102, NULL, 2.44000005722045898, NULL, 2.33999991416931152, NULL, 2.44000005722045898, NULL, 4.21999979019165039, NULL),
     ('08MG021', 1978, 6, 1, 30, 6.65000009536743164, 199.399993896484403, 16, 2.97000002861022905, 4, 9.85000038146972834, 6.65000009536743164, NULL, 8.18000030517578125, NULL, 9.65999984741210938, NULL, 9.85000038146972834, NULL, 9.68000030517577947, NULL, 8.89000034332275391, NULL, 8.30000019073486328, NULL, 8.03999996185302734, NULL, 7.86999988555908203, NULL, 5.6399998664855957, NULL, 4.92999982833862305, NULL, 4.73000001907348633, NULL, 6.51000022888183594, NULL, 3.99000000953674316, NULL, 3.08999991416931152, NULL, 2.97000002861022905, NULL, 5.17999982833862305, NULL, 5.8899998664855957, NULL, 5.30000019073486328, NULL, 6.11999988555908203, NULL, 7.05000019073486328, NULL, 9.82999992370605646, NULL, 6.40000009536743164, NULL, 5.94999980926513672, NULL, 5.21000003814697266, NULL, 5.57999992370605469, NULL, 6.98999977111816406, NULL, 7.32999992370605469, NULL, 6.71000003814697266, NULL, 6.88000011444091797, NULL, NULL, NULL),
     ('08MG021', 1978, 7, 1, 31, 2.88000011444091797, 89.266998291015625, 31, 0.996999979019165039, 4, 6.17000007629394531, 5.38000011444091797, NULL, 5.75, NULL, 6.03000020980834961, NULL, 6.17000007629394531, NULL, 5.71999979019165039, NULL, 5.07000017166137695, NULL, 4.73000001907348633, NULL, 4.67000007629394531, NULL, 3.45000004768371582, NULL, 2.8599998950958252, NULL, 2.33999991416931152, NULL, 2.50999999046325684, NULL, 2.57999992370605469, NULL, 2.52999997138977051, NULL, 2.41000008583068848, NULL, 2.33999991416931152, NULL, 2.09999990463256836, NULL, 1.91999995708465598, NULL, 1.87000000476837203, NULL, 1.77999997138977051, NULL, 1.78999996185302712, NULL, 1.85000002384185791, NULL, 1.77999997138977051, NULL, 1.73000001907348633, NULL, 1.66999995708465576, NULL, 1.62000000476837158, NULL, 2.13000011444091797, NULL, 1.38999998569488525, NULL, 1.10000002384185791, NULL, 1, NULL, 0.996999979019165039, NULL),
     ('08MG021', 1978, 8, 1, 31, 1.12999999523162842, 35.01300048828125, 23, 0.58899998664855957, 25, 2.92000007629394531, 0.985000014305114746, NULL, 0.982999980449676403, NULL, 0.976999998092651367, NULL, 0.985000014305114746, NULL, 0.898000001907348633, NULL, 0.78200000524520874, NULL, 0.716000020503997803, NULL, 0.767000019550323486, NULL, 0.815999984741210938, NULL, 0.93199998140335083, NULL, 1.26999998092651367, NULL, 1.75, NULL, 0.912000000476837158, NULL, 0.820999979972839355, NULL, 1.1799999475479126, NULL, 1.36000001430511475, NULL, 0.878000020980834961, NULL, 0.864000022411346436, NULL, 0.973999977111816406, NULL, 0.971000015735626221, NULL, 0.820999979972839355, NULL, 0.680000007152557373, NULL, 0.58899998664855957, NULL, 1.38999998569488525, NULL, 2.92000007629394531, NULL, 2.56999993324279785, NULL, 1.35000002384185791, NULL, 0.959999978542327992, NULL, 0.892000019550323486, NULL, 0.829999983310699463, NULL, 2.19000005722045898, NULL),
     ('08MG021', 1978, 9, 1, 30, 1.78999996185302712, 53.6090011596679688, 19, 0.634000003337860107, 3, 4.84000015258789062, 2.28999996185302779, NULL, 3.23000001907348633, NULL, 4.84000015258789062, NULL, 2.78999996185302779, NULL, 2.03999996185302779, NULL, 2.18000006675720215, NULL, 1.52999997138977051, NULL, 1.02999997138977051, NULL, 2.56999993324279785, NULL, 3.27999997138977051, NULL, 2.41000008583068848, NULL, 1.76999998092651367, NULL, 1.25, NULL, 1.01999998092651367, NULL, 1.51999998092651367, NULL, 1, NULL, 0.833000004291534424, NULL, 0.71399998664855957, NULL, 0.634000003337860107, NULL, 0.667999982833862305, NULL, 1.12999999523162842, NULL, 1.63999998569488525, NULL, 1.4299999475479126, NULL, 1.94000005722045898, NULL, 2.09999990463256836, NULL, 1.63999998569488525, NULL, 1.5, NULL, 1.10000002384185791, NULL, 1.52999997138977051, NULL, 2, NULL, NULL, NULL),
     ('08MG021', 1978, 10, 1, 31, 0.953000009059906006, 29.5450000762939453, 22, 0.535000026226043701, 23, 3.23000001907348633, 1.60000002384185791, NULL, 1.09000003337860107, NULL, 0.976999998092651367, 'A', 0.869000017642974854, NULL, 0.778999984264373779, NULL, 0.732999980449676514, NULL, 0.72500002384185791, NULL, 0.764999985694885254, NULL, 0.953999996185302845, NULL, 1.40999996662139893, NULL, 1.12999999523162842, NULL, 0.871999979019165039, NULL, 0.732999980449676514, NULL, 0.685000002384185791, NULL, 0.637000024318695068, NULL, 0.592000007629394531, NULL, 0.579999983310699463, NULL, 0.56099998950958252, NULL, 0.555000007152557373, NULL, 0.800999999046325684, NULL, 0.609000027179718018, NULL, 0.535000026226043701, NULL, 3.23000001907348633, NULL, 2.27999997138977051, NULL, 1.21000003814697288, NULL, 0.912000000476837158, NULL, 0.813000023365020752, NULL, 0.792999982833862305, NULL, 0.783999979496002197, NULL, 0.688000023365020752, NULL, 0.643000006675720215, NULL),
     ('08MG021', 1978, 11, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 0.630999982357025146, NULL, 0.685000002384185791, NULL, 0.646000027656555176, NULL, 0.579999983310699463, NULL, 0.53200000524520874, NULL, 0.625999987125396729, NULL, 8.89000034332275391, NULL, 6.63000011444091797, NULL, 3.1400001049041748, NULL, 1.5, NULL, 1.19000005722045898, NULL, 1, NULL, 0.800999999046325684, NULL, 0.748000025749206543, NULL, 0.708000004291534424, NULL, 0.72500002384185791, NULL, 0.595000028610229492, 'A', 0.458999991416931208, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1979, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.187000006437301636, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1979, 2, 0, 28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.152999997138977051, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.14699999988079071, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1979, 3, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.31099998950958252, 'A', 0.728999972343444824, NULL, 1.69000005722045898, NULL, 2.08999991416931152, NULL, 1.3200000524520874, NULL, 0.873000025749206543, NULL, 0.734000027179718018, NULL, 0.708000004291534424, NULL, 0.71399998664855957, NULL, 0.65700000524520874, NULL, 0.642000019550323486, NULL, 0.875, NULL, 0.801999986171722412, NULL, 0.675000011920928955, NULL, 0.583999991416931152, NULL, 0.531000018119812012, NULL, 0.528999984264373779, NULL, 0.570999979972839355, NULL, 0.620999991893768311, NULL, 0.726000010967254639, NULL, 0.839999973773956299, NULL, 0.861000001430511475, NULL, 0.751999974250793457, NULL, 0.657999992370605469, NULL, 0.596000015735626221, NULL, 0.532999992370605469, NULL, 0.483999997377395574, NULL, 0.444999992847442627, NULL),
     ('08MG021', 1979, 4, 1, 30, 0.772000014781951904, 23.1660003662109375, 19, 0.381999999284744263, 30, 2.55999994277954102, 0.416000008583068903, NULL, 0.400000005960464478, NULL, 0.388999998569488525, NULL, 0.388000011444091797, NULL, 0.428000003099441528, NULL, 0.574999988079071045, NULL, 0.612999975681304932, NULL, 0.583999991416931152, NULL, 0.541000008583068848, NULL, 0.486000001430511475, NULL, 0.43599998950958252, NULL, 0.419999986886978149, NULL, 0.448000013828277588, NULL, 0.441000014543533325, NULL, 0.407999992370605524, NULL, 0.39500001072883606, NULL, 0.405000001192092896, NULL, 0.39500001072883606, NULL, 0.381999999284744263, NULL, 0.38499999046325678, NULL, 0.423999994993209783, NULL, 0.550999999046325684, NULL, 0.66100001335144043, NULL, 0.764999985694885254, NULL, 0.920000016689300426, NULL, 1.30999994277954102, NULL, 2.05999994277954102, NULL, 2.47000002861022905, NULL, 2.50999999046325684, NULL, 2.55999994277954102, NULL, NULL, NULL),
     ('08MG021', 1979, 5, 1, 31, 3.3900001049041748, 105.069999694824219, 11, 1.65999996662139893, 26, 7.19000005722045898, 2.68000006675720215, NULL, 2.81999993324279785, NULL, 2.77999997138977051, NULL, 5.34999990463256836, NULL, 3.48000001907348633, NULL, 2.38000011444091797, NULL, 1.92999994754791282, NULL, 1.82000005245208762, NULL, 1.87999999523162842, NULL, 2.04999995231628418, NULL, 1.65999996662139893, NULL, 1.70000004768371582, NULL, 1.70000004768371582, NULL, 2.15000009536743208, NULL, 3.47000002861022905, NULL, 4.80999994277954102, NULL, 3.43000006675720215, NULL, 2.6099998950958252, NULL, 2.8900001049041748, NULL, 3.1400001049041748, NULL, 3.75, NULL, 5.44999980926513672, NULL, 5.65000009536743164, NULL, 5.80000019073486328, NULL, 5, NULL, 7.19000005722045898, NULL, 4.05999994277954102, NULL, 2.91000008583068848, NULL, 2.56999993324279785, NULL, 3.24000000953674316, NULL, 4.71999979019165039, NULL),
     ('08MG021', 1979, 6, 1, 30, 4.03000020980834961, 120.839996337890625, 15, 2.46000003814697266, 2, 5.94999980926513672, 5.76000022888183594, NULL, 5.94999980926513672, NULL, 5.19999980926513672, NULL, 5.28999996185302734, NULL, 5.59000015258789062, NULL, 4.05999994277954102, NULL, 3.52999997138977051, NULL, 3.73000001907348633, NULL, 4.5, NULL, 4.84999990463256836, NULL, 4.69999980926513672, NULL, 4.01999998092651367, NULL, 3.25999999046325684, NULL, 2.83999991416931152, NULL, 2.46000003814697266, NULL, 2.75, NULL, 4.09999990463256836, NULL, 3.93000006675720215, NULL, 3.86999988555908203, NULL, 4.05000019073486328, NULL, 3.45000004768371582, NULL, 3.28999996185302779, NULL, 3.76999998092651367, NULL, 3.3900001049041748, NULL, 3.69000005722045898, NULL, 3.95000004768371582, NULL, 3.99000000953674316, NULL, 3.68000006675720215, NULL, 3.20000004768371582, NULL, 3.99000000953674316, NULL, NULL, NULL),
     ('08MG021', 1979, 7, 1, 31, 2.17000007629394531, 67.1179962158203125, 30, 0.869000017642974854, 10, 4, 3.44000005722045898, NULL, 3.00999999046325684, NULL, 2.56999993324279785, NULL, 2.79999995231628418, NULL, 2.99000000953674316, NULL, 2.81999993324279785, NULL, 2.71000003814697266, NULL, 3.81999993324279785, NULL, 3.25999999046325684, NULL, 4, NULL, 3.29999995231628418, NULL, 2.93000006675720215, NULL, 2.33999991416931152, NULL, 2.01999998092651367, NULL, 2, NULL, 2.09999990463256836, NULL, 2.08999991416931152, NULL, 2.04999995231628418, NULL, 1.91999995708465598, NULL, 1.87000000476837203, NULL, 1.80999994277954102, NULL, 1.46000003814697288, NULL, 1.24000000953674316, NULL, 1.26999998092651367, NULL, 1.29999995231628418, NULL, 1.11000001430511475, NULL, 1.09000003337860107, NULL, 0.977999985218047985, NULL, 0.91100001335144043, NULL, 0.869000017642974854, NULL, 1.03999996185302712, NULL),
     ('08MG021', 1979, 8, 1, 31, 0.721000015735626221, 22.3360004425048828, 31, 0.501999974250793457, 22, 1.16999995708465576, 0.933000028133392445, NULL, 0.871999979019165039, NULL, 0.804000020027160645, NULL, 0.744000017642974854, NULL, 0.722999989986419678, NULL, 0.676999986171722412, NULL, 0.646000027656555176, NULL, 0.626999974250793457, NULL, 0.674000024795532227, NULL, 0.679000020027160645, NULL, 0.639999985694885254, NULL, 0.660000026226043701, NULL, 0.663999974727630615, NULL, 0.658999979496002197, NULL, 0.684000015258789062, NULL, 0.610000014305114746, NULL, 0.852999985218048096, NULL, 1.02999997138977051, NULL, 0.824999988079071045, NULL, 0.777000010013580322, NULL, 0.804000020027160645, NULL, 1.16999995708465576, NULL, 0.819000005722045898, NULL, 0.667999982833862305, NULL, 0.609000027179718018, NULL, 0.620999991893768311, NULL, 0.614000022411346436, NULL, 0.595000028610229492, NULL, 0.587000012397766113, NULL, 0.565999984741210938, NULL, 0.501999974250793457, NULL),
     ('08MG021', 1979, 9, 1, 30, 1.25999999046325684, 37.7019996643066406, 25, 0.551999986171722412, 8, 4.44999980926513672, 0.660000026226043701, NULL, 1.36000001430511475, NULL, 2.01999998092651367, NULL, 1.70000004768371582, NULL, 2.84999990463256836, NULL, 1.75999999046325684, NULL, 1.65999996662139893, NULL, 4.44999980926513672, NULL, 2.68000006675720215, NULL, 1.38999998569488525, NULL, 1, NULL, 0.879000008106231689, NULL, 0.845000028610229492, NULL, 0.827000021934509277, NULL, 0.823000013828277588, NULL, 0.773000001907348633, NULL, 0.744000017642974854, NULL, 0.726000010967254639, NULL, 0.714999973773956299, NULL, 0.694999992847442627, NULL, 0.796000003814697266, NULL, 0.642000019550323486, NULL, 0.574999988079071045, NULL, 0.564999997615814209, NULL, 0.551999986171722412, NULL, 0.564999997615814209, NULL, 1.61000001430511475, NULL, 1.59000003337860107, NULL, 1.04999995231628418, NULL, 1.20000004768371582, NULL, NULL, NULL),
     ('08MG021', 1979, 10, 1, 31, 1.12999999523162842, 35.0460014343261719, 21, 0.462000012397766113, 26, 5.23999977111816406, 0.921000003814697155, NULL, 0.787000000476837158, NULL, 0.704999983310699463, NULL, 0.64999997615814209, NULL, 0.64999997615814209, NULL, 0.657999992370605469, NULL, 0.630999982357025146, NULL, 0.621999979019165039, NULL, 0.578000009059906006, NULL, 0.583000004291534424, NULL, 0.569999992847442627, NULL, 0.550000011920928955, NULL, 0.529999971389770508, NULL, 0.625999987125396729, NULL, 0.578999996185302734, NULL, 0.666000008583068848, NULL, 0.708999991416931152, NULL, 0.621999979019165039, NULL, 0.558000028133392334, NULL, 0.504999995231628418, NULL, 0.462000012397766113, NULL, 0.68199998140335083, NULL, 0.944999992847442627, NULL, 0.897000014781951904, NULL, 4.40000009536743164, NULL, 5.23999977111816406, NULL, 4.01000022888183594, NULL, 2.08999991416931152, NULL, 1.4299999475479126, NULL, 1.19000005722045898, NULL, 1, NULL),
     ('08MG021', 1979, 11, 1, 30, 0.603999972343444824, 18.1280002593994105, 30, 0.282999992370605469, 17, 1.08000004291534424, 0.930999994277953991, NULL, 0.880999982357025146, NULL, 0.823000013828277588, NULL, 0.792999982833862305, NULL, 0.736999988555908203, NULL, 0.723999977111816406, NULL, 0.677999973297119141, NULL, 0.623000025749206543, NULL, 0.611999988555908203, NULL, 0.582000017166137695, NULL, 0.55699998140335083, NULL, 0.555000007152557373, NULL, 0.533999979496002197, NULL, 0.542999982833862305, NULL, 0.544000029563903809, NULL, 1.03999996185302712, NULL, 1.08000004291534424, NULL, 0.797999978065490723, NULL, 0.666999995708465576, NULL, 0.551999986171722412, 'B', 0.495999991893768311, 'B', 0.537999987602233887, 'B', 0.467000007629394476, 'B', 0.425000011920928955, 'B', 0.391000002622604426, 'B', 0.344999998807907104, 'B', 0.331000000238418579, 'B', 0.305999994277954102, 'B', 0.291999995708465576, 'B', 0.282999992370605469, 'B', NULL, NULL),
     ('08MG021', 1979, 12, 1, 31, 1.23000001907348633, 37.9910011291503906, 1, 0.31099998950958252, 17, 3.65000009536743208, 0.31099998950958252, 'B', 0.340000003576278687, 'B', 0.393999993801116943, 'B', 0.453000009059906006, 'B', 0.425000011920928955, 'B', 0.535000026226043701, NULL, 0.481999993324279785, NULL, 0.528999984264373779, NULL, 3.38000011444091797, NULL, 1.99000000953674316, NULL, 1.24000000953674316, NULL, 0.94300001859664917, NULL, 0.907000005245208851, NULL, 1.99000000953674316, NULL, 1.14999997615814209, NULL, 0.883000016212463379, 'A', 3.65000009536743208, 'A', 2.96000003814697266, NULL, 3.44000005722045898, NULL, 2.21000003814697266, NULL, 1.62000000476837158, NULL, 1.12000000476837158, NULL, 0.984000027179718018, NULL, 0.927999973297119252, NULL, 0.862999975681304932, NULL, 0.81400001049041748, NULL, 0.772000014781951904, NULL, 0.72500002384185791, NULL, 0.685000002384185791, NULL, 0.625, NULL, 0.643000006675720215, NULL),
     ('08MG021', 1980, 1, 1, 31, 0.361999988555908203, 11.2220001220703125, 30, 0.254999995231628418, 1, 0.633000016212463379, 0.633000016212463379, NULL, 0.595000028610229492, NULL, 0.583999991416931152, NULL, 0.560000002384185791, 'B', 0.519999980926513672, 'B', 0.49000000953674322, 'B', 0.449999988079071045, 'B', 0.425000011920928955, 'B', 0.409999996423721313, 'B', 0.38499999046325678, 'B', 0.370000004768371582, 'B', 0.360000014305114746, 'B', 0.344999998807907104, 'B', 0.335000008344650269, 'B', 0.321999996900558472, 'B', 0.312000006437301636, 'B', 0.305000007152557373, 'B', 0.300000011920928955, 'B', 0.294999986886978094, 'B', 0.289999991655349731, 'B', 0.282999992370605469, 'B', 0.280000001192092896, 'B', 0.277999997138977051, 'B', 0.272000014781951904, 'B', 0.268000006675720215, 'B', 0.263999998569488525, 'B', 0.259999990463256836, 'B', 0.257999986410140991, 'B', 0.257999986410140991, 'B', 0.254999995231628418, 'B', 0.259999990463256836, 'B'),
     ('08MG021', 1980, 2, 1, 29, 0.654999971389770508, 18.9810009002685547, 1, 0.27000001072883606, 27, 3.1099998950958252, 0.27000001072883606, 'B', 0.280000001192092896, 'B', 0.287999987602233887, 'B', 0.289999991655349731, 'B', 0.289999991655349731, 'B', 0.291999995708465576, 'B', 0.293999999761581421, 'B', 0.296999990940093994, 'B', 0.300000011920928955, 'B', 0.305000007152557373, 'B', 0.307999998331069946, 'B', 0.310000002384185791, 'B', 0.314999997615814209, 'B', 0.317999988794326782, 'B', 0.321000009775161743, 'B', 0.328000009059906006, 'B', 0.335000008344650269, 'B', 0.344999998807907104, 'B', 0.360000014305114746, 'B', 0.375, 'B', 0.389999985694885254, 'B', 0.409999996423721313, 'B', 0.449999988079071045, 'B', 0.540000021457672119, 'B', 0.629999995231628418, 'B', 2.48000001907348633, NULL, 3.1099998950958252, NULL, 2.66000008583068848, NULL, 2.08999991416931152, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1980, 3, 1, 31, 0.508000016212463379, 15.7589998245239258, 27, 0.326000005006790161, 1, 1.44000005722045898, 1.44000005722045898, NULL, 1.19000005722045898, NULL, 0.972000002861022949, NULL, 0.816999971866607666, NULL, 0.644999980926513672, NULL, 0.602999985218048096, NULL, 0.554000020027160645, NULL, 0.527000010013580322, NULL, 0.515999972820281982, NULL, 0.509000003337860107, NULL, 0.479999989271163996, NULL, 0.446999996900558472, NULL, 0.455000013113021851, NULL, 0.462000012397766113, NULL, 0.419999986886978149, NULL, 0.391000002622604426, NULL, 0.418000012636184692, NULL, 0.388000011444091797, NULL, 0.363000005483627319, NULL, 0.363000005483627319, NULL, 0.363000005483627319, NULL, 0.372999995946884155, NULL, 0.368999987840652466, NULL, 0.358000010251998901, NULL, 0.345999985933303833, NULL, 0.338999986648559626, NULL, 0.326000005006790161, NULL, 0.330000013113021851, NULL, 0.337999999523162842, NULL, 0.331000000238418579, NULL, 0.326000005006790161, NULL),
     ('08MG021', 1980, 4, 1, 30, 1.62000000476837158, 48.6910018920898366, 1, 0.326000005006790161, 19, 5.78000020980834961, 0.326000005006790161, NULL, 0.335999995470046997, NULL, 0.356999993324279785, NULL, 0.381000012159347534, NULL, 0.377000004053115845, NULL, 0.397000014781951904, NULL, 0.361000001430511475, NULL, 0.347999989986419678, NULL, 0.349000006914138794, NULL, 0.349999994039535522, NULL, 0.36500000953674322, NULL, 0.50700002908706665, NULL, 0.837000012397766113, NULL, 1.20000004768371582, NULL, 1.22000002861022949, NULL, 1.09000003337860107, NULL, 1.05999994277954102, NULL, 1.60000002384185791, NULL, 5.78000020980834961, NULL, 4.34000015258789062, NULL, 2.94000005722045898, NULL, 2.57999992370605469, NULL, 2.56999993324279785, NULL, 2.54999995231628418, NULL, 2.04999995231628418, NULL, 1.86000001430511475, NULL, 2.81999993324279785, NULL, 3.43000006675720215, NULL, 3.24000000953674316, NULL, 3.06999993324279785, NULL, NULL, NULL),
     ('08MG021', 1980, 5, 1, 31, 4.25, 131.720001220703125, 24, 2.6400001049041748, 12, 6.48999977111816406, 3.55999994277954102, NULL, 5.01000022888183594, NULL, 3.82999992370605513, NULL, 3.90000009536743208, NULL, 5.26999998092651367, NULL, 5.76999998092651367, NULL, 4.28999996185302734, NULL, 3.82999992370605513, NULL, 3.07999992370605469, NULL, 4.1100001335144043, NULL, 5.40000009536743164, NULL, 6.48999977111816406, NULL, 5.67000007629394531, NULL, 4.34000015258789062, NULL, 3.28999996185302779, NULL, 2.98000001907348633, NULL, 3.55999994277954102, NULL, 4.51999998092651367, NULL, 4.59999990463256836, NULL, 4.34999990463256836, NULL, 4.32999992370605469, NULL, 3.40000009536743208, NULL, 2.69000005722045898, NULL, 2.6400001049041748, NULL, 3.1400001049041748, NULL, 3.71000003814697266, NULL, 4.28000020980834961, NULL, 3.6400001049041748, NULL, 4.51000022888183594, NULL, 5.73000001907348633, NULL, 5.80000019073486328, NULL),
     ('08MG021', 1980, 6, 1, 30, 5.65999984741210938, 169.699996948242188, 4, 3.55999994277954102, 17, 6.98000001907348633, 6.82000017166137695, NULL, 4.17000007629394531, NULL, 3.84999990463256792, NULL, 3.55999994277954102, NULL, 3.75, NULL, 5.3899998664855957, NULL, 6.05999994277954102, NULL, 6.34000015258789062, NULL, 6.05999994277954102, NULL, 5.57999992370605469, NULL, 5, NULL, 5.25, NULL, 6.73000001907348633, NULL, 6.40000009536743164, NULL, 6.61999988555908203, NULL, 5.8899998664855957, NULL, 6.98000001907348633, NULL, 6.26000022888183594, NULL, 5.86999988555908203, NULL, 6.55000019073486328, NULL, 6.53999996185302734, NULL, 6.8600001335144043, NULL, 5.98999977111816406, NULL, 5.30999994277954102, NULL, 5.59000015258789062, NULL, 6.57000017166137695, NULL, 5.07000017166137695, NULL, 5.21000003814697266, NULL, 4.96999979019165039, NULL, 4.46000003814697266, NULL, NULL, NULL),
     ('08MG021', 1980, 7, 1, 31, 3.69000005722045898, 114.290000915527344, 31, 1.38999998569488525, 2, 5.46000003814697266, 5.17999982833862305, NULL, 5.46000003814697266, NULL, 5.40000009536743164, NULL, 4.44999980926513672, NULL, 4, NULL, 3.71000003814697266, NULL, 4.55000019073486328, NULL, 5.30999994277954102, NULL, 5.15000009536743164, NULL, 4.57000017166137695, NULL, 5.34000015258789062, NULL, 4.09999990463256836, NULL, 4.15999984741210938, NULL, 4.30999994277954102, NULL, 5.19999980926513672, NULL, 4.01999998092651367, NULL, 3.20000004768371582, NULL, 3.27999997138977051, NULL, 2.96000003814697266, NULL, 3.00999999046325684, NULL, 3.30999994277954102, NULL, 3.6099998950958252, NULL, 3.5, NULL, 2.71000003814697266, NULL, 2.48000001907348633, NULL, 2.30999994277954102, NULL, 2.28999996185302779, NULL, 2.1400001049041748, NULL, 1.71000003814697288, NULL, 1.48000001907348633, NULL, 1.38999998569488525, NULL),
     ('08MG021', 1980, 8, 1, 31, 0.847999989986419678, 26.3010005950927734, 31, 0.423999994993209783, 2, 1.70000004768371582, 1.34000003337860107, NULL, 1.70000004768371582, NULL, 1.36000001430511475, NULL, 1.02999997138977051, NULL, 0.962999999523162842, NULL, 0.888999998569488525, NULL, 0.853999972343444824, NULL, 0.912999987602233998, NULL, 0.898999989032745361, NULL, 0.845000028610229492, NULL, 0.973999977111816406, NULL, 0.962999999523162842, NULL, 0.859000027179718018, NULL, 0.802999973297119141, NULL, 0.744000017642974854, NULL, 0.694999992847442627, NULL, 1.38999998569488525, NULL, 1.19000005722045898, NULL, 0.791000008583068848, NULL, 0.665000021457672119, NULL, 0.606000006198883057, NULL, 0.55699998140335083, NULL, 0.549000024795532227, NULL, 0.519999980926513672, NULL, 0.497999995946884155, NULL, 0.653999984264373779, NULL, 0.955999970436096191, NULL, 0.68900001049041748, NULL, 0.527999997138977051, NULL, 0.453000009059906006, NULL, 0.423999994993209783, NULL),
     ('08MG021', 1980, 9, 1, 30, 1.27999997138977051, 38.26300048828125, 18, 0.470999985933303833, 29, 7.21000003814697266, 1.11000001430511475, NULL, 0.994000017642974854, NULL, 0.648999989032745361, NULL, 0.537999987602233887, NULL, 0.559000015258789062, NULL, 1.73000001907348633, NULL, 1.78999996185302712, NULL, 0.948000013828277588, NULL, 0.712999999523162842, NULL, 0.634999990463256836, NULL, 0.583000004291534424, NULL, 0.819000005722045898, NULL, 0.750999987125396729, NULL, 0.598999977111816406, NULL, 0.522000014781951904, NULL, 0.518999993801116943, NULL, 0.523000001907348633, NULL, 0.470999985933303833, NULL, 3.21000003814697266, NULL, 2.70000004768371582, NULL, 1.37000000476837158, NULL, 0.949000000953674427, NULL, 0.769999980926513672, NULL, 0.677999973297119141, NULL, 0.593999981880187988, NULL, 0.537000000476837158, NULL, 0.492000013589859009, NULL, 0.769999980926513672, NULL, 7.21000003814697266, NULL, 4.53000020980834961, NULL, NULL, NULL),
     ('08MG021', 1980, 10, 1, 31, 0.814999997615814209, 25.2609996795654297, 19, 0.474999994039535522, 1, 2.19000005722045898, 2.19000005722045898, NULL, 1.37000000476837158, NULL, 1.11000001430511475, NULL, 0.944999992847442627, NULL, 0.860000014305114746, NULL, 0.852999985218048096, NULL, 0.837000012397766113, NULL, 0.902000010013580433, NULL, 0.705999970436096191, NULL, 0.586000025272369385, NULL, 0.515999972820281982, NULL, 0.779999971389770508, NULL, 0.991999983787536621, NULL, 0.732999980449676514, NULL, 0.621999979019165039, NULL, 0.523999989032745361, NULL, 0.513000011444091797, NULL, 0.49000000953674322, NULL, 0.474999994039535522, NULL, 1.19000005722045898, NULL, 0.861000001430511475, NULL, 0.654999971389770508, NULL, 0.550000011920928955, NULL, 0.605000019073486328, NULL, 0.920000016689300426, NULL, 0.714999973773956299, NULL, 0.580999970436096191, NULL, 0.569999992847442627, NULL, 0.676999986171722412, NULL, 0.623000025749206543, NULL, 1.30999994277954102, NULL),
     ('08MG021', 1980, 11, 1, 30, 2.30999994277954102, 69.4459991455078125, 26, 0.986000001430511586, 1, 7.40000009536743164, 7.40000009536743164, NULL, 3.66000008583068892, NULL, 2.3599998950958252, NULL, 5.48999977111816406, NULL, 3.33999991416931152, NULL, 4.80999994277954102, NULL, 4.3899998664855957, NULL, 4.34999990463256836, NULL, 2.82999992370605469, NULL, 2, NULL, 1.63999998569488525, NULL, 1.49000000953674316, NULL, 1.37999999523162842, NULL, 1.30999994277954102, NULL, 1.1799999475479126, NULL, 1.15999996662139893, NULL, 1.12999999523162842, NULL, 1.23000001907348633, NULL, 1.25, NULL, 1.39999997615814209, NULL, 1.62000000476837158, NULL, 1.20000004768371582, NULL, 1.0700000524520874, NULL, 1, NULL, 1.00999999046325684, NULL, 0.986000001430511586, NULL, 3.90000009536743208, NULL, 1.99000000953674316, NULL, 1.53999996185302712, NULL, 1.33000004291534424, NULL, NULL, NULL),
     ('08MG021', 1980, 12, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 1.16999995708465576, NULL, 1.08000004291534424, NULL, 1, 'B', 0.970000028610229603, 'B', 0.930000007152557373, 'B', 0.89999997615814209, 'B', 0.870000004768371582, 'B', 0.860000014305114746, 'B', 0.91000002622604359, 'B', 1.0700000524520874, 'B', 2.16000008583068848, 'A', 1.5, NULL, 1.19000005722045898, NULL, 2.17000007629394531, NULL, 5.34999990463256836, NULL, 5.65000009536743164, NULL, 3.17000007629394531, NULL, 2.29999995231628418, NULL, 1.72000002861022949, NULL, 1.52999997138977051, NULL, 1.47000002861022949, NULL, 1.63999998569488525, NULL, 1.64999997615814209, NULL, 1.51999998092651367, NULL, 2.68000006675720215, NULL, 42.2999992370605469, 'E', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1982, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.303000003099441584, 'A', 0.221000000834465027, NULL, 0.225999996066093445, NULL, 0.238999992609024048, NULL, 0.246999993920326233, NULL),
     ('08MG021', 1982, 2, 1, 28, 0.319999992847442627, 8.9720001220703125, 9, 0.100000001490116119, 17, 1.08000004291534424, 0.224999994039535522, NULL, 0.196999996900558472, NULL, 0.173999994993209839, NULL, 0.165999993681907654, NULL, 0.150000005960464478, 'B', 0.140000000596046448, 'B', 0.125, 'B', 0.109999999403953566, 'B', 0.100000001490116119, 'B', 0.101999998092651353, 'B', 0.104999996721744537, 'B', 0.109999999403953566, 'B', 0.140000000596046448, 'B', 0.200000002980232239, 'B', 0.49000000953674322, NULL, 0.91000002622604359, NULL, 1.08000004291534424, NULL, 0.643999993801116943, NULL, 0.547999978065490723, NULL, 0.643000006675720215, NULL, 0.544000029563903809, NULL, 0.446999996900558472, NULL, 0.340999990701675415, NULL, 0.303999990224838257, NULL, 0.272000014781951904, NULL, 0.24500000476837161, NULL, 0.24300000071525571, NULL, 0.21699999272823331, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1982, 3, 1, 31, 0.162000000476837158, 5.02299976348876953, 7, 0.120999999344348921, 1, 0.250999987125396784, 0.250999987125396784, NULL, 0.240999996662139893, NULL, 0.200000002980232239, NULL, 0.168999999761581421, NULL, 0.172000005841255188, NULL, 0.164000004529953003, NULL, 0.120999999344348921, NULL, 0.136000007390975952, NULL, 0.150999993085861206, NULL, 0.165999993681907654, NULL, 0.152999997138977051, NULL, 0.149000003933906555, NULL, 0.159999996423721313, NULL, 0.153999999165534973, NULL, 0.14100000262260437, NULL, 0.13099999725818634, NULL, 0.126000002026557922, NULL, 0.126000002026557922, NULL, 0.13500000536441803, NULL, 0.133000001311302213, NULL, 0.13500000536441803, NULL, 0.128000006079673767, NULL, 0.136000007390975952, NULL, 0.159999996423721313, NULL, 0.182999998331069946, NULL, 0.224999994039535522, NULL, 0.215000003576278687, NULL, 0.186000004410743713, NULL, 0.166999995708465576, NULL, 0.158999994397163391, NULL, 0.150000005960464478, NULL),
     ('08MG021', 1982, 4, 1, 30, 0.421000003814697266, 12.630000114440918, 8, 0.127000004053115845, 23, 1.35000002384185791, 0.14699999988079071, NULL, 0.14100000262260437, NULL, 0.128999993205070496, NULL, 0.131999999284744263, NULL, 0.136999994516372681, NULL, 0.14699999988079071, NULL, 0.129999995231628418, NULL, 0.127000004053115845, NULL, 0.138999998569488525, NULL, 0.166999995708465576, NULL, 0.192000001668930054, NULL, 0.172000005841255188, NULL, 0.200000002980232239, NULL, 0.214000001549720792, NULL, 0.168999999761581421, NULL, 0.158000007271766663, NULL, 0.165999993681907654, NULL, 0.136999994516372681, NULL, 0.128000006079673767, NULL, 0.158000007271766663, NULL, 0.319999992847442627, NULL, 0.797999978065490723, NULL, 1.35000002384185791, NULL, 1.13999998569488525, NULL, 0.957000017166137584, NULL, 1.03999996185302712, NULL, 1.16999995708465576, NULL, 1.08000004291534424, NULL, 0.916999995708465576, NULL, 0.768000006675720215, NULL, NULL, NULL),
     ('08MG021', 1982, 5, 1, 31, 1.76999998092651367, 54.9249992370605469, 4, 0.68900001049041748, 25, 2.53999996185302779, 0.787000000476837158, NULL, 1.00999999046325684, NULL, 0.847000002861022949, NULL, 0.68900001049041748, NULL, 0.801999986171722412, NULL, 1.23000001907348633, NULL, 1.69000005722045898, NULL, 1.65999996662139893, NULL, 1.69000005722045898, NULL, 2.04999995231628418, NULL, 2.07999992370605469, NULL, 2.1099998950958252, NULL, 2.09999990463256836, NULL, 2.1099998950958252, NULL, 2.05999994277954102, NULL, 2.06999993324279785, NULL, 1.97000002861022927, NULL, 2.07999992370605469, NULL, 2.1400001049041748, NULL, 2.1400001049041748, NULL, 2.03999996185302779, NULL, 1.79999995231628418, NULL, 1.82000005245208762, NULL, 2.03999996185302779, NULL, 2.53999996185302779, NULL, 1.84000003337860107, NULL, 1.77999997138977051, NULL, 1.83000004291534402, NULL, 1.74000000953674316, NULL, 1.99000000953674316, NULL, 2.19000005722045898, NULL),
     ('08MG021', 1982, 6, 1, 30, 3.06999993324279785, 92.160003662109375, 5, 1.63999998569488525, 21, 4.88000011444091797, 2.47000002861022905, NULL, 2.1400001049041748, NULL, 1.78999996185302712, NULL, 1.77999997138977051, NULL, 1.63999998569488525, NULL, 1.70000004768371582, NULL, 1.66999995708465576, NULL, 1.71000003814697288, NULL, 2.26999998092651367, NULL, 2.78999996185302779, NULL, 2.56999993324279785, NULL, 2.55999994277954102, NULL, 2.6400001049041748, NULL, 2.50999999046325684, NULL, 2.50999999046325684, NULL, 2.88000011444091797, NULL, 3.50999999046325684, NULL, 3.69000005722045898, NULL, 4.34999990463256836, NULL, 4.86999988555908203, NULL, 4.88000011444091797, NULL, 4.59000015258789062, NULL, 4.26999998092651367, NULL, 4.05000019073486328, NULL, 3.61999988555908203, NULL, 4, NULL, 3.58999991416931152, NULL, 3.75, NULL, 3.92000007629394487, NULL, 3.44000005722045898, NULL, NULL, NULL),
     ('08MG021', 1982, 7, 1, 31, 4.19999980926513672, 130.160003662109375, 1, 3.53999996185302779, 20, 4.8600001335144043, 3.53999996185302779, NULL, 3.65000009536743208, NULL, 3.67000007629394487, NULL, 3.6400001049041748, NULL, 4.09999990463256836, NULL, 4.28999996185302734, NULL, 3.93000006675720215, NULL, 3.86999988555908203, NULL, 3.81999993324279785, NULL, 3.6099998950958252, NULL, 3.58999991416931152, NULL, 3.59999990463256836, NULL, 3.61999988555908203, NULL, 3.69000005722045898, NULL, 4.84000015258789062, NULL, 4.73999977111816406, NULL, 4.61999988555908203, NULL, 4.44999980926513672, NULL, 4.1100001335144043, NULL, 4.8600001335144043, NULL, 4.8600001335144043, NULL, 4.46999979019165039, NULL, 4.30999994277954102, NULL, 4.55999994277954102, NULL, 4.71000003814697266, NULL, 4.78000020980834961, NULL, 4.57000017166137695, NULL, 4.6399998664855957, NULL, 4.57999992370605469, NULL, 4.34000015258789062, NULL, 4.09999990463256836, NULL),
     ('08MG021', 1982, 8, 1, 31, 1.59000003337860107, 49.2360000610351634, 29, 0.477999985218048096, 1, 3.54999995231628418, 3.54999995231628418, NULL, 3.40000009536743208, NULL, 3.13000011444091797, NULL, 2.96000003814697266, NULL, 2.81999993324279785, NULL, 2.76999998092651367, NULL, 2.6400001049041748, NULL, 2.56999993324279785, NULL, 2.43000006675720215, NULL, 2.26999998092651367, NULL, 2.02999997138977051, NULL, 2.04999995231628418, NULL, 2.38000011444091797, NULL, 1.75999999046325684, NULL, 1.15999996662139893, NULL, 0.929000020027160645, NULL, 0.759000003337860107, NULL, 0.722000002861022949, NULL, 0.74299997091293335, NULL, 0.762000024318695068, NULL, 0.852999985218048096, NULL, 0.795000016689300537, NULL, 0.754000008106231689, NULL, 0.750999987125396729, NULL, 0.722000002861022949, NULL, 0.727999985218048096, NULL, 0.660000026226043701, NULL, 0.555999994277954102, NULL, 0.477999985218048096, NULL, 0.527000010013580322, NULL, 0.577000021934509277, NULL),
     ('08MG021', 1982, 9, 1, 30, 0.91000002622604359, 27.3059997558593714, 30, 0.256999999284744263, 9, 3.26999998092651367, 0.529999971389770508, NULL, 0.56800001859664917, NULL, 0.621999979019165039, NULL, 1.34000003337860107, NULL, 0.779999971389770508, NULL, 0.53600001335144043, NULL, 0.888999998569488525, NULL, 1.38999998569488525, NULL, 3.26999998092651367, NULL, 2.51999998092651367, NULL, 2.75999999046325684, NULL, 1.79999995231628418, NULL, 1.11000001430511475, NULL, 0.741999983787536621, NULL, 0.606999993324279785, NULL, 0.609000027179718018, NULL, 0.616999983787536621, NULL, 0.625, NULL, 0.640999972820281982, NULL, 0.620999991893768311, NULL, 0.637000024318695068, NULL, 0.570999979972839355, NULL, 0.505999982357025146, NULL, 0.481000006198883112, NULL, 0.605000019073486328, NULL, 0.583000004291534424, NULL, 0.441000014543533325, NULL, 0.358000010251998901, NULL, 0.289999991655349731, NULL, 0.256999999284744263, NULL, NULL, NULL),
     ('08MG021', 1982, 10, 1, 31, 1.50999999046325684, 46.9519996643066406, 1, 0.248999997973442078, 24, 3.13000011444091797, 0.248999997973442078, NULL, 1.20000004768371582, NULL, 0.565999984741210938, NULL, 0.398000001907348633, NULL, 0.323000013828277588, NULL, 2.78999996185302779, NULL, 2.16000008583068848, NULL, 1.12999999523162842, NULL, 0.917999982833862416, NULL, 1.33000004291534424, NULL, 1.60000002384185791, NULL, 1.37000000476837158, NULL, 1.48000001907348633, NULL, 1.5700000524520874, NULL, 1.15999996662139893, NULL, 1.10000002384185791, NULL, 1.33000004291534424, NULL, 0.916999995708465576, NULL, 0.714999973773956299, NULL, 0.589999973773956299, NULL, 0.796000003814697266, NULL, 1.87999999523162842, NULL, 2.16000008583068848, NULL, 3.13000011444091797, NULL, 2.17000007629394531, NULL, 2.24000000953674316, NULL, 2.72000002861022905, NULL, 2.69000005722045898, NULL, 2.3900001049041748, NULL, 2, NULL, 1.87999999523162842, NULL),
     ('08MG021', 1982, 11, 1, 30, 0.694999992847442627, 20.8409996032714844, 29, 0.24500000476837161, 4, 1.80999994277954102, 1.62000000476837158, NULL, 1.33000004291534424, NULL, 1.27999997138977051, NULL, 1.80999994277954102, NULL, 1.52999997138977051, NULL, 1.29999995231628418, NULL, 1.14999997615814209, NULL, 0.902000010013580433, NULL, 0.704999983310699463, NULL, 0.71799999475479126, NULL, 0.680000007152557373, NULL, 0.648000001907348633, NULL, 0.541999995708465576, NULL, 0.554000020027160645, NULL, 0.606000006198883057, NULL, 0.626999974250793457, NULL, 0.620999991893768311, NULL, 0.537000000476837158, NULL, 0.523999989032745361, NULL, 0.479000002145767212, NULL, 0.324999988079071045, 'B', 0.300000011920928955, 'B', 0.275000005960464478, 'B', 0.27000001072883606, 'B', 0.264999985694885254, 'B', 0.254999995231628418, 'B', 0.25, 'B', 0.247999995946884155, 'B', 0.24500000476837161, 'B', 0.24500000476837161, 'B', NULL, NULL),
     ('08MG021', 1982, 12, 1, 31, 0.453999996185302734, 14.0889997482299805, 30, 0.202000007033348083, 3, 1.75, 0.241999998688697787, 'B', 0.239999994635581998, 'B', 1.75, 'B', 1.59000003337860107, NULL, 0.783999979496002197, NULL, 0.591000020503997803, NULL, 0.476999998092651367, NULL, 0.419999986886978149, 'B', 0.389999985694885254, 'B', 0.370000004768371582, 'B', 0.349999994039535522, 'B', 0.344999998807907104, 'B', 0.340000003576278687, 'B', 0.342000007629394531, 'B', 0.361999988555908203, NULL, 0.653999984264373779, NULL, 0.55699998140335083, NULL, 0.481999993324279785, NULL, 0.46799999475479126, NULL, 0.418999999761581421, NULL, 0.370999991893768311, NULL, 0.34299999475479126, NULL, 0.305999994277954102, NULL, 0.284000009298324585, NULL, 0.289999991655349731, NULL, 0.256000012159347534, NULL, 0.225999996066093445, NULL, 0.229000002145767212, NULL, 0.207000002264976501, NULL, 0.202000007033348083, NULL, 0.202000007033348083, NULL),
     ('08MG021', 1983, 1, 1, 31, 0.651000022888183594, 20.1749992370605469, 1, 0.13500000536441803, 12, 2.5, 0.13500000536441803, NULL, 0.14100000262260437, NULL, 0.163000002503395081, NULL, 0.15700000524520874, NULL, 0.158999994397163391, NULL, 0.143999993801116943, NULL, 0.782999992370605469, NULL, 1.30999994277954102, NULL, 0.718999981880187988, NULL, 1.23000001907348633, NULL, 2.44000005722045898, NULL, 2.5, NULL, 1.51999998092651367, NULL, 0.935999989509582409, NULL, 0.704999983310699463, NULL, 0.570999979972839355, NULL, 0.493000000715255682, NULL, 0.518000006675720215, NULL, 0.660000026226043701, NULL, 0.574000000953674316, NULL, 0.504000008106231689, NULL, 0.441000014543533325, NULL, 0.405000001192092896, NULL, 0.386000007390976008, NULL, 0.370999991893768311, NULL, 0.386000007390976008, NULL, 0.421999990940093994, NULL, 0.418999999761581421, NULL, 0.361999988555908203, NULL, 0.319999992847442627, NULL, 0.300999999046325684, NULL),
     ('08MG021', 1983, 2, 1, 28, 0.829999983310699463, 23.2290000915527308, 4, 0.150000005960464478, 24, 2.81999993324279785, 0.261999994516372681, NULL, 0.200000002980232239, 'B', 0.170000001788139343, 'B', 0.150000005960464478, 'B', 0.159999996423721313, 'B', 0.197999998927116394, NULL, 0.195999994874000522, NULL, 0.197999998927116394, NULL, 0.186000004410743713, NULL, 0.186000004410743713, NULL, 1.59000003337860107, NULL, 2.65000009536743208, NULL, 1.75999999046325684, NULL, 1.14999997615814209, NULL, 0.855000019073486328, NULL, 0.694999992847442627, NULL, 0.708000004291534424, NULL, 0.920000016689300426, NULL, 0.663999974727630615, NULL, 0.637000024318695068, NULL, 0.552999973297119141, NULL, 0.501999974250793457, NULL, 0.824999988079071045, NULL, 2.81999993324279785, NULL, 1.98000001907348633, NULL, 1.24000000953674316, NULL, 0.975000023841858021, NULL, 0.799000024795532227, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1983, 3, 1, 31, 0.873000025749206543, 27.0629997253418004, 7, 0.398000001907348633, 10, 3.44000005722045898, 0.700999975204467773, NULL, 0.609000027179718018, NULL, 0.537999987602233887, NULL, 0.456000000238418579, NULL, 0.428000003099441528, NULL, 0.421999990940093994, NULL, 0.398000001907348633, NULL, 0.470999985933303833, NULL, 2.76999998092651367, NULL, 3.44000005722045898, NULL, 2.3599998950958252, NULL, 1.51999998092651367, NULL, 1.13999998569488525, NULL, 1.02999997138977051, NULL, 0.879999995231628418, NULL, 0.796000003814697266, NULL, 0.751999974250793457, NULL, 0.702000021934509277, NULL, 0.690999984741210938, NULL, 0.68900001049041748, NULL, 0.643000006675720215, NULL, 0.607999980449676514, NULL, 0.595000028610229492, NULL, 0.577000021934509277, NULL, 0.56800001859664917, NULL, 0.563000023365020752, NULL, 0.552999973297119141, NULL, 0.527999997138977051, NULL, 0.509000003337860107, NULL, 0.583999991416931152, NULL, 0.541999995708465576, NULL),
     ('08MG021', 1983, 4, 1, 30, 1.64999997615814209, 49.5029983520507812, 13, 0.405999988317489624, 25, 3.84999990463256792, 0.497999995946884155, NULL, 0.481000006198883112, NULL, 0.446999996900558472, NULL, 0.414000004529953003, NULL, 0.453000009059906006, NULL, 0.607999980449676514, NULL, 0.755999982357025146, NULL, 0.731999993324279785, NULL, 0.652000010013580322, NULL, 0.540000021457672119, NULL, 0.486999988555908203, NULL, 0.43700000643730158, NULL, 0.405999988317489624, NULL, 0.414000004529953003, NULL, 0.501999974250793457, NULL, 0.759000003337860107, NULL, 0.96700000762939442, NULL, 1.53999996185302712, NULL, 2.30999994277954102, NULL, 3.11999988555908203, NULL, 3.30999994277954102, NULL, 2.6099998950958252, NULL, 3.23000001907348633, NULL, 3.79999995231628418, NULL, 3.84999990463256792, NULL, 2.90000009536743208, NULL, 2.55999994277954102, NULL, 3.28999996185302779, NULL, 3.84999990463256792, NULL, 3.57999992370605469, NULL, NULL, NULL),
     ('08MG021', 1983, 5, 1, 31, 4.57999992370605469, 141.889999389648438, 11, 2.27999997138977051, 31, 11.3999996185302717, 3.55999994277954102, NULL, 3.65000009536743208, NULL, 3.79999995231628418, NULL, 3.8900001049041748, NULL, 3.82999992370605513, NULL, 3.66000008583068892, NULL, 3.71000003814697266, NULL, 3.46000003814697266, NULL, 2.75999999046325684, NULL, 2.34999990463256836, NULL, 2.27999997138977051, NULL, 3.23000001907348633, NULL, 3.93000006675720215, NULL, 3.6400001049041748, NULL, 3.92000007629394487, NULL, 3.63000011444091797, NULL, 3.68000006675720215, NULL, 3.53999996185302779, NULL, 3.17000007629394531, NULL, 2.73000001907348633, NULL, 3.28999996185302779, NULL, 3.74000000953674316, NULL, 4.46999979019165039, NULL, 5.55999994277954102, NULL, 6.46000003814697266, NULL, 5.94999980926513672, NULL, 6.55000019073486328, NULL, 7.17000007629394531, NULL, 8.47999954223632812, NULL, 10.3999996185302717, NULL, 11.3999996185302717, NULL),
     ('08MG021', 1983, 6, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 10.1999998092651367, NULL, 7.69999980926513672, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 10.6000003814697283, 'A', 5.67999982833862305, NULL, 5.90999984741210938, NULL, 5.94999980926513672, NULL, 5.71000003814697266, NULL, 5.67999982833862305, NULL, 5.3899998664855957, NULL, 6.55000019073486328, NULL, 4.82999992370605469, NULL, 4.94999980926513672, NULL, 5.38000011444091797, NULL, 5.09000015258789062, NULL, 5, NULL, 5.15000009536743164, NULL, NULL, NULL),
     ('08MG021', 1983, 7, 1, 31, 4.86999988555908203, 150.850006103515625, 30, 2.11999988555908203, 11, 15.5, 5.09999990463256836, NULL, 6.09000015258789062, NULL, 4.94000005722045898, NULL, 5.34000015258789062, NULL, 5.30000019073486328, NULL, 5.19000005722045898, NULL, 5.6399998664855957, NULL, 5.55999994277954102, NULL, 5.67999982833862305, NULL, 5.48999977111816406, NULL, 15.5, NULL, 12.3999996185302717, NULL, 9.39000034332275391, NULL, 5.65000009536743164, NULL, 4.30999994277954102, NULL, 4.26000022888183594, 'E', 4.1399998664855957, 'E', 4.01999998092651367, 'E', 3.90000009536743208, 'E', 3.77999997138977051, 'E', 3.66000008583068892, 'E', 3.54999995231628418, NULL, 2.68000006675720215, NULL, 2.61999988555908203, NULL, 2.75999999046325684, NULL, 2.59999990463256836, NULL, 2.50999999046325684, NULL, 2.22000002861022905, NULL, 2.28999996185302779, NULL, 2.11999988555908203, NULL, 2.16000008583068848, NULL),
     ('08MG021', 1983, 8, 1, 31, 1.20000004768371582, 37.2639999389648509, 27, 0.610000014305114746, 1, 2.20000004768371582, 2.20000004768371582, NULL, 2.11999988555908203, NULL, 1.91999995708465598, NULL, 1.65999996662139893, NULL, 1.55999994277954102, NULL, 1.55999994277954102, NULL, 1.47000002861022949, NULL, 1.53999996185302712, NULL, 1.61000001430511475, NULL, 1.59000003337860107, NULL, 1.55999994277954102, NULL, 1.39999997615814209, NULL, 1.27999997138977051, NULL, 1.44000005722045898, NULL, 1.19000005722045898, NULL, 1.01999998092651367, NULL, 0.925000011920928955, NULL, 0.883000016212463379, NULL, 0.845000028610229492, NULL, 0.805000007152557373, NULL, 0.740000009536743164, NULL, 0.699000000953674316, NULL, 0.68900001049041748, NULL, 0.707000017166137695, NULL, 0.672999978065490723, NULL, 0.639999985694885254, NULL, 0.610000014305114746, NULL, 1.01999998092651367, NULL, 1.1799999475479126, NULL, 0.920000016689300426, NULL, 0.808000028133392334, NULL),
     ('08MG021', 1983, 9, 1, 30, 0.740000009536743164, 22.1849994659423828, 30, 0.333999991416931152, 11, 1.53999996185302712, 1.25999999046325684, NULL, 1.40999996662139893, NULL, 1.03999996185302712, NULL, 0.935000002384185791, NULL, 0.810000002384185791, NULL, 1.10000002384185791, NULL, 1.14999997615814209, NULL, 0.883000016212463379, NULL, 0.703999996185302734, NULL, 1, NULL, 1.53999996185302712, NULL, 0.996999979019165039, NULL, 0.791000008583068848, NULL, 0.697000026702880859, NULL, 0.61799997091293335, NULL, 0.658999979496002197, NULL, 0.624000012874603271, NULL, 0.572000026702880859, NULL, 0.499000012874603271, NULL, 0.462000012397766113, NULL, 0.441000014543533325, NULL, 0.442000001668930054, NULL, 0.458000004291534424, NULL, 0.472000002861022949, NULL, 0.479000002145767212, NULL, 0.483000010251998901, NULL, 0.513000011444091797, NULL, 0.432999998331070002, NULL, 0.379000008106231689, NULL, 0.333999991416931152, NULL, NULL, NULL),
     ('08MG021', 1983, 10, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 0.319000005722045898, NULL, 0.310000002384185791, NULL, 0.305999994277954102, NULL, 0.354000002145767212, NULL, 0.324000000953674316, NULL, 0.293999999761581421, NULL, 0.268000006675720215, NULL, 0.252999991178512573, NULL, 0.24500000476837161, NULL, 0.219999998807907104, NULL, 0.21899999678134921, NULL, 0.216000005602836609, NULL, 0.212999999523162842, NULL, 0.215000003576278687, NULL, 0.211999997496604892, NULL, 0.202000007033348083, NULL, 0.301999986171722412, NULL, 0.349999994039535522, NULL, 0.400999993085861206, NULL, 0.919000029563903809, NULL, 1.87000000476837203, NULL, 2.72000002861022905, NULL, 1.5, NULL, 0.990000009536743164, NULL, 1.70000004768371582, NULL, 6.34999990463256836, NULL, 3.88000011444091797, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1983, 12, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.564999997615814209, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1984, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.75999999046325684, NULL, 2.04999995231628418, NULL, 2, NULL, 2.01999998092651367, NULL, 1.59000003337860107, NULL, 1.5, NULL, 1.35000002384185791, NULL, 1.05999994277954102, NULL, 0.827000021934509277, NULL, 0.717000007629394531, NULL, 0.643999993801116943, NULL, 0.642000019550323486, NULL, 0.518000006675720215, NULL, 0.500999987125396729, NULL, 0.538999974727630615, NULL, 0.546999990940093994, NULL, 0.56800001859664917, NULL, 0.555000007152557373, NULL, 0.555999994277954102, NULL, 0.577000021934509277, NULL, 0.893000006675720215, NULL, 0.667999982833862305, NULL, 0.945999979972839355, NULL, 1.46000003814697288, NULL, 1.24000000953674316, NULL, 0.936999976634979248, NULL, 0.78600001335144043, NULL),
     ('08MG021', 1984, 2, 1, 29, 0.637000024318695068, 18.4740009307861328, 17, 0.421999990940093994, 20, 1.80999994277954102, 0.68900001049041748, NULL, 0.615000009536743164, NULL, 0.589999973773956299, NULL, 0.552999973297119141, NULL, 0.527000010013580322, NULL, 0.531000018119812012, NULL, 0.537999987602233887, NULL, 0.653999984264373779, NULL, 0.889999985694885254, NULL, 0.748000025749206543, NULL, 0.630999982357025146, NULL, 0.598999977111816406, NULL, 0.597999989986419678, NULL, 0.523000001907348633, NULL, 0.509000003337860107, NULL, 0.477999985218048096, NULL, 0.421999990940093994, NULL, 0.426999986171722412, NULL, 0.485000014305114802, NULL, 1.80999994277954102, NULL, 1.16999995708465576, NULL, 0.810000002384185791, NULL, 0.671000003814697266, NULL, 0.583000004291534424, NULL, 0.514999985694885254, NULL, 0.477999985218048096, NULL, 0.488999992609024103, NULL, 0.481999993324279785, NULL, 0.458999991416931208, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1984, 3, 1, 31, 0.665000021457672119, 20.6140003204345703, 4, 0.384000003337860107, 21, 1.74000000953674316, 0.426999986171722412, NULL, 0.409999996423721313, NULL, 0.391999989748001099, NULL, 0.384000003337860107, NULL, 0.384000003337860107, NULL, 0.426999986171722412, NULL, 0.490999996662139893, NULL, 0.547999978065490723, NULL, 0.679000020027160645, NULL, 0.778999984264373779, NULL, 0.832000017166137695, NULL, 0.75700002908706665, NULL, 0.679000020027160645, NULL, 0.586000025272369385, NULL, 0.565999984741210938, NULL, 0.538999974727630615, NULL, 0.514999985694885254, NULL, 0.508000016212463379, NULL, 0.504999995231628418, NULL, 0.800000011920928955, NULL, 1.74000000953674316, NULL, 1.30999994277954102, NULL, 1.16999995708465576, NULL, 0.954999983310699574, NULL, 0.792999982833862305, NULL, 0.656000018119812012, NULL, 0.615000009536743164, NULL, 0.579999983310699463, NULL, 0.544000029563903809, NULL, 0.527000010013580322, NULL, 0.515999972820281982, NULL),
     ('08MG021', 1984, 4, 1, 30, 0.598999977111816406, 17.9740009307861328, 13, 0.391999989748001099, 16, 1.45000004768371582, 0.509999990463256836, NULL, 0.509000003337860107, NULL, 0.513000011444091797, NULL, 0.503000020980834961, NULL, 0.492000013589859009, NULL, 0.462999999523162897, NULL, 0.444999992847442627, NULL, 0.430000007152557373, NULL, 0.418999999761581421, NULL, 0.414000004529953003, NULL, 0.409000009298324585, NULL, 0.393999993801116943, NULL, 0.391999989748001099, NULL, 0.433999985456466675, NULL, 1.24000000953674316, NULL, 1.45000004768371582, NULL, 1.05999994277954102, NULL, 0.825999975204467773, NULL, 0.684000015258789062, NULL, 0.665000021457672119, NULL, 0.648999989032745361, NULL, 0.66100001335144043, NULL, 0.629999995231628418, NULL, 0.541000008583068848, NULL, 0.535000026226043701, NULL, 0.550999999046325684, NULL, 0.555999994277954102, NULL, 0.555000007152557373, NULL, 0.535000026226043701, NULL, 0.509000003337860107, NULL, NULL, NULL),
     ('08MG021', 1984, 5, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 0.53600001335144043, NULL, 0.574000000953674316, NULL, 0.586000025272369385, NULL, 0.580999970436096191, NULL, 0.560000002384185791, NULL, 0.558000028133392334, NULL, 0.679000020027160645, NULL, 1.62000000476837158, NULL, 1.63999998569488525, NULL, 1.24000000953674316, NULL, 1.11000001430511475, NULL, 1.03999996185302712, NULL, 1.26999998092651367, NULL, 1.80999994277954102, NULL, 1.63999998569488525, NULL, 1.36000001430511475, NULL, 1.27999997138977051, NULL, 1.27999997138977051, NULL, 1.75, NULL, 1.80999994277954102, NULL, 1.55999994277954102, NULL, 1.40999996662139893, NULL, 1.38999998569488525, NULL, 1.37000000476837158, NULL, 1.37999999523162842, NULL, 1.4299999475479126, NULL, 2.07999992370605469, NULL, 2.17000007629394531, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1984, 6, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4.07999992370605469, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1984, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.07999992370605469, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1984, 10, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.6099998950958252, NULL, 2.17000007629394531, NULL, 2.05999994277954102, NULL, 1.82000005245208762, NULL, 1.62999999523162842, NULL, 1.51999998092651367, NULL, 1.39999997615814209, NULL, 1.27999997138977051, NULL, 1.21000003814697288, NULL, 1.15999996662139893, NULL, 1.10000002384185791, NULL, 1.01999998092651367, NULL, 0.984000027179718018, NULL, 1, NULL, 1.53999996185302712, NULL, 1.22000002861022949, NULL, 1.04999995231628418, NULL, 0.962000012397766002, NULL, 0.720000028610229492, 'B', 0.603999972343444824, 'B', 0.555999994277954102, 'B'),
     ('08MG021', 1984, 11, 1, 30, 0.626999974250793457, 18.8069992065429688, 30, 0.474000006914138794, 3, 1.03999996185302712, 0.540000021457672119, 'B', 0.819999992847442627, 'B', 1.03999996185302712, NULL, 0.870999991893768311, NULL, 0.785000026226043701, NULL, 0.745999991893768311, NULL, 0.834999978542327881, NULL, 0.753000020980834961, NULL, 0.694000005722045898, NULL, 0.647000014781951904, NULL, 0.630999982357025146, NULL, 0.605000019073486328, NULL, 0.596000015735626221, NULL, 0.593999981880187988, NULL, 0.532999992370605469, NULL, 0.522000014781951904, NULL, 0.533999979496002197, NULL, 0.533999979496002197, NULL, 0.575999975204467773, NULL, 0.595000028610229492, NULL, 0.52499997615814209, NULL, 0.5, NULL, 0.643999993801116943, NULL, 0.644999980926513672, NULL, 0.564999997615814209, NULL, 0.514999985694885254, NULL, 0.509000003337860107, NULL, 0.486000001430511475, NULL, 0.493000000715255682, NULL, 0.474000006914138794, NULL, NULL, NULL),
     ('08MG021', 1984, 12, 1, 31, 0.335000008344650269, 10.3979997634887695, 31, 0.25, 8, 0.52499997615814209, 0.402000010013580322, 'B', 0.342000007629394531, 'B', 0.324000000953674316, 'B', 0.312000006437301636, 'B', 0.300000011920928955, 'B', 0.300000011920928955, 'B', 0.389999985694885254, 'B', 0.52499997615814209, NULL, 0.449999988079071045, NULL, 0.43599998950958252, NULL, 0.407000005245208796, NULL, 0.389999985694885254, NULL, 0.388999998569488525, NULL, 0.365999996662139893, 'B', 0.342000007629394531, 'B', 0.319999992847442627, 'B', 0.314999997615814209, 'B', 0.312000006437301636, 'B', 0.310000002384185791, 'B', 0.307999998331069946, 'B', 0.307000011205673218, 'B', 0.307000011205673218, 'B', 0.305999994277954102, 'B', 0.300000011920928955, 'B', 0.29800000786781311, 'B', 0.294999986886978094, 'B', 0.289999991655349731, 'B', 0.280000001192092896, 'B', 0.27000001072883606, 'B', 0.254999995231628418, 'B', 0.25, 'B'),
     ('08MG021', 1985, 1, 1, 31, 0.31299999356269842, 9.7089996337890625, 12, 0.222000002861022921, 18, 0.670000016689300537, 0.24500000476837161, 'B', 0.244000002741813687, 'B', 0.241999998688697787, 'B', 0.241999998688697787, 'B', 0.24500000476837161, 'B', 0.241999998688697787, 'B', 0.239999994635581998, 'B', 0.234999999403953552, 'B', 0.231000006198883029, NULL, 0.231999993324279757, NULL, 0.22800000011920929, NULL, 0.222000002861022921, NULL, 0.225999996066093445, NULL, 0.319999992847442627, NULL, 0.301999986171722412, NULL, 0.273999989032745361, NULL, 0.367000013589859009, NULL, 0.670000016689300537, NULL, 0.52499997615814209, NULL, 0.510999977588653564, NULL, 0.442999988794326782, NULL, 0.391000002622604426, NULL, 0.368999987840652466, NULL, 0.347999989986419678, NULL, 0.340000003576278687, 'B', 0.319999992847442627, 'B', 0.310000002384185791, 'B', 0.294999986886978094, 'B', 0.284999996423721313, 'B', 0.284999996423721313, 'B', 0.280000001192092896, 'B'),
     ('08MG021', 1985, 2, 1, 28, 0.230000004172325162, 6.44199991226196289, 20, 0.200000002980232239, 24, 0.308999985456466675, 0.275000005960464478, 'B', 0.259999990463256836, 'B', 0.254999995231628418, 'B', 0.24500000476837161, 'B', 0.239999994635581998, 'B', 0.239999994635581998, 'B', 0.239999994635581998, 'B', 0.234999999403953552, 'B', 0.230000004172325162, 'B', 0.219999998807907104, 'B', 0.219999998807907104, 'B', 0.217999994754791288, 'B', 0.215000003576278687, 'B', 0.219999998807907104, 'B', 0.219999998807907104, 'B', 0.215000003576278687, 'B', 0.209999993443489075, 'B', 0.204999998211860629, 'B', 0.202999994158744812, 'B', 0.200000002980232239, 'B', 0.200000002980232239, 'B', 0.204999998211860629, 'B', 0.209999993443489075, 'B', 0.308999985456466675, NULL, 0.263999998569488525, NULL, 0.234999999403953552, NULL, 0.225999996066093445, NULL, 0.226999998092651367, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1985, 3, 1, 31, 0.236000001430511475, 7.31400012969970703, 10, 0.194000005722045898, 20, 0.31099998950958252, 0.224000006914138794, NULL, 0.216000005602836609, NULL, 0.207000002264976501, NULL, 0.21699999272823331, NULL, 0.222000002861022921, NULL, 0.214000001549720792, NULL, 0.200000002980232239, NULL, 0.200000002980232239, NULL, 0.195999994874000522, 'B', 0.194000005722045898, 'B', 0.194999992847442627, NULL, 0.194999992847442627, NULL, 0.199000000953674316, NULL, 0.203999996185302762, NULL, 0.211999997496604892, NULL, 0.219999998807907104, NULL, 0.273999989032745361, NULL, 0.307999998331069946, NULL, 0.308999985456466675, NULL, 0.31099998950958252, NULL, 0.289000004529953003, NULL, 0.275999993085861206, NULL, 0.272000014781951904, NULL, 0.268999993801116943, NULL, 0.264999985694885254, NULL, 0.241999998688697787, NULL, 0.238999992609024048, NULL, 0.224999994039535522, NULL, 0.223000004887580872, NULL, 0.224999994039535522, NULL, 0.272000014781951904, NULL),
     ('08MG021', 1985, 4, 1, 30, 1.41999995708465576, 42.5929985046386719, 30, 0.658999979496002197, 12, 2.50999999046325684, 1.28999996185302712, NULL, 2.33999991416931152, NULL, 1.86000001430511475, NULL, 1.22000002861022949, NULL, 0.906000018119812012, NULL, 0.773000001907348633, NULL, 0.908999979496002197, NULL, 1.33000004291534424, NULL, 1.89999997615814209, NULL, 2.25, NULL, 2.32999992370605469, NULL, 2.50999999046325684, NULL, 2.45000004768371582, NULL, 2.3599998950958252, NULL, 2.22000002861022905, NULL, 1.99000000953674316, NULL, 1.85000002384185791, NULL, 1.63999998569488525, NULL, 1.38999998569488525, NULL, 1.1799999475479126, NULL, 1.00999999046325684, NULL, 0.921000003814697155, NULL, 0.837999999523162842, NULL, 0.751999974250793457, NULL, 0.703000009059906006, NULL, 0.69300001859664917, NULL, 0.851999998092651367, NULL, 0.783999979496002197, NULL, 0.683000028133392334, NULL, 0.658999979496002197, NULL, NULL, NULL),
     ('08MG021', 1985, 5, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 0.71799999475479126, NULL, 1.11000001430511475, NULL, 1.94000005722045898, NULL, 1.50999999046325684, NULL, 1.25999999046325684, NULL, 1.11000001430511475, NULL, 1.0700000524520874, NULL, 1, NULL, 1.02999997138977051, NULL, 1.16999995708465576, NULL, 1.03999996185302712, NULL, 0.929000020027160645, NULL, 0.865999996662139893, NULL, 1.00999999046325684, NULL, 1.60000002384185791, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1985, 6, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 8.05000019073486328, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG021', 1985, 7, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.45000004768371582, NULL, 2.36999988555908203, NULL, 2.28999996185302779, NULL, 2.24000000953674316, NULL, 2.20000004768371582, NULL, 2.31999993324279785, NULL, 2.26999998092651367, NULL, 2.15000009536743208, NULL, 2.07999992370605469, NULL, 2.03999996185302779, NULL, 2.05999994277954102, NULL, 1.97000002861022927, NULL, 1.87999999523162842, NULL, 1.70000004768371582, NULL, 1.51999998092651367, NULL, 1.36000001430511475, NULL, 1.25, NULL, 1.27999997138977051, NULL, 1.34000003337860107, NULL, 1.29999995231628418, NULL, 1.4299999475479126, NULL),
     ('08MG021', 1985, 8, 1, 31, 0.707000017166137695, 21.9050006866455078, 31, 0.374000012874603271, 1, 1.25999999046325684, 1.25999999046325684, NULL, 1.11000001430511475, NULL, 1.04999995231628418, NULL, 1.14999997615814209, NULL, 0.941999971866607555, NULL, 0.759000003337860107, NULL, 1.13999998569488525, NULL, 0.86799997091293335, NULL, 0.889999985694885254, NULL, 0.870000004768371582, NULL, 0.74299997091293335, NULL, 0.734000027179718018, NULL, 0.662999987602233887, NULL, 0.644999980926513672, NULL, 0.667999982833862305, NULL, 0.653999984264373779, NULL, 0.652000010013580322, NULL, 0.663999974727630615, NULL, 0.59299999475479126, NULL, 0.569999992847442627, NULL, 0.503000020980834961, NULL, 0.469999998807907104, NULL, 0.513999998569488525, NULL, 0.552999973297119141, NULL, 0.606999993324279785, NULL, 0.527000010013580322, NULL, 0.456000000238418579, NULL, 0.442999988794326782, NULL, 0.411000013351440374, NULL, 0.421999990940093994, NULL, 0.374000012874603271, NULL),
     ('08MG021', 1985, 9, 1, 30, 0.31400001049041748, 9.43000030517577947, 30, 0.192000001668930054, 6, 0.779999971389770508, 0.333999991416931152, NULL, 0.32699999213218689, NULL, 0.347000002861022894, NULL, 0.379999995231628418, NULL, 0.43799999356269842, NULL, 0.779999971389770508, NULL, 0.469000011682510376, NULL, 0.337999999523162842, NULL, 0.266000002622604426, NULL, 0.287999987602233887, NULL, 0.294999986886978094, NULL, 0.386999994516372681, NULL, 0.370999991893768311, NULL, 0.391999989748001099, NULL, 0.317000001668930054, NULL, 0.470999985933303833, NULL, 0.382999986410140991, NULL, 0.29800000786781311, NULL, 0.252000004053115845, NULL, 0.224999994039535522, NULL, 0.219999998807907104, NULL, 0.21699999272823331, NULL, 0.208000004291534396, NULL, 0.209999993443489075, NULL, 0.210999995470046997, NULL, 0.219999998807907104, NULL, 0.207000002264976501, NULL, 0.194000005722045898, NULL, 0.193000003695488004, NULL, 0.192000001668930054, NULL, NULL, NULL),
     ('08MG021', 1985, 10, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 0.190999999642372131, NULL, 0.186000004410743713, NULL, 0.186000004410743713, NULL, 0.188999995589256287, NULL, 0.193000003695488004, NULL, 0.190999999642372131, NULL, 0.165999993681907654, NULL, 0.158000007271766663, NULL, 0.159999996423721313, NULL, 0.268999993801116943, NULL, 0.551999986171722412, NULL, 0.317000001668930054, NULL, 0.398999989032745361, NULL, 1.62000000476837158, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.31999993324279785, NULL, 1.82000005245208762, NULL, 1.66999995708465576, NULL, 1.45000004768371582, NULL, 1.39999997615814209, NULL, 1.47000002861022949, NULL, 1.25, NULL, 1.0700000524520874, NULL, 1.11000001430511475, NULL, 1.02999997138977051, NULL),
     ('08MG021', 1985, 11, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.23000001907348633, NULL, 1.79999995231628418, NULL, 1.51999998092651367, NULL, 1.35000002384185791, NULL, 1.21000003814697288, NULL, 1, 'B', 0.915000021457672008, 'B', 0.730000019073486328, 'B', 0.720000028610229492, 'B', 0.680000007152557373, 'B', 0.64999997615814209, 'B', 0.639999985694885254, 'B', 0.629999995231628418, 'B', 0.610000014305114746, 'B', 0.60000002384185791, 'B', 0.5, 'B', 0.469999998807907104, 'B', 0.439999997615814209, 'B', 0.409999996423721313, 'B', 0.38499999046325678, 'B', 0.36500000953674322, 'B', 0.344999998807907104, 'B', 0.335000008344650269, 'B', 0.32699999213218689, 'B', 0.324999988079071045, 'B', 0.335000008344650269, 'B', 0.35499998927116394, 'B', 0.370000004768371582, 'B', NULL, NULL),
     ('08MG021', 1985, 12, 1, 31, 0.386999994516372681, 12.0109996795654297, 19, 0.330000013113021851, 5, 0.722999989986419678, 0.379999995231628418, 'B', 0.400000005960464478, 'B', 0.439999997615814209, 'B', 0.519999980926513672, 'B', 0.722999989986419678, NULL, 0.60000002384185791, NULL, 0.49000000953674322, NULL, 0.439999997615814209, NULL, 0.404000014066696167, NULL, 0.379000008106231689, NULL, 0.377000004053115845, NULL, 0.356000006198883057, NULL, 0.347999989986419678, NULL, 0.349999994039535522, NULL, 0.335999995470046997, NULL, 0.34299999475479126, NULL, 0.337000012397766113, NULL, 0.333000004291534424, NULL, 0.330000013113021851, 'B', 0.335000008344650269, 'B', 0.330000013113021851, 'B', 0.330000013113021851, 'B', 0.340000003576278687, 'B', 0.340000003576278687, 'B', 0.349999994039535522, 'B', 0.360000014305114746, 'B', 0.35499998927116394, 'B', 0.349999994039535522, 'B', 0.349999994039535522, 'B', 0.344999998807907104, 'B', 0.340000003576278687, 'B'),
     ('08MG026', 1993, 9, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4.98999977111816406, 'A', 4.82999992370605469, NULL, 5.25, NULL, 4.59000015258789062, NULL, 4.17999982833862305, NULL, 2.61999988555908203, NULL, 2.46000003814697266, NULL, 2.59999990463256836, NULL, 2.05999994277954102, NULL, 1.78999996185302712, NULL, 1.80999994277954102, NULL, 1.73000001907348633, NULL, 1.72000002861022949, NULL, 1.50999999046325684, NULL, 1.30999994277954102, NULL, 1.29999995231628418, NULL, 1.27999997138977051, NULL, 1.29999995231628418, NULL, 1.25999999046325684, NULL, 1.71000003814697288, NULL, 2.28999996185302779, NULL, 2.63000011444091797, NULL, 2.75, NULL, 2.25, NULL, NULL, NULL),
     ('08MG026', 1993, 10, 1, 31, 1.77999997138977051, 55.0719985961914062, 21, 0.955999970436096191, 23, 4.76000022888183594, 2.40000009536743208, NULL, 2.6400001049041748, NULL, 2.6099998950958252, NULL, 2.41000008583068848, NULL, 2.11999988555908203, NULL, 1.82000005245208762, NULL, 1.39999997615814209, NULL, 1.22000002861022949, NULL, 1.21000003814697288, NULL, 1.1799999475479126, NULL, 1.16999995708465576, NULL, 1.15999996662139893, NULL, 1.12000000476837158, NULL, 1.15999996662139893, NULL, 1.21000003814697288, NULL, 1.14999997615814209, NULL, 1.05999994277954102, NULL, 1.01999998092651367, NULL, 1.01999998092651367, NULL, 0.976000010967254639, NULL, 0.955999970436096191, NULL, 1.98000001907348633, NULL, 4.76000022888183594, 'A', 4.3600001335144043, 'A', 2.45000004768371582, NULL, 1.88999998569488525, NULL, 1.77999997138977051, NULL, 1.95000004768371604, NULL, 1.74000000953674316, NULL, 1.61000001430511475, NULL, 1.53999996185302712, NULL),
     ('08MG026', 1993, 11, 1, 30, 1.16999995708465576, 35, 25, 1.01999998092651367, 3, 1.65999996662139893, 1.37999999523162842, NULL, 1.38999998569488525, NULL, 1.65999996662139893, NULL, 1.37000000476837158, NULL, 1.20000004768371582, NULL, 1.16999995708465576, NULL, 1.12999999523162842, NULL, 1.10000002384185791, NULL, 1.12000000476837158, NULL, 1.04999995231628418, NULL, 1.03999996185302712, NULL, 1.04999995231628418, NULL, 1.08000004291534424, NULL, 1.03999996185302712, NULL, 1.40999996662139893, NULL, 1.20000004768371582, NULL, 1.11000001430511475, NULL, 1.11000001430511475, NULL, 1.13999998569488525, NULL, 1.21000003814697288, NULL, 1.28999996185302712, NULL, 1.12000000476837158, NULL, 1.08000004291534424, NULL, 1.03999996185302712, NULL, 1.01999998092651367, NULL, 1.12000000476837158, NULL, 1.12000000476837158, NULL, 1.08000004291534424, NULL, 1.05999994277954102, NULL, 1.11000001430511475, NULL, NULL, NULL),
     ('08MG026', 1993, 12, 1, 31, 1.5700000524520874, 48.7620010375976562, 2, 0.962000012397766002, 10, 5.48999977111816406, 1.01999998092651367, NULL, 0.962000012397766002, NULL, 1.80999994277954102, NULL, 2.36999988555908203, NULL, 1.40999996662139893, NULL, 1.19000005722045898, NULL, 1.13999998569488525, NULL, 1.05999994277954102, NULL, 1.09000003337860107, NULL, 5.48999977111816406, NULL, 3.55999994277954102, NULL, 2.63000011444091797, NULL, 2.27999997138977051, NULL, 1.97000002861022927, NULL, 1.73000001907348633, NULL, 1.58000004291534424, NULL, 1.39999997615814209, 'B', 1.37000000476837158, 'B', 1.34000003337860107, 'B', 1.27999997138977051, 'B', 1.25, 'B', 1.1799999475479126, 'B', 1.14999997615814209, 'B', 1.12000000476837158, 'B', 1.10000002384185791, 'B', 1.08000004291534424, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.03999996185302712, 'B', 1.02999997138977051, 'B', 1.01999998092651367, 'B'),
     ('08MG026', 1994, 1, 1, 31, 1.58000004291534424, 49.1100006103515625, 1, 1.08000004291534424, 24, 3.11999988555908203, 1.08000004291534424, NULL, 1.10000002384185791, NULL, 1.13999998569488525, NULL, 1.39999997615814209, NULL, 1.37999999523162842, NULL, 1.20000004768371582, NULL, 1.16999995708465576, NULL, 1.16999995708465576, NULL, 1.10000002384185791, NULL, 1.11000001430511475, NULL, 1.10000002384185791, NULL, 1.14999997615814209, NULL, 1.35000002384185791, NULL, 1.5, NULL, 1.52999997138977051, NULL, 1.53999996185302712, NULL, 1.53999996185302712, NULL, 1.52999997138977051, NULL, 1.50999999046325684, NULL, 1.51999998092651367, NULL, 1.36000001430511475, NULL, 1.97000002861022927, NULL, 2.65000009536743208, NULL, 3.11999988555908203, NULL, 2.48000001907348633, NULL, 2.28999996185302779, NULL, 2.08999991416931152, NULL, 1.92999994754791282, NULL, 1.84000003337860107, NULL, 1.69000005722045898, NULL, 1.5700000524520874, NULL),
     ('08MG026', 1994, 2, 1, 28, 1.11000001430511475, 31.1739997863769567, 27, 0.930000007152557373, 1, 1.46000003814697288, 1.46000003814697288, 'B', 1.37000000476837158, 'B', 1.3200000524520874, 'B', 1.26999998092651367, 'B', 1.20000004768371582, 'B', 1.16999995708465576, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.05999994277954102, 'B', 1.12000000476837158, 'B', 1.05999994277954102, 'B', 1.10000002384185791, 'B', 1.20000004768371582, 'B', 1.11000001430511475, NULL, 1.12999999523162842, NULL, 1.14999997615814209, NULL, 1.12999999523162842, NULL, 1.12999999523162842, NULL, 1.12000000476837158, NULL, 1.09000003337860107, NULL, 1.0700000524520874, NULL, 1.01999998092651367, NULL, 0.994000017642974854, 'B', 0.970000028610229603, 'B', 0.949999988079071045, 'B', 0.939999997615814209, 'B', 0.930000007152557373, 'B', 1, 'B', NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1994, 3, 1, 31, 2.17000007629394531, 67.3000030517578125, 23, 1.19000005722045898, 2, 6.80000019073486328, 2.75, NULL, 6.80000019073486328, 'A', 6.44000005722045898, NULL, 4.55999994277954102, NULL, 3.31999993324279785, NULL, 2.6099998950958252, NULL, 2.29999995231628418, NULL, 1.92999994754791282, NULL, 1.78999996185302712, NULL, 1.6799999475479126, NULL, 1.65999996662139893, NULL, 1.63999998569488525, NULL, 1.65999996662139893, NULL, 1.75999999046325684, NULL, 1.66999995708465576, NULL, 1.6799999475479126, NULL, 1.63999998569488525, NULL, 1.53999996185302712, NULL, 1.41999995708465576, NULL, 1.47000002861022949, NULL, 1.39999997615814209, NULL, 1.25999999046325684, NULL, 1.19000005722045898, NULL, 1.21000003814697288, NULL, 1.21000003814697288, NULL, 1.22000002861022949, NULL, 1.26999998092651367, NULL, 1.45000004768371582, NULL, 1.75, NULL, 2.24000000953674316, NULL, 2.77999997138977051, NULL),
     ('08MG026', 1994, 4, 1, 30, 3.20000004768371582, 95.9599990844726562, 10, 2.01999998092651367, 19, 5.21999979019165039, 3.03999996185302779, NULL, 3.19000005722045898, NULL, 3.17000007629394531, NULL, 3.15000009536743208, NULL, 2.98000001907348633, NULL, 2.77999997138977051, NULL, 2.40000009536743208, NULL, 2.25999999046325684, NULL, 2.19000005722045898, NULL, 2.01999998092651367, NULL, 2.1099998950958252, NULL, 2.66000008583068848, NULL, 2.56999993324279785, NULL, 2.52999997138977051, NULL, 2.23000001907348633, NULL, 2.15000009536743208, NULL, 2.56999993324279785, NULL, 3.48000001907348633, NULL, 5.21999979019165039, NULL, 4.84000015258789062, NULL, 4.69999980926513672, NULL, 4.3899998664855957, NULL, 4.01000022888183594, NULL, 3.50999999046325684, NULL, 3.27999997138977051, NULL, 3.31999993324279785, NULL, 3.67000007629394487, NULL, 3.72000002861022949, NULL, 3.93000006675720215, NULL, 3.8900001049041748, NULL, NULL, NULL),
     ('08MG026', 1994, 5, 1, 31, 4.73999977111816406, 146.80999755859375, 4, 2.90000009536743208, 11, 7.07999992370605469, 3.49000000953674316, NULL, 3.13000011444091797, NULL, 2.96000003814697266, NULL, 2.90000009536743208, NULL, 3.26999998092651367, NULL, 4.09999990463256836, NULL, 5.3600001335144043, NULL, 6.8899998664855957, NULL, 6.1399998664855957, NULL, 6.75, NULL, 7.07999992370605469, NULL, 6.28999996185302734, NULL, 5.44999980926513672, NULL, 4.8600001335144043, NULL, 4.09999990463256836, NULL, 3.81999993324279785, NULL, 3.79999995231628418, NULL, 3.98000001907348633, NULL, 4.76000022888183594, NULL, 4.76999998092651367, NULL, 5.01000022888183594, NULL, 4.42999982833862305, NULL, 4.51000022888183594, NULL, 4.82000017166137695, NULL, 6.55000019073486328, NULL, 6.53999996185302734, NULL, 5.11999988555908203, NULL, 4.34999990463256836, NULL, 4.05000019073486328, NULL, 3.77999997138977051, NULL, 3.75, NULL),
     ('08MG026', 1994, 6, 1, 30, 6.3899998664855957, 191.699996948242188, 2, 3.63000011444091797, 24, 13.5, 3.83999991416931197, NULL, 3.63000011444091797, NULL, 4.19000005722045898, NULL, 4.67000007629394531, NULL, 4.51000022888183594, NULL, 4.3899998664855957, NULL, 4.48999977111816406, NULL, 4.07999992370605469, NULL, 3.8900001049041748, NULL, 4.69999980926513672, 'E', 6, 'E', 8.30000019073486328, 'E', 7.5, 'E', 6.30000019073486328, 'E', 5.59999990463256836, 'E', 5.09999990463256836, 'E', 5.19999980926513672, 'E', 5.40000009536743164, 'E', 4.80000019073486328, 'E', 5, 'E', 5.59999990463256836, 'E', 7.40999984741210938, 'A', 8.40999984741210938, NULL, 13.5, NULL, 9.71000003814697266, NULL, 8.88000011444091797, NULL, 8.48999977111816406, NULL, 8.64999961853027344, NULL, 9.71000003814697266, NULL, 9.75, NULL, NULL, NULL),
     ('08MG026', 1994, 7, 1, 31, 7.03000020980834961, 218.039993286132812, 31, 3.75999999046325684, 21, 13.6000003814697283, 10.1999998092651367, NULL, 8.02000045776367188, NULL, 6.42000007629394531, NULL, 5.82000017166137695, NULL, 6, NULL, 6.19999980926513672, NULL, 6.63000011444091797, NULL, 7.57000017166137695, NULL, 7.15000009536743164, NULL, 6.76999998092651367, NULL, 6.67999982833862305, NULL, 6.28000020980834961, NULL, 7.48999977111816406, NULL, 7.26000022888183594, NULL, 7.26000022888183594, NULL, 6.36999988555908203, NULL, 7.6399998664855957, NULL, 8.48999977111816406, NULL, 6.53999996185302734, NULL, 6.71000003814697266, NULL, 13.6000003814697283, NULL, 10.6000003814697283, NULL, 8.40999984741210938, NULL, 7.57999992370605469, NULL, 7.3899998664855957, NULL, 6.15000009536743164, NULL, 5.42000007629394531, NULL, 5.05999994277954102, NULL, 4.48000001907348633, NULL, 4.09000015258789062, NULL, 3.75999999046325684, NULL),
     ('08MG026', 1994, 8, 1, 31, 2.6400001049041748, 81.7900009155273438, 25, 1.96000003814697288, 4, 4.26000022888183594, 3.59999990463256836, NULL, 3.6099998950958252, NULL, 4.1399998664855957, NULL, 4.26000022888183594, NULL, 3.86999988555908203, NULL, 3.21000003814697266, NULL, 2.99000000953674316, NULL, 3.18000006675720215, NULL, 2.84999990463256836, NULL, 2.25999999046325684, NULL, 2.40000009536743208, NULL, 2.74000000953674316, NULL, 2.71000003814697266, NULL, 2.54999995231628418, NULL, 2.32999992370605469, NULL, 2.13000011444091797, NULL, 2.17000007629394531, NULL, 2.25, NULL, 2.44000005722045898, NULL, 2.22000002861022905, NULL, 2.1099998950958252, NULL, 2.23000001907348633, NULL, 2.20000004768371582, NULL, 2.16000008583068848, NULL, 1.96000003814697288, NULL, 2.11999988555908203, NULL, 2.01999998092651367, NULL, 2.13000011444091797, NULL, 2.21000003814697266, NULL, 2.32999992370605469, NULL, 2.41000008583068848, NULL),
     ('08MG026', 1994, 9, 1, 30, 2.68000006675720215, 80.410003662109375, 5, 1.89999997615814209, 8, 3.45000004768371582, 2.18000006675720215, NULL, 2, NULL, 2.09999990463256836, NULL, 1.92999994754791282, NULL, 1.89999997615814209, NULL, 2, NULL, 2.29999995231628418, NULL, 3.45000004768371582, NULL, 2.76999998092651367, NULL, 2.75999999046325684, NULL, 2.32999992370605469, NULL, 2.19000005722045898, NULL, 2.34999990463256836, NULL, 2.96000003814697266, NULL, 3.13000011444091797, NULL, 3.23000001907348633, NULL, 3.31999993324279785, NULL, 2.97000002861022905, NULL, 2.93000006675720215, NULL, 3.05999994277954102, NULL, 2.91000008583068848, NULL, 3, NULL, 2.72000002861022905, NULL, 2.6400001049041748, NULL, 2.74000000953674316, NULL, 2.66000008583068848, NULL, 3, NULL, 2.8900001049041748, NULL, 2.84999990463256836, NULL, 3.1400001049041748, NULL, NULL, NULL),
     ('08MG026', 1994, 10, 1, 31, 1.48000001907348633, 45.8100013732910156, 17, 1.12000000476837158, 1, 3.20000004768371582, 3.20000004768371582, NULL, 2.27999997138977051, NULL, 1.88999998569488525, NULL, 1.86000001430511475, NULL, 1.75, NULL, 1.62000000476837158, NULL, 1.47000002861022949, NULL, 1.36000001430511475, NULL, 1.39999997615814209, NULL, 1.45000004768371582, NULL, 1.27999997138977051, NULL, 1.25, NULL, 1.22000002861022949, NULL, 1.21000003814697288, NULL, 1.15999996662139893, NULL, 1.15999996662139893, NULL, 1.12000000476837158, NULL, 1.16999995708465576, NULL, 1.1799999475479126, NULL, 1.3200000524520874, NULL, 1.37999999523162842, 'A', 1.29999995231628418, 'E', 1.22000002861022949, 'E', 1.1799999475479126, 'E', 1.16999995708465576, 'E', 2.09999990463256836, 'E', 1.79999995231628418, 'E', 1.50999999046325684, 'A', 1.25, NULL, 1.24000000953674316, NULL, 1.30999994277954102, NULL),
     ('08MG026', 1994, 11, 1, 30, 1.01999998092651367, 30.5760002136230469, 21, 0.861999988555908203, 1, 1.48000001907348633, 1.48000001907348633, NULL, 1.1799999475479126, NULL, 1.11000001430511475, 'B', 1.10000002384185791, 'B', 1.08000004291534424, 'B', 1.0700000524520874, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.03999996185302712, 'B', 1.03999996185302712, NULL, 1.00999999046325684, NULL, 1.02999997138977051, NULL, 1.03999996185302712, NULL, 1.02999997138977051, NULL, 1.01999998092651367, NULL, 1.02999997138977051, NULL, 0.876999974250793457, NULL, 0.864000022411346436, NULL, 1.02999997138977051, NULL, 0.953000009059906006, NULL, 0.861999988555908203, NULL, 1.00999999046325684, NULL, 1.08000004291534424, 'A', 1, 'E', 0.920000016689300426, 'E', 0.889999985694885254, 'E', 0.879999995231628418, 'E', 0.870000004768371582, 'E', 0.870000004768371582, 'E', 1.10000002384185791, 'E', NULL, NULL),
     ('08MG026', 1994, 12, 1, 31, 1.34000003337860107, 41.38800048828125, 31, 0.870000004768371582, 20, 3.01999998092651367, 1.40999996662139893, NULL, 1.24000000953674316, NULL, 0.954999983310699574, NULL, 0.945999979972839355, NULL, 1.00999999046325684, NULL, 1.04999995231628418, NULL, 1.05999994277954102, NULL, 1.12000000476837158, NULL, 1.04999995231628418, NULL, 1.03999996185302712, NULL, 1.02999997138977051, NULL, 0.986999988555908203, NULL, 0.96700000762939442, NULL, 0.977999985218047985, NULL, 0.980000019073486439, NULL, 0.995000004768371582, NULL, 1.45000004768371582, NULL, 1.75, NULL, 2.18000006675720215, NULL, 3.01999998092651367, NULL, 2.34999990463256836, NULL, 2.04999995231628418, NULL, 1.85000002384185791, NULL, 1.70000004768371582, NULL, 1.60000002384185791, NULL, 1.53999996185302712, NULL, 1.51999998092651367, 'B', 0.920000016689300426, 'B', 0.889999985694885254, 'B', 0.879999995231628418, 'B', 0.870000004768371582, 'B'),
     ('08MG026', 1995, 1, 1, 31, 1.05999994277954102, 32.7099990844726562, 27, 0.828999996185302734, 29, 2.6400001049041748, 1.02999997138977051, NULL, 1.00999999046325684, NULL, 1.00999999046325684, NULL, 0.980000019073486439, NULL, 0.941999971866607555, NULL, 0.912999987602233998, NULL, 0.939000010490417591, NULL, 0.959999978542327992, NULL, 1.00999999046325684, NULL, 1.09000003337860107, NULL, 1.01999998092651367, NULL, 0.987999975681304821, NULL, 0.962000012397766002, NULL, 0.944000005722046009, NULL, 0.944000005722046009, NULL, 0.939999997615814209, NULL, 0.939000010490417591, NULL, 0.96399998664855957, NULL, 0.927999973297119252, NULL, 0.91100001335144043, NULL, 0.885999977588653564, NULL, 0.865999996662139893, NULL, 0.847000002861022949, NULL, 0.851000010967254639, NULL, 0.836000025272369385, NULL, 0.843999981880187988, NULL, 0.828999996185302734, NULL, 0.847000002861022949, NULL, 2.6400001049041748, NULL, 1.90999996662139893, NULL, 1.92999994754791282, NULL),
     ('08MG026', 1995, 2, 1, 28, 1.71000003814697288, 47.8089981079101634, 13, 0.772000014781951904, 21, 3.67000007629394487, 2.38000011444091797, NULL, 1.95000004768371604, NULL, 1.73000001907348633, NULL, 1.5700000524520874, NULL, 1.45000004768371582, NULL, 1.54999995231628418, NULL, 1.53999996185302712, NULL, 1.41999995708465576, NULL, 1.28999996185302712, NULL, 1.20000004768371582, NULL, 1.11000001430511475, NULL, 0.885999977588653564, NULL, 0.772000014781951904, NULL, 0.887000024318695068, NULL, 0.973999977111816406, NULL, 1.0700000524520874, NULL, 1.14999997615814209, NULL, 1.09000003337860107, NULL, 1.0700000524520874, NULL, 2.72000002861022905, NULL, 3.67000007629394487, NULL, 3.1400001049041748, NULL, 2.25999999046325684, NULL, 2.29999995231628418, NULL, 2.24000000953674316, NULL, 2.20000004768371582, NULL, 2.11999988555908203, NULL, 2.06999993324279785, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1995, 3, 1, 31, 2.06999993324279785, 64.0500030517578125, 7, 1.91999995708465598, 31, 2.24000000953674316, 2.00999999046325684, NULL, 1.99000000953674316, NULL, 1.97000002861022927, NULL, 1.95000004768371604, NULL, 1.94000005722045898, NULL, 1.92999994754791282, NULL, 1.91999995708465598, NULL, 1.91999995708465598, NULL, 2.07999992370605469, NULL, 2.21000003814697266, NULL, 2.07999992370605469, NULL, 2.04999995231628418, NULL, 2, NULL, 2.11999988555908203, NULL, 2.11999988555908203, NULL, 2.02999997138977051, NULL, 2, NULL, 2.01999998092651367, NULL, 2.09999990463256836, NULL, 2.18000006675720215, NULL, 2.18000006675720215, NULL, 2.13000011444091797, NULL, 2.1099998950958252, NULL, 2.08999991416931152, NULL, 2.06999993324279785, NULL, 2.07999992370605469, NULL, 2.08999991416931152, NULL, 2.09999990463256836, NULL, 2.15000009536743208, NULL, 2.19000005722045898, NULL, 2.24000000953674316, NULL),
     ('08MG026', 1995, 4, 1, 30, 2.3900001049041748, 71.5500030517578125, 19, 2.07999992370605469, 30, 4.01000022888183594, 2.24000000953674316, NULL, 2.24000000953674316, NULL, 2.20000004768371582, NULL, 2.40000009536743208, NULL, 2.31999993324279785, NULL, 2.24000000953674316, NULL, 2.40000009536743208, NULL, 2.3599998950958252, NULL, 2.26999998092651367, NULL, 2.15000009536743208, NULL, 2.1099998950958252, NULL, 2.09999990463256836, NULL, 2.1099998950958252, NULL, 2.09999990463256836, NULL, 2.1099998950958252, NULL, 2.09999990463256836, NULL, 2.08999991416931152, NULL, 2.08999991416931152, NULL, 2.07999992370605469, NULL, 2.07999992370605469, NULL, 2.21000003814697266, NULL, 2.16000008583068848, NULL, 2.21000003814697266, NULL, 2.3599998950958252, NULL, 2.53999996185302779, NULL, 2.70000004768371582, NULL, 2.86999988555908203, NULL, 3.29999995231628418, NULL, 3.40000009536743208, NULL, 4.01000022888183594, NULL, NULL, NULL),
     ('08MG026', 1995, 5, 1, 31, 6.3600001335144043, 197.100006103515597, 5, 3.81999993324279785, 30, 11.1999998092651367, 3.98000001907348633, NULL, 4.19999980926513672, NULL, 4.09000015258789062, NULL, 3.84999990463256792, NULL, 3.81999993324279785, NULL, 4.03999996185302734, NULL, 4.36999988555908203, NULL, 5.01000022888183594, NULL, 5.71000003814697266, NULL, 6.61999988555908203, NULL, 5.78000020980834961, NULL, 5.32000017166137695, NULL, 5.57999992370605469, NULL, 6.69000005722045898, NULL, 6.44999980926513672, 'E', 6.30000019073486328, 'E', 6.19999980926513672, 'E', 6.09999990463256836, 'E', 6.03999996185302734, NULL, 5.98000001907348633, NULL, 5.94000005722045898, NULL, 6.05999994277954102, NULL, 6.34000015258789062, NULL, 6.86999988555908203, NULL, 7.51000022888183594, NULL, 8.84000015258789062, NULL, 9.11999988555908203, NULL, 9.22000026702880859, NULL, 9.06999969482422053, NULL, 11.1999998092651367, NULL, 10.8000001907348633, NULL),
     ('08MG026', 1995, 6, 1, 30, 9.71000003814697266, 291.420013427734375, 7, 7.25, 30, 12.1999998092651367, 9.96000003814697266, NULL, 10.5, NULL, 10.6999998092651367, NULL, 8.93000030517578125, NULL, 8.21000003814697266, NULL, 7.26999998092651367, NULL, 7.25, NULL, 8.22999954223632812, NULL, 10.1000003814697283, NULL, 10.6999998092651367, NULL, 10.8000001907348633, NULL, 9.60000038146972834, NULL, 9.07999992370605646, NULL, 8.31999969482421875, NULL, 8.27999973297119141, NULL, 8.93000030517578125, NULL, 9.35000038146972834, NULL, 8.89999961853027344, NULL, 8.30000019073486328, NULL, 8.72000026702880859, NULL, 10.1000003814697283, NULL, 10.1999998092651367, NULL, 9.78999996185302734, NULL, 10.8000001907348633, NULL, 11.1000003814697283, NULL, 11.1999998092651367, NULL, 10.8999996185302717, NULL, 11.1000003814697283, NULL, 11.8999996185302717, NULL, 12.1999998092651367, NULL, NULL, NULL),
     ('08MG026', 1995, 7, 1, 31, 9.43000030517577947, 292.3599853515625, 30, 6.86999988555908203, 26, 15, 11.3999996185302717, NULL, 11.5, NULL, 10.6000003814697283, NULL, 8.72000026702880859, NULL, 7.57000017166137695, NULL, 7.53999996185302734, NULL, 7.48999977111816406, NULL, 7.46000003814697266, NULL, 8.21000003814697266, NULL, 13.5, NULL, 9.68999958038330078, NULL, 8.76000022888183594, NULL, 8.55000019073486328, NULL, 8.31000041961669922, NULL, 8.69999980926513672, NULL, 9.42000007629394354, NULL, 9.86999988555908203, NULL, 10.3000001907348633, NULL, 11, NULL, 11.6999998092651367, NULL, 10.1000003814697283, NULL, 9.64999961853027166, NULL, 9.35000038146972834, NULL, 8.60000038146972656, NULL, 9.90999984741210938, NULL, 15, NULL, 9.71000003814697266, NULL, 8.35999965667724609, NULL, 7.55999994277954102, NULL, 6.86999988555908203, NULL, 6.96000003814697266, NULL),
     ('08MG026', 1995, 8, 1, 31, 6.44999980926513672, 199.919998168945312, 27, 4.80999994277954102, 5, 8.88000011444091797, 7.69000005722045898, NULL, 7.46000003814697266, NULL, 8.15999984741210938, NULL, 8.52000045776367188, NULL, 8.88000011444091797, NULL, 8.80000019073486328, NULL, 8.73999977111816406, NULL, 7.11999988555908203, NULL, 6.61999988555908203, NULL, 7.03000020980834961, NULL, 7.90000009536743164, NULL, 7.28999996185302734, NULL, 6.28000020980834961, NULL, 6.63000011444091797, NULL, 7.21000003814697266, NULL, 6.07999992370605469, NULL, 5.6100001335144043, NULL, 5.44999980926513672, NULL, 5.69999980926513672, NULL, 5.61999988555908203, NULL, 5.78999996185302734, NULL, 5.98000001907348633, NULL, 5.6399998664855957, NULL, 5.23000001907348633, NULL, 5.05999994277954102, NULL, 4.92000007629394531, NULL, 4.80999994277954102, NULL, 4.84999990463256836, NULL, 4.88000011444091797, NULL, 4.98999977111816406, NULL, 4.98000001907348633, NULL),
     ('08MG026', 1995, 9, 1, 30, 5.34000015258789062, 160.110000610351562, 24, 4, 4, 6.53999996185302734, 5.05000019073486328, NULL, 5.15999984741210938, NULL, 5.13000011444091797, NULL, 6.53999996185302734, NULL, 6.1399998664855957, NULL, 5.88000011444091797, NULL, 5.80000019073486328, NULL, 5.80000019073486328, NULL, 5.94000005722045898, NULL, 5.78000020980834961, NULL, 5.6100001335144043, NULL, 5.76000022888183594, NULL, 5.92000007629394531, NULL, 6.03999996185302734, NULL, 6.05000019073486328, NULL, 5.98000001907348633, NULL, 5.96999979019165039, 'A', 5.90999984741210938, 'E', 5.80000019073486328, 'E', 5.30000019073486328, 'E', 4.80000019073486328, 'E', 4.40000009536743164, 'E', 4.19999980926513672, 'E', 4, 'E', 4, 'E', 4.30000019073486328, 'E', 4.90000009536743164, 'E', 5.09999990463256836, 'E', 4.59999990463256836, 'E', 4.25, 'E', NULL, NULL),
     ('08MG026', 1995, 10, 1, 31, 3.3900001049041748, 104.940002441406236, 31, 1.61000001430511475, 16, 7.30000019073486328, 3.95000004768371582, 'E', 3.59999990463256836, 'E', 3.20000004768371582, 'E', 2.70000004768371582, 'E', 2.5, 'E', 2.38000011444091797, 'E', 2.28999996185302779, 'E', 2.25999999046325684, 'E', 2.59999990463256836, 'E', 3.59999990463256836, 'E', 3.70000004768371582, 'E', 3.5, 'E', 3.29999995231628418, 'E', 4.19999980926513672, 'E', 5.80000019073486328, 'E', 7.30000019073486328, 'E', 7, 'E', 5.5, 'E', 4.59999990463256836, 'E', 4.19999980926513672, 'E', 3.79999995231628418, 'E', 3.29999995231628418, 'E', 2.90000009536743208, 'E', 2.75, 'E', 2.65000009536743208, 'E', 2.40000009536743208, 'E', 2.09999990463256836, 'E', 1.85000002384185791, 'E', 1.72000002861022949, 'E', 1.6799999475479126, 'E', 1.61000001430511475, 'E'),
     ('08MG026', 1995, 11, 1, 30, 5.44000005722045898, 163.1199951171875, 5, 1.53999996185302712, 29, 13, 1.60000002384185791, 'E', 1.58000004291534424, 'E', 1.5700000524520874, 'E', 1.54999995231628418, 'E', 1.53999996185302712, 'E', 1.59000003337860107, 'E', 3.70000004768371582, 'E', 5.5, 'E', 9, 'E', 8, 'E', 7, 'E', 6, 'E', 5.40000009536743164, 'E', 6.19999980926513672, 'E', 7, 'E', 6.32000017166137695, 'A', 5.80000019073486328, 'E', 5.30000019073486328, 'E', 4.80000019073486328, 'A', 6.5, NULL, 4.21999979019165039, NULL, 4.07999992370605469, NULL, 8.93999958038330078, NULL, 6.40999984741210938, NULL, 7.44000005722045898, NULL, 5.84999990463256836, NULL, 5.25, NULL, 5.98000001907348633, NULL, 13, NULL, 6, NULL, NULL, NULL),
     ('08MG026', 1995, 12, 1, 31, 2.83999991416931152, 87.970001220703125, 31, 1.89999997615814209, 1, 5.25, 5.25, NULL, 4.26999998092651367, NULL, 4.01000022888183594, NULL, 2.97000002861022905, NULL, 2.23000001907348633, NULL, 2.36999988555908203, 'A', 2.40000009536743208, 'E', 2.70000004768371582, 'E', 2.95000004768371582, 'E', 3.04999995231628418, 'E', 3.5, 'E', 4.05000019073486328, 'E', 3.90000009536743208, 'E', 3.65000009536743208, 'E', 3.48000001907348633, 'E', 3.29999995231628418, 'E', 3, 'E', 2.79999995231628418, 'E', 2.65000009536743208, 'E', 2.54999995231628418, 'E', 2.45000004768371582, 'E', 2.29999995231628418, 'E', 2.15000009536743208, 'E', 2.09999990463256836, 'E', 2.07999992370605469, 'E', 2.03999996185302779, 'E', 2, 'E', 1.97000002861022927, 'E', 1.96000003814697288, 'E', 1.94000005722045898, 'E', 1.89999997615814209, 'E'),
     ('08MG026', 1997, 1, 1, 31, 1.16999995708465576, 36.3680000305175781, 16, 0.953000009059906006, 30, 1.54999995231628418, 1.46000003814697288, 'E', 1.39999997615814209, 'E', 1.35000002384185791, 'E', 1.29999995231628418, 'E', 1.25, 'E', 1.20000004768371582, 'E', 1.1799999475479126, 'E', 1.12999999523162842, 'E', 1.10000002384185791, 'E', 1.08000004291534424, 'E', 1.04999995231628418, 'E', 1.01999998092651367, 'E', 1, 'E', 0.980000019073486439, NULL, 0.954999983310699574, NULL, 0.953000009059906006, NULL, 1, NULL, 1, NULL, 1.40999996662139893, NULL, 1.47000002861022949, NULL, 1.28999996185302712, NULL, 1.23000001907348633, NULL, 1.19000005722045898, NULL, 1.14999997615814209, 'B', 1.12999999523162842, 'B', 1.10000002384185791, 'B', 1.08000004291534424, 'B', 1.05999994277954102, 'B', 1.11000001430511475, NULL, 1.54999995231628418, NULL, 1.19000005722045898, NULL),
     ('08MG026', 1997, 2, 1, 28, 1.00999999046325684, 28.3710002899169922, 12, 0.870000004768371582, 1, 1.14999997615814209, 1.14999997615814209, NULL, 1.12000000476837158, NULL, 1.08000004291534424, NULL, 1.01999998092651367, 'A', 0.959999978542327992, 'E', 0.949999988079071045, 'E', 0.930000007152557373, 'E', 0.91000002622604359, 'E', 0.89999997615814209, 'E', 0.889999985694885254, 'E', 0.879999995231628418, 'E', 0.870000004768371582, 'E', 0.953000009059906006, NULL, 0.948000013828277588, NULL, 1.00999999046325684, NULL, 1.01999998092651367, NULL, 1.08000004291534424, NULL, 1.05999994277954102, NULL, 1.0700000524520874, NULL, 1.05999994277954102, NULL, 1.04999995231628418, NULL, 1.04999995231628418, 'A', 1.04999995231628418, 'E', 1.04999995231628418, NULL, 1.0700000524520874, NULL, 1.08000004291534424, NULL, 1.08000004291534424, NULL, 1.08000004291534424, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1997, 3, 1, 31, 1.60000002384185791, 49.6699981689453125, 14, 1.05999994277954102, 19, 3.40000009536743208, 1.11000001430511475, NULL, 1.12000000476837158, NULL, 1.09000003337860107, NULL, 1.08000004291534424, NULL, 1.10000002384185791, NULL, 1.12000000476837158, 'A', 1.12999999523162842, 'E', 1.12000000476837158, 'E', 1.10000002384185791, 'E', 1.11000001430511475, 'E', 1.12000000476837158, 'E', 1.11000001430511475, 'E', 1.0700000524520874, 'A', 1.05999994277954102, NULL, 1.09000003337860107, NULL, 1.09000003337860107, NULL, 1.11000001430511475, NULL, 1.5700000524520874, NULL, 3.40000009536743208, NULL, 3.27999997138977051, NULL, 2.90000009536743208, NULL, 2.57999992370605469, NULL, 2.23000001907348633, NULL, 2.00999999046325684, NULL, 1.99000000953674316, NULL, 1.98000001907348633, NULL, 1.87000000476837203, NULL, 1.79999995231628418, NULL, 1.77999997138977051, NULL, 1.78999996185302712, NULL, 1.75999999046325684, NULL),
     ('08MG026', 1997, 4, 1, 30, 3.01999998092651367, 90.5599975585937642, 5, 1.62999999523162842, 16, 7.48999977111816406, 1.72000002861022949, NULL, 1.69000005722045898, NULL, 1.69000005722045898, NULL, 1.64999997615814209, NULL, 1.62999999523162842, NULL, 1.64999997615814209, NULL, 1.6799999475479126, NULL, 1.73000001907348633, NULL, 1.77999997138977051, NULL, 1.84000003337860107, NULL, 1.89999997615814209, NULL, 1.91999995708465598, NULL, 1.98000001907348633, NULL, 1.98000001907348633, NULL, 2.22000002861022905, NULL, 7.48999977111816406, NULL, 5.23000001907348633, NULL, 3.63000011444091797, NULL, 3.22000002861022905, NULL, 3.21000003814697266, NULL, 3.06999993324279785, NULL, 2.99000000953674316, NULL, 3.05999994277954102, NULL, 3.02999997138977051, NULL, 3.15000009536743208, NULL, 4.48000001907348633, NULL, 7.1399998664855957, NULL, 5.11999988555908203, NULL, 4.55000019073486328, 'A', 4.13000011444091797, 'A', NULL, NULL),
     ('08MG026', 1997, 5, 1, 31, 7.42999982833862305, 230.330001831054688, 4, 3.6400001049041748, 31, 15, 3.82999992370605513, NULL, 3.69000005722045898, NULL, 3.67000007629394487, NULL, 3.6400001049041748, 'A', 4, 'E', 5, 'E', 4.09999990463256836, 'E', 3.79999995231628418, 'E', 4.59999990463256836, 'E', 5.59999990463256836, 'E', 6.69999980926513672, 'E', 8, 'E', 9.5, 'E', 11, 'E', 13, 'E', 10.5, 'E', 8.30000019073486328, 'E', 6.5, 'E', 7, 'E', 7.30000019073486328, 'E', 6.5, 'E', 5.59999990463256836, 'E', 5, 'E', 6, 'E', 7.5, 'E', 9, 'E', 8.5, 'E', 10, 'A', 13.5, NULL, 14, NULL, 15, NULL),
     ('08MG026', 1997, 6, 1, 30, 8.15999984741210938, 244.839996337890653, 9, 4.78999996185302734, 17, 13.3999996185302717, 7.82999992370605469, NULL, 6.55999994277954102, NULL, 6.96999979019165039, NULL, 8.68000030517578125, NULL, 6.48999977111816406, NULL, 5.23000001907348633, NULL, 5.3899998664855957, NULL, 4.98000001907348633, NULL, 4.78999996185302734, NULL, 6.26999998092651367, NULL, 6.32999992370605469, NULL, 6.53000020980834961, NULL, 7.51999998092651367, NULL, 9.18999958038330078, NULL, 9.52999973297119141, NULL, 9.48999977111816406, NULL, 13.3999996185302717, NULL, 11.1999998092651367, NULL, 13.3999996185302717, NULL, 8.84000015258789062, NULL, 8.65999984741210938, NULL, 9.81999969482422053, NULL, 8.18000030517578125, NULL, 7.88000011444091797, NULL, 9.03999996185302734, NULL, 9.31000041961669922, NULL, 8.65999984741210938, NULL, 8.53999996185302734, NULL, 8.52000045776367188, NULL, 7.6100001335144043, 'A', NULL, NULL),
     ('08MG026', 1997, 7, 1, 31, 8.5, 263.3599853515625, 31, 6.30000019073486328, 8, 16.7000007629394531, 8.47999954223632812, NULL, 8.63000011444091797, 'A', 8.43999958038330078, NULL, 9.27999973297119141, 'A', 14.8000001907348633, NULL, 13, NULL, 10.6999998092651367, NULL, 16.7000007629394531, NULL, 10.6000003814697283, NULL, 7.6399998664855957, NULL, 7.01999998092651367, NULL, 7.11999988555908203, NULL, 7.28000020980834961, NULL, 7.71999979019165039, NULL, 7.6399998664855957, NULL, 7.32999992370605469, NULL, 7.5, 'A', 7.55999994277954102, 'A', 7.76000022888183594, NULL, 9.93000030517577947, 'A', 8.82999992370605469, 'A', 8.11999988555908203, 'A', 7.55999994277954102, NULL, 6.94000005722045898, NULL, 6.73000001907348633, NULL, 6.36999988555908203, NULL, 6.48999977111816406, NULL, 6.75, NULL, 7.26999998092651367, NULL, 6.86999988555908203, NULL, 6.30000019073486328, NULL),
     ('08MG026', 1997, 8, 1, 31, 5.96999979019165039, 185.080001831054688, 31, 3.40000009536743208, 14, 8.69999980926513672, 6.03999996185302734, NULL, 5.92999982833862305, NULL, 5.67999982833862305, NULL, 6.07000017166137695, NULL, 6.1399998664855957, NULL, 6.40000009536743164, NULL, 7.07999992370605469, NULL, 6.34000015258789062, 'A', 6.19999980926513672, 'E', 6, 'E', 6.40000009536743164, 'E', 7, 'E', 8, 'E', 8.69999980926513672, 'E', 8.5, 'E', 7.5, 'E', 6, 'E', 5, 'E', 4.59999990463256836, 'E', 4.90000009536743164, 'E', 5.46999979019165039, 'A', 4.71999979019165039, 'A', 4.53000020980834961, NULL, 4.15999984741210938, NULL, 4.26000022888183594, NULL, 5.71000003814697266, NULL, 8.17000007629394531, NULL, 6.34999990463256836, 'A', 5.23000001907348633, 'A', 4.59999990463256836, 'E', 3.40000009536743208, 'E'),
     ('08MG026', 1997, 9, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 3.79999995231628418, 'E', 4.19999980926513672, 'E', 4.61999988555908203, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1997, 11, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 12.1999998092651367, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1998, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1.54999995231628418, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1998, 4, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1.44000005722045898, 'A', 1.51999998092651367, NULL, 1.94000005722045898, NULL, 2.04999995231628418, NULL, 1.83000004291534402, NULL, 1.71000003814697288, NULL, 1.85000002384185791, NULL, 2.22000002861022905, NULL, 2.48000001907348633, NULL, 2.90000009536743208, NULL, NULL, NULL),
     ('08MG026', 1998, 5, 1, 31, 6.34000015258789062, 196.460006713867188, 1, 4, 31, 10.8000001907348633, 4, NULL, 4.88000011444091797, NULL, 5.71000003814697266, NULL, 6.03999996185302734, NULL, 6.28000020980834961, NULL, 6.30999994277954102, NULL, 6.53000020980834961, NULL, 6.19999980926513672, NULL, 5.67000007629394531, NULL, 5.94000005722045898, NULL, 6.15000009536743164, NULL, 6.34999990463256836, NULL, 6.76000022888183594, NULL, 6.07999992370605469, NULL, 5.3600001335144043, NULL, 4.98000001907348633, NULL, 4.94999980926513672, NULL, 5.07000017166137695, NULL, 5.30000019073486328, NULL, 5.57000017166137695, NULL, 6.07000017166137695, NULL, 6.59999990463256836, NULL, 6.53000020980834961, NULL, 6.57999992370605469, NULL, 6.96000003814697266, NULL, 6.46000003814697266, NULL, 7.76999998092651367, NULL, 7.61999988555908203, NULL, 8.02999973297119141, NULL, 8.90999984741210938, NULL, 10.8000001907348633, NULL),
     ('08MG026', 1998, 6, 1, 30, 12.1999998092651367, 365.399993896484375, 7, 10.8000001907348633, 13, 14.3999996185302717, 11.3000001907348633, NULL, 11.6000003814697283, NULL, 11.3000001907348633, NULL, 11.3000001907348633, NULL, 11.6000003814697283, NULL, 11.6000003814697283, NULL, 10.8000001907348633, NULL, 12, NULL, 13.6000003814697283, 'A', 13.3000001907348633, NULL, 13.5, NULL, 13.3999996185302717, NULL, 14.3999996185302717, NULL, 13.6999998092651367, NULL, 12.8999996185302717, NULL, 12, NULL, 11.8999996185302717, NULL, 11.3000001907348633, NULL, 10.8999996185302717, NULL, 11.3000001907348633, NULL, 11.5, NULL, 12.3000001907348633, NULL, 13, NULL, 13.3000001907348633, NULL, 12.6000003814697283, NULL, 12, NULL, 11.6999998092651367, NULL, 11.6999998092651367, NULL, 11.8000001907348633, NULL, 11.8000001907348633, NULL, NULL, NULL),
     ('08MG026', 1998, 7, 1, 31, 10, 311.489990234375, 24, 7.8899998664855957, 5, 12.6999998092651367, 12.6000003814697283, NULL, 12.6000003814697283, NULL, 12, NULL, 12.3000001907348633, NULL, 12.6999998092651367, NULL, 11.8999996185302717, NULL, 11.1000003814697283, NULL, 10.5, NULL, 10.3000001907348633, NULL, 9.94999980926513672, NULL, 9.60999965667724609, NULL, 9.22999954223632812, NULL, 8.80000019073486328, NULL, 8.10999965667724609, NULL, 8.75, NULL, 10.3000001907348633, NULL, 11, NULL, 9.97999954223632812, NULL, 9.10000038146972834, NULL, 8.47000026702880859, NULL, 8.28999996185302734, NULL, 8.60000038146972656, NULL, 8.64999961853027344, NULL, 7.8899998664855957, NULL, 8.15999984741210938, NULL, 9, NULL, 10.5, NULL, 11.1000003814697283, NULL, 11.3999996185302717, NULL, 9.30000019073486328, NULL, 9.30000019073486328, NULL),
     ('08MG026', 1998, 8, 1, 31, 6.71999979019165039, 208.289993286132812, 17, 4.17000007629394531, 29, 10.1000003814697283, 8.46000003814697266, NULL, 7.8600001335144043, NULL, 7.34000015258789062, NULL, 6.59000015258789062, NULL, 6.21000003814697266, NULL, 5.8899998664855957, NULL, 5.67999982833862305, NULL, 5.63000011444091797, NULL, 5.57000017166137695, NULL, 5.75, NULL, 5.57000017166137695, NULL, 5.88000011444091797, NULL, 6.01000022888183594, NULL, 5.94000005722045898, NULL, 4.90999984741210938, NULL, 4.65999984741210938, NULL, 4.17000007629394531, NULL, 4.32000017166137695, NULL, 5.36999988555908203, NULL, 5.90999984741210938, NULL, 6.09000015258789062, NULL, 6.38000011444091797, NULL, 9.42000007629394354, NULL, 9.36999988555908203, NULL, 8.69999980926513672, NULL, 6.76999998092651367, NULL, 7.46000003814697266, NULL, 8.68000030517578125, NULL, 10.1000003814697283, NULL, 8.72999954223632812, NULL, 8.86999988555908203, NULL),
     ('08MG026', 1998, 9, 1, 30, 6.92000007629394531, 207.720001220703125, 29, 3.95000004768371582, 7, 9.21000003814697266, 9.01000022888183594, NULL, 7.65999984741210938, NULL, 7.51999998092651367, NULL, 9.10999965667724609, NULL, 8.69999980926513672, NULL, 8.68000030517578125, NULL, 9.21000003814697266, NULL, 8.5, NULL, 7.5, NULL, 7.07000017166137695, NULL, 8.01000022888183594, NULL, 7.65000009536743164, NULL, 8.52999973297119141, NULL, 7.61999988555908203, NULL, 7.44000005722045898, NULL, 7.65999984741210938, NULL, 7.80999994277954102, NULL, 6.98999977111816406, NULL, 6.65999984741210938, NULL, 6, NULL, 5.92000007629394531, NULL, 5.78000020980834961, NULL, 5.46000003814697266, NULL, 5.90000009536743164, NULL, 5.86999988555908203, NULL, 4.44000005722045898, NULL, 4.59000015258789062, NULL, 4.30999994277954102, NULL, 3.95000004768371582, NULL, 4.17000007629394531, NULL, NULL, NULL),
     ('08MG026', 1998, 10, 1, 31, 2.77999997138977051, 86.160003662109375, 23, 1.71000003814697288, 2, 5.8899998664855957, 5.15999984741210938, NULL, 5.8899998664855957, NULL, 4.07000017166137695, NULL, 3.3900001049041748, NULL, 3.22000002861022905, NULL, 3.84999990463256792, NULL, 3.72000002861022949, NULL, 4.15999984741210938, NULL, 3.48000001907348633, NULL, 2.74000000953674316, NULL, 2.32999992370605469, NULL, 3.31999993324279785, NULL, 3.16000008583068848, NULL, 2.70000004768371582, NULL, 2.11999988555908203, NULL, 1.97000002861022927, NULL, 2.71000003814697266, NULL, 2.26999998092651367, NULL, 1.91999995708465598, NULL, 1.83000004291534402, NULL, 1.86000001430511475, NULL, 1.82000005245208762, NULL, 1.71000003814697288, NULL, 1.74000000953674316, NULL, 1.71000003814697288, NULL, 1.87999999523162842, NULL, 2.78999996185302779, NULL, 2.94000005722045898, NULL, 2.06999993324279785, NULL, 1.80999994277954102, NULL, 1.82000005245208762, NULL),
     ('08MG026', 1998, 11, 1, 30, 1.64999997615814209, 49.5449981689453125, 11, 0.919000029563903809, 16, 4.57999992370605469, 1.59000003337860107, NULL, 1.45000004768371582, NULL, 1.37000000476837158, NULL, 1.38999998569488525, NULL, 1.25999999046325684, NULL, 1.14999997615814209, NULL, 1.11000001430511475, NULL, 1.08000004291534424, NULL, 1.09000003337860107, NULL, 1.00999999046325684, NULL, 0.919000029563903809, NULL, 1.29999995231628418, NULL, 3.83999991416931197, NULL, 3.16000008583068848, NULL, 3.88000011444091797, NULL, 4.57999992370605469, NULL, 3.13000011444091797, NULL, 2.3599998950958252, NULL, 1.76999998092651367, 'A', 1.30999994277954102, NULL, 1.23000001907348633, NULL, 1.09000003337860107, NULL, 1.11000001430511475, NULL, 1.08000004291534424, NULL, 1.11000001430511475, NULL, 1.12999999523162842, NULL, 1.05999994277954102, NULL, 1.03999996185302712, NULL, 0.970000028610229603, NULL, 0.976000010967254639, NULL, NULL, NULL),
     ('08MG026', 1998, 12, 1, 31, 0.926999986171722412, 28.7290000915527308, 23, 0.730000019073486328, 17, 1.13999998569488525, 0.972999989986419567, NULL, 0.978999972343444824, NULL, 0.944000005722046009, NULL, 0.897000014781951904, NULL, 0.978999972343444824, NULL, 0.930999994277953991, NULL, 0.949000000953674427, NULL, 0.929000020027160645, NULL, 0.984000027179718018, NULL, 1.02999997138977051, NULL, 1.09000003337860107, NULL, 1.10000002384185791, NULL, 1.08000004291534424, NULL, 0.986000001430511586, NULL, 0.96499997377395641, NULL, 1.04999995231628418, NULL, 1.13999998569488525, NULL, 0.862999975681304932, 'B', 0.819999992847442627, 'B', 0.769999980926513672, 'B', 0.75, 'B', 0.740000009536743164, 'B', 0.730000019073486328, 'B', 0.740000009536743164, 'B', 0.829999983310699463, 'B', 0.870000004768371582, 'B', 0.829999983310699463, 'B', 0.819999992847442627, 'B', 0.800000011920928955, 'B', 1.04999995231628418, 'B', 1.11000001430511475, NULL),
     ('08MG026', 1999, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1.41999995708465576, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 1999, 4, 1, 30, 2.67000007629394531, 80.1100006103515625, 9, 1.4299999475479126, 25, 7.05000019073486328, 1.5, NULL, 1.48000001907348633, NULL, 1.47000002861022949, NULL, 1.46000003814697288, NULL, 1.45000004768371582, NULL, 1.44000005722045898, NULL, 1.47000002861022949, NULL, 1.45000004768371582, NULL, 1.4299999475479126, NULL, 1.4299999475479126, NULL, 1.47000002861022949, NULL, 1.60000002384185791, NULL, 1.48000001907348633, NULL, 1.5, NULL, 1.65999996662139893, NULL, 1.80999994277954102, NULL, 2.21000003814697266, NULL, 3.72000002861022949, NULL, 4.09999990463256836, NULL, 3.6400001049041748, NULL, 3.54999995231628418, NULL, 3.30999994277954102, NULL, 3.26999998092651367, NULL, 4.23999977111816406, NULL, 7.05000019073486328, NULL, 6.13000011444091797, NULL, 4.46000003814697266, NULL, 3.65000009536743208, NULL, 3.27999997138977051, NULL, 3.40000009536743208, NULL, NULL, NULL),
     ('08MG026', 1999, 5, 1, 31, 3.91000008583068892, 121.309997558593764, 5, 2.20000004768371582, 25, 9, 3.5, NULL, 3.26999998092651367, NULL, 2.93000006675720215, NULL, 2.5, NULL, 2.20000004768371582, NULL, 2.79999995231628418, NULL, 3.57999992370605469, NULL, 2.76999998092651367, NULL, 2.3900001049041748, NULL, 2.32999992370605469, NULL, 2.3599998950958252, NULL, 2.31999993324279785, NULL, 2.31999993324279785, NULL, 2.40000009536743208, NULL, 2.76999998092651367, NULL, 3.49000000953674316, 'A', 3.41000008583068848, NULL, 3.6400001049041748, NULL, 4.07000017166137695, 'A', 3.73000001907348633, 'A', 3.82999992370605513, 'E', 4.5, 'E', 5.59999990463256836, 'E', 7, 'E', 9, 'E', 7.5, 'E', 6, 'E', 5.19999980926513672, 'E', 4.69999980926513672, 'E', 4.40000009536743164, 'E', 4.80000019073486328, 'E'),
     ('08MG026', 1999, 6, 1, 30, 8.71000003814697266, 261.20001220703125, 8, 3.79999995231628418, 16, 26, 6.5, 'E', 5, 'E', 5.80000019073486328, 'E', 7, 'E', 8, 'E', 6.80000019073486328, 'E', 5.40000009536743164, 'E', 3.79999995231628418, 'E', 4, 'E', 4.80000019073486328, 'E', 5.80000019073486328, 'E', 7.30000019073486328, 'E', 9, 'E', 11, 'E', 16, 'E', 26, 'E', 23, 'E', 13.8999996185302717, 'A', 11, NULL, 8.73999977111816406, NULL, 8.22000026702880859, NULL, 8, NULL, 7.57000017166137695, NULL, 7.57000017166137695, NULL, 8.14000034332275391, NULL, 7.98000001907348633, NULL, 7.03000020980834961, NULL, 6.25, NULL, 5.6100001335144043, NULL, 5.98999977111816406, NULL, NULL, NULL),
     ('08MG026', 1999, 7, 1, 31, 9.96000003814697266, 308.8599853515625, 4, 4.40999984741210938, 14, 15.1000003814697283, 6.88000011444091797, NULL, 6.65000009536743164, NULL, 5.94000005722045898, NULL, 4.40999984741210938, NULL, 4.6100001335144043, NULL, 6.44000005722045898, NULL, 8.56000041961669922, NULL, 7.67999982833862305, NULL, 7.96000003814697266, NULL, 9.18000030517577947, NULL, 11.1999998092651367, NULL, 13.1000003814697283, NULL, 14.6999998092651367, 'A', 15.1000003814697283, NULL, 13.5, NULL, 12.8999996185302717, NULL, 10.8000001907348633, NULL, 9.28999996185302734, NULL, 9.36999988555908203, NULL, 9.21000003814697266, NULL, 9.34000015258789062, NULL, 9.40999984741210938, NULL, 9.35999965667724609, NULL, 10.6999998092651367, NULL, 11.6999998092651367, NULL, 11, NULL, 11.8999996185302717, NULL, 11.8999996185302717, NULL, 9.06999969482422053, NULL, 13.1999998092651367, NULL, 13.8000001907348633, NULL),
     ('08MG026', 1999, 8, 1, 31, 13.5, 417.1199951171875, 17, 9.92000007629394354, 25, 18, 12.8999996185302717, NULL, 13.1999998092651367, NULL, 14.8000001907348633, NULL, 14.8999996185302717, NULL, 17.2000007629394531, NULL, 15.6999998092651367, NULL, 15, NULL, 14.8000001907348633, NULL, 14.6999998092651367, NULL, 14, NULL, 13.3000001907348633, NULL, 12.6999998092651367, NULL, 11.8000001907348633, NULL, 11.1000003814697283, NULL, 10.8000001907348633, NULL, 10.6000003814697283, NULL, 9.92000007629394354, NULL, 10.5, NULL, 16.2000007629394531, NULL, 15.8000001907348633, NULL, 15.8000001907348633, NULL, 13.8000001907348633, NULL, 14.3000001907348633, NULL, 13.8999996185302717, NULL, 18, NULL, 13.3999996185302717, NULL, 12.8000001907348633, NULL, 12.1999998092651367, NULL, 11.3000001907348633, NULL, 10.6999998092651367, NULL, 11, NULL),
     ('08MG026', 1999, 9, 1, 30, 4.8899998664855957, 146.589996337890625, 30, 1.88999998569488525, 1, 10.1999998092651367, 10.1999998092651367, NULL, 9.09000015258789062, NULL, 8.46000003814697266, NULL, 7.96999979019165039, NULL, 7.40000009536743164, NULL, 7.13000011444091797, NULL, 6.6100001335144043, NULL, 6.28999996185302734, NULL, 6.11999988555908203, NULL, 5.42000007629394531, NULL, 4.88000011444091797, NULL, 4.44000005722045898, NULL, 4.40999984741210938, NULL, 4.32999992370605469, NULL, 4.19000005722045898, NULL, 4.05999994277954102, NULL, 4, NULL, 4.05999994277954102, NULL, 4.46999979019165039, NULL, 4.6100001335144043, NULL, 4.23000001907348633, NULL, 3.84999990463256792, NULL, 3.90000009536743208, NULL, 3.15000009536743208, NULL, 2.95000004768371582, NULL, 2.3599998950958252, NULL, 2.1400001049041748, NULL, 2, NULL, 1.98000001907348633, NULL, 1.88999998569488525, NULL, NULL, NULL),
     ('08MG026', 1999, 10, 1, 31, 1.65999996662139893, 51.4000015258789062, 27, 1.37999999523162842, 13, 3.01999998092651367, 1.79999995231628418, NULL, 1.72000002861022949, NULL, 1.6799999475479126, NULL, 1.63999998569488525, NULL, 1.65999996662139893, NULL, 1.65999996662139893, NULL, 1.98000001907348633, NULL, 1.78999996185302712, NULL, 1.61000001430511475, NULL, 1.53999996185302712, NULL, 1.5, NULL, 1.63999998569488525, NULL, 3.01999998092651367, NULL, 1.85000002384185791, NULL, 1.64999997615814209, NULL, 1.62999999523162842, NULL, 1.62000000476837158, NULL, 1.5700000524520874, NULL, 1.53999996185302712, NULL, 1.52999997138977051, NULL, 1.5, NULL, 1.48000001907348633, NULL, 1.51999998092651367, NULL, 1.49000000953674316, NULL, 1.45000004768371582, NULL, 1.39999997615814209, NULL, 1.37999999523162842, NULL, 1.71000003814697288, NULL, 1.59000003337860107, NULL, 1.69000005722045898, NULL, 1.55999994277954102, NULL),
     ('08MG026', 1999, 11, 1, 30, 2.61999988555908203, 78.6800003051757812, 28, 1.29999995231628418, 16, 5.03000020980834961, 1.46000003814697288, NULL, 1.45000004768371582, NULL, 1.45000004768371582, NULL, 1.40999996662139893, NULL, 1.37999999523162842, NULL, 2.38000011444091797, NULL, 3.83999991416931197, NULL, 3.57999992370605469, NULL, 3.40000009536743208, NULL, 2.96000003814697266, NULL, 3.05999994277954102, NULL, 4.90999984741210938, NULL, 4.1100001335144043, NULL, 4.51000022888183594, NULL, 4.48999977111816406, NULL, 5.03000020980834961, NULL, 4.23000001907348633, NULL, 2.43000006675720215, 'A', 2, 'E', 2.09999990463256836, 'E', 2, 'E', 1.89999997615814209, 'E', 1.70000004768371582, 'E', 1.75, 'E', 1.66999995708465576, 'E', 1.54999995231628418, 'E', 1.39999997615814209, 'E', 1.29999995231628418, 'E', 1.60000002384185791, 'E', 3.63000011444091797, 'A', NULL, NULL),
     ('08MG026', 2000, 1, 1, 31, 1.55999994277954102, 48.3100013732910156, 31, 1.3200000524520874, 1, 2.16000008583068848, 2.16000008583068848, 'E', 2.02999997138977051, 'E', 1.95000004768371604, 'E', 1.89999997615814209, 'E', 1.77999997138977051, 'E', 1.70000004768371582, 'E', 1.64999997615814209, 'E', 1.69000005722045898, 'E', 1.63999998569488525, 'E', 1.58000004291534424, 'E', 1.54999995231628418, 'E', 1.50999999046325684, 'A', 1.55999994277954102, NULL, 1.54999995231628418, NULL, 1.55999994277954102, NULL, 1.52999997138977051, NULL, 1.52999997138977051, NULL, 1.49000000953674316, NULL, 1.47000002861022949, 'B', 1.45000004768371582, 'B', 1.4299999475479126, NULL, 1.39999997615814209, NULL, 1.38999998569488525, NULL, 1.37000000476837158, NULL, 1.37000000476837158, NULL, 1.36000001430511475, NULL, 1.35000002384185791, NULL, 1.35000002384185791, NULL, 1.34000003337860107, NULL, 1.35000002384185791, NULL, 1.3200000524520874, NULL),
     ('08MG026', 2000, 2, 1, 29, 1.24000000953674316, 36.0600013732910156, 20, 1.15999996662139893, 1, 1.37000000476837158, 1.37000000476837158, NULL, 1.34000003337860107, NULL, 1.30999994277954102, NULL, 1.29999995231628418, NULL, 1.27999997138977051, NULL, 1.28999996185302712, NULL, 1.30999994277954102, NULL, 1.3200000524520874, NULL, 1.29999995231628418, NULL, 1.28999996185302712, NULL, 1.27999997138977051, NULL, 1.26999998092651367, NULL, 1.25, 'B', 1.23000001907348633, 'B', 1.21000003814697288, 'B', 1.20000004768371582, 'B', 1.19000005722045898, 'B', 1.1799999475479126, 'B', 1.16999995708465576, 'B', 1.15999996662139893, 'B', 1.19000005722045898, 'B', 1.25999999046325684, NULL, 1.21000003814697288, NULL, 1.20000004768371582, NULL, 1.19000005722045898, NULL, 1.20000004768371582, NULL, 1.20000004768371582, NULL, 1.1799999475479126, NULL, 1.1799999475479126, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2000, 3, 1, 31, 1.20000004768371582, 37.0800018310546875, 20, 1.15999996662139893, 31, 1.25, 1.19000005722045898, NULL, 1.20000004768371582, NULL, 1.21000003814697288, NULL, 1.21000003814697288, NULL, 1.19000005722045898, NULL, 1.1799999475479126, NULL, 1.1799999475479126, NULL, 1.1799999475479126, NULL, 1.16999995708465576, NULL, 1.16999995708465576, NULL, 1.19000005722045898, NULL, 1.16999995708465576, NULL, 1.1799999475479126, NULL, 1.19000005722045898, NULL, 1.16999995708465576, NULL, 1.19000005722045898, NULL, 1.16999995708465576, NULL, 1.1799999475479126, NULL, 1.16999995708465576, NULL, 1.15999996662139893, NULL, 1.16999995708465576, NULL, 1.24000000953674316, NULL, 1.24000000953674316, NULL, 1.21000003814697288, NULL, 1.21000003814697288, NULL, 1.21000003814697288, NULL, 1.23000001907348633, NULL, 1.23000001907348633, NULL, 1.22000002861022949, NULL, 1.22000002861022949, NULL, 1.25, NULL),
     ('08MG026', 2000, 4, 1, 30, 2.09999990463256836, 62.8699989318847656, 1, 1.3200000524520874, 28, 3.3599998950958252, 1.3200000524520874, NULL, 1.41999995708465576, NULL, 1.58000004291534424, NULL, 1.69000005722045898, NULL, 1.61000001430511475, NULL, 1.53999996185302712, NULL, 1.47000002861022949, NULL, 1.48000001907348633, NULL, 1.61000001430511475, NULL, 1.83000004291534402, NULL, 2.07999992370605469, NULL, 2.41000008583068848, NULL, 2.97000002861022905, NULL, 2.78999996185302779, NULL, 2.25, NULL, 2, NULL, 1.88999998569488525, NULL, 1.88999998569488525, NULL, 1.94000005722045898, NULL, 2.03999996185302779, NULL, 2.30999994277954102, NULL, 3.1400001049041748, NULL, 2.45000004768371582, NULL, 2.15000009536743208, NULL, 1.99000000953674316, NULL, 1.87000000476837203, NULL, 3.01999998092651367, NULL, 3.3599998950958252, NULL, 2.46000003814697266, NULL, 2.30999994277954102, NULL, NULL, NULL),
     ('08MG026', 2000, 5, 1, 31, 4.26999998092651367, 132.339996337890625, 8, 1.88999998569488525, 21, 8.89999961853027344, 2.41000008583068848, NULL, 2.30999994277954102, NULL, 2.52999997138977051, NULL, 2.3599998950958252, NULL, 2.22000002861022905, NULL, 2.00999999046325684, NULL, 1.91999995708465598, NULL, 1.88999998569488525, NULL, 1.88999998569488525, NULL, 1.92999994754791282, NULL, 2.00999999046325684, NULL, 2, NULL, 2.15000009536743208, NULL, 2.46000003814697266, NULL, 3.16000008583068848, NULL, 4.32000017166137695, NULL, 4.90000009536743164, NULL, 4.5, NULL, 5.28999996185302734, NULL, 5.78999996185302734, NULL, 8.89999961853027344, NULL, 8.60999965667724609, NULL, 6.90000009536743164, NULL, 6.92000007629394531, NULL, 6.25, NULL, 5.57000017166137695, NULL, 6.30000019073486328, NULL, 6.65999984741210938, NULL, 5.73999977111816406, NULL, 5.61999988555908203, NULL, 6.82000017166137695, NULL),
     ('08MG026', 2000, 6, 1, 30, 10.8000001907348633, 322.6199951171875, 1, 8.02999973297119141, 17, 12.3999996185302717, 8.02999973297119141, NULL, 8.42000007629394531, NULL, 9.40999984741210938, NULL, 11.8000001907348633, NULL, 12.1000003814697283, NULL, 11.5, NULL, 11.3999996185302717, NULL, 11.1000003814697283, NULL, 10.8999996185302717, NULL, 10, NULL, 8.61999988555908203, NULL, 9.40999984741210938, NULL, 9.68999958038330078, NULL, 10.8000001907348633, NULL, 11.8000001907348633, NULL, 11.8000001907348633, NULL, 12.3999996185302717, NULL, 12.3999996185302717, NULL, 12.1999998092651367, NULL, 11.5, NULL, 11.8000001907348633, NULL, 11.3000001907348633, NULL, 10.8999996185302717, NULL, 10.6999998092651367, NULL, 10.6999998092651367, NULL, 10.6000003814697283, NULL, 11.1000003814697283, NULL, 11.8000001907348633, NULL, 10, 'E', 8.43999958038330078, NULL, NULL, NULL),
     ('08MG026', 2000, 7, 1, 31, 8.57999992370605469, 266.04998779296875, 8, 5.28000020980834961, 28, 19.1000003814697266, 7.73999977111816406, NULL, 7.80999994277954102, NULL, 7.25, NULL, 6.55000019073486328, NULL, 5.96999979019165039, NULL, 6.05000019073486328, NULL, 5.53000020980834961, NULL, 5.28000020980834961, NULL, 6.46000003814697266, NULL, 5.76999998092651367, NULL, 6.23000001907348633, NULL, 7.78999996185302734, NULL, 8.10999965667724609, NULL, 8.27000045776367188, NULL, 7.78999996185302734, NULL, 7.3600001335144043, NULL, 7.92000007629394531, NULL, 9.43000030517577947, NULL, 9.56000041961669922, NULL, 9.93999958038330078, NULL, 11.8000001907348633, NULL, 11.1000003814697283, NULL, 10.6000003814697283, NULL, 10.5, NULL, 9.69999980926513672, NULL, 9.06999969482422053, NULL, 11.1000003814697283, 'A', 19.1000003814697266, NULL, 9.73999977111816406, NULL, 8.17000007629394531, NULL, 8.35999965667724609, NULL),
     ('08MG026', 2000, 8, 1, 31, 6.03999996185302734, 187.1300048828125, 29, 4.94000005722045898, 1, 7.92999982833862305, 7.92999982833862305, NULL, 7.51000022888183594, NULL, 7.53999996185302734, NULL, 7.32000017166137695, NULL, 7.51000022888183594, NULL, 7.51000022888183594, NULL, 7.73000001907348633, NULL, 7.26000022888183594, NULL, 7.3600001335144043, NULL, 7.5, NULL, 6.51999998092651367, NULL, 6.07999992370605469, NULL, 5.78999996185302734, NULL, 5.59999990463256836, NULL, 5.36999988555908203, NULL, 5.36999988555908203, NULL, 5.32000017166137695, NULL, 5.23000001907348633, NULL, 5.28000020980834961, NULL, 5.1100001335144043, NULL, 5.13000011444091797, NULL, 5.07999992370605469, NULL, 5.15999984741210938, NULL, 5.32000017166137695, NULL, 5.40999984741210938, NULL, 5.34999990463256836, NULL, 4.98000001907348633, NULL, 5, NULL, 4.94000005722045898, NULL, 4.96999979019165039, NULL, 4.94999980926513672, NULL),
     ('08MG026', 2000, 9, 1, 30, 3.66000008583068892, 109.739997863769517, 23, 2.80999994277954102, 1, 4.80000019073486328, 4.80000019073486328, NULL, 4.38000011444091797, NULL, 4.25, NULL, 3.8599998950958252, NULL, 3.67000007629394487, NULL, 3.72000002861022949, NULL, 4, NULL, 4.5, NULL, 3.93000006675720215, NULL, 4.07000017166137695, NULL, 3.75, NULL, 4, NULL, 4.05999994277954102, NULL, 3.81999993324279785, 'A', 3.6099998950958252, NULL, 3.6400001049041748, NULL, 3.57999992370605469, NULL, 4, NULL, 3.65000009536743208, NULL, 3.71000003814697266, NULL, 3.43000006675720215, NULL, 3.01999998092651367, NULL, 2.80999994277954102, NULL, 2.80999994277954102, NULL, 2.8599998950958252, NULL, 2.83999991416931152, NULL, 2.81999993324279785, NULL, 2.86999988555908203, NULL, 3.6400001049041748, NULL, 3.6400001049041748, NULL, NULL, NULL),
     ('08MG026', 2000, 10, 1, 31, 2.75, 85.1500015258789062, 15, 2.00999999046325684, 18, 4.69000005722045898, 3.30999994277954102, NULL, 2.86999988555908203, NULL, 2.6400001049041748, NULL, 2.48000001907348633, NULL, 2.30999994277954102, NULL, 2.30999994277954102, NULL, 2.32999992370605469, NULL, 2.41000008583068848, NULL, 2.63000011444091797, NULL, 2.56999993324279785, NULL, 2.27999997138977051, NULL, 2.15000009536743208, NULL, 2.15000009536743208, NULL, 2.06999993324279785, NULL, 2.00999999046325684, NULL, 2.17000007629394531, NULL, 4.03000020980834961, NULL, 4.69000005722045898, NULL, 3.36999988555908203, NULL, 4.32999992370605469, NULL, 3.90000009536743208, NULL, 3.09999990463256836, NULL, 2.84999990463256836, NULL, 2.75, NULL, 2.57999992370605469, NULL, 2.47000002861022905, NULL, 2.46000003814697266, NULL, 2.84999990463256836, NULL, 2.50999999046325684, NULL, 2.3599998950958252, NULL, 2.21000003814697266, NULL),
     ('08MG026', 2000, 11, 1, 30, 1.73000001907348633, 52.0200004577636719, 28, 1.35000002384185791, 4, 3.50999999046325684, 2.03999996185302779, NULL, 2, NULL, 2.04999995231628418, NULL, 3.50999999046325684, NULL, 2.52999997138977051, NULL, 2.25, NULL, 2.20000004768371582, NULL, 2.1400001049041748, NULL, 2, 'A', 1.89999997615814209, 'E', 1.79999995231628418, 'E', 1.75, 'E', 1.64999997615814209, 'E', 1.60000002384185791, 'E', 1.54999995231628418, 'E', 1.48000001907348633, 'E', 1.4299999475479126, 'E', 1.39999997615814209, 'E', 1.37999999523162842, 'E', 1.36000001430511475, 'E', 1.39999997615814209, 'A', 1.36000001430511475, NULL, 1.46000003814697288, NULL, 1.40999996662139893, NULL, 1.44000005722045898, NULL, 1.41999995708465576, NULL, 1.36000001430511475, NULL, 1.35000002384185791, NULL, 1.38999998569488525, NULL, 1.40999996662139893, NULL, NULL, NULL),
     ('08MG026', 2000, 12, 1, 31, 1.23000001907348633, 38.0600013732910156, 24, 1.10000002384185791, 2, 1.4299999475479126, 1.37999999523162842, NULL, 1.4299999475479126, NULL, 1.39999997615814209, NULL, 1.34000003337860107, NULL, 1.3200000524520874, NULL, 1.33000004291534424, NULL, 1.27999997138977051, NULL, 1.27999997138977051, NULL, 1.25999999046325684, NULL, 1.21000003814697288, NULL, 1.16999995708465576, 'B', 1.14999997615814209, 'B', 1.13999998569488525, 'B', 1.12999999523162842, 'B', 1.12999999523162842, 'B', 1.20000004768371582, 'B', 1.16999995708465576, 'B', 1.14999997615814209, 'B', 1.13999998569488525, 'B', 1.12999999523162842, 'B', 1.12000000476837158, 'B', 1.11000001430511475, 'B', 1.11000001430511475, 'B', 1.10000002384185791, 'B', 1.23000001907348633, NULL, 1.37000000476837158, NULL, 1.3200000524520874, NULL, 1.25999999046325684, NULL, 1.24000000953674316, NULL, 1.22000002861022949, NULL, 1.24000000953674316, NULL),
     ('08MG026', 2001, 1, 1, 31, 1.23000001907348633, 38.141998291015625, 31, 0.991999983787536621, 5, 1.90999996662139893, 1.12000000476837158, NULL, 1.15999996662139893, NULL, 1.28999996185302712, NULL, 1.26999998092651367, NULL, 1.90999996662139893, NULL, 1.55999994277954102, NULL, 1.47000002861022949, NULL, 1.37999999523162842, NULL, 1.29999995231628418, 'A', 1.21000003814697288, 'E', 1.25, 'E', 1.29999995231628418, 'E', 1.35000002384185791, 'E', 1.3200000524520874, 'E', 1.29999995231628418, 'E', 1.28999996185302712, 'E', 1.28999996185302712, 'A', 1.21000003814697288, NULL, 1.16999995708465576, NULL, 1.14999997615814209, NULL, 1.1799999475479126, NULL, 1.14999997615814209, NULL, 1.12999999523162842, NULL, 1.12000000476837158, NULL, 1.09000003337860107, NULL, 1.05999994277954102, NULL, 1.02999997138977051, NULL, 1.03999996185302712, NULL, 1.03999996185302712, NULL, 1.00999999046325684, NULL, 0.991999983787536621, NULL),
     ('08MG026', 2001, 2, 1, 28, 0.870999991893768311, 24.399999618530277, 28, 0.767000019550323486, 2, 1.03999996185302712, 0.989000022411346436, NULL, 1.03999996185302712, NULL, 0.990999996662140004, NULL, 1.01999998092651367, NULL, 1, NULL, 0.91100001335144043, NULL, 0.904999971389770397, NULL, 0.985000014305114746, NULL, 0.944999992847442627, NULL, 0.935999989509582409, NULL, 0.898000001907348633, NULL, 0.912999987602233998, NULL, 0.841000020503997803, NULL, 0.847999989986419678, NULL, 0.829999983310699463, 'B', 0.819999992847442627, 'B', 0.810000002384185791, 'B', 0.800000011920928955, 'B', 0.800000011920928955, 'B', 0.81800001859664917, NULL, 0.791000008583068848, NULL, 0.796999990940093994, NULL, 0.80699998140335083, NULL, 0.800999999046325684, NULL, 0.790000021457672119, NULL, 0.776000022888183594, NULL, 0.771000027656555176, NULL, 0.767000019550323486, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2001, 3, 1, 31, 0.938000023365020752, 29.0919990539550817, 4, 0.72500002384185791, 25, 1.39999997615814209, 0.777999997138977051, NULL, 0.760999977588653564, NULL, 0.737999975681304932, NULL, 0.72500002384185791, NULL, 0.744000017642974854, NULL, 0.744000017642974854, NULL, 0.768999993801116943, NULL, 0.873000025749206543, NULL, 0.843999981880187988, NULL, 0.811999976634979248, NULL, 0.795000016689300537, NULL, 0.816999971866607666, NULL, 0.91100001335144043, NULL, 0.837999999523162842, NULL, 0.848999977111816406, NULL, 0.829999983310699463, NULL, 0.828000009059906006, NULL, 1.08000004291534424, NULL, 1.12000000476837158, NULL, 1.03999996185302712, NULL, 0.985000014305114746, NULL, 0.953000009059906006, NULL, 0.935000002384185791, NULL, 0.953000009059906006, NULL, 1.39999997615814209, NULL, 1.36000001430511475, NULL, 1.22000002861022949, NULL, 1.14999997615814209, NULL, 1.10000002384185791, NULL, 1.03999996185302712, NULL, 1.10000002384185791, NULL),
     ('08MG026', 2001, 4, 1, 30, 1.4299999475479126, 42.9560012817382812, 12, 0.795000016689300537, 27, 4.05000019073486328, 1.04999995231628418, NULL, 0.998000025749206432, NULL, 0.986000001430511586, NULL, 0.933000028133392445, NULL, 0.925000011920928955, NULL, 0.890999972820281982, NULL, 0.845000028610229492, NULL, 0.829999983310699463, NULL, 0.828000009059906006, NULL, 0.828999996185302734, NULL, 0.813000023365020752, NULL, 0.795000016689300537, NULL, 0.805000007152557373, NULL, 0.796000003814697266, NULL, 0.80699998140335083, NULL, 0.845000028610229492, NULL, 1.23000001907348633, NULL, 1.29999995231628418, NULL, 1.22000002861022949, NULL, 1.1799999475479126, NULL, 1.19000005722045898, NULL, 1.19000005722045898, NULL, 1.21000003814697288, NULL, 1.44000005722045898, NULL, 2.49000000953674316, NULL, 3.33999991416931152, NULL, 4.05000019073486328, NULL, 3.74000000953674316, NULL, 2.96000003814697266, NULL, 2.44000005722045898, NULL, NULL, NULL),
     ('08MG026', 2001, 5, 1, 31, 3.70000004768371582, 114.690002441406236, 6, 1.61000001430511475, 25, 8.01000022888183594, 2.03999996185302779, NULL, 1.84000003337860107, NULL, 1.75, NULL, 1.83000004291534402, NULL, 1.75999999046325684, NULL, 1.61000001430511475, NULL, 1.64999997615814209, NULL, 1.85000002384185791, NULL, 1.91999995708465598, NULL, 1.86000001430511475, NULL, 2.13000011444091797, NULL, 2.99000000953674316, NULL, 4, NULL, 3.74000000953674316, NULL, 3.25999999046325684, NULL, 2.8900001049041748, NULL, 2.51999998092651367, NULL, 2.33999991416931152, NULL, 2.44000005722045898, NULL, 2.57999992370605469, NULL, 3.50999999046325684, NULL, 5.92999982833862305, NULL, 7.5, NULL, 7.92000007629394531, NULL, 8.01000022888183594, NULL, 7.67000007629394531, NULL, 6.90000009536743164, NULL, 6.40000009536743164, NULL, 4.92000007629394531, NULL, 4.13000011444091797, NULL, 4.80000019073486328, NULL),
     ('08MG026', 2001, 6, 1, 30, 5.96000003814697266, 178.759994506835938, 12, 4.76000022888183594, 27, 8, 7.1399998664855957, NULL, 6.15000009536743164, NULL, 5.19999980926513672, NULL, 5.07999992370605469, NULL, 5.01999998092651367, NULL, 4.98000001907348633, NULL, 5, NULL, 5.05000019073486328, NULL, 6.55999994277954102, NULL, 5.34999990463256836, NULL, 4.78999996185302734, NULL, 4.76000022888183594, NULL, 4.86999988555908203, NULL, 5.13000011444091797, NULL, 5.15000009536743164, NULL, 4.8600001335144043, NULL, 4.82999992370605469, NULL, 5.11999988555908203, NULL, 5.73999977111816406, NULL, 6.76999998092651367, NULL, 7.28000020980834961, NULL, 7.71999979019165039, NULL, 7.44000005722045898, NULL, 7.11999988555908203, NULL, 6.55000019073486328, NULL, 6.69999980926513672, 'E', 8, 'E', 7.19999980926513672, 'E', 6.80000019073486328, 'E', 6.40000009536743164, 'E', NULL, NULL),
     ('08MG026', 2001, 7, 1, 31, 7.57999992370605469, 235.100006103515597, 20, 6, 11, 10.1999998092651367, 6.40000009536743164, 'E', 6.5, 'E', 7, 'E', 8.10000038146972656, 'E', 8.69999980926513672, 'E', 8, 'E', 7.5, 'E', 7.69999980926513672, 'E', 8.5, 'E', 9.30000019073486328, 'E', 10.1999998092651367, 'E', 9.69999980926513672, 'E', 9, 'E', 8.5, 'E', 7.69999980926513672, 'E', 7.09999990463256836, 'E', 6.69999980926513672, 'E', 6.40000009536743164, 'E', 6.19999980926513672, 'E', 6, 'E', 7, 'E', 8.19999980926513672, 'E', 7.59999990463256836, 'E', 7.19999980926513672, 'E', 6.80000019073486328, 'E', 6.80000019073486328, 'E', 7.40000009536743164, 'E', 8, 'E', 7.40000009536743164, 'E', 7, 'E', 6.5, 'E'),
     ('08MG026', 2001, 8, 1, 31, 7.23999977111816406, 224.300003051757812, 28, 4.5, 23, 11, 5.90000009536743164, 'E', 10, 'E', 10.6999998092651367, 'E', 9.5, 'E', 8.60000038146972656, 'E', 8, 'E', 7.69999980926513672, 'E', 7.5, 'E', 7.40000009536743164, 'E', 7.30000019073486328, 'E', 7.40000009536743164, 'E', 7.40000009536743164, 'E', 7.5, 'E', 7.59999990463256836, 'E', 7.90000009536743164, 'E', 7.80000019073486328, 'E', 7.19999980926513672, 'E', 6.59999990463256836, 'E', 5.80000019073486328, 'E', 5.40000009536743164, 'E', 7, 'E', 8.5, 'E', 11, 'E', 9, 'E', 7, 'E', 5, 'E', 4.59999990463256836, 'E', 4.5, 'E', 4.5, 'E', 4.80000019073486328, 'E', 5.19999980926513672, 'E'),
     ('08MG026', 2001, 9, 1, 30, 4.44000005722045898, 133.289993286132812, 20, 2.59999990463256836, 24, 8.69999980926513672, 7.80000019073486328, 'E', 6.5, 'E', 5.90000009536743164, 'E', 5.19999980926513672, 'E', 4.69999980926513672, 'E', 4, 'E', 3.40000009536743208, 'E', 3.09999990463256836, 'E', 3.20000004768371582, 'E', 3.29999995231628418, 'E', 3.40000009536743208, 'E', 3.70000004768371582, 'E', 4.09999990463256836, 'E', 4.19999980926513672, 'E', 4.19999980926513672, 'E', 4, 'E', 3.5, 'E', 3.20000004768371582, 'E', 2.90000009536743208, 'E', 2.59999990463256836, 'E', 2.92000007629394531, 'A', 4.57999992370605469, NULL, 7.15999984741210938, NULL, 8.69999980926513672, NULL, 6.15000009536743164, NULL, 7.61999988555908203, NULL, 4.51999998092651367, NULL, 2.83999991416931152, NULL, 3.13000011444091797, NULL, 2.76999998092651367, NULL, NULL, NULL),
     ('08MG026', 2001, 10, 1, 31, 2.15000009536743208, 66.5100021362304688, 8, 1.15999996662139893, 26, 8.65999984741210938, 2.69000005722045898, NULL, 2.55999994277954102, NULL, 2.08999991416931152, NULL, 1.69000005722045898, NULL, 1.60000002384185791, NULL, 1.40999996662139893, NULL, 1.3200000524520874, NULL, 1.15999996662139893, NULL, 1.25999999046325684, NULL, 1.85000002384185791, NULL, 1.74000000953674316, NULL, 2.02999997138977051, NULL, 1.87000000476837203, NULL, 1.60000002384185791, NULL, 1.58000004291534424, NULL, 2.77999997138977051, NULL, 2.13000011444091797, NULL, 1.86000001430511475, NULL, 1.92999994754791282, NULL, 1.78999996185302712, NULL, 1.75999999046325684, NULL, 1.92999994754791282, NULL, 1.90999996662139893, NULL, 1.70000004768371582, NULL, 1.63999998569488525, NULL, 8.65999984741210938, NULL, 4.03999996185302734, NULL, 2.22000002861022905, NULL, 1.73000001907348633, NULL, 1.69000005722045898, NULL, 2.28999996185302779, NULL),
     ('08MG026', 2001, 11, 1, 30, 4.8600001335144043, 145.669998168945312, 8, 1.49000000953674316, 15, 17.6000003814697266, 1.85000002384185791, NULL, 1.87000000476837203, NULL, 1.60000002384185791, NULL, 2.88000011444091797, NULL, 2.18000006675720215, NULL, 1.75999999046325684, NULL, 1.58000004291534424, NULL, 1.49000000953674316, NULL, 1.66999995708465576, NULL, 1.60000002384185791, NULL, 1.97000002861022927, NULL, 8.73999977111816406, NULL, 9.44999980926513672, NULL, 8.81999969482421875, NULL, 17.6000003814697266, NULL, 9.48999977111816406, NULL, 6.1399998664855957, NULL, 4.88000011444091797, NULL, 7.01999998092651367, NULL, 11.5, NULL, 7.32999992370605469, NULL, 5.75, NULL, 4.80000019073486328, NULL, 4.21999979019165039, NULL, 3.83999991416931197, NULL, 3.50999999046325684, NULL, 3.25999999046325684, NULL, 3.16000008583068848, NULL, 2.97000002861022905, NULL, 2.74000000953674316, NULL, NULL, NULL),
     ('08MG026', 2001, 12, 1, 31, 1.64999997615814209, 51.0540008544921875, 31, 0.994000017642974854, 1, 2.72000002861022905, 2.72000002861022905, NULL, 2.50999999046325684, NULL, 2.22000002861022905, NULL, 2.09999990463256836, NULL, 1.94000005722045898, NULL, 1.91999995708465598, NULL, 1.82000005245208762, NULL, 1.86000001430511475, NULL, 1.72000002861022949, NULL, 1.70000004768371582, NULL, 1.60000002384185791, NULL, 1.53999996185302712, NULL, 1.5700000524520874, NULL, 1.54999995231628418, NULL, 1.46000003814697288, NULL, 2.15000009536743208, NULL, 2.3599998950958252, NULL, 1.97000002861022927, NULL, 1.75999999046325684, NULL, 1.49000000953674316, NULL, 1.33000004291534424, NULL, 1.4299999475479126, NULL, 1.37999999523162842, NULL, 1.25999999046325684, NULL, 1.14999997615814209, NULL, 1.12999999523162842, NULL, 1.14999997615814209, NULL, 1.12999999523162842, NULL, 1.0700000524520874, NULL, 1.0700000524520874, NULL, 0.994000017642974854, NULL),
     ('08MG026', 2002, 1, 1, 31, 2.53999996185302779, 78.8799972534179688, 1, 1.0700000524520874, 7, 7.92999982833862305, 1.0700000524520874, NULL, 2.94000005722045898, NULL, 2.34999990463256836, NULL, 1.86000001430511475, NULL, 1.69000005722045898, NULL, 2.15000009536743208, NULL, 7.92999982833862305, NULL, 7.84999990463256836, NULL, 4.86999988555908203, NULL, 3.94000005722045898, NULL, 3.51999998092651367, NULL, 3.26999998092651367, NULL, 2.98000001907348633, NULL, 2.72000002861022905, NULL, 2.48000001907348633, NULL, 2.33999991416931152, NULL, 2.1400001049041748, NULL, 2.1400001049041748, NULL, 2.07999992370605469, NULL, 1.98000001907348633, NULL, 1.83000004291534402, NULL, 1.75999999046325684, NULL, 1.71000003814697288, NULL, 1.46000003814697288, 'B', 1.45000004768371582, NULL, 1.59000003337860107, NULL, 1.40999996662139893, NULL, 1.12999999523162842, NULL, 1.47000002861022949, NULL, 1.47000002861022949, NULL, 1.29999995231628418, NULL),
     ('08MG026', 2002, 2, 1, 28, 0.869000017642974854, 24.3390007019042969, 28, 0.689999997615814209, 1, 1.19000005722045898, 1.19000005722045898, NULL, 1.11000001430511475, NULL, 1.11000001430511475, NULL, 1.02999997138977051, NULL, 1.03999996185302712, NULL, 1.03999996185302712, NULL, 1.03999996185302712, NULL, 0.949000000953674427, NULL, 0.902999997138977051, NULL, 0.926999986171722412, NULL, 0.902000010013580433, NULL, 0.879999995231628418, NULL, 0.859000027179718018, NULL, 0.83899998664855957, NULL, 0.834999978542327881, NULL, 0.820999979972839355, NULL, 0.802999973297119141, NULL, 0.78200000524520874, NULL, 0.843999981880187988, NULL, 0.735000014305114746, NULL, 0.740000009536743164, 'B', 0.730000019073486328, 'B', 0.720000028610229492, 'B', 0.709999978542327881, 'B', 0.709999978542327881, 'B', 0.699999988079071045, 'B', 0.699999988079071045, 'B', 0.689999997615814209, 'B', NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2002, 3, 1, 31, 0.518999993801116943, 16.0979995727539062, 22, 0.414000004529953003, 1, 0.675000011920928955, 0.675000011920928955, 'B', 0.643999993801116943, 'B', 0.63200002908706665, NULL, 0.639999985694885254, NULL, 0.619000017642974854, NULL, 0.493000000715255682, 'B', 0.564999997615814209, 'B', 0.640999972820281982, 'B', 0.658999979496002197, 'B', 0.634000003337860107, 'B', 0.635999977588653564, 'B', 0.570999979972839355, NULL, 0.546000003814697266, NULL, 0.513000011444091797, NULL, 0.499000012874603271, NULL, 0.481000006198883112, NULL, 0.458000004291534424, 'B', 0.446000009775161743, 'B', 0.439999997615814209, 'B', 0.421999990940093994, 'B', 0.428000003099441528, NULL, 0.414000004529953003, NULL, 0.419999986886978149, 'B', 0.419999986886978149, 'B', 0.419999986886978149, 'B', 0.419999986886978149, 'B', 0.419999986886978149, 'B', 0.418999999761581421, NULL, 0.439999997615814209, NULL, 0.497000008821487427, NULL, 0.586000025272369385, NULL),
     ('08MG026', 2002, 4, 1, 30, 1.54999995231628418, 46.4469985961914062, 2, 0.514999985694885254, 14, 3.73000001907348633, 0.55699998140335083, NULL, 0.514999985694885254, NULL, 0.544000029563903809, NULL, 0.629999995231628418, NULL, 0.740000009536743164, NULL, 0.921999990940093994, NULL, 0.944000005722046009, NULL, 0.888999998569488525, NULL, 0.892000019550323486, NULL, 0.984000027179718018, NULL, 1.08000004291534424, NULL, 1.5, NULL, 3.09999990463256836, NULL, 3.73000001907348633, NULL, 2.74000000953674316, NULL, 2.15000009536743208, NULL, 1.77999997138977051, NULL, 1.61000001430511475, NULL, 1.55999994277954102, NULL, 1.75999999046325684, NULL, 2.09999990463256836, NULL, 1.98000001907348633, NULL, 1.75, NULL, 1.59000003337860107, NULL, 1.5, NULL, 1.49000000953674316, NULL, 1.38999998569488525, NULL, 1.45000004768371582, NULL, 1.79999995231628418, NULL, 2.76999998092651367, NULL, NULL, NULL),
     ('08MG026', 2002, 5, 1, 31, 4.40000009536743164, 136.339996337890625, 10, 1.98000001907348633, 29, 12.3000001907348633, 3.73000001907348633, NULL, 4.17999982833862305, NULL, 3.54999995231628418, NULL, 3.04999995231628418, NULL, 2.72000002861022905, NULL, 2.40000009536743208, NULL, 2.17000007629394531, NULL, 2.03999996185302779, NULL, 2, NULL, 1.98000001907348633, NULL, 2.19000005722045898, NULL, 2.84999990463256836, NULL, 3.97000002861022949, NULL, 4.30000019073486328, NULL, 3.8599998950958252, NULL, 3.63000011444091797, NULL, 3.93000006675720215, NULL, 3.72000002861022949, NULL, 3.69000005722045898, NULL, 4.88000011444091797, NULL, 5.03000020980834961, NULL, 4.90000009536743164, NULL, 4.76999998092651367, NULL, 4.71999979019165039, NULL, 4.98000001907348633, NULL, 5.42000007629394531, NULL, 6.17000007629394531, NULL, 8.61999988555908203, NULL, 12.3000001907348633, NULL, 8.02999973297119141, NULL, 6.55999994277954102, NULL),
     ('08MG026', 2002, 6, 1, 30, 9.89999961853027166, 296.8800048828125, 8, 5.48999977111816406, 27, 15.1000003814697283, 5.90999984741210938, NULL, 6.44000005722045898, NULL, 7.05999994277954102, NULL, 7.23000001907348633, NULL, 9.14000034332275391, NULL, 7.67000007629394531, NULL, 6.15000009536743164, NULL, 5.48999977111816406, NULL, 6, NULL, 7.57000017166137695, NULL, 9.11999988555908203, NULL, 10.3000001907348633, NULL, 11.1999998092651367, NULL, 11.8000001907348633, NULL, 13, NULL, 13.1000003814697283, NULL, 12, NULL, 10.8000001907348633, NULL, 9.42000007629394354, NULL, 9.23999977111816406, NULL, 10, NULL, 10.6000003814697283, NULL, 10.5, NULL, 10.3999996185302717, NULL, 11.8000001907348633, NULL, 15, NULL, 15.1000003814697283, NULL, 14.1000003814697283, NULL, 11.6999998092651367, NULL, 9.03999996185302734, NULL, NULL, NULL),
     ('08MG026', 2002, 7, 1, 31, 8.32999992370605469, 258.230010986328125, 5, 4.46999979019165039, 26, 11.1000003814697283, 6.90000009536743164, NULL, 5.92000007629394531, NULL, 5.51000022888183594, NULL, 4.8899998664855957, NULL, 4.46999979019165039, NULL, 4.5, NULL, 5.1399998664855957, NULL, 5.8600001335144043, NULL, 6.15999984741210938, NULL, 7.44000005722045898, NULL, 9.43999958038330078, NULL, 9.89000034332275391, NULL, 10.1999998092651367, NULL, 10.6999998092651367, NULL, 10, NULL, 9.46000003814697266, NULL, 10, NULL, 9.80000019073486328, NULL, 9.65999984741210938, NULL, 9.56000041961669922, NULL, 9.18000030517577947, NULL, 9.65999984741210938, NULL, 9.59000015258789062, NULL, 10.5, NULL, 10.6999998092651367, NULL, 11.1000003814697283, NULL, 9.56999969482422053, NULL, 9.14999961853027166, NULL, 8.57999992370605469, NULL, 7.90999984741210938, NULL, 6.78999996185302734, NULL),
     ('08MG026', 2002, 8, 1, 31, 6.21000003814697266, 192.600006103515597, 8, 4.90999984741210938, 24, 7.40999984741210938, 6.13000011444091797, NULL, 5.92999982833862305, NULL, 5.28999996185302734, NULL, 6.82000017166137695, NULL, 5.46999979019165039, NULL, 5.03000020980834961, NULL, 4.94999980926513672, NULL, 4.90999984741210938, NULL, 6.07999992370605469, NULL, 6.78999996185302734, NULL, 6.57999992370605469, NULL, 6.71000003814697266, NULL, 7.32000017166137695, NULL, 7.38000011444091797, NULL, 6.98999977111816406, NULL, 6.48999977111816406, NULL, 5.46999979019165039, NULL, 5.28000020980834961, NULL, 5.73999977111816406, NULL, 5.30000019073486328, NULL, 5.09999990463256836, NULL, 5.67999982833862305, NULL, 6.71999979019165039, NULL, 7.40999984741210938, NULL, 7.26000022888183594, NULL, 6.73000001907348633, NULL, 6.6399998664855957, NULL, 6.76999998092651367, NULL, 6.92999982833862305, NULL, 6.6399998664855957, NULL, 6.05999994277954102, NULL),
     ('08MG026', 2002, 9, 1, 30, 3.1099998950958252, 93.279998779296875, 30, 1.84000003337860107, 1, 6.19000005722045898, 6.19000005722045898, NULL, 6.15000009536743164, NULL, 4.96000003814697266, NULL, 3.75, NULL, 3.1400001049041748, NULL, 2.76999998092651367, NULL, 2.50999999046325684, NULL, 2.40000009536743208, NULL, 2.72000002861022905, NULL, 2.91000008583068848, NULL, 3.1099998950958252, NULL, 3.36999988555908203, NULL, 3.44000005722045898, NULL, 3.32999992370605469, NULL, 3.24000000953674316, NULL, 4.5, NULL, 3.28999996185302779, NULL, 2.6400001049041748, NULL, 3.3900001049041748, NULL, 2.88000011444091797, NULL, 2.44000005722045898, NULL, 2.5, NULL, 2.69000005722045898, NULL, 2.59999990463256836, NULL, 2.25, NULL, 2.20000004768371582, NULL, 2.01999998092651367, NULL, 2.00999999046325684, NULL, 2.03999996185302779, NULL, 1.84000003337860107, NULL, NULL, NULL),
     ('08MG026', 2002, 10, 1, 31, 1.27999997138977051, 39.7360000610351634, 30, 0.828000009059906006, 3, 1.83000004291534402, 1.65999996662139893, NULL, 1.62000000476837158, NULL, 1.83000004291534402, NULL, 1.62000000476837158, NULL, 1.5700000524520874, NULL, 1.53999996185302712, NULL, 1.70000004768371582, NULL, 1.65999996662139893, NULL, 1.52999997138977051, NULL, 1.4299999475479126, NULL, 1.33000004291534424, NULL, 1.27999997138977051, NULL, 1.24000000953674316, NULL, 1.20000004768371582, NULL, 1.25, NULL, 1.3200000524520874, NULL, 1.29999995231628418, NULL, 1.24000000953674316, NULL, 1.25999999046325684, NULL, 1.25999999046325684, NULL, 1.21000003814697288, NULL, 1.11000001430511475, NULL, 1.03999996185302712, NULL, 1.02999997138977051, NULL, 0.998000025749206432, NULL, 0.978999972343444824, NULL, 0.982999980449676403, NULL, 0.970000028610229603, NULL, 0.880999982357025146, NULL, 0.828000009059906006, NULL, 0.866999983787536621, NULL),
     ('08MG026', 2002, 11, 1, 30, 1.45000004768371582, 43.5019989013671875, 4, 0.871999979019165039, 20, 2.8599998950958252, 0.887000024318695068, NULL, 0.890999972820281982, NULL, 0.884999990463256836, NULL, 0.871999979019165039, NULL, 0.916999995708465576, NULL, 1.39999997615814209, NULL, 1.33000004291534424, NULL, 1.23000001907348633, NULL, 1.15999996662139893, NULL, 1.09000003337860107, NULL, 1.11000001430511475, NULL, 2.22000002861022905, NULL, 1.84000003337860107, NULL, 1.4299999475479126, NULL, 1.26999998092651367, NULL, 1.28999996185302712, 'B', 1.34000003337860107, 'B', 1.40999996662139893, 'B', 2.03999996185302779, NULL, 2.8599998950958252, NULL, 2.47000002861022905, NULL, 2.20000004768371582, NULL, 1.79999995231628418, NULL, 1.50999999046325684, NULL, 1.44000005722045898, NULL, 1.37000000476837158, NULL, 1.3200000524520874, NULL, 1.29999995231628418, NULL, 1.3200000524520874, NULL, 1.29999995231628418, NULL, NULL, NULL),
     ('08MG026', 2002, 12, 1, 31, 1.55999994277954102, 48.4799995422363281, 8, 1.10000002384185791, 15, 3.91000008583068892, 1.28999996185302712, NULL, 1.28999996185302712, NULL, 1.24000000953674316, NULL, 1.20000004768371582, NULL, 1.22000002861022949, NULL, 1.16999995708465576, NULL, 1.12999999523162842, NULL, 1.10000002384185791, NULL, 1.11000001430511475, NULL, 1.16999995708465576, NULL, 1.12999999523162842, NULL, 2.46000003814697266, NULL, 1.98000001907348633, NULL, 2.34999990463256836, NULL, 3.91000008583068892, NULL, 2.74000000953674316, NULL, 2.16000008583068848, NULL, 1.90999996662139893, NULL, 1.72000002861022949, NULL, 1.58000004291534424, NULL, 1.46000003814697288, NULL, 1.44000005722045898, NULL, 1.34000003337860107, NULL, 1.30999994277954102, NULL, 1.37000000476837158, NULL, 1.37000000476837158, NULL, 1.34000003337860107, NULL, 1.26999998092651367, NULL, 1.20000004768371582, NULL, 1.27999997138977051, NULL, 1.24000000953674316, NULL),
     ('08MG026', 2003, 1, 1, 31, 1.64999997615814209, 51.220001220703125, 1, 1.08000004291534424, 26, 4.65000009536743164, 1.08000004291534424, NULL, 1.23000001907348633, NULL, 1.47000002861022949, NULL, 2.24000000953674316, NULL, 2.27999997138977051, NULL, 1.79999995231628418, NULL, 1.65999996662139893, NULL, 1.58000004291534424, NULL, 1.5, NULL, 1.40999996662139893, NULL, 1.37000000476837158, NULL, 1.35000002384185791, NULL, 1.29999995231628418, NULL, 1.26999998092651367, NULL, 1.21000003814697288, NULL, 1.1799999475479126, NULL, 1.15999996662139893, NULL, 1.13999998569488525, NULL, 1.12000000476837158, NULL, 1.09000003337860107, NULL, 1.08000004291534424, NULL, 1.11000001430511475, NULL, 1.34000003337860107, NULL, 1.23000001907348633, NULL, 1.25, NULL, 4.65000009536743164, NULL, 3.42000007629394531, NULL, 2.55999994277954102, NULL, 2.18000006675720215, NULL, 1.97000002861022927, NULL, 1.99000000953674316, NULL),
     ('08MG026', 2003, 2, 1, 28, 1.23000001907348633, 34.430999755859375, 28, 0.962999999523162842, 1, 1.91999995708465598, 1.91999995708465598, NULL, 1.80999994277954102, NULL, 1.69000005722045898, NULL, 1.55999994277954102, NULL, 1.5, NULL, 1.41999995708465576, NULL, 1.36000001430511475, NULL, 1.30999994277954102, NULL, 1.26999998092651367, NULL, 1.22000002861022949, NULL, 1.20000004768371582, NULL, 1.19000005722045898, NULL, 1.16999995708465576, NULL, 1.14999997615814209, NULL, 1.14999997615814209, NULL, 1.15999996662139893, NULL, 1.11000001430511475, NULL, 1.09000003337860107, NULL, 1.05999994277954102, NULL, 1.0700000524520874, NULL, 1.03999996185302712, NULL, 1.01999998092651367, NULL, 1, 'B', 1, 'B', 1, 'B', 1.02999997138977051, NULL, 0.967999994754791149, NULL, 0.962999999523162842, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2003, 3, 1, 31, 2.04999995231628418, 63.4939994812011719, 9, 0.84299999475479126, 14, 7.82000017166137695, 0.929000020027160645, NULL, 0.930000007152557373, NULL, 0.920000016689300426, NULL, 0.901000022888183594, NULL, 0.896000027656555176, NULL, 0.888999998569488525, NULL, 0.879999995231628418, 'B', 0.85000002384185791, 'B', 0.84299999475479126, NULL, 0.880999982357025146, NULL, 0.925000011920928955, NULL, 1.16999995708465576, NULL, 5.6100001335144043, NULL, 7.82000017166137695, NULL, 4.80000019073486328, NULL, 3.45000004768371582, NULL, 2.65000009536743208, NULL, 2.26999998092651367, NULL, 2.03999996185302779, NULL, 1.98000001907348633, NULL, 1.88999998569488525, NULL, 2.02999997138977051, NULL, 1.82000005245208762, NULL, 1.62999999523162842, NULL, 1.53999996185302712, NULL, 1.48000001907348633, NULL, 1.39999997615814209, NULL, 1.34000003337860107, NULL, 1.35000002384185791, NULL, 3.5, NULL, 3.88000011444091797, NULL),
     ('08MG026', 2003, 4, 1, 30, 2.28999996185302779, 68.6999969482421875, 6, 1.5700000524520874, 9, 3.05999994277954102, 2.83999991416931152, NULL, 2.3900001049041748, NULL, 2.09999990463256836, NULL, 1.84000003337860107, NULL, 1.6799999475479126, NULL, 1.5700000524520874, NULL, 1.62999999523162842, NULL, 2.3599998950958252, NULL, 3.05999994277954102, NULL, 2.46000003814697266, NULL, 2.53999996185302779, NULL, 2.3900001049041748, NULL, 2.55999994277954102, NULL, 2.49000000953674316, NULL, 2.32999992370605469, NULL, 2.20000004768371582, NULL, 2.08999991416931152, NULL, 1.94000005722045898, NULL, 1.87000000476837203, NULL, 1.96000003814697288, NULL, 2.25, NULL, 2.59999990463256836, NULL, 2.66000008583068848, NULL, 2.51999998092651367, NULL, 2.45000004768371582, NULL, 2.32999992370605469, NULL, 2.28999996185302779, NULL, 2.26999998092651367, NULL, 2.40000009536743208, NULL, 2.63000011444091797, NULL, NULL, NULL),
     ('08MG026', 2003, 5, 1, 31, 4.69000005722045898, 145.289993286132812, 8, 2.18000006675720215, 25, 11.8000001907348633, 3.06999993324279785, NULL, 3.47000002861022905, NULL, 3.16000008583068848, NULL, 2.8900001049041748, NULL, 2.67000007629394531, NULL, 2.45000004768371582, NULL, 2.32999992370605469, NULL, 2.18000006675720215, NULL, 2.20000004768371582, NULL, 2.49000000953674316, NULL, 3.04999995231628418, NULL, 3.45000004768371582, NULL, 3.65000009536743208, NULL, 3.70000004768371582, NULL, 3.21000003814697266, NULL, 2.74000000953674316, NULL, 2.48000001907348633, NULL, 2.32999992370605469, NULL, 2.25, NULL, 2.19000005722045898, NULL, 2.29999995231628418, NULL, 3.11999988555908203, NULL, 4.3899998664855957, NULL, 10.3000001907348633, NULL, 11.8000001907348633, NULL, 9.18000030517577947, NULL, 7.86999988555908203, NULL, 10.3000001907348633, NULL, 10.6999998092651367, NULL, 9.92000007629394354, NULL, 9.44999980926513672, NULL),
     ('08MG026', 2003, 6, 1, 30, 10.1999998092651367, 306.1199951171875, 23, 6.69999980926513672, 8, 15.8000001907348633, 8.73999977111816406, NULL, 8.69999980926513672, NULL, 8.76000022888183594, NULL, 9.42000007629394354, NULL, 11.1000003814697283, NULL, 13.1000003814697283, NULL, 14.1000003814697283, NULL, 15.8000001907348633, NULL, 13.6999998092651367, NULL, 12.1999998092651367, NULL, 10.5, NULL, 10.1000003814697283, NULL, 11.8000001907348633, NULL, 9.05000019073486328, NULL, 7.32999992370605469, NULL, 7.34000015258789062, NULL, 8.76000022888183594, NULL, 11.5, NULL, 10.1000003814697283, NULL, 8.67000007629394531, NULL, 7.51999998092651367, NULL, 6.96000003814697266, NULL, 6.69999980926513672, NULL, 6.94000005722045898, NULL, 7.98999977111816406, NULL, 9.73999977111816406, NULL, 11.6000003814697283, NULL, 11.8000001907348633, NULL, 11.8000001907348633, NULL, 14.3000001907348633, NULL, NULL, NULL),
     ('08MG026', 2003, 7, 1, 31, 9.57999992370605646, 296.829986572265625, 4, 7.63000011444091797, 1, 12, 12, NULL, 9.27000045776367188, NULL, 7.82999992370605469, NULL, 7.63000011444091797, NULL, 8.68999958038330078, NULL, 9.60000038146972834, NULL, 9.89999961853027166, NULL, 9.56000041961669922, NULL, 9.13000011444091797, NULL, 10.6000003814697283, NULL, 11.3999996185302717, NULL, 11.3000001907348633, NULL, 11.6000003814697283, NULL, 10.5, NULL, 10.1999998092651367, NULL, 9.25, NULL, 8.06999969482421875, 'A', 8.17000007629394531, NULL, 8.42000007629394531, NULL, 9.73999977111816406, NULL, 9.78999996185302734, NULL, 9.21000003814697266, NULL, 9.27000045776367188, NULL, 9.27999973297119141, NULL, 8.81999969482421875, NULL, 8.36999988555908203, NULL, 8.64999961853027344, NULL, 9.07999992370605646, NULL, 10.1999998092651367, NULL, 10.5, NULL, 10.8000001907348633, NULL),
     ('08MG026', 2003, 8, 1, 31, 6.19999980926513672, 192.169998168945312, 24, 4.19000005722045898, 1, 10, 10, NULL, 8.92000007629394531, NULL, 8.25, NULL, 7.82000017166137695, NULL, 7.46000003814697266, NULL, 6.96000003814697266, NULL, 6.38000011444091797, NULL, 6.65999984741210938, NULL, 6.76000022888183594, NULL, 6.32999992370605469, NULL, 6.19999980926513672, NULL, 5.71999979019165039, NULL, 5.28999996185302734, NULL, 5.53999996185302734, NULL, 5.98999977111816406, NULL, 6.44999980926513672, NULL, 6.55000019073486328, NULL, 6.40000009536743164, NULL, 6.03999996185302734, NULL, 5.65999984741210938, NULL, 5.80999994277954102, NULL, 5.78999996185302734, NULL, 4.82000017166137695, NULL, 4.19000005722045898, NULL, 5.3600001335144043, NULL, 5.78000020980834961, NULL, 5.01999998092651367, NULL, 4.78000020980834961, NULL, 4.98999977111816406, NULL, 5.09999990463256836, NULL, 5.15000009536743164, NULL),
     ('08MG026', 2003, 9, 1, 30, 3.82999992370605513, 114.75, 21, 2.26999998092651367, 7, 7.1399998664855957, 4.80999994277954102, NULL, 5.1399998664855957, NULL, 5.42999982833862305, NULL, 5.67000007629394531, NULL, 5.67999982833862305, NULL, 5.67000007629394531, NULL, 7.1399998664855957, NULL, 4.65000009536743164, NULL, 3.68000006675720215, NULL, 3.6099998950958252, NULL, 3.96000003814697266, NULL, 3.29999995231628418, NULL, 3, NULL, 4.28999996185302734, NULL, 3.31999993324279785, NULL, 2.78999996185302779, NULL, 2.3599998950958252, NULL, 2.58999991416931152, NULL, 2.93000006675720215, NULL, 2.40000009536743208, NULL, 2.26999998092651367, NULL, 2.93000006675720215, NULL, 3.19000005722045898, NULL, 2.90000009536743208, NULL, 3.02999997138977051, NULL, 3.22000002861022905, NULL, 3.96000003814697266, NULL, 3.8599998950958252, NULL, 3.52999997138977051, NULL, 3.44000005722045898, NULL, NULL, NULL),
     ('08MG026', 2003, 10, 1, 31, 6.01999998092651367, 186.710006713867188, 31, 1.63999998569488525, 18, 30, 3.33999991416931152, NULL, 3.06999993324279785, NULL, 3.03999996185302779, NULL, 2.8599998950958252, NULL, 3.02999997138977051, NULL, 4.8899998664855957, NULL, 4.78999996185302734, NULL, 3.8900001049041748, NULL, 2.77999997138977051, NULL, 2.24000000953674316, NULL, 2.09999990463256836, NULL, 2.33999991416931152, NULL, 2.13000011444091797, NULL, 1.90999996662139893, NULL, 1.83000004291534402, NULL, 5.26000022888183594, NULL, 12.3000001907348633, 'A', 30, 'E', 22, 'E', 16, 'E', 8, 'E', 7.5, 'E', 6, 'E', 5, 'E', 4.40000009536743164, 'E', 5, 'E', 6.5, 'E', 6.5, 'E', 4.40000009536743164, 'E', 1.97000002861022927, NULL, 1.63999998569488525, NULL),
     ('08MG026', 2003, 11, 1, 30, 2.48000001907348633, 74.279998779296875, 22, 1.15999996662139893, 27, 4.80000019073486328, 1.60000002384185791, NULL, 1.91999995708465598, NULL, 1.60000002384185791, NULL, 1.41999995708465576, NULL, 1.40999996662139893, NULL, 1.46000003814697288, NULL, 1.50999999046325684, NULL, 1.82000005245208762, NULL, 2.02999997138977051, NULL, 3.8599998950958252, NULL, 4.30999994277954102, NULL, 2.6400001049041748, NULL, 1.91999995708465598, NULL, 1.96000003814697288, NULL, 3.1400001049041748, NULL, 3.61999988555908203, NULL, 3.19000005722045898, NULL, 2.80999994277954102, NULL, 2.15000009536743208, NULL, 1.61000001430511475, NULL, 1.22000002861022949, NULL, 1.15999996662139893, NULL, 1.44000005722045898, NULL, 1.74000000953674316, NULL, 2.05999994277954102, NULL, 4.65000009536743164, 'B', 4.80000019073486328, 'B', 4.75, 'B', 4.69999980926513672, 'B', 1.77999997138977051, NULL, NULL, NULL),
     ('08MG026', 2003, 12, 1, 31, 1.37000000476837158, 42.4000015258789062, 29, 1.09000003337860107, 6, 2.06999993324279785, 1.35000002384185791, NULL, 1.63999998569488525, NULL, 1.66999995708465576, NULL, 1.47000002861022949, NULL, 1.78999996185302712, NULL, 2.06999993324279785, NULL, 2.02999997138977051, NULL, 1.76999998092651367, NULL, 1.3200000524520874, NULL, 1.3200000524520874, NULL, 1.29999995231628418, NULL, 1.33000004291534424, NULL, 1.28999996185302712, NULL, 1.25999999046325684, NULL, 1.23000001907348633, NULL, 1.25, NULL, 1.23000001907348633, NULL, 1.22000002861022949, NULL, 1.22000002861022949, NULL, 1.25, NULL, 1.24000000953674316, NULL, 1.23000001907348633, NULL, 1.24000000953674316, NULL, 1.28999996185302712, NULL, 1.26999998092651367, NULL, 1.23000001907348633, NULL, 1.23000001907348633, NULL, 1.20000004768371582, NULL, 1.09000003337860107, NULL, 1.16999995708465576, NULL, 1.20000004768371582, NULL),
     ('08MG026', 2004, 1, 1, 31, 1.38999998569488525, 42.9500007629394531, 4, 1.11000001430511475, 15, 2.65000009536743208, 1.21000003814697288, NULL, 1.21000003814697288, NULL, 1.16999995708465576, NULL, 1.11000001430511475, NULL, 1.16999995708465576, NULL, 1.1799999475479126, 'B', 1.20000004768371582, 'B', 1.22000002861022949, 'B', 1.23000001907348633, 'B', 1.24000000953674316, 'B', 1.25, NULL, 1.25999999046325684, NULL, 1.35000002384185791, NULL, 1.95000004768371604, NULL, 2.65000009536743208, NULL, 2.08999991416931152, NULL, 1.92999994754791282, NULL, 1.60000002384185791, 'B', 1.5, 'B', 1.39999997615814209, 'B', 1.37999999523162842, 'B', 1.35000002384185791, 'B', 1.33000004291534424, 'B', 1.29999995231628418, 'B', 1.27999997138977051, 'B', 1.25999999046325684, 'B', 1.25, 'B', 1.24000000953674316, 'B', 1.23000001907348633, 'B', 1.21000003814697288, 'B', 1.20000004768371582, 'B'),
     ('08MG026', 2004, 2, 1, 29, 1.09000003337860107, 31.4799995422363281, 19, 1.03999996185302712, 1, 1.19000005722045898, 1.19000005722045898, 'B', 1.1799999475479126, 'B', 1.16999995708465576, 'B', 1.15999996662139893, 'B', 1.13999998569488525, 'B', 1.12999999523162842, 'B', 1.12000000476837158, 'B', 1.10000002384185791, 'B', 1.09000003337860107, 'B', 1.08000004291534424, 'B', 1.05999994277954102, 'B', 1.0700000524520874, 'B', 1.08000004291534424, 'B', 1.09000003337860107, 'B', 1.09000003337860107, 'B', 1.0700000524520874, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.03999996185302712, 'B', 1.03999996185302712, 'B', 1.03999996185302712, 'B', 1.04999995231628418, 'B', 1.04999995231628418, 'B', 1.05999994277954102, 'B', 1.0700000524520874, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.04999995231628418, 'B', 1.03999996185302712, 'B', NULL, NULL, NULL, NULL),
     ('08MG026', 2004, 3, 1, 31, 1.47000002861022949, 45.5600013732910156, 1, 1.01999998092651367, 30, 2.84999990463256836, 1.01999998092651367, 'B', 1.02999997138977051, 'B', 1.03999996185302712, 'B', 1.0700000524520874, 'B', 1.09000003337860107, 'B', 1.14999997615814209, 'B', 1.35000002384185791, 'B', 1.45000004768371582, 'B', 1.58000004291534424, 'B', 1.45000004768371582, 'B', 1.29999995231628418, 'B', 1.22000002861022949, 'B', 1.1799999475479126, 'B', 1.16999995708465576, 'B', 1.14999997615814209, 'B', 1.25, 'B', 1.39999997615814209, 'B', 1.5, 'B', 1.54999995231628418, 'B', 1.45000004768371582, 'B', 1.4299999475479126, 'B', 1.45000004768371582, 'B', 1.51999998092651367, 'B', 1.60000002384185791, 'B', 1.64999997615814209, 'B', 1.70000004768371582, 'B', 1.64999997615814209, 'B', 1.79999995231628418, NULL, 1.85000002384185791, NULL, 2.84999990463256836, NULL, 2.66000008583068848, NULL),
     ('08MG026', 2004, 4, 1, 30, 2.8599998950958252, 85.8499984741210938, 21, 2.18000006675720215, 12, 4.38000011444091797, 2.32999992370605469, NULL, 2.22000002861022905, NULL, 2.21000003814697266, NULL, 2.25, NULL, 2.30999994277954102, NULL, 2.55999994277954102, NULL, 2.74000000953674316, NULL, 2.79999995231628418, NULL, 2.8599998950958252, NULL, 3.1099998950958252, NULL, 3.84999990463256792, NULL, 4.38000011444091797, NULL, 4.17000007629394531, NULL, 3.81999993324279785, NULL, 3.24000000953674316, NULL, 3.08999991416931152, NULL, 2.73000001907348633, NULL, 2.43000006675720215, NULL, 2.28999996185302779, NULL, 2.24000000953674316, NULL, 2.18000006675720215, NULL, 2.19000005722045898, NULL, 2.30999994277954102, NULL, 2.22000002861022905, NULL, 2.23000001907348633, NULL, 2.78999996185302779, NULL, 3.86999988555908203, NULL, 3.18000006675720215, NULL, 3.07999992370605469, NULL, 4.17000007629394531, NULL, NULL, NULL),
     ('08MG026', 2004, 5, 1, 31, 5.03000020980834961, 155.80999755859375, 13, 3.27999997138977051, 2, 8.10000038146972656, 5.82999992370605469, NULL, 8.10000038146972656, NULL, 6.73999977111816406, NULL, 5.8600001335144043, NULL, 4.73000001907348633, NULL, 3.84999990463256792, NULL, 3.68000006675720215, NULL, 4.03000020980834961, NULL, 3.81999993324279785, NULL, 3.6099998950958252, NULL, 3.76999998092651367, NULL, 3.42000007629394531, NULL, 3.27999997138977051, NULL, 3.42000007629394531, NULL, 3.72000002861022949, NULL, 3.92000007629394487, NULL, 4.63000011444091797, NULL, 5.55000019073486328, NULL, 6.6399998664855957, NULL, 7.90000009536743164, NULL, 8.07999992370605469, NULL, 7.3600001335144043, NULL, 5.26000022888183594, NULL, 4.69000005722045898, NULL, 5.3899998664855957, NULL, 6.09999990463256836, NULL, 6.09000015258789062, NULL, 4.92000007629394531, NULL, 4.19000005722045898, NULL, 3.75, NULL, 3.48000001907348633, NULL),
     ('08MG026', 2004, 6, 1, 30, 9.53999996185302734, 286.1300048828125, 1, 3.25, 26, 24.7999992370605469, 3.25, NULL, 3.29999995231628418, NULL, 4.09999990463256836, NULL, 6.55000019073486328, NULL, 8.67000007629394531, NULL, 6.92000007629394531, NULL, 5.69999980926513672, NULL, 6.69000005722045898, NULL, 8.5, NULL, 9.56999969482422053, NULL, 7.78000020980834961, NULL, 6.53999996185302734, NULL, 6.01000022888183594, NULL, 4.8899998664855957, NULL, 4.19999980926513672, NULL, 4.82999992370605469, NULL, 6.5, NULL, 7.53000020980834961, NULL, 7.3899998664855957, NULL, 8.40999984741210938, NULL, 10.6999998092651367, NULL, 12.8999996185302717, NULL, 13.3000001907348633, NULL, 17.6000003814697266, NULL, 17.2000007629394531, NULL, 24.7999992370605469, NULL, 22.7000007629394531, NULL, 16.2999992370605469, NULL, 12.1999998092651367, NULL, 11.1000003814697283, NULL, NULL, NULL),
     ('08MG026', 2004, 7, 1, 31, 9.60999965667724609, 297.769989013671875, 11, 4.53999996185302734, 6, 15.1000003814697283, 12.1999998092651367, NULL, 12.6999998092651367, NULL, 10.6000003814697283, NULL, 7.46000003814697266, NULL, 7.3600001335144043, NULL, 15.1000003814697283, NULL, 12.6999998092651367, NULL, 7.59999990463256836, NULL, 5.34999990463256836, NULL, 4.76999998092651367, NULL, 4.53999996185302734, NULL, 5.34999990463256836, NULL, 7.59000015258789062, NULL, 7.76999998092651367, NULL, 9.31000041961669922, NULL, 9.30000019073486328, NULL, 8.40999984741210938, NULL, 10.6000003814697283, NULL, 13.1000003814697283, NULL, 10.8000001907348633, NULL, 8.71000003814697266, NULL, 9.43000030517577947, NULL, 11.1999998092651367, NULL, 12.8999996185302717, NULL, 14.6000003814697283, NULL, 12.3999996185302717, NULL, 11.1999998092651367, NULL, 11.5, NULL, 9.22000026702880859, 'A', 7.19999980926513672, 'E', 6.80000019073486328, 'E'),
     ('08MG026', 2004, 8, 1, 31, 6.80999994277954102, 211, 28, 4.69999980926513672, 30, 9.25, 6.75, 'E', 6.59999990463256836, 'E', 6.5, 'E', 6.30000019073486328, 'E', 6, 'E', 5.80000019073486328, 'E', 5.40000009536743164, 'E', 5.30000019073486328, 'E', 5.69999980926513672, 'E', 6, 'E', 6.30000019073486328, 'E', 6.69999980926513672, 'E', 7.19999980926513672, 'E', 7.59999990463256836, 'E', 8, 'E', 8.19999980926513672, 'E', 7.80000019073486328, 'E', 7.59999990463256836, 'E', 7.5, 'E', 7.40000009536743164, 'E', 8.10000038146972656, 'E', 7.80000019073486328, 'E', 7.59999990463256836, 'E', 7, 'E', 6.59999990463256836, 'E', 6, 'E', 5.19999980926513672, 'E', 4.69999980926513672, 'E', 6, 'E', 9.25, 'E', 8.10000038146972656, 'E'),
     ('08MG026', 2004, 9, 1, 30, 2.56999993324279785, 76.9499969482421875, 21, 1.6799999475479126, 1, 8.60000038146972656, 8.60000038146972656, 'E', 3.11999988555908203, NULL, 2.43000006675720215, NULL, 2.45000004768371582, NULL, 2.08999991416931152, NULL, 1.97000002861022927, NULL, 2.09999990463256836, NULL, 2.67000007629394531, NULL, 2.53999996185302779, NULL, 4.19999980926513672, NULL, 6.21999979019165039, NULL, 2.52999997138977051, NULL, 2.08999991416931152, NULL, 1.91999995708465598, NULL, 1.98000001907348633, NULL, 2.17000007629394531, NULL, 2.79999995231628418, NULL, 2.1099998950958252, NULL, 1.88999998569488525, NULL, 1.75, NULL, 1.6799999475479126, NULL, 1.87999999523162842, NULL, 1.96000003814697288, NULL, 1.80999994277954102, NULL, 1.90999996662139893, NULL, 2, NULL, 2.13000011444091797, NULL, 2.03999996185302779, NULL, 2.07999992370605469, NULL, 1.83000004291534402, NULL, NULL, NULL),
     ('08MG026', 2004, 10, 1, 31, 3.18000006675720215, 98.5199966430664062, 31, 1.58000004291534424, 8, 16.5, 1.72000002861022949, NULL, 1.79999995231628418, NULL, 1.94000005722045898, NULL, 1.94000005722045898, NULL, 5.32999992370605469, NULL, 7.3899998664855957, NULL, 1.95000004768371604, NULL, 16.5, NULL, 7.86999988555908203, NULL, 4, NULL, 3.30999994277954102, NULL, 3.19000005722045898, NULL, 3.6400001049041748, NULL, 3.49000000953674316, NULL, 3.33999991416931152, NULL, 3.03999996185302779, NULL, 2.45000004768371582, NULL, 2.26999998092651367, NULL, 2.09999990463256836, NULL, 1.99000000953674316, NULL, 1.90999996662139893, NULL, 1.92999994754791282, NULL, 1.83000004291534402, NULL, 1.76999998092651367, NULL, 1.75999999046325684, NULL, 1.73000001907348633, NULL, 1.6799999475479126, NULL, 1.65999996662139893, NULL, 1.69000005722045898, NULL, 1.72000002861022949, NULL, 1.58000004291534424, NULL),
     ('08MG026', 2004, 11, 1, 30, 2.90000009536743208, 86.8899993896484375, 3, 1.48000001907348633, 15, 9.34000015258789062, 1.5700000524520874, NULL, 1.5700000524520874, NULL, 1.48000001907348633, NULL, 1.48000001907348633, NULL, 1.48000001907348633, NULL, 1.82000005245208762, NULL, 3.81999993324279785, NULL, 6.59000015258789062, NULL, 5.92000007629394531, NULL, 3.51999998092651367, NULL, 2.84999990463256836, NULL, 2.52999997138977051, NULL, 2.38000011444091797, NULL, 2.54999995231628418, NULL, 9.34000015258789062, NULL, 4.17000007629394531, NULL, 3.00999999046325684, NULL, 2.75999999046325684, NULL, 2.5, NULL, 2.3599998950958252, NULL, 2.25, NULL, 2.1400001049041748, NULL, 2.05999994277954102, NULL, 2.8599998950958252, NULL, 3.01999998092651367, NULL, 2.42000007629394531, NULL, 2.23000001907348633, NULL, 2.09999990463256836, NULL, 2.07999992370605469, NULL, 2.02999997138977051, NULL, NULL, NULL),
     ('08MG026', 2004, 12, 1, 31, 1.75, 54.1899986267089773, 31, 1.37000000476837158, 19, 2.40000009536743208, 1.95000004768371604, NULL, 1.91999995708465598, NULL, 1.88999998569488525, NULL, 1.87999999523162842, NULL, 1.83000004291534402, NULL, 1.78999996185302712, NULL, 1.76999998092651367, NULL, 1.75999999046325684, NULL, 1.70000004768371582, NULL, 2.02999997138977051, NULL, 2.05999994277954102, NULL, 1.55999994277954102, NULL, 1.62999999523162842, NULL, 1.75, NULL, 1.84000003337860107, NULL, 1.85000002384185791, NULL, 1.78999996185302712, NULL, 1.95000004768371604, NULL, 2.40000009536743208, NULL, 1.78999996185302712, NULL, 1.72000002861022949, NULL, 1.5700000524520874, NULL, 1.49000000953674316, NULL, 1.58000004291534424, NULL, 1.75, NULL, 1.69000005722045898, NULL, 1.5, NULL, 1.37999999523162842, NULL, 1.45000004768371582, NULL, 1.54999995231628418, NULL, 1.37000000476837158, NULL),
     ('08MG026', 2005, 1, 1, 31, 1.54999995231628418, 47.9199981689453125, 20, 1.04999995231628418, 23, 3.07999992370605469, 1.28999996185302712, NULL, 1.27999997138977051, 'B', 1.26999998092651367, 'B', 1.25, 'B', 1.3200000524520874, 'B', 1.29999995231628418, 'B', 1.27999997138977051, 'B', 1.25999999046325684, 'B', 1.25, 'B', 1.24000000953674316, 'B', 1.1799999475479126, 'B', 1.15999996662139893, 'B', 1.14999997615814209, 'B', 1.12000000476837158, 'B', 1.11000001430511475, 'B', 1.10000002384185791, 'B', 1.08000004291534424, 'B', 1.0700000524520874, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.0700000524520874, 'B', 1.11000001430511475, 'B', 3.07999992370605469, NULL, 2.96000003814697266, NULL, 2.36999988555908203, NULL, 2.22000002861022905, NULL, 2.27999997138977051, NULL, 2.04999995231628418, NULL, 2.04999995231628418, NULL, 2.33999991416931152, NULL, 2.56999993324279785, NULL),
     ('08MG026', 2005, 2, 1, 28, 1.70000004768371582, 47.5, 28, 1.44000005722045898, 2, 2.68000006675720215, 2.30999994277954102, NULL, 2.68000006675720215, NULL, 2, 'B', 1.98000001907348633, 'B', 1.95000004768371604, 'B', 1.91999995708465598, 'B', 1.87999999523162842, 'B', 1.75, 'B', 1.70000004768371582, 'B', 1.65999996662139893, 'B', 1.63999998569488525, 'B', 1.62000000476837158, 'B', 1.60000002384185791, 'B', 1.58000004291534424, 'B', 1.55999994277954102, 'B', 1.54999995231628418, 'E', 1.53999996185302712, 'E', 1.53999996185302712, 'E', 1.53999996185302712, 'E', 1.52999997138977051, 'E', 1.52999997138977051, 'E', 1.51999998092651367, 'E', 1.5, 'A', 1.53999996185302712, NULL, 1.51999998092651367, NULL, 1.47000002861022949, NULL, 1.45000004768371582, NULL, 1.44000005722045898, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2005, 3, 1, 31, 1.48000001907348633, 45.8899993896484375, 25, 1.29999995231628418, 9, 2.02999997138977051, 1.41999995708465576, NULL, 1.37999999523162842, NULL, 1.35000002384185791, NULL, 1.35000002384185791, NULL, 1.34000003337860107, NULL, 1.34000003337860107, NULL, 1.54999995231628418, NULL, 1.51999998092651367, NULL, 2.02999997138977051, NULL, 1.75, NULL, 1.89999997615814209, NULL, 1.92999994754791282, NULL, 1.73000001907348633, NULL, 1.69000005722045898, NULL, 1.63999998569488525, NULL, 1.59000003337860107, NULL, 1.46000003814697288, NULL, 1.41999995708465576, NULL, 1.40999996662139893, NULL, 1.45000004768371582, NULL, 1.36000001430511475, NULL, 1.35000002384185791, NULL, 1.3200000524520874, NULL, 1.30999994277954102, NULL, 1.29999995231628418, NULL, 1.36000001430511475, NULL, 1.37999999523162842, NULL, 1.34000003337860107, NULL, 1.30999994277954102, NULL, 1.29999995231628418, NULL, 1.30999994277954102, NULL),
     ('08MG026', 2005, 4, 1, 30, 2.31999993324279785, 69.470001220703125, 18, 1.19000005722045898, 26, 6.05999994277954102, 1.44000005722045898, NULL, 1.3200000524520874, NULL, 1.33000004291534424, NULL, 1.29999995231628418, NULL, 1.30999994277954102, NULL, 1.38999998569488525, NULL, 1.61000001430511475, NULL, 1.53999996185302712, NULL, 1.4299999475479126, NULL, 1.40999996662139893, NULL, 1.46000003814697288, NULL, 1.39999997615814209, NULL, 1.37999999523162842, NULL, 1.37999999523162842, NULL, 1.35000002384185791, NULL, 1.39999997615814209, NULL, 1.20000004768371582, NULL, 1.19000005722045898, NULL, 1.19000005722045898, NULL, 1.4299999475479126, NULL, 2.21000003814697266, NULL, 3.18000006675720215, NULL, 4.01000022888183594, NULL, 4.71999979019165039, NULL, 5.23999977111816406, NULL, 6.05999994277954102, NULL, 5.84000015258789062, NULL, 4.3600001335144043, NULL, 3.5, NULL, 2.8900001049041748, NULL, NULL, NULL),
     ('08MG026', 2005, 5, 1, 31, 5.40000009536743164, 167.449996948242188, 1, 2.61999988555908203, 15, 9.43000030517577947, 2.61999988555908203, NULL, 2.65000009536743208, NULL, 2.88000011444091797, NULL, 2.84999990463256836, NULL, 3.02999997138977051, NULL, 3.25999999046325684, NULL, 3.04999995231628418, NULL, 2.8599998950958252, NULL, 3.40000009536743208, NULL, 4.51999998092651367, NULL, 5.01999998092651367, NULL, 4.82999992370605469, NULL, 4.69999980926513672, NULL, 6.09000015258789062, NULL, 9.43000030517577947, NULL, 7.78999996185302734, NULL, 6.71999979019165039, NULL, 6.42999982833862305, NULL, 6.69000005722045898, NULL, 6.28999996185302734, NULL, 5.55999994277954102, NULL, 5.42999982833862305, NULL, 5.01999998092651367, NULL, 4.76999998092651367, NULL, 4.78000020980834961, NULL, 5.57000017166137695, NULL, 6.94999980926513672, NULL, 7.86999988555908203, NULL, 8.30000019073486328, NULL, 9.13000011444091797, NULL, 8.96000003814697266, NULL),
     ('08MG026', 2005, 6, 1, 30, 5.90999984741210938, 177.419998168945312, 15, 3.77999997138977051, 22, 8.59000015258789062, 7.55999994277954102, NULL, 6.73999977111816406, NULL, 6.59000015258789062, NULL, 6.21000003814697266, NULL, 6.01999998092651367, NULL, 5.38000011444091797, NULL, 4.82999992370605469, NULL, 4.6399998664855957, NULL, 4.63000011444091797, NULL, 4.42000007629394531, NULL, 4.3899998664855957, NULL, 4.30999994277954102, NULL, 4.17000007629394531, NULL, 3.92000007629394487, NULL, 3.77999997138977051, NULL, 3.78999996185302734, NULL, 5.30000019073486328, NULL, 6.46999979019165039, NULL, 5.8899998664855957, NULL, 6.03000020980834961, NULL, 6.63000011444091797, NULL, 8.59000015258789062, NULL, 7.55000019073486328, NULL, 6.90999984741210938, NULL, 6.57999992370605469, NULL, 6.44000005722045898, NULL, 6.88000011444091797, NULL, 7.51999998092651367, NULL, 7.40999984741210938, NULL, 7.84000015258789062, NULL, NULL, NULL),
     ('08MG026', 2005, 7, 1, 31, 8.85999965667724609, 274.600006103515625, 3, 5.76999998092651367, 6, 12.8999996185302717, 7.38000011444091797, NULL, 6.30999994277954102, NULL, 5.76999998092651367, NULL, 5.76999998092651367, NULL, 7.51999998092651367, NULL, 12.8999996185302717, NULL, 9.85000038146972834, NULL, 11.8000001907348633, NULL, 8.52999973297119141, NULL, 8.05000019073486328, NULL, 7.90999984741210938, NULL, 11.5, NULL, 10.1000003814697283, NULL, 9.22000026702880859, NULL, 10.1999998092651367, NULL, 10.3999996185302717, NULL, 11.1999998092651367, NULL, 10.3000001907348633, NULL, 11.1999998092651367, NULL, 10.3000001907348633, NULL, 9.48999977111816406, NULL, 8.19999980926513672, NULL, 7.8600001335144043, NULL, 7.55000019073486328, NULL, 7.32000017166137695, NULL, 7.40000009536743164, NULL, 7.80000019073486328, NULL, 8, NULL, 8.31999969482421875, NULL, 8.47000026702880859, NULL, 7.98000001907348633, NULL),
     ('08MG026', 2005, 8, 1, 31, 5.84999990463256836, 181.210006713867188, 30, 3.57999992370605469, 1, 8.42000007629394531, 8.42000007629394531, NULL, 6.57999992370605469, NULL, 6.3600001335144043, NULL, 6.55999994277954102, NULL, 6.86999988555908203, NULL, 7.15999984741210938, NULL, 7.07999992370605469, NULL, 6.73999977111816406, NULL, 6.84999990463256836, NULL, 6.71000003814697266, NULL, 6.59000015258789062, NULL, 6.57999992370605469, NULL, 6.48000001907348633, NULL, 6.40999984741210938, NULL, 6.57999992370605469, NULL, 6.76000022888183594, NULL, 7.67999982833862305, NULL, 5.6100001335144043, NULL, 5.32999992370605469, NULL, 5.38000011444091797, NULL, 5.51000022888183594, NULL, 4.65999984741210938, NULL, 4.17000007629394531, NULL, 4.01999998092651367, NULL, 4.32000017166137695, NULL, 4.30999994277954102, NULL, 4.40000009536743164, NULL, 5.92999982833862305, NULL, 3.94000005722045898, NULL, 3.57999992370605469, NULL, 3.6400001049041748, NULL),
     ('08MG026', 2005, 9, 1, 30, 2.36999988555908203, 70.970001220703125, 23, 1.23000001907348633, 29, 4.78000020980834961, 3.95000004768371582, NULL, 4.44999980926513672, NULL, 3.6400001049041748, NULL, 3.50999999046325684, NULL, 2.56999993324279785, NULL, 2.41000008583068848, NULL, 2.49000000953674316, NULL, 3.20000004768371582, NULL, 2.41000008583068848, NULL, 1.97000002861022927, NULL, 2.16000008583068848, NULL, 2.5, NULL, 2.42000007629394531, NULL, 2.49000000953674316, NULL, 2.68000006675720215, NULL, 2.42000007629394531, NULL, 2.00999999046325684, NULL, 1.89999997615814209, NULL, 2.15000009536743208, NULL, 1.50999999046325684, NULL, 1.34000003337860107, NULL, 1.26999998092651367, NULL, 1.23000001907348633, NULL, 1.23000001907348633, NULL, 1.27999997138977051, NULL, 1.38999998569488525, NULL, 1.30999994277954102, NULL, 1.46000003814697288, NULL, 4.78000020980834961, NULL, 2.83999991416931152, NULL, NULL, NULL),
     ('08MG026', 2005, 10, 1, 31, 3.08999991416931152, 95.6699981689453267, 9, 1.24000000953674316, 15, 10.3000001907348633, 1.69000005722045898, NULL, 1.39999997615814209, NULL, 1.35000002384185791, NULL, 1.27999997138977051, NULL, 1.25999999046325684, NULL, 1.53999996185302712, NULL, 1.69000005722045898, NULL, 1.3200000524520874, NULL, 1.24000000953674316, NULL, 1.86000001430511475, NULL, 1.50999999046325684, NULL, 1.45000004768371582, NULL, 1.52999997138977051, NULL, 3.49000000953674316, NULL, 10.3000001907348633, NULL, 5.17000007629394531, NULL, 8.09000015258789062, NULL, 4.90999984741210938, NULL, 4.75, NULL, 4.25, NULL, 3.40000009536743208, NULL, 4.23000001907348633, NULL, 5.21999979019165039, NULL, 3.50999999046325684, NULL, 3.46000003814697266, NULL, 3.06999993324279785, NULL, 2.6099998950958252, NULL, 2.65000009536743208, NULL, 2.51999998092651367, NULL, 2.36999988555908203, NULL, 2.54999995231628418, NULL),
     ('08MG026', 2005, 11, 1, 30, 2.17000007629394531, 65.2399978637695312, 30, 1.64999997615814209, 10, 4.23000001907348633, 2.5, NULL, 2.38000011444091797, NULL, 2.36999988555908203, NULL, 2.25999999046325684, NULL, 2.16000008583068848, NULL, 2.09999990463256836, NULL, 2.05999994277954102, NULL, 2.02999997138977051, NULL, 2.05999994277954102, NULL, 4.23000001907348633, NULL, 3.19000005722045898, NULL, 2.46000003814697266, NULL, 2.25999999046325684, NULL, 2.08999991416931152, NULL, 2.01999998092651367, NULL, 1.95000004768371604, NULL, 1.87999999523162842, NULL, 1.89999997615814209, NULL, 1.97000002861022927, NULL, 2.03999996185302779, NULL, 2.03999996185302779, NULL, 2.05999994277954102, NULL, 2.02999997138977051, NULL, 2, NULL, 2.1400001049041748, NULL, 2, NULL, 1.87000000476837203, NULL, 1.76999998092651367, NULL, 1.76999998092651367, NULL, 1.64999997615814209, NULL, NULL, NULL),
     ('08MG026', 2005, 12, 1, 31, 2.79999995231628418, 86.75, 18, 1.23000001907348633, 25, 12.1000003814697283, 1.59000003337860107, NULL, 1.55999994277954102, NULL, 1.47000002861022949, NULL, 1.5, NULL, 1.52999997138977051, NULL, 1.4299999475479126, NULL, 1.38999998569488525, NULL, 1.37000000476837158, NULL, 1.37999999523162842, NULL, 1.37999999523162842, NULL, 1.37000000476837158, NULL, 1.33000004291534424, NULL, 1.29999995231628418, NULL, 1.27999997138977051, NULL, 1.26999998092651367, NULL, 1.26999998092651367, NULL, 1.25, NULL, 1.23000001907348633, NULL, 1.26999998092651367, NULL, 2.20000004768371582, NULL, 3.75, NULL, 4.09999990463256836, NULL, 2.95000004768371582, NULL, 8.42000007629394531, NULL, 12.1000003814697283, NULL, 6.42000007629394531, NULL, 5.09999990463256836, NULL, 4.38000011444091797, NULL, 3.95000004768371582, NULL, 3.72000002861022949, NULL, 3.49000000953674316, NULL),
     ('08MG026', 2006, 1, 1, 31, 2.49000000953674316, 77.1299972534179688, 31, 1.66999995708465576, 7, 3.55999994277954102, 3.41000008583068848, NULL, 3.33999991416931152, NULL, 3.09999990463256836, NULL, 3.00999999046325684, NULL, 3.47000002861022905, NULL, 3.49000000953674316, NULL, 3.55999994277954102, NULL, 3.23000001907348633, NULL, 3.09999990463256836, NULL, 2.96000003814697266, NULL, 2.75, NULL, 2.54999995231628418, NULL, 2.68000006675720215, NULL, 2.69000005722045898, NULL, 2.45000004768371582, NULL, 2.3900001049041748, NULL, 2.42000007629394531, NULL, 2.26999998092651367, NULL, 2.09999990463256836, NULL, 2.05999994277954102, NULL, 1.94000005722045898, NULL, 1.90999996662139893, NULL, 1.89999997615814209, NULL, 1.87000000476837203, NULL, 1.90999996662139893, NULL, 1.85000002384185791, NULL, 1.75999999046325684, NULL, 1.83000004291534402, NULL, 1.72000002861022949, NULL, 1.74000000953674316, NULL, 1.66999995708465576, NULL),
     ('08MG026', 2006, 2, 1, 28, 1.25, 34.9129981994628906, 24, 0.902999997138977051, 4, 1.83000004291534402, 1.66999995708465576, NULL, 1.61000001430511475, NULL, 1.59000003337860107, NULL, 1.83000004291534402, NULL, 1.60000002384185791, NULL, 1.54999995231628418, NULL, 1.52999997138977051, NULL, 1.51999998092651367, NULL, 1.36000001430511475, NULL, 1.34000003337860107, NULL, 1.39999997615814209, NULL, 1.39999997615814209, NULL, 1.37999999523162842, NULL, 1.1799999475479126, NULL, 1.09000003337860107, NULL, 1.08000004291534424, NULL, 0.938000023365020752, NULL, 1.00999999046325684, NULL, 1.03999996185302712, NULL, 1.00999999046325684, NULL, 0.981000006198883168, NULL, 0.986000001430511586, NULL, 0.935000002384185791, NULL, 0.902999997138977051, NULL, 0.907000005245208851, NULL, 0.922999978065490834, NULL, 1.09000003337860107, NULL, 1.05999994277954102, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2006, 3, 1, 31, 0.995999991893768422, 30.8740005493164062, 5, 0.904999971389770397, 24, 1.1799999475479126, 1.02999997138977051, NULL, 0.994000017642974854, NULL, 0.91000002622604359, NULL, 0.906000018119812012, NULL, 0.904999971389770397, NULL, 0.927999973297119252, NULL, 0.998000025749206432, NULL, 0.962000012397766002, NULL, 0.920000016689300426, NULL, 0.907000005245208851, NULL, 0.948000013828277588, NULL, 0.935000002384185791, NULL, 0.926999986171722412, NULL, 0.939000010490417591, NULL, 0.953000009059906006, NULL, 0.961000025272369385, NULL, 0.930000007152557373, NULL, 0.933000028133392445, NULL, 0.935999989509582409, NULL, 0.986000001430511586, NULL, 0.966000020503997803, NULL, 1.00999999046325684, NULL, 1.01999998092651367, NULL, 1.1799999475479126, NULL, 1.16999995708465576, NULL, 1.10000002384185791, NULL, 1.13999998569488525, NULL, 1.09000003337860107, NULL, 1.05999994277954102, NULL, 1.08000004291534424, NULL, 1.14999997615814209, NULL),
     ('08MG026', 2006, 4, 1, 30, 1.86000001430511475, 55.7999992370605469, 1, 1.12999999523162842, 29, 4.65999984741210938, 1.12999999523162842, NULL, 1.20000004768371582, NULL, 1.13999998569488525, NULL, 1.24000000953674316, NULL, 1.29999995231628418, NULL, 1.37999999523162842, NULL, 1.37999999523162842, NULL, 1.46000003814697288, NULL, 1.54999995231628418, NULL, 1.66999995708465576, NULL, 1.70000004768371582, NULL, 1.78999996185302712, NULL, 1.80999994277954102, NULL, 1.78999996185302712, NULL, 1.60000002384185791, NULL, 1.48000001907348633, NULL, 1.33000004291534424, NULL, 1.28999996185302712, NULL, 1.35000002384185791, NULL, 1.50999999046325684, NULL, 1.84000003337860107, NULL, 1.66999995708465576, NULL, 1.6799999475479126, NULL, 1.92999994754791282, NULL, 2.5, NULL, 2.72000002861022905, NULL, 2.47000002861022905, NULL, 2.68000006675720215, NULL, 4.65999984741210938, NULL, 4.55000019073486328, NULL, NULL, NULL),
     ('08MG026', 2006, 5, 1, 31, 5.82999992370605469, 180.759994506835966, 3, 3.00999999046325684, 17, 9.82999992370605646, 3.57999992370605469, NULL, 3.1099998950958252, NULL, 3.00999999046325684, NULL, 3.22000002861022905, NULL, 3.74000000953674316, NULL, 3.97000002861022949, NULL, 3.75, NULL, 3.47000002861022905, NULL, 3.22000002861022905, NULL, 3.34999990463256836, NULL, 3.50999999046325684, NULL, 3.45000004768371582, NULL, 3.29999995231628418, NULL, 3.44000005722045898, NULL, 4.53000020980834961, NULL, 8.02999973297119141, NULL, 9.82999992370605646, NULL, 9.13000011444091797, NULL, 9.68000030517577947, NULL, 9.17000007629394354, NULL, 7.71000003814697266, NULL, 8.02000045776367188, NULL, 8, NULL, 7.84000015258789062, NULL, 7.48000001907348633, NULL, 7.05999994277954102, NULL, 7.13000011444091797, NULL, 7.53000020980834961, NULL, 7.11999988555908203, NULL, 7.1100001335144043, NULL, 7.26999998092651367, NULL),
     ('08MG026', 2006, 6, 1, 30, 8.5, 255.07000732421875, 26, 7.07000017166137695, 2, 13.5, 8.77000045776367188, NULL, 13.5, NULL, 11.8000001907348633, NULL, 10.6999998092651367, NULL, 9.47000026702880859, NULL, 9.18000030517577947, NULL, 8.93999958038330078, NULL, 9.14999961853027166, NULL, 8.75, NULL, 7.84999990463256836, NULL, 8.02000045776367188, NULL, 8.11999988555908203, NULL, 8.18999958038330078, NULL, 8.48999977111816406, NULL, 7.76000022888183594, NULL, 8.01000022888183594, NULL, 8.80000019073486328, NULL, 8.61999988555908203, NULL, 7.8899998664855957, NULL, 7.59000015258789062, NULL, 7.36999988555908203, NULL, 7.19999980926513672, NULL, 7.23000001907348633, NULL, 7.8899998664855957, NULL, 8.18000030517578125, NULL, 7.07000017166137695, NULL, 7.71000003814697266, NULL, 7.90000009536743164, NULL, 7.3899998664855957, NULL, 7.53000020980834961, NULL, NULL, NULL),
     ('08MG026', 2006, 7, 1, 31, 6.67000007629394531, 206.779998779296875, 19, 5.11999988555908203, 24, 8.89000034332275391, 7.65000009536743164, NULL, 7.53000020980834961, NULL, 7.26000022888183594, NULL, 6.80999994277954102, NULL, 6.6100001335144043, NULL, 6.92999982833862305, NULL, 6.38000011444091797, NULL, 6.67000007629394531, NULL, 8.09000015258789062, NULL, 6.28000020980834961, NULL, 6.19999980926513672, NULL, 6.42999982833862305, NULL, 5.94999980926513672, NULL, 5.90999984741210938, NULL, 5.86999988555908203, NULL, 5.55999994277954102, NULL, 5.48999977111816406, NULL, 5.26000022888183594, NULL, 5.11999988555908203, NULL, 5.42000007629394531, NULL, 6.73000001907348633, NULL, 7.71000003814697266, NULL, 7.61999988555908203, NULL, 8.89000034332275391, NULL, 8.36999988555908203, NULL, 7.88000011444091797, 'A', 7.71999979019165039, NULL, 7.21999979019165039, NULL, 6.40000009536743164, NULL, 5.65999984741210938, NULL, 5.15999984741210938, NULL),
     ('08MG026', 2006, 8, 1, 31, 4.80999994277954102, 149.199996948242188, 31, 3.21000003814697266, 15, 5.75, 4.86999988555908203, NULL, 4.67999982833862305, NULL, 4.75, NULL, 4.80000019073486328, NULL, 4.8899998664855957, NULL, 5.15999984741210938, NULL, 5.23000001907348633, NULL, 5.07000017166137695, NULL, 5.44000005722045898, NULL, 5.69999980926513672, NULL, 4.96999979019165039, NULL, 4.76999998092651367, NULL, 4.92000007629394531, NULL, 5.40000009536743164, NULL, 5.75, NULL, 5.42999982833862305, NULL, 5.03999996185302734, NULL, 4.90000009536743164, NULL, 4.96000003814697266, NULL, 5.01000022888183594, NULL, 4.71000003814697266, NULL, 4.71000003814697266, NULL, 4.75, NULL, 4.59000015258789062, NULL, 4.53000020980834961, NULL, 4.48000001907348633, NULL, 4.53000020980834961, NULL, 4.3899998664855957, NULL, 4.11999988555908203, NULL, 3.44000005722045898, NULL, 3.21000003814697266, NULL),
     ('08MG026', 2006, 9, 1, 30, 3.32999992370605469, 99.8799972534179545, 22, 2.13000011444091797, 18, 4.71000003814697266, 3.49000000953674316, NULL, 3.76999998092651367, NULL, 4.09999990463256836, NULL, 4.3600001335144043, NULL, 4.34000015258789062, NULL, 4.30999994277954102, NULL, 4.28000020980834961, NULL, 3.94000005722045898, NULL, 3.86999988555908203, NULL, 3.75, NULL, 4, NULL, 3.93000006675720215, NULL, 3.5, NULL, 2.8599998950958252, NULL, 2.42000007629394531, NULL, 2.15000009536743208, NULL, 2.31999993324279785, NULL, 4.71000003814697266, NULL, 3.32999992370605469, NULL, 2.86999988555908203, NULL, 2.43000006675720215, NULL, 2.13000011444091797, NULL, 2.5, NULL, 2.79999995231628418, NULL, 2.73000001907348633, NULL, 3, NULL, 3.45000004768371582, NULL, 3.26999998092651367, NULL, 2.83999991416931152, NULL, 2.43000006675720215, NULL, NULL, NULL),
     ('08MG026', 2006, 10, 1, 31, 1.61000001430511475, 50.0499992370605469, 31, 1.11000001430511475, 27, 2.38000011444091797, 2.09999990463256836, NULL, 1.83000004291534402, NULL, 1.69000005722045898, NULL, 1.5, 'A', 1.45000004768371582, 'A', 1.75999999046325684, NULL, 1.5, 'A', 1.45000004768371582, 'A', 1.39999997615814209, 'E', 1.47000002861022949, 'A', 1.70000004768371582, NULL, 1.87999999523162842, NULL, 1.78999996185302712, NULL, 1.74000000953674316, NULL, 2.05999994277954102, NULL, 1.78999996185302712, NULL, 1.47000002861022949, NULL, 1.41999995708465576, NULL, 1.49000000953674316, NULL, 1.40999996662139893, NULL, 1.3200000524520874, NULL, 1.27999997138977051, NULL, 1.26999998092651367, NULL, 1.37000000476837158, NULL, 1.37000000476837158, NULL, 1.87000000476837203, NULL, 2.38000011444091797, NULL, 2.17000007629394531, NULL, 1.84000003337860107, NULL, 1.16999995708465576, NULL, 1.11000001430511475, NULL),
     ('08MG026', 2006, 11, 1, 30, 2.77999997138977051, 83.339996337890625, 1, 1.25, 6, 8.14000034332275391, 1.25, NULL, 1.37000000476837158, NULL, 3.45000004768371582, NULL, 5.51999998092651367, NULL, 4.28999996185302734, NULL, 8.14000034332275391, NULL, 5.13000011444091797, NULL, 3.27999997138977051, NULL, 2.66000008583068848, NULL, 2.43000006675720215, NULL, 2.25, NULL, 2.13000011444091797, NULL, 2.04999995231628418, NULL, 1.88999998569488525, NULL, 2.96000003814697266, NULL, 3.17000007629394531, NULL, 2.58999991416931152, NULL, 2.3599998950958252, NULL, 3.34999990463256836, NULL, 3.1400001049041748, NULL, 2.73000001907348633, NULL, 2.45000004768371582, NULL, 2.29999995231628418, NULL, 2.13000011444091797, NULL, 1.97000002861022927, NULL, 1.85000002384185791, NULL, 1.64999997615814209, NULL, 1.45000004768371582, NULL, 1.63999998569488525, NULL, 1.75999999046325684, NULL, NULL, NULL),
     ('08MG026', 2006, 12, 1, 31, 1.50999999046325684, 46.75, 30, 1.27999997138977051, 13, 1.75, 1.65999996662139893, NULL, 1.52999997138977051, NULL, 1.53999996185302712, NULL, 1.54999995231628418, NULL, 1.50999999046325684, NULL, 1.5, NULL, 1.50999999046325684, NULL, 1.5700000524520874, NULL, 1.54999995231628418, NULL, 1.53999996185302712, NULL, 1.70000004768371582, NULL, 1.71000003814697288, NULL, 1.75, NULL, 1.72000002861022949, NULL, 1.66999995708465576, NULL, 1.52999997138977051, NULL, 1.48000001907348633, NULL, 1.46000003814697288, NULL, 1.46000003814697288, NULL, 1.47000002861022949, NULL, 1.58000004291534424, NULL, 1.47000002861022949, NULL, 1.45000004768371582, NULL, 1.46000003814697288, NULL, 1.4299999475479126, NULL, 1.40999996662139893, NULL, 1.36000001430511475, NULL, 1.29999995231628418, NULL, 1.30999994277954102, NULL, 1.27999997138977051, NULL, 1.28999996185302712, NULL),
     ('08MG026', 2007, 1, 1, 31, 1.29999995231628418, 40.2799987792968821, 31, 1.11000001430511475, 2, 1.78999996185302712, 1.33000004291534424, NULL, 1.78999996185302712, NULL, 1.69000005722045898, NULL, 1.51999998092651367, NULL, 1.49000000953674316, NULL, 1.46000003814697288, NULL, 1.45000004768371582, NULL, 1.41999995708465576, NULL, 1.49000000953674316, NULL, 1.41999995708465576, NULL, 1.20000004768371582, NULL, 1.24000000953674316, NULL, 1.3200000524520874, NULL, 1.27999997138977051, NULL, 1.33000004291534424, NULL, 1.30999994277954102, NULL, 1.23000001907348633, NULL, 1.21000003814697288, NULL, 1.19000005722045898, NULL, 1.15999996662139893, NULL, 1.14999997615814209, NULL, 1.19000005722045898, NULL, 1.23000001907348633, NULL, 1.21000003814697288, NULL, 1.19000005722045898, NULL, 1.14999997615814209, NULL, 1.13999998569488525, NULL, 1.13999998569488525, NULL, 1.12000000476837158, NULL, 1.12000000476837158, NULL, 1.11000001430511475, NULL),
     ('08MG026', 2007, 2, 1, 28, 1.09000003337860107, 30.5259990692138672, 28, 0.958999991416931152, 18, 1.16999995708465576, 1.10000002384185791, NULL, 1.08000004291534424, NULL, 1.08000004291534424, NULL, 1.10000002384185791, NULL, 1.09000003337860107, NULL, 1.10000002384185791, NULL, 1.11000001430511475, NULL, 1.11000001430511475, NULL, 1.11000001430511475, NULL, 1.12000000476837158, NULL, 1.12000000476837158, NULL, 1.12000000476837158, NULL, 1.12000000476837158, NULL, 1.11000001430511475, NULL, 1.15999996662139893, NULL, 1.12000000476837158, NULL, 1.15999996662139893, NULL, 1.16999995708465576, NULL, 1.13999998569488525, NULL, 1.11000001430511475, NULL, 1.08000004291534424, NULL, 1.05999994277954102, NULL, 1.04999995231628418, NULL, 1.03999996185302712, NULL, 1.02999997138977051, NULL, 1, NULL, 0.976999998092651367, NULL, 0.958999991416931152, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2007, 3, 1, 31, 2.3900001049041748, 74.0120010375976562, 1, 0.90799999237060558, 12, 4.3899998664855957, 0.90799999237060558, NULL, 0.945999979972839355, NULL, 0.935000002384185791, NULL, 0.916999995708465576, NULL, 0.916000008583068848, NULL, 0.959999978542327992, NULL, 1.29999995231628418, NULL, 1.21000003814697288, NULL, 1.14999997615814209, NULL, 1.25999999046325684, NULL, 2.73000001907348633, NULL, 4.3899998664855957, NULL, 3.13000011444091797, NULL, 3.25999999046325684, NULL, 2.83999991416931152, NULL, 2.70000004768371582, NULL, 2.97000002861022905, NULL, 3.08999991416931152, NULL, 3.6400001049041748, NULL, 3.58999991416931152, NULL, 3.16000008583068848, NULL, 2.97000002861022905, NULL, 2.90000009536743208, NULL, 3.21000003814697266, NULL, 3.23000001907348633, NULL, 2.96000003814697266, NULL, 2.76999998092651367, NULL, 2.63000011444091797, NULL, 2.52999997138977051, NULL, 2.43000006675720215, NULL, 2.38000011444091797, NULL),
     ('08MG026', 2007, 4, 1, 30, 2.19000005722045898, 65.5999984741210938, 21, 1.75999999046325684, 9, 2.97000002861022905, 2.25999999046325684, NULL, 2.1400001049041748, NULL, 2.05999994277954102, NULL, 1.94000005722045898, NULL, 1.95000004768371604, NULL, 2, NULL, 2.27999997138977051, NULL, 2.81999993324279785, NULL, 2.97000002861022905, NULL, 2.70000004768371582, NULL, 2.5, NULL, 2.30999994277954102, NULL, 2.27999997138977051, NULL, 2.25, NULL, 2.18000006675720215, NULL, 2.06999993324279785, NULL, 1.98000001907348633, NULL, 1.86000001430511475, NULL, 1.82000005245208762, NULL, 1.76999998092651367, NULL, 1.75999999046325684, NULL, 1.75999999046325684, NULL, 1.82000005245208762, NULL, 2.04999995231628418, NULL, 2.07999992370605469, NULL, 2.08999991416931152, NULL, 2.52999997138977051, NULL, 2.6400001049041748, NULL, 2.40000009536743208, NULL, 2.32999992370605469, NULL, NULL, NULL),
     ('08MG026', 2007, 5, 1, 31, 4.80000019073486328, 148.699996948242188, 1, 2.30999994277954102, 31, 8.32999992370605469, 2.30999994277954102, NULL, 2.51999998092651367, NULL, 2.54999995231628418, NULL, 2.45000004768371582, NULL, 2.45000004768371582, NULL, 2.52999997138977051, NULL, 2.79999995231628418, NULL, 3.54999995231628418, NULL, 3.95000004768371582, NULL, 3.8599998950958252, NULL, 4.03000020980834961, NULL, 4.28999996185302734, NULL, 4.48999977111816406, NULL, 4.6399998664855957, NULL, 5.26000022888183594, NULL, 5.94999980926513672, NULL, 5.86999988555908203, NULL, 5.48000001907348633, NULL, 5.3899998664855957, NULL, 4.92999982833862305, NULL, 4.63000011444091797, NULL, 4.73999977111816406, NULL, 5.26000022888183594, NULL, 5.73999977111816406, NULL, 6.15999984741210938, NULL, 6.6399998664855957, NULL, 6.71999979019165039, NULL, 6.53000020980834961, NULL, 6.94999980926513672, NULL, 7.69999980926513672, NULL, 8.32999992370605469, NULL),
     ('08MG026', 2007, 6, 1, 30, 8.96000003814697266, 268.69000244140625, 12, 7.90000009536743164, 20, 10.3000001907348633, 8.71000003814697266, NULL, 8.96000003814697266, NULL, 9.43000030517577947, 'A', 9.90999984741210938, 'A', 8.92000007629394531, NULL, 9.14999961853027166, NULL, 9.03999996185302734, NULL, 8.77999973297119141, NULL, 8.93999958038330078, NULL, 9.23999977111816406, NULL, 8.26000022888183594, NULL, 7.90000009536743164, NULL, 8.38000011444091797, NULL, 7.96999979019165039, NULL, 8.13000011444091797, NULL, 7.94000005722045898, NULL, 8.07999992370605469, NULL, 7.98999977111816406, NULL, 8.17000007629394531, NULL, 10.3000001907348633, NULL, 10.1000003814697283, NULL, 10.1000003814697283, NULL, 9.60999965667724609, NULL, 9.21000003814697266, NULL, 8.69999980926513672, NULL, 8.55000019073486328, NULL, 8.89000034332275391, NULL, 9.88000011444091797, NULL, 10.1000003814697283, NULL, 9.35000038146972834, NULL, NULL, NULL),
     ('08MG026', 2007, 7, 1, 31, 9.69999980926513672, 300.559997558593693, 31, 6.48999977111816406, 22, 13.5, 9.27999973297119141, NULL, 9.25, NULL, 9.73999977111816406, NULL, 9.94999980926513672, NULL, 9.61999988555908203, NULL, 9.51000022888183594, NULL, 9.10000038146972834, NULL, 8.97999954223632812, NULL, 9.03999996185302734, NULL, 9.44999980926513672, NULL, 10.3999996185302717, NULL, 10.5, NULL, 11, NULL, 11.5, NULL, 11.6000003814697283, NULL, 11.1999998092651367, NULL, 10.6000003814697283, NULL, 10.5, NULL, 10.8999996185302717, NULL, 10.6000003814697283, NULL, 11.3999996185302717, NULL, 13.5, NULL, 11.1000003814697283, NULL, 9.68999958038330078, NULL, 8.30000019073486328, NULL, 8.14000034332275391, NULL, 7.73999977111816406, NULL, 7.30000019073486328, NULL, 7.26999998092651367, NULL, 6.90999984741210938, NULL, 6.48999977111816406, NULL),
     ('08MG026', 2007, 8, 1, 31, 5.61999988555908203, 174.229995727539062, 28, 4.67999982833862305, 2, 6.69000005722045898, 6.48000001907348633, NULL, 6.69000005722045898, NULL, 6.6100001335144043, NULL, 6.34000015258789062, NULL, 6.44000005722045898, NULL, 6.59000015258789062, NULL, 6.48999977111816406, NULL, 6.05999994277954102, NULL, 5.94000005722045898, NULL, 6.19999980926513672, NULL, 5.55999994277954102, NULL, 5.51000022888183594, NULL, 5.30000019073486328, NULL, 5.28000020980834961, NULL, 5.48000001907348633, NULL, 5.6100001335144043, NULL, 5.51999998092651367, NULL, 5.30999994277954102, NULL, 5.07999992370605469, NULL, 5, NULL, 5.05000019073486328, NULL, 5.09000015258789062, NULL, 5.09000015258789062, NULL, 5.15000009536743164, NULL, 5.32000017166137695, NULL, 5.3600001335144043, NULL, 4.92000007629394531, NULL, 4.67999982833862305, NULL, 5.17999982833862305, NULL, 5.46999979019165039, NULL, 5.42999982833862305, NULL),
     ('08MG026', 2007, 9, 1, 30, 4.1399998664855957, 124.120002746582045, 24, 3.26999998092651367, 4, 5.32000017166137695, 5.01000022888183594, NULL, 4.96999979019165039, NULL, 5.25, 'A', 5.32000017166137695, NULL, 5.15999984741210938, NULL, 4.8899998664855957, NULL, 4.59999990463256836, NULL, 4.3600001335144043, NULL, 4.28999996185302734, NULL, 4.63000011444091797, NULL, 4.8600001335144043, NULL, 4.71999979019165039, NULL, 4.36999988555908203, NULL, 4.28999996185302734, NULL, 4.21999979019165039, NULL, 4.05999994277954102, NULL, 3.81999993324279785, NULL, 3.65000009536743208, NULL, 3.52999997138977051, NULL, 3.51999998092651367, NULL, 3.5, NULL, 3.54999995231628418, NULL, 3.34999990463256836, NULL, 3.26999998092651367, NULL, 3.26999998092651367, NULL, 3.31999993324279785, NULL, 3.76999998092651367, NULL, 3.59999990463256836, NULL, 3.33999991416931152, NULL, 3.63000011444091797, 'A', NULL, NULL),
     ('08MG026', 2007, 10, 1, 31, 3.52999997138977051, 109.550003051757798, 20, 2.55999994277954102, 10, 6.61999988555908203, 3.63000011444091797, NULL, 3.93000006675720215, NULL, 3.55999994277954102, NULL, 3.3599998950958252, NULL, 3.24000000953674316, NULL, 3.23000001907348633, NULL, 5.19999980926513672, NULL, 4.44000005722045898, NULL, 5.51000022888183594, NULL, 6.61999988555908203, NULL, 3.78999996185302734, NULL, 3.24000000953674316, NULL, 2.95000004768371582, NULL, 2.81999993324279785, NULL, 2.8900001049041748, NULL, 3.21000003814697266, NULL, 2.75999999046325684, NULL, 2.70000004768371582, NULL, 2.63000011444091797, NULL, 2.55999994277954102, NULL, 2.56999993324279785, NULL, 3.36999988555908203, NULL, 4.6399998664855957, NULL, 5.05999994277954102, NULL, 3.63000011444091797, NULL, 3.18000006675720215, NULL, 2.99000000953674316, NULL, 3.17000007629394531, NULL, 3.18000006675720215, NULL, 2.81999993324279785, NULL, 2.67000007629394531, NULL),
     ('08MG026', 2007, 11, 1, 30, 2.40000009536743208, 71.8499984741210938, 30, 1.76999998092651367, 9, 3.25, 2.54999995231628418, NULL, 2.46000003814697266, NULL, 2.50999999046325684, NULL, 2.54999995231628418, NULL, 2.3599998950958252, NULL, 2.32999992370605469, NULL, 2.34999990463256836, NULL, 2.38000011444091797, NULL, 3.25, NULL, 2.94000005722045898, NULL, 2.73000001907348633, NULL, 3.01999998092651367, NULL, 2.78999996185302779, NULL, 2.59999990463256836, NULL, 2.67000007629394531, NULL, 2.78999996185302779, NULL, 2.61999988555908203, NULL, 2.49000000953674316, NULL, 2.36999988555908203, NULL, 2.26999998092651367, NULL, 2.19000005722045898, NULL, 2.1099998950958252, NULL, 2.04999995231628418, NULL, 2.00999999046325684, NULL, 1.96000003814697288, NULL, 2, NULL, 1.97000002861022927, NULL, 1.88999998569488525, NULL, 1.87000000476837203, NULL, 1.76999998092651367, NULL, NULL, NULL),
     ('08MG026', 2007, 12, 1, 31, 1.87000000476837203, 58.0900001525878906, 31, 1.38999998569488525, 4, 4.88000011444091797, 1.78999996185302712, NULL, 1.84000003337860107, NULL, 2.68000006675720215, NULL, 4.88000011444091797, NULL, 3.19000005722045898, NULL, 2.56999993324279785, NULL, 2.23000001907348633, NULL, 2.03999996185302779, NULL, 1.98000001907348633, NULL, 1.83000004291534402, NULL, 1.80999994277954102, NULL, 1.75999999046325684, NULL, 1.74000000953674316, NULL, 1.75999999046325684, NULL, 1.74000000953674316, NULL, 1.70000004768371582, NULL, 1.65999996662139893, NULL, 1.62000000476837158, NULL, 1.59000003337860107, NULL, 1.55999994277954102, NULL, 1.54999995231628418, NULL, 1.54999995231628418, NULL, 1.50999999046325684, NULL, 1.48000001907348633, NULL, 1.47000002861022949, NULL, 1.45000004768371582, NULL, 1.44000005722045898, NULL, 1.44000005722045898, NULL, 1.4299999475479126, NULL, 1.40999996662139893, NULL, 1.38999998569488525, NULL),
     ('08MG026', 2008, 1, 1, 31, 1.33000004291534424, 41.3600006103515625, 24, 1.14999997615814209, 3, 1.5700000524520874, 1.53999996185302712, NULL, 1.55999994277954102, NULL, 1.5700000524520874, NULL, 1.53999996185302712, NULL, 1.51999998092651367, NULL, 1.49000000953674316, NULL, 1.45000004768371582, NULL, 1.41999995708465576, NULL, 1.44000005722045898, NULL, 1.44000005722045898, NULL, 1.40999996662139893, NULL, 1.41999995708465576, NULL, 1.41999995708465576, NULL, 1.39999997615814209, 'B', 1.29999995231628418, 'B', 1.28999996185302712, 'B', 1.30999994277954102, 'B', 1.33000004291534424, NULL, 1.30999994277954102, NULL, 1.25999999046325684, NULL, 1.23000001907348633, 'B', 1.19000005722045898, 'B', 1.15999996662139893, 'B', 1.14999997615814209, 'B', 1.14999997615814209, 'B', 1.15999996662139893, 'B', 1.16999995708465576, 'B', 1.1799999475479126, 'B', 1.1799999475479126, 'B', 1.16999995708465576, 'B', 1.20000004768371582, NULL),
     ('08MG026', 2008, 2, 1, 29, 1.0700000524520874, 31.1599998474121094, 20, 1.03999996185302712, 29, 1.16999995708465576, 1.15999996662139893, NULL, 1.12999999523162842, NULL, 1.09000003337860107, 'B', 1.0700000524520874, 'B', 1.09000003337860107, NULL, 1.0700000524520874, NULL, 1.08000004291534424, NULL, 1.0700000524520874, NULL, 1.0700000524520874, NULL, 1.08000004291534424, NULL, 1.05999994277954102, NULL, 1.05999994277954102, 'B', 1.05999994277954102, NULL, 1.04999995231628418, NULL, 1.04999995231628418, NULL, 1.04999995231628418, NULL, 1.04999995231628418, NULL, 1.04999995231628418, NULL, 1.04999995231628418, NULL, 1.03999996185302712, NULL, 1.04999995231628418, NULL, 1.05999994277954102, NULL, 1.0700000524520874, NULL, 1.0700000524520874, NULL, 1.05999994277954102, NULL, 1.0700000524520874, NULL, 1.09000003337860107, NULL, 1.09000003337860107, NULL, 1.16999995708465576, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2008, 3, 1, 31, 1.15999996662139893, 36.0600013732910156, 31, 1.08000004291534424, 11, 1.38999998569488525, 1.12999999523162842, NULL, 1.10000002384185791, NULL, 1.12000000476837158, NULL, 1.11000001430511475, NULL, 1.09000003337860107, NULL, 1.11000001430511475, NULL, 1.12000000476837158, 'A', 1.12999999523162842, 'E', 1.14999997615814209, 'A', 1.25999999046325684, 'E', 1.38999998569488525, 'A', 1.26999998092651367, 'A', 1.24000000953674316, 'A', 1.23000001907348633, 'A', 1.19000005722045898, 'A', 1.1799999475479126, 'A', 1.19000005722045898, NULL, 1.1799999475479126, 'A', 1.1799999475479126, 'A', 1.15999996662139893, NULL, 1.13999998569488525, 'A', 1.16999995708465576, 'A', 1.20000004768371582, 'A', 1.15999996662139893, 'A', 1.14999997615814209, 'A', 1.15999996662139893, 'A', 1.12999999523162842, NULL, 1.12000000476837158, NULL, 1.11000001430511475, NULL, 1.11000001430511475, NULL, 1.08000004291534424, 'A'),
     ('08MG026', 2008, 4, 1, 30, 1.12999999523162842, 34.0099983215332031, 21, 1.01999998092651367, 29, 1.35000002384185791, 1.10000002384185791, 'E', 1.12000000476837158, 'A', 1.11000001430511475, 'E', 1.11000001430511475, 'A', 1.12000000476837158, NULL, 1.12000000476837158, 'A', 1.12999999523162842, 'A', 1.11000001430511475, 'A', 1.13999998569488525, 'E', 1.15999996662139893, 'A', 1.21000003814697288, 'A', 1.25, 'E', 1.28999996185302712, 'A', 1.24000000953674316, NULL, 1.15999996662139893, NULL, 1.12000000476837158, 'A', 1.15999996662139893, 'A', 1.12000000476837158, NULL, 1.0700000524520874, NULL, 1.02999997138977051, NULL, 1.01999998092651367, NULL, 1.01999998092651367, NULL, 1.01999998092651367, NULL, 1.01999998092651367, NULL, 1.02999997138977051, NULL, 1.04999995231628418, NULL, 1.10000002384185791, NULL, 1.26999998092651367, NULL, 1.35000002384185791, NULL, 1.25999999046325684, NULL, NULL, NULL),
     ('08MG026', 2008, 5, 1, 31, 5.61999988555908203, 174.330001831054688, 2, 1.19000005722045898, 18, 12.6999998092651367, 1.23000001907348633, NULL, 1.19000005722045898, NULL, 1.25, NULL, 1.38999998569488525, 'A', 1.75, 'E', 2.21000003814697266, 'A', 2.30999994277954102, 'A', 2.16000008583068848, NULL, 1.99000000953674316, NULL, 1.96000003814697288, NULL, 2.02999997138977051, NULL, 2, NULL, 2.02999997138977051, NULL, 2.16000008583068848, NULL, 2.97000002861022905, NULL, 4.25, NULL, 5.36999988555908203, NULL, 12.6999998092651367, NULL, 12, NULL, 11.6999998092651367, NULL, 8.93000030517578125, NULL, 7.07000017166137695, NULL, 6.78000020980834961, NULL, 7.92000007629394531, NULL, 10.3000001907348633, NULL, 10.1999998092651367, NULL, 9.77000045776367188, NULL, 9.93999958038330078, NULL, 9.82999992370605646, NULL, 9.56999969482422053, NULL, 9.36999988555908203, NULL),
     ('08MG026', 2008, 6, 1, 30, 7.13000011444091797, 213.809997558593722, 10, 5.65000009536743164, 30, 10.6000003814697283, 9.98999977111816406, NULL, 8.93000030517578125, NULL, 7.67000007629394531, NULL, 7.01999998092651367, NULL, 7, NULL, 6.57000017166137695, NULL, 6.19999980926513672, NULL, 5.94999980926513672, NULL, 5.73000001907348633, NULL, 5.65000009536743164, NULL, 6.09999990463256836, NULL, 6.51999998092651367, NULL, 6.69999980926513672, NULL, 6.36999988555908203, NULL, 6.53999996185302734, NULL, 7.09999990463256836, NULL, 6.94999980926513672, NULL, 6.46000003814697266, NULL, 5.98000001907348633, NULL, 6.32000017166137695, NULL, 7.17000007629394531, NULL, 7.42999982833862305, NULL, 6.96000003814697266, NULL, 6.75, NULL, 6.44999980926513672, NULL, 6.55999994277954102, NULL, 7.30000019073486328, NULL, 8.94999980926513672, NULL, 9.89000034332275391, NULL, 10.6000003814697283, NULL, NULL, NULL),
     ('08MG026', 2008, 7, 1, 31, 6.6399998664855957, 205.839996337890653, 31, 4.82000017166137695, 1, 11.1999998092651367, 11.1999998092651367, NULL, 9.60999965667724609, NULL, 8.77999973297119141, NULL, 8.22999954223632812, NULL, 8.10000038146972656, NULL, 7.80000019073486328, NULL, 6.84000015258789062, NULL, 6.67999982833862305, NULL, 6.96999979019165039, NULL, 6.59999990463256836, NULL, 5.96999979019165039, NULL, 6.13000011444091797, NULL, 6.55000019073486328, NULL, 6.44000005722045898, NULL, 6.01999998092651367, NULL, 5.98999977111816406, NULL, 5.92999982833862305, NULL, 5.82000017166137695, NULL, 5.82999992370605469, NULL, 5.90999984741210938, NULL, 6.19999980926513672, NULL, 6.21000003814697266, NULL, 6.07000017166137695, NULL, 6.05999994277954102, NULL, 6.03999996185302734, NULL, 5.90000009536743164, NULL, 5.86999988555908203, NULL, 5.69999980926513672, NULL, 5.94999980926513672, NULL, 5.61999988555908203, NULL, 4.82000017166137695, NULL),
     ('08MG026', 2008, 8, 1, 31, 5.84000015258789062, 181.17999267578125, 31, 4.23000001907348633, 18, 7.92999982833862305, 5.34999990463256836, NULL, 4.84999990463256836, NULL, 4.76000022888183594, NULL, 5, NULL, 5.48999977111816406, NULL, 5.88000011444091797, NULL, 6.48000001907348633, NULL, 6.38000011444091797, NULL, 6.19000005722045898, NULL, 5.44000005722045898, NULL, 4.8600001335144043, NULL, 4.84000015258789062, NULL, 5.38000011444091797, NULL, 6.46000003814697266, NULL, 7.01999998092651367, NULL, 6.6100001335144043, NULL, 6.8899998664855957, NULL, 7.92999982833862305, NULL, 7.23999977111816406, NULL, 7.59000015258789062, NULL, 6.21999979019165039, NULL, 5.23000001907348633, NULL, 5.53000020980834961, NULL, 7.42999982833862305, NULL, 6.17000007629394531, NULL, 4.90999984741210938, NULL, 4.78999996185302734, NULL, 4.76999998092651367, NULL, 6.13000011444091797, NULL, 5.13000011444091797, NULL, 4.23000001907348633, NULL),
     ('08MG026', 2008, 9, 1, 30, 3.24000000953674316, 97.2099990844726562, 28, 1.91999995708465598, 6, 4.21999979019165039, 3.76999998092651367, NULL, 3.40000009536743208, NULL, 3.38000011444091797, NULL, 3.38000011444091797, NULL, 3.81999993324279785, NULL, 4.21999979019165039, NULL, 3.90000009536743208, NULL, 3.75, NULL, 3.58999991416931152, NULL, 3.16000008583068848, NULL, 3.54999995231628418, NULL, 4.01000022888183594, NULL, 3.53999996185302779, NULL, 3.25, NULL, 3.34999990463256836, NULL, 3.27999997138977051, NULL, 3.23000001907348633, NULL, 3.46000003814697266, NULL, 3.27999997138977051, NULL, 3.81999993324279785, NULL, 3.55999994277954102, NULL, 3.16000008583068848, NULL, 2.41000008583068848, NULL, 2.52999997138977051, NULL, 3.17000007629394531, NULL, 2.47000002861022905, NULL, 2.22000002861022905, NULL, 1.91999995708465598, NULL, 2.11999988555908203, NULL, 2.50999999046325684, NULL, NULL, NULL),
     ('08MG026', 2008, 10, 1, 31, 2.84999990463256836, 88.1999969482421875, 27, 1.66999995708465576, 3, 5.65999984741210938, 3.28999996185302779, NULL, 4.05999994277954102, NULL, 5.65999984741210938, NULL, 5.6399998664855957, NULL, 4.23999977111816406, NULL, 3.32999992370605469, NULL, 3.76999998092651367, NULL, 2.75999999046325684, NULL, 2.40000009536743208, NULL, 2.20000004768371582, NULL, 1.98000001907348633, NULL, 1.98000001907348633, NULL, 3, NULL, 2.48000001907348633, NULL, 2.1400001049041748, NULL, 2.13000011444091797, NULL, 4.23000001907348633, NULL, 3.11999988555908203, NULL, 2.46000003814697266, NULL, 2.3599998950958252, NULL, 2.1400001049041748, NULL, 2.16000008583068848, NULL, 2.19000005722045898, NULL, 1.97000002861022927, NULL, 1.85000002384185791, NULL, 1.71000003814697288, NULL, 1.66999995708465576, NULL, 1.6799999475479126, NULL, 1.80999994277954102, NULL, 2.25999999046325684, NULL, 5.53000020980834961, NULL),
     ('08MG026', 2008, 11, 1, 30, 3.70000004768371582, 110.930000305175781, 27, 2.23000001907348633, 8, 6.69000005722045898, 4.65999984741210938, NULL, 5.82000017166137695, NULL, 4.48000001907348633, NULL, 3.78999996185302734, NULL, 3.18000006675720215, NULL, 3.17000007629394531, NULL, 3.88000011444091797, NULL, 6.69000005722045898, NULL, 5.5, NULL, 4.67000007629394531, NULL, 4.21999979019165039, NULL, 4.98999977111816406, NULL, 4.1100001335144043, NULL, 3.69000005722045898, NULL, 4.5, NULL, 4.44000005722045898, NULL, 4.07000017166137695, NULL, 3.70000004768371582, NULL, 3.23000001907348633, NULL, 3.19000005722045898, NULL, 2.99000000953674316, NULL, 2.81999993324279785, NULL, 2.57999992370605469, NULL, 2.48000001907348633, NULL, 2.52999997138977051, NULL, 2.32999992370605469, NULL, 2.23000001907348633, NULL, 2.23000001907348633, NULL, 2.30999994277954102, NULL, 2.45000004768371582, NULL, NULL, NULL),
     ('08MG026', 2008, 12, 1, 31, 1.60000002384185791, 49.720001220703125, 31, 1.14999997615814209, 6, 2.76999998092651367, 2.70000004768371582, NULL, 2.57999992370605469, NULL, 2.28999996185302779, NULL, 2.11999988555908203, NULL, 2.11999988555908203, NULL, 2.76999998092651367, NULL, 2.44000005722045898, NULL, 2.13000011444091797, NULL, 2.06999993324279785, NULL, 1.95000004768371604, NULL, 1.75999999046325684, NULL, 1.92999994754791282, NULL, 1.54999995231628418, NULL, 1.25999999046325684, NULL, 1.20000004768371582, 'B', 1.16999995708465576, 'B', 1.16999995708465576, 'B', 1.16999995708465576, 'B', 1.19000005722045898, 'B', 1.1799999475479126, 'B', 1.1799999475479126, 'B', 1.19000005722045898, 'B', 1.19000005722045898, 'B', 1.19000005722045898, 'B', 1.19000005722045898, 'B', 1.19000005722045898, 'B', 1.1799999475479126, 'B', 1.15999996662139893, 'B', 1.16999995708465576, 'B', 1.1799999475479126, 'B', 1.14999997615814209, 'B'),
     ('08MG026', 2009, 1, 1, 31, 1.09000003337860107, 33.7700004577636719, 27, 1.01999998092651367, 7, 1.29999995231628418, 1.12000000476837158, 'B', 1.09000003337860107, 'B', 1.08000004291534424, 'B', 1.0700000524520874, 'B', 1.05999994277954102, 'B', 1.10000002384185791, NULL, 1.29999995231628418, NULL, 1.26999998092651367, NULL, 1.12000000476837158, NULL, 1.11000001430511475, NULL, 1.09000003337860107, NULL, 1.12999999523162842, NULL, 1.16999995708465576, NULL, 1.16999995708465576, NULL, 1.15999996662139893, NULL, 1.13999998569488525, NULL, 1.0700000524520874, 'B', 1.0700000524520874, 'B', 1.05999994277954102, 'B', 1.04999995231628418, 'B', 1.04999995231628418, 'B', 1.03999996185302712, 'B', 1.03999996185302712, 'B', 1.03999996185302712, 'B', 1.02999997138977051, 'B', 1.02999997138977051, 'B', 1.01999998092651367, 'B', 1.01999998092651367, 'B', 1.01999998092651367, 'B', 1.01999998092651367, 'B', 1.02999997138977051, NULL),
     ('08MG026', 2009, 2, 1, 28, 0.902000010013580433, 25.2430000305175746, 7, 0.837000012397766113, 1, 1.01999998092651367, 1.01999998092651367, NULL, 1.00999999046325684, NULL, 0.91000002622604359, NULL, 0.898000001907348633, NULL, 0.894999980926513672, NULL, 0.870000004768371582, NULL, 0.837000012397766113, NULL, 0.859000027179718018, NULL, 0.904999971389770397, NULL, 0.922999978065490834, NULL, 0.907000005245208851, NULL, 0.913999974727630615, NULL, 0.90799999237060558, NULL, 0.893999993801116943, NULL, 0.870000004768371582, NULL, 0.851000010967254639, NULL, 0.878000020980834961, NULL, 0.86799997091293335, NULL, 0.859000027179718018, NULL, 0.85000002384185791, NULL, 0.847999989986419678, NULL, 0.884999990463256836, NULL, 0.972000002861022949, NULL, 0.981000006198883168, NULL, 0.916000008583068848, NULL, 0.879999995231628418, 'B', 0.91000002622604359, 'B', 0.925000011920928955, 'B', NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2009, 3, 1, 31, 0.91100001335144043, 28.25, 30, 0.819000005722045898, 2, 1.3200000524520874, 0.929000020027160645, NULL, 1.3200000524520874, NULL, 1.09000003337860107, NULL, 1.01999998092651367, NULL, 0.980000019073486439, NULL, 0.922999978065490834, NULL, 0.925000011920928955, 'B', 0.920000016689300426, 'B', 0.915000021457672008, 'B', 0.91000002622604359, 'B', 0.89999997615814209, 'B', 0.898999989032745361, 'B', 0.888000011444091797, NULL, 0.875999987125396729, NULL, 0.871999979019165039, NULL, 0.851000010967254639, NULL, 0.837999999523162842, NULL, 0.847000002861022949, NULL, 0.889999985694885254, NULL, 1.00999999046325684, NULL, 0.897000014781951904, NULL, 0.879000008106231689, NULL, 0.864000022411346436, NULL, 0.862999975681304932, NULL, 0.866999983787536621, NULL, 0.843999981880187988, NULL, 0.865999996662139893, NULL, 0.866999983787536621, NULL, 0.833999991416931152, NULL, 0.819000005722045898, NULL, 0.847000002861022949, NULL),
     ('08MG026', 2009, 4, 1, 30, 1.27999997138977051, 38.4620018005371094, 4, 0.828999996185302734, 22, 2.27999997138977051, 0.833000004291534424, NULL, 0.862999975681304932, NULL, 0.855000019073486328, NULL, 0.828999996185302734, NULL, 0.859000027179718018, NULL, 0.926999986171722412, NULL, 0.995999991893768422, NULL, 1.0700000524520874, NULL, 1.11000001430511475, NULL, 1.11000001430511475, NULL, 1.12999999523162842, NULL, 1.1799999475479126, NULL, 1.1799999475479126, NULL, 1.12999999523162842, NULL, 1.13999998569488525, NULL, 1.15999996662139893, NULL, 1.34000003337860107, NULL, 1.28999996185302712, NULL, 1.33000004291534424, NULL, 1.50999999046325684, NULL, 1.95000004768371604, NULL, 2.27999997138977051, NULL, 1.82000005245208762, NULL, 1.64999997615814209, NULL, 1.59000003337860107, NULL, 1.53999996185302712, NULL, 1.50999999046325684, NULL, 1.44000005722045898, NULL, 1.40999996662139893, NULL, 1.4299999475479126, NULL, NULL, NULL),
     ('08MG026', 2009, 5, 1, 31, 4.01000022888183594, 124.309997558593764, 1, 1.5700000524520874, 27, 7.5, 1.5700000524520874, NULL, 1.85000002384185791, NULL, 2.08999991416931152, NULL, 1.98000001907348633, NULL, 2.45000004768371582, NULL, 2.26999998092651367, NULL, 2.18000006675720215, NULL, 2.19000005722045898, NULL, 2.28999996185302779, NULL, 2.52999997138977051, NULL, 2.88000011444091797, NULL, 2.78999996185302779, NULL, 2.47000002861022905, NULL, 2.31999993324279785, NULL, 2.42000007629394531, NULL, 2.73000001907348633, NULL, 4.28999996185302734, NULL, 5.3899998664855957, NULL, 4.82000017166137695, NULL, 4.1399998664855957, NULL, 3.8599998950958252, NULL, 4.09999990463256836, 'A', 4.90000009536743164, 'E', 6, 'E', 6.69999980926513672, 'E', 7.25, 'E', 7.5, 'E', 7.25, 'E', 6.59999990463256836, 'E', 7, 'E', 7.5, 'E'),
     ('08MG026', 2009, 6, 1, 30, 8.97999954223632812, 269.29998779296875, 23, 6.42000007629394531, 14, 12.1999998092651367, 7.80000019073486328, 'E', 8.25, 'E', 9.47000026702880859, 'A', 10.1000003814697283, NULL, 10.3999996185302717, NULL, 10.5, NULL, 9.85999965667724609, NULL, 9.65999984741210938, NULL, 9.02000045776367188, NULL, 9.32999992370605646, NULL, 9.89000034332275391, NULL, 11.1999998092651367, NULL, 11.8999996185302717, NULL, 12.1999998092651367, NULL, 11.8999996185302717, NULL, 9.76000022888183594, NULL, 9.42000007629394354, NULL, 9.14000034332275391, NULL, 8.43000030517578125, NULL, 7.73999977111816406, NULL, 7.1399998664855957, NULL, 6.44999980926513672, NULL, 6.42000007629394531, NULL, 8.96000003814697266, NULL, 8.63000011444091797, NULL, 7.61999988555908203, NULL, 7.51000022888183594, NULL, 7.36999988555908203, NULL, 6.65000009536743164, NULL, 6.57999992370605469, NULL, NULL, NULL),
     ('08MG026', 2009, 7, 1, 31, 8.14999961853027344, 252.580001831054688, 9, 5.96999979019165039, 26, 12.3000001907348633, 6.57999992370605469, NULL, 6.78999996185302734, NULL, 7.30999994277954102, NULL, 7.84000015258789062, NULL, 8.06999969482421875, NULL, 7.38000011444091797, NULL, 6.92999982833862305, NULL, 6.23000001907348633, NULL, 5.96999979019165039, NULL, 6.57999992370605469, NULL, 7.30000019073486328, NULL, 7.42999982833862305, NULL, 7.32000017166137695, NULL, 7.44000005722045898, NULL, 7.40999984741210938, NULL, 7.42000007629394531, NULL, 7.65000009536743164, NULL, 7.82000017166137695, NULL, 7.30999994277954102, NULL, 7.15000009536743164, NULL, 7.69000005722045898, NULL, 8.38000011444091797, NULL, 8.72000026702880859, NULL, 9.01000022888183594, NULL, 10.3999996185302717, NULL, 12.3000001907348633, NULL, 11.3000001907348633, NULL, 10.8000001907348633, NULL, 10.5, NULL, 10.5, NULL, 9.05000019073486328, NULL),
     ('08MG026', 2009, 8, 1, 31, 6.13000011444091797, 189.949996948242188, 26, 4.13000011444091797, 1, 9.47999954223632812, 9.47999954223632812, NULL, 9.38000011444091797, NULL, 9.05000019073486328, NULL, 8.17000007629394531, NULL, 7.17999982833862305, NULL, 6.55999994277954102, NULL, 6.26999998092651367, NULL, 5.96999979019165039, NULL, 5.71999979019165039, NULL, 8.27000045776367188, NULL, 6.59000015258789062, NULL, 5.25, NULL, 4.75, NULL, 4.48000001907348633, NULL, 4.42000007629394531, NULL, 4.73000001907348633, NULL, 5.65000009536743164, NULL, 6.51999998092651367, NULL, 7.32999992370605469, NULL, 7.88000011444091797, NULL, 6.48999977111816406, NULL, 5.26000022888183594, NULL, 4.51000022888183594, NULL, 4.5, NULL, 4.48000001907348633, NULL, 4.13000011444091797, NULL, 4.5, NULL, 5.15000009536743164, NULL, 5.32000017166137695, NULL, 5.8600001335144043, NULL, 6.09999990463256836, NULL),
     ('08MG026', 2009, 9, 1, 30, 4.44999980926513672, 133.460006713867188, 30, 2.54999995231628418, 19, 6.94000005722045898, 6.5, NULL, 5.78000020980834961, NULL, 5.84000015258789062, NULL, 4.19000005722045898, NULL, 5.84999990463256836, NULL, 4.84999990463256836, NULL, 3.84999990463256792, NULL, 3.38000011444091797, NULL, 5.76999998092651367, NULL, 4.34000015258789062, NULL, 4.78999996185302734, NULL, 5.23999977111816406, NULL, 5.38000011444091797, NULL, 4.73000001907348633, NULL, 4.32000017166137695, NULL, 5.28000020980834961, NULL, 4.05000019073486328, NULL, 4.94999980926513672, NULL, 6.94000005722045898, NULL, 3.71000003814697266, NULL, 6, 'E', 4.19999980926513672, 'E', 3.59999990463256836, 'E', 3.25, 'E', 3.09999990463256836, 'E', 2.92000007629394531, 'E', 2.79999995231628418, 'E', 2.70000004768371582, 'E', 2.59999990463256836, 'E', 2.54999995231628418, 'E', NULL, NULL),
     ('08MG026', 2009, 10, 1, 31, 2.8599998950958252, 88.6699981689453125, 12, 1.83000004291534402, 31, 7.98000001907348633, 2.45000004768371582, 'E', 2.11999988555908203, NULL, 2, NULL, 1.91999995708465598, NULL, 1.87999999523162842, NULL, 2.05999994277954102, NULL, 2.01999998092651367, NULL, 1.96000003814697288, NULL, 1.95000004768371604, NULL, 1.92999994754791282, NULL, 1.85000002384185791, NULL, 1.83000004291534402, NULL, 1.87000000476837203, NULL, 1.92999994754791282, NULL, 1.92999994754791282, NULL, 5.3600001335144043, NULL, 5.28000020980834961, NULL, 4.90999984741210938, NULL, 3.31999993324279785, NULL, 2.83999991416931152, NULL, 2.71000003814697266, NULL, 2.53999996185302779, NULL, 2.76999998092651367, NULL, 2.61999988555908203, NULL, 2.48000001907348633, NULL, 2.68000006675720215, NULL, 2.43000006675720215, NULL, 2.31999993324279785, NULL, 2.34999990463256836, NULL, 6.38000011444091797, NULL, 7.98000001907348633, NULL),
     ('08MG026', 2009, 11, 1, 30, 3.55999994277954102, 106.790000915527344, 14, 2.29999995231628418, 16, 6.82000017166137695, 3.55999994277954102, NULL, 3.00999999046325684, NULL, 2.68000006675720215, NULL, 2.6099998950958252, NULL, 4.96000003814697266, NULL, 4.71999979019165039, NULL, 3.31999993324279785, NULL, 2.94000005722045898, NULL, 3.15000009536743208, NULL, 2.90000009536743208, NULL, 2.71000003814697266, NULL, 2.52999997138977051, NULL, 2.49000000953674316, NULL, 2.29999995231628418, NULL, 2.46000003814697266, NULL, 6.82000017166137695, NULL, 5.34000015258789062, NULL, 4.03000020980834961, NULL, 3.50999999046325684, NULL, 3.98000001907348633, NULL, 3.32999992370605469, NULL, 3.05999994277954102, NULL, 2.84999990463256836, NULL, 2.65000009536743208, NULL, 4.48000001907348633, NULL, 5.57000017166137695, NULL, 4.19999980926513672, NULL, 3.61999988555908203, NULL, 3.31999993324279785, NULL, 3.69000005722045898, NULL, NULL, NULL),
     ('08MG026', 2009, 12, 1, 31, 1.95000004768371604, 60.4500007629394531, 30, 1.66999995708465576, 1, 2.83999991416931152, 2.83999991416931152, NULL, 2.47000002861022905, NULL, 2.30999994277954102, 'B', 2.22000002861022905, 'B', 2.15000009536743208, 'B', 2.07999992370605469, 'B', 2.00999999046325684, 'B', 1.98000001907348633, 'B', 1.95000004768371604, 'B', 1.91999995708465598, 'B', 1.90999996662139893, 'B', 1.89999997615814209, 'B', 1.88999998569488525, 'B', 1.88999998569488525, 'B', 1.87999999523162842, 'B', 1.87999999523162842, 'B', 1.88999998569488525, NULL, 1.90999996662139893, NULL, 1.96000003814697288, NULL, 2.08999991416931152, NULL, 2.1099998950958252, NULL, 1.87000000476837203, NULL, 1.75999999046325684, NULL, 1.74000000953674316, 'B', 1.72000002861022949, 'B', 1.71000003814697288, 'B', 1.70000004768371582, 'B', 1.69000005722045898, 'B', 1.6799999475479126, NULL, 1.66999995708465576, NULL, 1.66999995708465576, NULL),
     ('08MG026', 2010, 1, 1, 31, 2.07999992370605469, 64.5199966430664062, 8, 1.36000001430511475, 12, 4.09999990463256836, 1.55999994277954102, 'B', 1.51999998092651367, 'B', 1.49000000953674316, 'B', 1.45000004768371582, 'B', 1.41999995708465576, 'B', 1.39999997615814209, 'B', 1.37000000476837158, 'B', 1.36000001430511475, 'B', 1.87000000476837203, NULL, 1.86000001430511475, NULL, 4.01000022888183594, NULL, 4.09999990463256836, NULL, 3.8599998950958252, NULL, 3.43000006675720215, NULL, 3.17000007629394531, NULL, 2.70000004768371582, 'B', 2.54999995231628418, 'B', 2.48000001907348633, 'B', 2.26999998092651367, 'B', 2.11999988555908203, 'B', 2.02999997138977051, 'B', 1.89999997615814209, 'B', 1.71000003814697288, 'B', 1.6799999475479126, 'B', 1.66999995708465576, 'B', 1.63999998569488525, 'B', 1.60000002384185791, 'B', 1.55999994277954102, 'B', 1.59000003337860107, NULL, 1.58000004291534424, NULL, 1.5700000524520874, NULL),
     ('08MG026', 2010, 2, 1, 28, 1.47000002861022949, 41.0600013732910156, 9, 1.27999997138977051, 14, 1.84000003337860107, 1.53999996185302712, NULL, 1.53999996185302712, NULL, 1.51999998092651367, NULL, 1.48000001907348633, NULL, 1.39999997615814209, NULL, 1.36000001430511475, NULL, 1.34000003337860107, NULL, 1.3200000524520874, NULL, 1.27999997138977051, 'B', 1.34000003337860107, 'B', 1.38999998569488525, NULL, 1.48000001907348633, NULL, 1.44000005722045898, NULL, 1.84000003337860107, NULL, 1.64999997615814209, NULL, 1.62000000476837158, NULL, 1.55999994277954102, NULL, 1.52999997138977051, NULL, 1.5, NULL, 1.48000001907348633, NULL, 1.45000004768371582, NULL, 1.41999995708465576, NULL, 1.4299999475479126, NULL, 1.4299999475479126, NULL, 1.41999995708465576, NULL, 1.44000005722045898, NULL, 1.4299999475479126, NULL, 1.4299999475479126, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2010, 3, 1, 31, 1.5, 46.5299987792968821, 10, 1.26999998092651367, 16, 1.92999994754791282, 1.40999996662139893, NULL, 1.46000003814697288, NULL, 1.48000001907348633, NULL, 1.47000002861022949, NULL, 1.4299999475479126, NULL, 1.37999999523162842, 'B', 1.4299999475479126, NULL, 1.37000000476837158, NULL, 1.28999996185302712, 'B', 1.26999998092651367, 'B', 1.36000001430511475, NULL, 1.35000002384185791, NULL, 1.29999995231628418, NULL, 1.28999996185302712, NULL, 1.28999996185302712, NULL, 1.92999994754791282, NULL, 1.78999996185302712, NULL, 1.62000000476837158, NULL, 1.5700000524520874, NULL, 1.53999996185302712, NULL, 1.58000004291534424, NULL, 1.54999995231628418, NULL, 1.49000000953674316, NULL, 1.50999999046325684, NULL, 1.53999996185302712, NULL, 1.53999996185302712, NULL, 1.52999997138977051, NULL, 1.74000000953674316, NULL, 1.77999997138977051, NULL, 1.66999995708465576, NULL, 1.5700000524520874, NULL),
     ('08MG026', 2010, 4, 1, 30, 2.1099998950958252, 63.3400001525878906, 10, 1.33000004291534424, 21, 3.90000009536743208, 1.53999996185302712, NULL, 1.55999994277954102, NULL, 1.50999999046325684, NULL, 1.47000002861022949, NULL, 1.46000003814697288, NULL, 1.41999995708465576, NULL, 1.39999997615814209, NULL, 1.39999997615814209, NULL, 1.35000002384185791, NULL, 1.33000004291534424, NULL, 1.35000002384185791, NULL, 1.37999999523162842, NULL, 1.47000002861022949, NULL, 1.49000000953674316, NULL, 1.55999994277954102, NULL, 1.75, NULL, 2.02999997138977051, NULL, 2.32999992370605469, NULL, 2.61999988555908203, NULL, 3.08999991416931152, NULL, 3.90000009536743208, NULL, 3.72000002861022949, NULL, 3.13000011444091797, NULL, 2.80999994277954102, NULL, 2.59999990463256836, NULL, 2.52999997138977051, NULL, 2.91000008583068848, NULL, 2.84999990463256836, NULL, 2.69000005722045898, NULL, 2.69000005722045898, NULL, NULL, NULL),
     ('08MG026', 2010, 5, 1, 31, 3.91000008583068892, 121.309997558593764, 8, 2.11999988555908203, 18, 6.98999977111816406, 2.66000008583068848, NULL, 2.6099998950958252, NULL, 2.49000000953674316, NULL, 2.32999992370605469, NULL, 2.26999998092651367, NULL, 2.20000004768371582, NULL, 2.13000011444091797, NULL, 2.11999988555908203, NULL, 2.11999988555908203, NULL, 2.1400001049041748, NULL, 2.41000008583068848, NULL, 2.82999992370605469, NULL, 3.16000008583068848, NULL, 3.78999996185302734, NULL, 4.6100001335144043, NULL, 5.21000003814697266, NULL, 6.17000007629394531, NULL, 6.98999977111816406, NULL, 6.5, NULL, 5.71999979019165039, NULL, 4.28000020980834961, NULL, 3.76999998092651367, NULL, 3.34999990463256836, NULL, 3.1400001049041748, NULL, 3.1099998950958252, NULL, 3.47000002861022905, NULL, 4.34000015258789062, NULL, 6.34000015258789062, NULL, 6.88000011444091797, NULL, 6.15000009536743164, NULL, 6.01999998092651367, NULL),
     ('08MG026', 2010, 6, 1, 30, 9.31000041961669922, 279.410003662109375, 6, 5.51000022888183594, 24, 15.1000003814697283, 6.86999988555908203, NULL, 8.86999988555908203, NULL, 7.51000022888183594, NULL, 6.01000022888183594, NULL, 5.51999998092651367, NULL, 5.51000022888183594, NULL, 5.92000007629394531, NULL, 6.67000007629394531, NULL, 6.84999990463256836, NULL, 6.67999982833862305, NULL, 6.80000019073486328, NULL, 8.52000045776367188, NULL, 12.1000003814697283, NULL, 11.1999998092651367, NULL, 7.73999977111816406, NULL, 6.94999980926513672, NULL, 6.96999979019165039, NULL, 8.01000022888183594, NULL, 12.3000001907348633, NULL, 12.3999996185302717, NULL, 11.8999996185302717, NULL, 10, NULL, 11, NULL, 15.1000003814697283, NULL, 14.6000003814697283, NULL, 13.6999998092651367, NULL, 12.1999998092651367, NULL, 11.6999998092651367, NULL, 11.1000003814697283, NULL, 8.71000003814697266, NULL, NULL, NULL),
     ('08MG026', 2010, 7, 1, 31, 12, 370.790008544921875, 3, 6.94999980926513672, 11, 18.7999992370605469, 7.07999992370605469, NULL, 7.11999988555908203, NULL, 6.94999980926513672, NULL, 7.11999988555908203, NULL, 7.98000001907348633, NULL, 9.65999984741210938, NULL, 14, NULL, 16.7999992370605469, NULL, 17.5, NULL, 17.2999992370605469, NULL, 18.7999992370605469, NULL, 17, NULL, 11.3000001907348633, NULL, 10, NULL, 11.3999996185302717, NULL, 12.1999998092651367, NULL, 12.6000003814697283, NULL, 12.1000003814697283, NULL, 11.6000003814697283, NULL, 11.5, NULL, 12.6999998092651367, NULL, 14.1999998092651367, NULL, 12.5, NULL, 11.8999996185302717, NULL, 11.8999996185302717, NULL, 11.6000003814697283, NULL, 13, NULL, 13.1000003814697283, NULL, 10.8000001907348633, NULL, 9.75, NULL, 9.32999992370605646, NULL),
     ('08MG026', 2010, 8, 1, 31, 5.80999994277954102, 179.990005493164062, 30, 2.70000004768371582, 7, 10.1000003814697283, 8.56000041961669922, 'E', 8.51000022888183594, 'E', 8.77999973297119141, 'E', 8.89999961853027344, 'E', 8.85000038146972656, 'E', 8.64999961853027344, 'E', 10.1000003814697283, 'E', 8.69999980926513672, 'E', 7.51999998092651367, 'E', 6.88000011444091797, 'E', 6.53999996185302734, 'E', 6.92000007629394531, 'E', 5.13000011444091797, 'A', 5.23000001907348633, NULL, 5.65999984741210938, NULL, 5.90000009536743164, NULL, 5.78999996185302734, NULL, 5.30000019073486328, NULL, 5.03999996185302734, NULL, 4.28999996185302734, NULL, 3.57999992370605469, NULL, 3.86999988555908203, NULL, 3.42000007629394531, NULL, 3.75999999046325684, NULL, 4.46000003814697266, NULL, 4.57000017166137695, NULL, 3.59999990463256836, NULL, 3.04999995231628418, NULL, 2.83999991416931152, NULL, 2.70000004768371582, NULL, 2.8900001049041748, NULL),
     ('08MG026', 2010, 9, 1, 30, 4.03999996185302734, 121.279998779296875, 9, 2.34999990463256836, 28, 13.1999998092651367, 2.75, NULL, 2.80999994277954102, NULL, 3.27999997138977051, NULL, 3.30999994277954102, NULL, 2.72000002861022905, NULL, 2.61999988555908203, NULL, 2.53999996185302779, NULL, 2.46000003814697266, NULL, 2.34999990463256836, NULL, 2.43000006675720215, NULL, 2.40000009536743208, NULL, 3.30999994277954102, NULL, 2.6099998950958252, NULL, 2.53999996185302779, NULL, 2.68000006675720215, NULL, 2.78999996185302779, NULL, 3, NULL, 3.42000007629394531, NULL, 4.44999980926513672, NULL, 6.73000001907348633, NULL, 3.92000007629394487, NULL, 3.1400001049041748, NULL, 2.91000008583068848, NULL, 2.97000002861022905, NULL, 4.88000011444091797, NULL, 12.6999998092651367, NULL, 6.92999982833862305, NULL, 13.1999998092651367, NULL, 5.34000015258789062, NULL, 4.09000015258789062, NULL, NULL, NULL),
     ('08MG026', 2010, 10, 1, 31, 2.58999991416931152, 80.3000030517578125, 29, 1.85000002384185791, 10, 6.1100001335144043, 3.8900001049041748, NULL, 3.55999994277954102, NULL, 3.06999993324279785, NULL, 2.92000007629394531, NULL, 2.61999988555908203, NULL, 2.63000011444091797, NULL, 2.61999988555908203, NULL, 2.70000004768371582, NULL, 4.26999998092651367, NULL, 6.1100001335144043, NULL, 3.26999998092651367, NULL, 2.77999997138977051, NULL, 2.53999996185302779, NULL, 2.50999999046325684, NULL, 2.32999992370605469, NULL, 2.17000007629394531, NULL, 2.03999996185302779, NULL, 2.02999997138977051, NULL, 2.03999996185302779, NULL, 1.97000002861022927, NULL, 1.96000003814697288, NULL, 2.33999991416931152, NULL, 2.01999998092651367, NULL, 2.40000009536743208, NULL, 2.11999988555908203, NULL, 1.97000002861022927, NULL, 1.89999997615814209, NULL, 1.87999999523162842, NULL, 1.85000002384185791, NULL, 1.85000002384185791, NULL, 1.94000005722045898, NULL),
     ('08MG026', 2010, 11, 1, 30, 2.1099998950958252, 63.220001220703125, 29, 1.33000004291534424, 5, 4.3600001335144043, 2.75999999046325684, NULL, 2.71000003814697266, NULL, 2.28999996185302779, NULL, 2.50999999046325684, NULL, 4.3600001335144043, NULL, 3.38000011444091797, NULL, 3.6099998950958252, NULL, 2.8900001049041748, NULL, 2.58999991416931152, NULL, 2.32999992370605469, NULL, 2.25, NULL, 2.11999988555908203, NULL, 2.06999993324279785, NULL, 2.00999999046325684, NULL, 2.09999990463256836, NULL, 2.05999994277954102, NULL, 1.98000001907348633, NULL, 1.84000003337860107, NULL, 1.64999997615814209, 'B', 1.51999998092651367, 'B', 1.48000001907348633, 'B', 1.45000004768371582, 'B', 1.40999996662139893, 'B', 1.39999997615814209, 'B', 1.4299999475479126, 'B', 1.45000004768371582, 'B', 1.48000001907348633, 'B', 1.40999996662139893, 'B', 1.33000004291534424, 'B', 1.35000002384185791, 'B', NULL, NULL),
     ('08MG026', 2010, 12, 1, 31, 1.37000000476837158, 42.5999984741210866, 31, 1.12999999523162842, 12, 1.63999998569488525, 1.33000004291534424, 'B', 1.34000003337860107, 'B', 1.30999994277954102, 'B', 1.24000000953674316, 'B', 1.20000004768371582, 'B', 1.25999999046325684, 'B', 1.38999998569488525, 'B', 1.5, NULL, 1.47000002861022949, NULL, 1.41999995708465576, NULL, 1.41999995708465576, NULL, 1.63999998569488525, NULL, 1.61000001430511475, NULL, 1.52999997138977051, 'B', 1.48000001907348633, 'B', 1.46000003814697288, NULL, 1.41999995708465576, NULL, 1.36000001430511475, 'B', 1.33000004291534424, 'B', 1.22000002861022949, 'B', 1.19000005722045898, 'B', 1.1799999475479126, 'B', 1.37999999523162842, NULL, 1.44000005722045898, NULL, 1.5, NULL, 1.5, NULL, 1.45000004768371582, NULL, 1.44000005722045898, NULL, 1.28999996185302712, 'B', 1.16999995708465576, 'B', 1.12999999523162842, 'B'),
     ('08MG026', 2011, 1, 1, 31, 1.71000003814697288, 52.9300003051757812, 1, 1.15999996662139893, 17, 3.01999998092651367, 1.15999996662139893, 'B', 1.1799999475479126, 'B', 1.20000004768371582, 'B', 1.24000000953674316, 'B', 1.5700000524520874, NULL, 1.54999995231628418, NULL, 1.72000002861022949, NULL, 1.50999999046325684, NULL, 1.30999994277954102, NULL, 1.1799999475479126, NULL, 1.21000003814697288, 'E', 1.25999999046325684, 'E', 1.38999998569488525, NULL, 1.87999999523162842, NULL, 2.05999994277954102, NULL, 2.79999995231628418, NULL, 3.01999998092651367, NULL, 2.53999996185302779, NULL, 2.29999995231628418, NULL, 2.16000008583068848, NULL, 2.04999995231628418, 'E', 1.94000005722045898, 'E', 1.82000005245208762, 'E', 1.75999999046325684, 'E', 1.70000004768371582, 'E', 1.6799999475479126, 'E', 1.64999997615814209, 'E', 1.60000002384185791, 'E', 1.5700000524520874, 'E', 1.50999999046325684, 'E', 1.40999996662139893, 'E'),
     ('08MG026', 2011, 2, 1, 28, 1.50999999046325684, 42.2000007629394531, 26, 1.1799999475479126, 16, 1.78999996185302712, 1.36000001430511475, 'E', 1.34000003337860107, 'E', 1.39999997615814209, 'E', 1.66999995708465576, 'E', 1.74000000953674316, 'E', 1.71000003814697288, 'E', 1.6799999475479126, 'E', 1.60000002384185791, 'E', 1.52999997138977051, 'E', 1.46000003814697288, 'E', 1.4299999475479126, 'E', 1.59000003337860107, 'E', 1.72000002861022949, 'E', 1.70000004768371582, 'E', 1.76999998092651367, 'E', 1.78999996185302712, 'E', 1.72000002861022949, 'E', 1.70000004768371582, 'E', 1.61000001430511475, 'E', 1.50999999046325684, 'E', 1.44000005722045898, 'E', 1.37999999523162842, 'E', 1.3200000524520874, 'E', 1.25999999046325684, 'E', 1.22000002861022949, 'E', 1.1799999475479126, 'E', 1.1799999475479126, 'E', 1.19000005722045898, 'E', NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2011, 3, 1, 31, 1.11000001430511475, 34.3260002136230469, 27, 0.975000023841858021, 31, 1.62999999523162842, 1.1799999475479126, NULL, 1.22000002861022949, NULL, 1.16999995708465576, NULL, 1.12999999523162842, NULL, 1.12000000476837158, NULL, 1.08000004291534424, NULL, 1.0700000524520874, NULL, 1.04999995231628418, NULL, 1.08000004291534424, NULL, 1.12999999523162842, NULL, 1.03999996185302712, NULL, 1.0700000524520874, NULL, 1.08000004291534424, NULL, 1.24000000953674316, NULL, 1.25, NULL, 1.23000001907348633, NULL, 1.11000001430511475, NULL, 1.08000004291534424, NULL, 1.08000004291534424, NULL, 1.02999997138977051, NULL, 1.04999995231628418, NULL, 1.01999998092651367, NULL, 1.00999999046325684, NULL, 1.00999999046325684, NULL, 0.992999970912933239, NULL, 0.984000027179718018, NULL, 0.975000023841858021, NULL, 0.984000027179718018, NULL, 1.01999998092651367, NULL, 1.21000003814697288, NULL, 1.62999999523162842, NULL),
     ('08MG026', 2011, 4, 1, 30, 1.12999999523162842, 33.8660011291503906, 20, 0.941999971866607555, 1, 1.51999998092651367, 1.51999998092651367, NULL, 1.4299999475479126, NULL, 1.33000004291534424, NULL, 1.29999995231628418, NULL, 1.25, NULL, 1.19000005722045898, NULL, 1.10000002384185791, NULL, 1.08000004291534424, NULL, 1.0700000524520874, NULL, 1.16999995708465576, NULL, 1.22000002861022949, NULL, 1.11000001430511475, NULL, 1.13999998569488525, NULL, 1.10000002384185791, NULL, 1.04999995231628418, NULL, 1.02999997138977051, NULL, 1, NULL, 1.00999999046325684, NULL, 0.952000021934509166, NULL, 0.941999971866607555, NULL, 0.954999983310699574, NULL, 0.96700000762939442, NULL, 1.03999996185302712, NULL, 1.00999999046325684, NULL, 1.0700000524520874, NULL, 1.13999998569488525, NULL, 1.16999995708465576, NULL, 1.11000001430511475, NULL, 1.16999995708465576, NULL, 1.24000000953674316, NULL, NULL, NULL),
     ('08MG026', 2011, 5, 1, 31, 3.25, 100.849998474121094, 1, 1.3200000524520874, 31, 5.26000022888183594, 1.3200000524520874, NULL, 1.47000002861022949, NULL, 1.5, NULL, 1.55999994277954102, NULL, 1.75, NULL, 1.91999995708465598, NULL, 1.98000001907348633, NULL, 2.04999995231628418, NULL, 2.20000004768371582, NULL, 2.43000006675720215, NULL, 2.97000002861022905, NULL, 2.80999994277954102, NULL, 2.59999990463256836, NULL, 2.93000006675720215, NULL, 4.15999984741210938, NULL, 4.59999990463256836, NULL, 3.79999995231628418, NULL, 3.19000005722045898, NULL, 3.16000008583068848, NULL, 3.72000002861022949, NULL, 4.34000015258789062, NULL, 4.25, NULL, 4.26999998092651367, NULL, 4.34000015258789062, NULL, 4.26999998092651367, NULL, 4.63000011444091797, NULL, 4.19000005722045898, NULL, 3.98000001907348633, NULL, 4.23999977111816406, NULL, 4.96000003814697266, NULL, 5.26000022888183594, NULL),
     ('08MG026', 2011, 6, 1, 30, 7.34000015258789062, 220.289993286132812, 1, 5.71999979019165039, 30, 11, 5.71999979019165039, NULL, 6.1399998664855957, NULL, 5.75, NULL, 6.09000015258789062, NULL, 6.51999998092651367, NULL, 7.38000011444091797, NULL, 8.76000022888183594, NULL, 8.01000022888183594, NULL, 8.01000022888183594, NULL, 7.76000022888183594, NULL, 7.53999996185302734, NULL, 7.40000009536743164, NULL, 6.86999988555908203, NULL, 6.92999982833862305, NULL, 6.78999996185302734, NULL, 6.78999996185302734, NULL, 6.96000003814697266, NULL, 7.46999979019165039, NULL, 7.36999988555908203, NULL, 7.28000020980834961, NULL, 7.67999982833862305, NULL, 8.27000045776367188, NULL, 8.28999996185302734, 'E', 7.17000007629394531, 'E', 6.51000022888183594, 'E', 6.21999979019165039, 'E', 6.48000001907348633, 'E', 7.44000005722045898, 'E', 9.68999958038330078, 'E', 11, 'E', NULL, NULL),
     ('08MG026', 2011, 7, 1, 31, 9.85000038146972834, 305.480010986328125, 2, 7.71999979019165039, 31, 14.5, 9.10999965667724609, 'E', 7.71999979019165039, 'E', 8.81000041961669922, 'E', 9.35999965667724609, 'E', 8.76000022888183594, 'E', 9.18000030517577947, 'E', 10.6000003814697283, 'E', 12, 'E', 10.3999996185302717, 'E', 9.06999969482422053, 'E', 8.43999958038330078, 'E', 8.22000026702880859, 'E', 8.59000015258789062, 'E', 9.14000034332275391, 'E', 9.19999980926513672, 'E', 9.40999984741210938, 'E', 10.6000003814697283, 'E', 10.3999996185302717, 'E', 10.1999998092651367, 'E', 10.1000003814697283, 'E', 10.8999996185302717, 'E', 9.61999988555908203, NULL, 8.85999965667724609, NULL, 9.51000022888183594, NULL, 11, NULL, 11.1999998092651367, NULL, 10.1000003814697283, NULL, 9.77999973297119141, NULL, 10.3000001907348633, NULL, 10.3999996185302717, NULL, 14.5, NULL),
     ('08MG026', 2011, 8, 1, 31, 8.26000022888183594, 255.919998168945312, 18, 6.53000020980834961, 22, 11.6000003814697283, 10.5, NULL, 9.57999992370605646, NULL, 9.23999977111816406, NULL, 9.64999961853027166, NULL, 10.3000001907348633, NULL, 10.5, NULL, 9.85000038146972834, NULL, 9.55000019073486328, NULL, 8.72999954223632812, NULL, 8.27999973297119141, NULL, 8.82999992370605469, NULL, 8.52000045776367188, NULL, 7.67000007629394531, NULL, 7.34999990463256836, NULL, 7.07999992370605469, NULL, 6.71000003814697266, NULL, 6.6100001335144043, NULL, 6.53000020980834961, NULL, 6.57000017166137695, NULL, 6.8600001335144043, NULL, 7.57999992370605469, NULL, 11.6000003814697283, NULL, 10.3000001907348633, NULL, 8.14999961853027344, NULL, 7.5, NULL, 7.26999998092651367, NULL, 6.98000001907348633, NULL, 7.03000020980834961, NULL, 7.09999990463256836, NULL, 6.92999982833862305, NULL, 6.57000017166137695, NULL),
     ('08MG026', 2011, 9, 1, 30, 6.25, 187.3800048828125, 20, 4.1399998664855957, 23, 11.6999998092651367, 6, NULL, 5.59000015258789062, NULL, 5.42999982833862305, NULL, 5.46000003814697266, NULL, 5.51999998092651367, NULL, 5.55999994277954102, NULL, 5.55999994277954102, NULL, 5.69999980926513672, NULL, 5.82000017166137695, NULL, 5.98000001907348633, NULL, 6.03999996185302734, NULL, 5.82999992370605469, NULL, 5.73000001907348633, NULL, 5.42999982833862305, NULL, 5.57999992370605469, NULL, 5.40999984741210938, NULL, 4.90999984741210938, NULL, 4.80000019073486328, NULL, 4.42999982833862305, NULL, 4.1399998664855957, NULL, 5.17000007629394531, NULL, 10.3000001907348633, NULL, 11.6999998092651367, NULL, 9.06999969482422053, NULL, 8.97000026702880859, NULL, 7.19000005722045898, 'E', 7.82000017166137695, 'E', 6.57999992370605469, NULL, 5.8899998664855957, NULL, 5.76999998092651367, NULL, NULL, NULL),
     ('08MG026', 2011, 10, 1, 31, 4.17999982833862305, 129.660003662109375, 27, 3.00999999046325684, 3, 6.17000007629394531, 5.32000017166137695, NULL, 4.94999980926513672, NULL, 6.17000007629394531, NULL, 6.11999988555908203, NULL, 5.46999979019165039, NULL, 5.01000022888183594, NULL, 4.94000005722045898, NULL, 4.57000017166137695, NULL, 4.53000020980834961, NULL, 4.5, NULL, 5.30000019073486328, NULL, 4.80999994277954102, NULL, 4.3600001335144043, NULL, 4.13000011444091797, NULL, 3.86999988555908203, NULL, 3.66000008583068892, NULL, 3.54999995231628418, NULL, 3.52999997138977051, 'E', 3.61999988555908203, NULL, 4.09999990463256836, NULL, 4.05999994277954102, NULL, 3.96000003814697266, NULL, 3.71000003814697266, NULL, 3.43000006675720215, NULL, 3.21000003814697266, NULL, 3.11999988555908203, NULL, 3.00999999046325684, NULL, 3.25, NULL, 3.08999991416931152, NULL, 3.24000000953674316, NULL, 3.06999993324279785, NULL),
     ('08MG026', 2011, 11, 1, 30, 2.50999999046325684, 75.220001220703125, 19, 1.84000003337860107, 27, 3.06999993324279785, 2.8599998950958252, NULL, 2.8900001049041748, NULL, 2.8900001049041748, NULL, 2.72000002861022905, NULL, 2.67000007629394531, NULL, 2.50999999046325684, NULL, 2.52999997138977051, NULL, 2.43000006675720215, NULL, 2.40000009536743208, NULL, 3.02999997138977051, NULL, 3.01999998092651367, NULL, 2.61999988555908203, NULL, 2.44000005722045898, NULL, 2.27999997138977051, NULL, 2.15000009536743208, NULL, 2.3599998950958252, NULL, 2.5, NULL, 2.33999991416931152, NULL, 1.84000003337860107, NULL, 1.99000000953674316, NULL, 2.18000006675720215, NULL, 2.47000002861022905, NULL, 2.33999991416931152, NULL, 2.30999994277954102, NULL, 2.15000009536743208, NULL, 2.31999993324279785, NULL, 3.06999993324279785, NULL, 2.76999998092651367, NULL, 2.75, NULL, 2.3900001049041748, NULL, NULL, NULL),
     ('08MG026', 2011, 12, 1, 31, 1.28999996185302712, 39.9690017700195312, 21, 0.888000011444091797, 1, 2.1099998950958252, 2.1099998950958252, NULL, 1.87000000476837203, NULL, 1.73000001907348633, NULL, 1.69000005722045898, NULL, 1.62999999523162842, NULL, 1.60000002384185791, NULL, 1.54999995231628418, NULL, 1.33000004291534424, NULL, 1.44000005722045898, NULL, 1.45000004768371582, NULL, 1.27999997138977051, NULL, 1.04999995231628418, NULL, 1.25, NULL, 1.13999998569488525, NULL, 1.10000002384185791, NULL, 1.09000003337860107, NULL, 1.16999995708465576, NULL, 1.12999999523162842, NULL, 1.02999997138977051, NULL, 1.08000004291534424, NULL, 0.888000011444091797, NULL, 0.925999999046325573, NULL, 1.12000000476837158, NULL, 1.08000004291534424, NULL, 1.00999999046325684, NULL, 0.958000004291534424, NULL, 0.996999979019165039, NULL, 1.39999997615814209, NULL, 1.44000005722045898, NULL, 1.3200000524520874, NULL, 1.11000001430511475, NULL),
     ('08MG026', 2012, 1, 1, 31, 1.40999996662139893, 43.5639991760253906, 18, 0.833000004291534424, 4, 2.93000006675720215, 1.11000001430511475, NULL, 1.19000005722045898, NULL, 1.3200000524520874, NULL, 2.93000006675720215, NULL, 2.86999988555908203, NULL, 2.25999999046325684, NULL, 1.99000000953674316, NULL, 1.82000005245208762, NULL, 2.1099998950958252, NULL, 1.64999997615814209, 'B', 1.47000002861022949, 'B', 1.60000002384185791, 'B', 1.45000004768371582, 'B', 1.41999995708465576, 'B', 1.13999998569488525, 'B', 1.04999995231628418, 'B', 0.939999997615814209, 'B', 0.833000004291534424, 'B', 1.05999994277954102, 'B', 1.25, 'B', 1.35000002384185791, 'B', 1.02999997138977051, NULL, 1.00999999046325684, NULL, 0.995999991893768422, NULL, 0.990999996662140004, NULL, 0.950999975204467773, NULL, 0.917999982833862416, NULL, 0.954999983310699574, NULL, 1.37999999523162842, NULL, 1.25, NULL, 1.26999998092651367, NULL),
     ('08MG026', 2012, 2, 1, 29, 1.11000001430511475, 32.0800018310546875, 27, 0.930000007152557373, 1, 1.25999999046325684, 1.25999999046325684, NULL, 1.20000004768371582, NULL, 1.20000004768371582, NULL, 1.20000004768371582, NULL, 1.14999997615814209, NULL, 1.15999996662139893, NULL, 1.20000004768371582, NULL, 1.13999998569488525, NULL, 1.12999999523162842, NULL, 1.14999997615814209, NULL, 1.16999995708465576, NULL, 1.16999995708465576, NULL, 1.12999999523162842, NULL, 1.10000002384185791, NULL, 1.05999994277954102, NULL, 1.08000004291534424, NULL, 1.0700000524520874, NULL, 1.08000004291534424, NULL, 1.0700000524520874, NULL, 1.03999996185302712, NULL, 1.03999996185302712, NULL, 1.09000003337860107, NULL, 1.03999996185302712, NULL, 1.09000003337860107, NULL, 1.08000004291534424, NULL, 1, NULL, 0.930000007152557373, NULL, 1.02999997138977051, NULL, 1.01999998092651367, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2012, 3, 1, 31, 0.955999970436096191, 29.6459999084472656, 19, 0.836000025272369385, 5, 1.12999999523162842, 0.972000002861022949, NULL, 0.952000021934509166, NULL, 0.978999972343444824, NULL, 1.11000001430511475, NULL, 1.12999999523162842, NULL, 0.972999989986419567, NULL, 0.989000022411346436, NULL, 1, NULL, 1.08000004291534424, NULL, 1.04999995231628418, NULL, 1.02999997138977051, NULL, 1.08000004291534424, NULL, 0.96700000762939442, NULL, 0.856999993324279785, NULL, 0.954999983310699574, NULL, 0.935000002384185791, NULL, 0.896000027656555176, NULL, 0.870999991893768311, NULL, 0.836000025272369385, NULL, 0.847000002861022949, NULL, 0.841000020503997803, NULL, 0.846000015735626221, NULL, 0.84299999475479126, NULL, 0.845000028610229492, NULL, 0.869000017642974854, NULL, 0.870000004768371582, NULL, 0.883000016212463379, NULL, 1.04999995231628418, NULL, 1.05999994277954102, NULL, 1.02999997138977051, NULL, 1, NULL),
     ('08MG026', 2012, 4, 1, 30, 2.16000008583068848, 64.792999267578125, 2, 0.96399998664855957, 26, 6.78000020980834961, 0.99900001287460316, NULL, 0.96399998664855957, NULL, 1.19000005722045898, NULL, 1.12999999523162842, NULL, 1.09000003337860107, NULL, 1.0700000524520874, NULL, 1.0700000524520874, NULL, 1.0700000524520874, NULL, 1.12000000476837158, NULL, 1.22000002861022949, NULL, 1.34000003337860107, NULL, 1.53999996185302712, NULL, 1.61000001430511475, NULL, 1.72000002861022949, NULL, 1.75999999046325684, NULL, 1.75999999046325684, NULL, 1.6799999475479126, NULL, 1.62000000476837158, NULL, 1.61000001430511475, NULL, 1.65999996662139893, NULL, 1.62000000476837158, NULL, 1.75, NULL, 2.91000008583068848, NULL, 3.84999990463256792, NULL, 5.01999998092651367, NULL, 6.78000020980834961, NULL, 4.71999979019165039, NULL, 3.75, NULL, 3.53999996185302779, NULL, 3.63000011444091797, NULL, NULL, NULL),
     ('08MG026', 2012, 5, 1, 31, 4.26999998092651367, 132.389999389648438, 5, 2.49000000953674316, 16, 6.46999979019165039, 3.32999992370605469, NULL, 2.93000006675720215, NULL, 2.72000002861022905, NULL, 2.6099998950958252, NULL, 2.49000000953674316, NULL, 2.49000000953674316, NULL, 2.74000000953674316, NULL, 3.28999996185302779, NULL, 3.31999993324279785, NULL, 2.83999991416931152, NULL, 2.66000008583068848, NULL, 2.80999994277954102, NULL, 3.57999992370605469, NULL, 4.78999996185302734, NULL, 5.96999979019165039, NULL, 6.46999979019165039, NULL, 5.76999998092651367, NULL, 4.98000001907348633, NULL, 4.5, NULL, 4.44000005722045898, NULL, 5.01000022888183594, NULL, 5.59000015258789062, NULL, 4.78999996185302734, NULL, 4.46999979019165039, NULL, 4.65999984741210938, NULL, 5.36999988555908203, NULL, 5.80999994277954102, NULL, 5.78999996185302734, NULL, 5.51999998092651367, NULL, 5.03999996185302734, NULL, 5.6100001335144043, NULL),
     ('08MG026', 2012, 6, 1, 30, 8.39999961853027344, 251.899993896484403, 8, 4.8600001335144043, 23, 14.8000001907348633, 7.46000003814697266, NULL, 7.78000020980834961, NULL, 6.05999994277954102, NULL, 5.28999996185302734, NULL, 5.38000011444091797, NULL, 5.42999982833862305, NULL, 5.13000011444091797, NULL, 4.8600001335144043, NULL, 4.8600001335144043, NULL, 5.28000020980834961, NULL, 5.90000009536743164, NULL, 7.48999977111816406, NULL, 9.07999992370605646, NULL, 8.18000030517578125, NULL, 6.82999992370605469, NULL, 8.73999977111816406, NULL, 11.6999998092651367, NULL, 11.3000001907348633, NULL, 9.15999984741210938, NULL, 8.65999984741210938, NULL, 10.3000001907348633, NULL, 12, NULL, 14.8000001907348633, NULL, 12.1000003814697283, NULL, 9.78999996185302734, NULL, 9.36999988555908203, NULL, 8.85000038146972656, NULL, 8.27000045776367188, NULL, 9.55000019073486328, NULL, 12.3000001907348633, NULL, NULL, NULL),
     ('08MG026', 2012, 7, 1, 31, 11.8999996185302717, 369.209991455078125, 31, 7.15999984741210938, 17, 17.2000007629394531, 12.1999998092651367, NULL, 10.3999996185302717, NULL, 9.67000007629394354, NULL, 8.94999980926513672, NULL, 8.80000019073486328, NULL, 9.26000022888183594, NULL, 9.97000026702880859, NULL, 11.1999998092651367, NULL, 13.1999998092651367, NULL, 15.8000001907348633, NULL, 15.1999998092651367, NULL, 14.3999996185302717, NULL, 14.8999996185302717, NULL, 16.6000003814697266, NULL, 16, NULL, 16.3999996185302734, NULL, 17.2000007629394531, NULL, 17, NULL, 14.1000003814697283, NULL, 12.8000001907348633, NULL, 11, NULL, 10.3000001907348633, NULL, 9.97999954223632812, NULL, 8.93000030517578125, NULL, 10.6000003814697283, NULL, 10.8999996185302717, NULL, 10.5, NULL, 9.52000045776367188, NULL, 8.60000038146972656, NULL, 7.67000007629394531, NULL, 7.15999984741210938, NULL),
     ('08MG026', 2012, 8, 1, 31, 6.38000011444091797, 197.92999267578125, 31, 2.79999995231628418, 6, 11, 6.88000011444091797, NULL, 6.94999980926513672, NULL, 7.32000017166137695, NULL, 8.82999992370605469, NULL, 10.5, NULL, 11, NULL, 10.3999996185302717, NULL, 10.3999996185302717, NULL, 8.06000041961669922, NULL, 6.73999977111816406, NULL, 6.67000007629394531, NULL, 6.82000017166137695, NULL, 6.42999982833862305, NULL, 7.26999998092651367, NULL, 7.1399998664855957, NULL, 6.61999988555908203, NULL, 6.76999998092651367, NULL, 6.88000011444091797, NULL, 7.32999992370605469, NULL, 6.32999992370605469, NULL, 5.36999988555908203, NULL, 4.84999990463256836, NULL, 4.3899998664855957, NULL, 3.86999988555908203, NULL, 3.74000000953674316, NULL, 3.98000001907348633, NULL, 3.99000000953674316, NULL, 3.44000005722045898, NULL, 3.11999988555908203, NULL, 3.03999996185302779, NULL, 2.79999995231628418, NULL),
     ('08MG026', 2012, 9, 1, 30, 2.70000004768371582, 80.8700027465820312, 30, 2.20000004768371582, 8, 3.36999988555908203, 2.6099998950958252, NULL, 2.5, NULL, 2.52999997138977051, NULL, 2.70000004768371582, NULL, 2.88000011444091797, NULL, 2.80999994277954102, NULL, 3.06999993324279785, NULL, 3.36999988555908203, NULL, 3.28999996185302779, NULL, 3.16000008583068848, NULL, 2.46000003814697266, NULL, 2.27999997138977051, NULL, 2.41000008583068848, NULL, 2.3599998950958252, NULL, 2.36999988555908203, NULL, 2.40000009536743208, NULL, 2.40000009536743208, NULL, 2.41000008583068848, NULL, 2.51999998092651367, NULL, 2.8900001049041748, NULL, 3.09999990463256836, NULL, 3.09999990463256836, NULL, 3.26999998092651367, NULL, 3.17000007629394531, NULL, 2.71000003814697266, NULL, 2.45000004768371582, NULL, 2.29999995231628418, NULL, 2.61999988555908203, NULL, 2.52999997138977051, NULL, 2.20000004768371582, NULL, NULL, NULL),
     ('08MG026', 2012, 10, 1, 31, 3.00999999046325684, 93.3300018310546733, 11, 1.53999996185302712, 19, 8.90999984741210938, 3.07999992370605469, NULL, 2.77999997138977051, NULL, 2.09999990463256836, NULL, 1.91999995708465598, NULL, 1.74000000953674316, NULL, 1.6799999475479126, NULL, 1.71000003814697288, NULL, 1.70000004768371582, NULL, 1.65999996662139893, NULL, 1.60000002384185791, NULL, 1.53999996185302712, NULL, 1.61000001430511475, NULL, 1.99000000953674316, NULL, 8.47999954223632812, NULL, 4.71000003814697266, NULL, 4.17000007629394531, NULL, 2.6400001049041748, NULL, 5.32999992370605469, NULL, 8.90999984741210938, NULL, 3.91000008583068892, NULL, 3.05999994277954102, NULL, 2.61999988555908203, NULL, 2.3599998950958252, NULL, 2.13000011444091797, NULL, 1.96000003814697288, NULL, 1.92999994754791282, NULL, 1.90999996662139893, NULL, 1.96000003814697288, NULL, 2.59999990463256836, NULL, 3.28999996185302779, NULL, 6.25, NULL),
     ('08MG026', 2012, 11, 1, 30, 2.83999991416931152, 85.0500030517578125, 28, 1.75999999046325684, 5, 6.48999977111816406, 5.6399998664855957, NULL, 3.81999993324279785, NULL, 4.86999988555908203, NULL, 6.46999979019165039, NULL, 6.48999977111816406, NULL, 4.48999977111816406, NULL, 3.75, NULL, 3.02999997138977051, NULL, 2.49000000953674316, NULL, 2.17000007629394531, NULL, 2.3599998950958252, NULL, 2.41000008583068848, NULL, 2.28999996185302779, NULL, 2.15000009536743208, NULL, 2.02999997138977051, NULL, 1.88999998569488525, NULL, 2.52999997138977051, NULL, 2.26999998092651367, NULL, 2.22000002861022905, NULL, 2.18000006675720215, NULL, 2.09999990463256836, NULL, 1.99000000953674316, NULL, 2.04999995231628418, NULL, 1.96000003814697288, NULL, 1.78999996185302712, NULL, 1.77999997138977051, NULL, 1.78999996185302712, NULL, 1.75999999046325684, NULL, 2.05999994277954102, NULL, 2.22000002861022905, NULL, NULL, NULL),
     ('08MG026', 2012, 12, 1, 31, 1.49000000953674316, 46.3300018310546875, 30, 1.09000003337860107, 1, 2.34999990463256836, 2.34999990463256836, NULL, 2.25999999046325684, NULL, 2.21000003814697266, NULL, 2.21000003814697266, NULL, 2.02999997138977051, NULL, 1.89999997615814209, NULL, 1.80999994277954102, NULL, 1.66999995708465576, NULL, 1.63999998569488525, NULL, 1.54999995231628418, NULL, 1.49000000953674316, NULL, 1.35000002384185791, NULL, 1.33000004291534424, NULL, 1.25999999046325684, NULL, 1.26999998092651367, NULL, 1.29999995231628418, NULL, 1.3200000524520874, NULL, 1.22000002861022949, NULL, 1.26999998092651367, NULL, 1.39999997615814209, NULL, 1.30999994277954102, NULL, 1.28999996185302712, NULL, 1.27999997138977051, NULL, 1.24000000953674316, NULL, 1.25, NULL, 1.23000001907348633, NULL, 1.20000004768371582, NULL, 1.21000003814697288, NULL, 1.21000003814697288, NULL, 1.09000003337860107, NULL, 1.1799999475479126, NULL),
     ('08MG026', 2013, 1, 1, 31, 0.941999971866607555, 29.2099990844726562, 12, 0.652000010013580322, 5, 1.16999995708465576, 1.12999999523162842, NULL, 1.13999998569488525, NULL, 1.14999997615814209, NULL, 1.15999996662139893, NULL, 1.16999995708465576, NULL, 1.14999997615814209, NULL, 1.14999997615814209, NULL, 1.13999998569488525, NULL, 1.15999996662139893, NULL, 0.981999993324279785, NULL, 0.772000014781951904, NULL, 0.652000010013580322, 'E', 0.708999991416931152, 'E', 0.754000008106231689, 'E', 0.837999999523162842, 'E', 0.904999971389770397, 'E', 0.944000005722046009, 'E', 0.862999975681304932, NULL, 0.825999975204467773, NULL, 0.800999999046325684, NULL, 0.805000007152557373, NULL, 0.794000029563903809, NULL, 0.890999972820281982, NULL, 0.935999989509582409, NULL, 0.939000010490417591, NULL, 0.921999990940093994, NULL, 0.925000011920928955, NULL, 0.912999987602233998, NULL, 0.892000019550323486, NULL, 0.888000011444091797, NULL, 0.908999979496002197, NULL),
     ('08MG026', 2013, 2, 1, 28, 0.827000021934509277, 23.1669998168945312, 19, 0.741999983787536621, 5, 0.920000016689300426, 0.896000027656555176, NULL, 0.876999974250793457, NULL, 0.884999990463256836, NULL, 0.90799999237060558, NULL, 0.920000016689300426, NULL, 0.903999984264373779, NULL, 0.902000010013580433, NULL, 0.856999993324279785, NULL, 0.805000007152557373, NULL, 0.746999979019165039, NULL, 0.772000014781951904, NULL, 0.778999984264373779, NULL, 0.769999980926513672, NULL, 0.753000020980834961, NULL, 0.762000024318695068, NULL, 0.851999998092651367, NULL, 0.799000024795532227, NULL, 0.81800001859664917, NULL, 0.741999983787536621, NULL, 0.744000017642974854, NULL, 0.864000022411346436, NULL, 0.875, NULL, 0.828999996185302734, NULL, 0.824000000953674316, NULL, 0.845000028610229492, NULL, 0.811999976634979248, NULL, 0.808000028133392334, NULL, 0.81800001859664917, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2013, 3, 1, 31, 1.45000004768371582, 45, 11, 1.04999995231628418, 14, 2.34999990463256836, 1.51999998092651367, NULL, 2.03999996185302779, NULL, 1.59000003337860107, NULL, 1.38999998569488525, NULL, 1.3200000524520874, NULL, 1.23000001907348633, NULL, 1.15999996662139893, NULL, 1.11000001430511475, NULL, 1.0700000524520874, NULL, 1.0700000524520874, NULL, 1.04999995231628418, NULL, 1.13999998569488525, NULL, 1.74000000953674316, NULL, 2.34999990463256836, NULL, 2.17000007629394531, NULL, 2.06999993324279785, NULL, 1.84000003337860107, NULL, 1.66999995708465576, NULL, 1.55999994277954102, NULL, 1.55999994277954102, NULL, 1.39999997615814209, NULL, 1.33000004291534424, NULL, 1.26999998092651367, NULL, 1.24000000953674316, NULL, 1.23000001907348633, NULL, 1.20000004768371582, NULL, 1.21000003814697288, NULL, 1.23000001907348633, NULL, 1.28999996185302712, NULL, 1.37000000476837158, NULL, 1.58000004291534424, NULL),
     ('08MG026', 2013, 4, 1, 30, 2.16000008583068848, 64.6999969482421875, 22, 1.62000000476837158, 6, 3.16000008583068848, 2.00999999046325684, NULL, 2.29999995231628418, NULL, 2.27999997138977051, NULL, 2.3900001049041748, NULL, 3.00999999046325684, NULL, 3.16000008583068848, NULL, 2.75999999046325684, NULL, 2.40000009536743208, NULL, 2.25, NULL, 2.52999997138977051, NULL, 2.42000007629394531, NULL, 2.26999998092651367, NULL, 2.09999990463256836, NULL, 1.97000002861022927, NULL, 1.83000004291534402, NULL, 1.74000000953674316, NULL, 1.66999995708465576, NULL, 1.66999995708465576, NULL, 1.72000002861022949, NULL, 1.76999998092651367, NULL, 1.70000004768371582, NULL, 1.62000000476837158, NULL, 1.63999998569488525, NULL, 1.72000002861022949, NULL, 1.91999995708465598, NULL, 2.36999988555908203, NULL, 2.71000003814697266, NULL, 2.48000001907348633, NULL, 2.24000000953674316, NULL, 2.04999995231628418, NULL, NULL, NULL),
     ('08MG026', 2013, 5, 1, 31, 7.3600001335144043, 228.309997558593722, 2, 1.94000005722045898, 12, 25.6000003814697266, 1.95000004768371604, NULL, 1.94000005722045898, NULL, 2.16000008583068848, NULL, 3.09999990463256836, NULL, 5.23999977111816406, NULL, 7.96000003814697266, NULL, 9.81000041961669922, NULL, 9.85000038146972834, NULL, 9.22000026702880859, NULL, 9.35000038146972834, NULL, 9.60999965667724609, NULL, 25.6000003814697266, 'E', 15.6999998092651367, NULL, 10.3000001907348633, NULL, 7.92000007629394531, NULL, 7.1100001335144043, NULL, 6.98000001907348633, NULL, 7.01999998092651367, NULL, 6.65000009536743164, NULL, 6.42000007629394531, NULL, 6.51999998092651367, NULL, 6.13000011444091797, NULL, 6.42999982833862305, NULL, 5.88000011444091797, NULL, 5.51999998092651367, NULL, 5.32999992370605469, NULL, 5.30999994277954102, NULL, 5.67000007629394531, NULL, 5.8899998664855957, NULL, 6.07999992370605469, NULL, 5.65999984741210938, NULL),
     ('08MG026', 2013, 6, 1, 30, 9.68000030517577947, 290.269989013671875, 1, 5.51999998092651367, 30, 15.8999996185302717, 5.51999998092651367, NULL, 5.76000022888183594, NULL, 6.51000022888183594, NULL, 7.6399998664855957, NULL, 8.93999958038330078, NULL, 9.53999996185302734, NULL, 10.3999996185302717, NULL, 10.1000003814697283, NULL, 8.40999984741210938, NULL, 7.69000005722045898, NULL, 7.40000009536743164, NULL, 6.90000009536743164, NULL, 6.73000001907348633, NULL, 6.71000003814697266, NULL, 7.07999992370605469, NULL, 8.59000015258789062, NULL, 9.94999980926513672, NULL, 10.1000003814697283, NULL, 10, NULL, 11.3999996185302717, NULL, 10.5, NULL, 10.3999996185302717, NULL, 10.8999996185302717, NULL, 12.6000003814697283, NULL, 12.3000001907348633, NULL, 11.8999996185302717, NULL, 12.3000001907348633, NULL, 12.5, NULL, 15.6000003814697283, NULL, 15.8999996185302717, NULL, NULL, NULL),
     ('08MG026', 2013, 7, 1, 31, 8.51000022888183594, 263.69000244140625, 30, 5.82999992370605469, 1, 18.399999618530277, 18.399999618530277, NULL, 18.1000003814697266, NULL, 14.8999996185302717, NULL, 12, NULL, 10.1999998092651367, NULL, 9.14999961853027166, NULL, 8.73999977111816406, NULL, 8.47000026702880859, NULL, 8.75, NULL, 8.81999969482421875, NULL, 8.03999996185302734, NULL, 6.88000011444091797, NULL, 6.25, NULL, 6.07999992370605469, NULL, 5.94999980926513672, NULL, 6.42000007629394531, NULL, 7.15999984741210938, NULL, 7.55000019073486328, NULL, 7.96999979019165039, NULL, 8.06000041961669922, NULL, 7.96000003814697266, NULL, 7.86999988555908203, NULL, 7.59000015258789062, NULL, 7.32000017166137695, NULL, 7.05999994277954102, NULL, 7.05000019073486328, NULL, 6.73999977111816406, NULL, 6.25, NULL, 5.92999982833862305, NULL, 5.82999992370605469, NULL, 6.19999980926513672, NULL),
     ('08MG026', 2013, 8, 1, 31, 6.40999984741210938, 198.839996337890653, 21, 4.55999994277954102, 30, 12.5, 6.94000005722045898, NULL, 6.6399998664855957, NULL, 7.01000022888183594, NULL, 7.23000001907348633, NULL, 7.15000009536743164, NULL, 7.13000011444091797, NULL, 6.73999977111816406, NULL, 6.42999982833862305, NULL, 6.6399998664855957, NULL, 6.73000001907348633, NULL, 6.44000005722045898, NULL, 6.09000015258789062, NULL, 5.76000022888183594, NULL, 5.26999998092651367, NULL, 5.94999980926513672, NULL, 6.32000017166137695, NULL, 7, NULL, 5.71999979019165039, NULL, 5.15000009536743164, NULL, 4.67000007629394531, NULL, 4.55999994277954102, NULL, 4.78999996185302734, NULL, 5.11999988555908203, NULL, 5.48999977111816406, NULL, 4.78000020980834961, NULL, 4.59999990463256836, NULL, 5.13000011444091797, NULL, 7.03999996185302734, NULL, 10.6000003814697283, NULL, 12.5, 'E', 7.21999979019165039, NULL),
     ('08MG026', 2013, 9, 1, 30, 5.25, 157.419998168945312, 26, 3.20000004768371582, 16, 7.1399998664855957, 7.09999990463256836, NULL, 6.90000009536743164, NULL, 6.80999994277954102, NULL, 6.07999992370605469, NULL, 6.19999980926513672, NULL, 6.19999980926513672, NULL, 6.40000009536743164, NULL, 6.21000003814697266, NULL, 5.98999977111816406, NULL, 5.92999982833862305, NULL, 7, NULL, 7.05999994277954102, NULL, 6.57000017166137695, NULL, 6.76999998092651367, NULL, 7.05000019073486328, NULL, 7.1399998664855957, NULL, 4.92999982833862305, NULL, 3.63000011444091797, NULL, 3.25999999046325684, NULL, 3.36999988555908203, NULL, 3.90000009536743208, NULL, 3.54999995231628418, NULL, 3.65000009536743208, 'E', 3.45000004768371582, 'E', 3.25999999046325684, 'E', 3.20000004768371582, 'E', 3.23000001907348633, 'E', 4.80999994277954102, 'E', 3.83999991416931197, NULL, 3.93000006675720215, NULL, NULL, NULL),
     ('08MG026', 2013, 10, 1, 31, 2.31999993324279785, 72.0199966430664062, 31, 1.5700000524520874, 6, 4.48999977111816406, 3.41000008583068848, 'E', 3.15000009536743208, 'E', 3.05999994277954102, 'E', 3.02999997138977051, 'E', 3.34999990463256836, 'E', 4.48999977111816406, NULL, 4.17999982833862305, NULL, 3.3900001049041748, 'E', 2.84999990463256836, 'E', 2.51999998092651367, 'E', 2.25999999046325684, 'E', 2.06999993324279785, 'E', 1.92999994754791282, 'E', 1.84000003337860107, 'E', 1.78999996185302712, 'E', 1.76999998092651367, 'E', 1.75999999046325684, 'E', 1.75999999046325684, 'E', 1.76999998092651367, 'E', 1.78999996185302712, 'E', 1.87999999523162842, 'E', 1.95000004768371604, 'E', 1.95000004768371604, 'E', 1.92999994754791282, 'E', 1.89999997615814209, 'E', 1.85000002384185791, 'E', 1.79999995231628418, 'E', 1.73000001907348633, 'E', 1.66999995708465576, 'E', 1.62000000476837158, 'E', 1.5700000524520874, 'E'),
     ('08MG026', 2013, 11, 1, 30, 1.40999996662139893, 42.2599983215332031, 28, 1.05999994277954102, 14, 1.75999999046325684, 1.51999998092651367, 'E', 1.69000005722045898, 'E', 1.58000004291534424, 'E', 1.5, 'E', 1.45000004768371582, 'E', 1.39999997615814209, 'E', 1.5, 'E', 1.54999995231628418, 'E', 1.5, 'E', 1.45000004768371582, 'E', 1.38999998569488525, 'E', 1.5, 'E', 1.75, 'E', 1.75999999046325684, 'E', 1.72000002861022949, 'E', 1.64999997615814209, 'E', 1.5700000524520874, 'E', 1.51999998092651367, 'E', 1.48000001907348633, 'E', 1.37000000476837158, 'E', 1.28999996185302712, 'E', 1.24000000953674316, 'E', 1.19000005722045898, 'E', 1.15999996662139893, 'E', 1.13999998569488525, 'E', 1.10000002384185791, 'E', 1.0700000524520874, 'E', 1.05999994277954102, 'E', 1.05999994277954102, 'E', 1.10000002384185791, 'E', NULL, NULL),
     ('08MG026', 2013, 12, 1, 31, 0.922999978065490834, 28.6130008697509766, 31, 0.861000001430511475, 1, 1.13999998569488525, 1.13999998569488525, 'E', 1.13999998569488525, 'E', 1.0700000524520874, 'E', 1.02999997138977051, 'E', 0.980000019073486439, 'E', 0.939999997615814209, 'E', 0.91000002622604359, 'E', 0.894999980926513672, 'E', 0.888999998569488525, 'E', 0.883000016212463379, 'E', 0.879999995231628418, 'E', 0.879000008106231689, 'E', 0.88200002908706665, 'E', 0.888999998569488525, 'E', 0.898000001907348633, 'E', 0.908999979496002197, 'E', 0.913999974727630615, 'E', 0.912000000476837158, 'E', 0.91000002622604359, 'E', 0.906000018119812012, 'E', 0.901000022888183594, 'E', 0.894999980926513672, 'E', 0.888000011444091797, 'E', 0.880999982357025146, 'E', 0.875999987125396729, 'E', 0.875, 'E', 0.904999971389770397, 'E', 0.913999974727630615, 'E', 0.888999998569488525, 'E', 0.871999979019165039, 'E', 0.861000001430511475, 'E'),
     ('08MG026', 2014, 1, 1, 31, 0.723999977111816406, 22.4549999237060511, 31, 0.544000029563903809, 3, 0.898000001907348633, 0.843999981880187988, 'E', 0.873000025749206543, 'E', 0.898000001907348633, 'E', 0.865999996662139893, 'E', 0.837999999523162842, 'E', 0.816999971866607666, 'E', 0.810000002384185791, 'E', 0.77499997615814209, 'E', 0.749000012874603271, NULL, 0.769999980926513672, NULL, 0.813000023365020752, NULL, 0.744000017642974854, NULL, 0.769999980926513672, NULL, 0.805000007152557373, NULL, 0.797999978065490723, NULL, 0.754000008106231689, NULL, 0.711000025272369385, NULL, 0.662999987602233887, NULL, 0.640999972820281982, NULL, 0.628000020980834961, NULL, 0.623000025749206543, NULL, 0.612999975681304932, NULL, 0.609000027179718018, NULL, 0.628000020980834961, NULL, 0.643999993801116943, NULL, 0.648000001907348633, NULL, 0.629000008106231689, NULL, 0.643999993801116943, NULL, 0.667999982833862305, NULL, 0.638000011444091797, NULL, 0.544000029563903809, NULL),
     ('08MG026', 2014, 2, 1, 28, 0.610000014305114746, 17.0750007629394531, 24, 0.505999982357025146, 12, 0.726999998092651367, 0.545000016689300537, NULL, 0.561999976634979248, NULL, 0.532999992370605469, NULL, 0.531000018119812012, NULL, 0.55699998140335083, NULL, 0.593999981880187988, NULL, 0.597999989986419678, NULL, 0.602999985218048096, NULL, 0.602999985218048096, NULL, 0.640999972820281982, NULL, 0.699000000953674316, NULL, 0.726999998092651367, NULL, 0.722999989986419678, NULL, 0.726000010967254639, NULL, 0.718999981880187988, NULL, 0.670000016689300537, NULL, 0.662000000476837158, NULL, 0.660000026226043701, NULL, 0.621999979019165039, NULL, 0.625999987125396729, NULL, 0.583999991416931152, NULL, 0.55699998140335083, NULL, 0.537000000476837158, NULL, 0.505999982357025146, NULL, 0.515999972820281982, NULL, 0.546999990940093994, NULL, 0.593999981880187988, NULL, 0.633000016212463379, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2014, 3, 1, 31, 0.644999980926513672, 20, 2, 0.510999977588653564, 30, 0.887000024318695068, 0.546999990940093994, NULL, 0.510999977588653564, NULL, 0.518999993801116943, NULL, 0.584999978542327881, NULL, 0.625999987125396729, NULL, 0.609000027179718018, NULL, 0.620000004768371582, NULL, 0.663999974727630615, NULL, 0.65700000524520874, NULL, 0.639999985694885254, NULL, 0.629000008106231689, 'A', 0.640999972820281982, NULL, 0.669000029563903809, NULL, 0.708000004291534424, NULL, 0.663999974727630615, NULL, 0.657999992370605469, NULL, 0.642000019550323486, NULL, 0.620000004768371582, NULL, 0.637000024318695068, NULL, 0.602999985218048096, NULL, 0.559000015258789062, NULL, 0.544000029563903809, NULL, 0.572000026702880859, NULL, 0.646000027656555176, NULL, 0.657999992370605469, NULL, 0.638999998569488525, 'E', 0.630999982357025146, 'E', 0.677999973297119141, 'E', 0.885999977588653564, 'E', 0.887000024318695068, 'E', 0.851000010967254639, 'E'),
     ('08MG026', 2014, 4, 1, 30, 1.33000004291534424, 39.8069992065429688, 2, 0.833999991416931152, 30, 1.76999998092651367, 0.847999989986419678, 'E', 0.833999991416931152, 'E', 0.842000007629394531, 'E', 0.870999991893768311, 'E', 0.903999984264373779, 'E', 0.967999994754791149, 'E', 1.0700000524520874, 'E', 1.41999995708465576, 'E', 1.37000000476837158, 'E', 1.25, 'E', 1.26999998092651367, 'E', 1.28999996185302712, 'E', 1.28999996185302712, 'E', 1.33000004291534424, 'E', 1.36000001430511475, 'E', 1.39999997615814209, 'E', 1.5700000524520874, 'E', 1.59000003337860107, 'E', 1.51999998092651367, 'E', 1.48000001907348633, 'E', 1.52999997138977051, 'E', 1.61000001430511475, 'E', 1.52999997138977051, 'E', 1.52999997138977051, 'E', 1.5, 'E', 1.48000001907348633, 'E', 1.47000002861022949, 'E', 1.44000005722045898, 'E', 1.47000002861022949, 'E', 1.76999998092651367, 'E', NULL, NULL),
     ('08MG026', 2014, 5, 1, 31, 5.30000019073486328, 164.360000610351562, 1, 3.03999996185302779, 23, 12.3999996185302717, 3.03999996185302779, 'E', 4.05000019073486328, 'E', 4.23000001907348633, 'E', 3.56999993324279785, 'E', 3.24000000953674316, 'E', 3.19000005722045898, 'E', 3.19000005722045898, 'E', 3.36999988555908203, 'E', 3.3900001049041748, 'E', 3.34999990463256836, 'E', 3.52999997138977051, 'E', 3.70000004768371582, 'E', 4.21999979019165039, 'E', 5.1399998664855957, 'E', 5.82999992370605469, 'E', 6.21999979019165039, 'E', 5.84999990463256836, 'E', 5.40999984741210938, 'E', 4.82999992370605469, 'E', 4.8899998664855957, 'E', 5.32999992370605469, 'E', 5.53999996185302734, 'E', 12.3999996185302717, 'E', 12, 'E', 9.10000038146972834, 'E', 7.90000009536743164, 'E', 6.21000003814697266, 'E', 5.28000020980834961, 'E', 5.23999977111816406, 'E', 5.44000005722045898, 'E', 5.67999982833862305, 'E'),
     ('08MG026', 2014, 6, 1, 30, 8.44999980926513672, 253.3800048828125, 1, 6.55999994277954102, 28, 9.98999977111816406, 6.55999994277954102, 'E', 7.1100001335144043, 'E', 7.65000009536743164, 'E', 7.6399998664855957, 'E', 6.94999980926513672, 'E', 7.15999984741210938, 'E', 7.57000017166137695, 'E', 7.71999979019165039, 'E', 8.05000019073486328, 'E', 7.88000011444091797, 'E', 7.55000019073486328, 'E', 7.84000015258789062, 'E', 8.43999958038330078, 'E', 8.13000011444091797, 'E', 8.57999992370605469, 'E', 8.02999973297119141, 'E', 8.31999969482421875, 'E', 9.14999961853027166, 'E', 9.40999984741210938, 'E', 9.36999988555908203, 'E', 8.46000003814697266, 'E', 8.64000034332275391, 'E', 9.02999973297119141, 'E', 9.48999977111816406, 'E', 9.59000015258789062, 'E', 9.72999954223632812, 'E', 9.94999980926513672, 'E', 9.98999977111816406, 'E', 9.78999996185302734, 'E', 9.60000038146972834, 'E', NULL, NULL),
     ('08MG026', 2014, 7, 1, 31, 7.98000001907348633, 247.339996337890653, 31, 5.75, 2, 11, 10.3999996185302717, 'E', 11, 'E', 10.1000003814697283, 'E', 9.21000003814697266, 'E', 8.75, 'E', 9.09000015258789062, 'E', 9.02999973297119141, 'E', 9, 'E', 8.94999980926513672, 'E', 8.77999973297119141, 'E', 8.48999977111816406, 'E', 8.82999992370605469, 'E', 8.77000045776367188, 'E', 9.18000030517577947, 'E', 9, 'E', 8.63000011444091797, 'E', 8.36999988555908203, 'E', 7.40999984741210938, 'E', 8.5, 'E', 7.34000015258789062, 'E', 7, 'E', 6.53000020980834961, 'E', 6.73000001907348633, 'E', 7.34000015258789062, 'E', 5.92000007629394531, 'E', 5.8600001335144043, 'E', 5.78999996185302734, 'E', 5.78000020980834961, 'E', 5.98000001907348633, 'E', 5.82999992370605469, 'E', 5.75, 'E'),
     ('08MG026', 2014, 8, 1, 31, 4.94999980926513672, 153.589996337890625, 31, 3.20000004768371582, 3, 6.11999988555908203, 5.61999988555908203, 'E', 5.80999994277954102, 'E', 6.11999988555908203, 'E', 6.03999996185302734, 'E', 5.76000022888183594, 'E', 5.51000022888183594, 'E', 5.19999980926513672, 'E', 4.90999984741210938, 'E', 4.94000005722045898, 'E', 5.05000019073486328, 'E', 5.57000017166137695, 'E', 5.71999979019165039, 'E', 5.61999988555908203, 'E', 5.80000019073486328, 'E', 5.73000001907348633, 'E', 5.44000005722045898, 'E', 5.26999998092651367, 'E', 5.1100001335144043, 'E', 4.82000017166137695, 'E', 4.30999994277954102, 'E', 4.03999996185302734, 'E', 3.99000000953674316, 'E', 4.1399998664855957, 'E', 4.17999982833862305, 'E', 4.1399998664855957, 'E', 4.48000001907348633, 'E', 4.65000009536743164, 'E', 4.48999977111816406, 'E', 4.23000001907348633, 'E', 3.70000004768371582, 'E', 3.20000004768371582, 'E'),
     ('08MG026', 2014, 9, 1, 30, 4.09999990463256836, 123.029998779296875, 11, 2.79999995231628418, 24, 7.61999988555908203, 3.16000008583068848, 'E', 3.24000000953674316, 'E', 2.97000002861022905, 'E', 3.11999988555908203, 'E', 3.42000007629394531, 'E', 4.01000022888183594, 'E', 4.1399998664855957, 'E', 4.03000020980834961, 'E', 3.55999994277954102, 'E', 3.16000008583068848, 'E', 2.79999995231628418, 'E', 2.86999988555908203, 'E', 3.03999996185302779, 'E', 3.32999992370605469, 'E', 3.63000011444091797, 'E', 3.59999990463256836, 'E', 3.94000005722045898, 'E', 4.6399998664855957, 'E', 4.71999979019165039, 'E', 4.42000007629394531, 'E', 4.92000007629394531, 'E', 5.19999980926513672, 'E', 5.09999990463256836, 'E', 7.61999988555908203, 'E', 5.44999980926513672, 'E', 4.90999984741210938, 'E', 4.51000022888183594, 'E', 4.25, 'E', 4.80999994277954102, 'E', 4.46000003814697266, 'E', NULL, NULL),
     ('08MG026', 2014, 10, 1, 31, 6.07000017166137695, 188.32000732421875, 2, 3.69000005722045898, 30, 10, 3.98000001907348633, 'E', 3.69000005722045898, 'E', 4.07999992370605469, 'E', 5.78999996185302734, 'E', 4.78999996185302734, 'E', 6.15000009536743164, 'E', 5.25, 'E', 4.8600001335144043, 'E', 4.76999998092651367, 'E', 4.73999977111816406, 'E', 5.3600001335144043, 'E', 4.71000003814697266, 'E', 5.32999992370605469, 'E', 5.03000020980834961, 'E', 4.42000007629394531, 'E', 4, 'E', 4.92999982833862305, 'E', 5.53999996185302734, 'E', 6.17000007629394531, 'E', 9.51000022888183594, 'E', 6.40000009536743164, 'E', 9.06000041961669922, 'E', 6.53000020980834961, 'E', 6.5, 'E', 6.90000009536743164, 'E', 7.30999994277954102, 'E', 6.63000011444091797, 'E', 7.86999988555908203, 'E', 9.76000022888183594, 'E', 10, 'E', 8.26000022888183594, 'E'),
     ('08MG026', 2014, 11, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 5.55999994277954102, 'E', 4.86999988555908203, 'E', 5.13000011444091797, 'E', 6.17000007629394531, 'E', 5.19000005722045898, 'E', 9.18999958038330078, 'E', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2015, 1, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1.75, 'B', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2015, 4, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1.83000004291534402, 'E', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2015, 6, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 6.17999982833862305, 'E', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2015, 7, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 4.36999988555908203, 'E', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3.1400001049041748, 'E', NULL, NULL, NULL, NULL, NULL, NULL),
     ('08MG026', 2015, 9, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3.63000011444091797, 'E', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2.67000007629394531, 'E', 4.05999994277954102, 'E', 4.21000003814697266, 'E', 2.83999991416931152, 'E', 2.6400001049041748, 'E', 2.52999997138977051, 'E', 2.46000003814697266, 'E', 2.40000009536743208, 'E', NULL, NULL),
     ('08MG026', 2015, 10, 1, 31, 2.74000000953674316, 84.9000015258789062, 6, 1.92999994754791282, 11, 6.98000001907348633, 2.29999995231628418, 'E', 2.29999995231628418, 'E', 2.11999988555908203, 'E', 2.02999997138977051, 'E', 2.02999997138977051, 'E', 1.92999994754791282, 'E', 1.92999994754791282, 'E', 2.06999993324279785, 'E', 2.25, 'E', 5.19999980926513672, 'E', 6.98000001907348633, 'E', 4.57000017166137695, 'E', 3.29999995231628418, 'E', 2.93000006675720215, 'E', 2.94000005722045898, 'E', 2.91000008583068848, 'E', 3.15000009536743208, 'E', 3.20000004768371582, 'E', 2.84999990463256836, 'E', 2.59999990463256836, 'E', 2.6099998950958252, 'E', 2.3900001049041748, 'E', 2.28999996185302779, 'E', 2.26999998092651367, 'E', 2.25, 'E', 2.22000002861022905, 'E', 2.1099998950958252, 'E', 2.24000000953674316, 'E', 2.11999988555908203, 'E', 2.31999993324279785, 'E', 2.49000000953674316, 'E'),
     ('08MG026', 2015, 11, 1, 30, 2.49000000953674316, 74.8199996948242188, 30, 1.40999996662139893, 8, 3.68000006675720215, 2.48000001907348633, 'E', 2.17000007629394531, 'E', 2.02999997138977051, 'E', 1.95000004768371604, 'E', 1.88999998569488525, 'E', 1.94000005722045898, 'E', 3.67000007629394487, 'E', 3.68000006675720215, 'E', 3.25999999046325684, 'E', 2.91000008583068848, 'E', 2.75, 'E', 2.55999994277954102, 'E', 3.31999993324279785, 'E', 3.20000004768371582, 'E', 2.96000003814697266, 'E', 2.72000002861022905, 'E', 3.19000005722045898, 'E', 3.36999988555908203, 'E', 2.95000004768371582, 'E', 2.67000007629394531, 'E', 2.46000003814697266, 'E', 2.29999995231628418, 'E', 2.23000001907348633, 'E', 2.07999992370605469, 'E', 1.95000004768371604, 'E', 1.85000002384185791, 'E', 1.74000000953674316, 'E', 1.65999996662139893, 'E', 1.47000002861022949, 'E', 1.40999996662139893, 'E', NULL, NULL),
     ('08MG026', 2015, 12, 1, 31, 2.11999988555908203, 65.6500015258789062, 29, 1.12999999523162842, 3, 4.8600001335144043, 1.39999997615814209, 'E', 1.37999999523162842, 'E', 4.8600001335144043, 'E', 3.57999992370605469, 'E', 2.76999998092651367, 'E', 2.56999993324279785, 'E', 2.70000004768371582, 'E', 3.90000009536743208, 'E', 3.72000002861022949, 'E', 3.00999999046325684, 'E', 2.67000007629394531, 'E', 2.51999998092651367, 'E', 2.3900001049041748, 'E', 2.17000007629394531, 'E', 2.04999995231628418, 'E', 1.82000005245208762, 'E', 1.87000000476837203, 'E', 1.84000003337860107, 'E', 1.79999995231628418, 'E', 1.74000000953674316, 'E', 1.61000001430511475, 'E', 1.51999998092651367, 'E', 1.46000003814697288, 'E', 1.41999995708465576, 'E', 1.35000002384185791, 'E', 1.39999997615814209, 'E', 1.34000003337860107, 'E', 1.26999998092651367, 'E', 1.12999999523162842, 'E', 1.13999998569488525, 'E', 1.25, 'E'),
     ('08MG026', 2016, 1, 1, 31, 1.59000003337860107, 49.3889999389648509, 15, 0.978999972343444824, 28, 7.03999996185302734, 1.27999997138977051, 'E', 1.25999999046325684, 'E', 1.19000005722045898, 'E', 1.25999999046325684, 'E', 1.22000002861022949, 'E', 1.19000005722045898, 'E', 1.12999999523162842, 'E', 1.11000001430511475, 'E', 1.04999995231628418, 'E', 1.00999999046325684, 'E', 1.04999995231628418, 'E', 1.08000004291534424, 'E', 1.05999994277954102, 'E', 1.01999998092651367, 'E', 0.978999972343444824, 'E', 1.00999999046325684, 'E', 1.05999994277954102, 'E', 1.05999994277954102, 'E', 1.0700000524520874, 'E', 1.04999995231628418, 'E', 1.22000002861022949, 'E', 2.18000006675720215, 'E', 1.64999997615814209, 'E', 1.48000001907348633, 'E', 1.40999996662139893, 'E', 1.52999997138977051, 'E', 2.05999994277954102, 'E', 7.03999996185302734, 'E', 3.61999988555908203, 'E', 2.75999999046325684, 'E', 2.29999995231628418, 'E'),
     ('08MG026', 2016, 2, 1, 29, 1.84000003337860107, 53.3499984741210866, 26, 1.50999999046325684, 12, 2.48000001907348633, 2.06999993324279785, 'E', 1.85000002384185791, 'E', 1.75999999046325684, 'E', 1.64999997615814209, 'E', 1.75999999046325684, 'E', 1.69000005722045898, 'E', 1.5700000524520874, 'E', 1.5700000524520874, 'E', 1.62000000476837158, 'E', 1.74000000953674316, 'E', 1.82000005245208762, 'E', 2.48000001907348633, 'E', 2.45000004768371582, 'E', 2.23000001907348633, 'E', 2.20000004768371582, 'E', 2.17000007629394531, 'E', 2.07999992370605469, 'E', 2.13000011444091797, 'E', 2.04999995231628418, 'E', 1.90999996662139893, 'E', 1.80999994277954102, 'E', 1.72000002861022949, 'E', 1.62999999523162842, 'E', 1.61000001430511475, 'E', 1.54999995231628418, 'E', 1.50999999046325684, 'E', 1.52999997138977051, 'E', 1.60000002384185791, 'E', 1.59000003337860107, 'E', NULL, NULL, NULL, NULL),
     ('08MG026', 2016, 3, 1, 31, 1.96000003814697288, 60.8800010681152344, 1, 1.59000003337860107, 31, 2.46000003814697266, 1.59000003337860107, 'E', 1.59000003337860107, 'E', 1.69000005722045898, 'E', 1.78999996185302712, 'E', 2.13000011444091797, 'E', 2.32999992370605469, 'E', 2.20000004768371582, 'E', 2.02999997138977051, 'E', 1.94000005722045898, 'E', 2.33999991416931152, 'E', 2.21000003814697266, 'E', 2.17000007629394531, 'E', 2.02999997138977051, 'E', 1.90999996662139893, 'E', 1.86000001430511475, 'E', 1.76999998092651367, 'E', 1.70000004768371582, 'E', 1.63999998569488525, 'E', 1.64999997615814209, 'E', 1.72000002861022949, 'E', 2.06999993324279785, 'E', 2.08999991416931152, 'E', 2.02999997138977051, 'E', 2.02999997138977051, 'E', 1.98000001907348633, 'E', 1.97000002861022927, 'E', 1.99000000953674316, 'E', 1.97000002861022927, 'E', 1.95000004768371604, 'E', 2.04999995231628418, 'E', 2.46000003814697266, 'E'),
     ('08MG026', 2016, 4, 1, 30, 4.38000011444091797, 131.5, 1, 2.95000004768371582, 22, 7.17000007629394531, 2.95000004768371582, 'E', 3.30999994277954102, 'E', 3.34999990463256836, 'E', 3.80999994277954102, 'E', 3.40000009536743208, 'E', 3.26999998092651367, 'E', 3.42000007629394531, 'E', 4.03000020980834961, 'E', 4.65999984741210938, 'E', 4.65999984741210938, 'E', 4.67000007629394531, 'E', 4.3899998664855957, 'E', 3.84999990463256792, 'E', 3.44000005722045898, 'E', 3.27999997138977051, 'E', 3.20000004768371582, 'E', 3.29999995231628418, 'E', 3.8900001049041748, 'E', 4.96999979019165039, 'E', 6.34999990463256836, 'E', 6.82000017166137695, 'E', 7.17000007629394531, 'E', 6.98999977111816406, 'E', 5.98999977111816406, 'E', 4.73999977111816406, 'E', 4.65999984741210938, 'E', 4.32000017166137695, 'E', 4.15000009536743164, 'E', 4.21999979019165039, 'E', 4.23999977111816406, 'E', NULL, NULL),
     ('08MG026', 2016, 5, 1, 31, 6.6100001335144043, 204.990005493164091, 1, 4.48999977111816406, 17, 10.5, 4.48999977111816406, 'E', 4.98999977111816406, 'E', 6.40000009536743164, 'E', 7.44999980926513672, 'E', 6.26999998092651367, 'E', 5.90000009536743164, 'E', 6.40999984741210938, 'E', 7.15999984741210938, 'E', 6.76000022888183594, 'E', 5.75, 'E', 5.84999990463256836, 'E', 5.78000020980834961, 'E', 5.90999984741210938, 'E', 6.8899998664855957, 'E', 7.6399998664855957, 'E', 8.34000015258789062, 'E', 10.5, 'E', 9.42000007629394354, 'E', 8.42000007629394531, 'E', 7.21000003814697266, 'E', 6.40999984741210938, 'E', 6.25, 'E', 6.17999982833862305, 'E', 6.19000005722045898, 'E', 6.44999980926513672, 'E', 6.86999988555908203, 'E', 5.90000009536743164, 'E', 5.8899998664855957, 'E', 5.90000009536743164, 'E', 5.76999998092651367, 'E', 5.6399998664855957, 'E'),
     ('08MG026', 2016, 6, 1, 30, 7.73999977111816406, 232.270004272460909, 17, 5.01000022888183594, 7, 15.6000003814697283, 5.84000015258789062, 'E', 7.94000005722045898, 'E', 7, 'E', 8, 'E', 9.35999965667724609, 'E', 13.5, 'E', 15.6000003814697283, 'E', 12.8000001907348633, 'E', 9.17000007629394354, 'E', 7.48999977111816406, 'E', 6.44999980926513672, 'E', 6.03999996185302734, 'E', 6.15000009536743164, 'E', 5.82000017166137695, 'E', 5.38000011444091797, 'E', 5.13000011444091797, 'E', 5.01000022888183594, 'E', 5.09000015258789062, 'E', 5.19000005722045898, 'E', 5.3600001335144043, 'E', 5.44999980926513672, 'E', 5.6399998664855957, 'E', 7.34000015258789062, 'E', 8.02999973297119141, 'E', 7.84999990463256836, 'E', 7.80000019073486328, 'E', 8.10999965667724609, 'E', 9.22999954223632812, 'E', 10.1999998092651367, 'E', 10.3000001907348633, 'E', NULL, NULL),
     ('08MG026', 2016, 7, 1, 31, 6.59000015258789062, 204.339996337890653, 15, 5.53999996185302734, 1, 8.81999969482421875, 8.81999969482421875, 'E', 7.76000022888183594, 'E', 7.76999998092651367, 'E', 7.63000011444091797, 'E', 7.09000015258789062, 'E', 6.76000022888183594, 'E', 6.46000003814697266, 'E', 7.48000001907348633, 'E', 7.36999988555908203, 'E', 6.96000003814697266, 'E', 6.21000003814697266, 'E', 5.98999977111816406, 'E', 5.69000005722045898, 'E', 6.07000017166137695, 'E', 5.53999996185302734, 'E', 6.1399998664855957, 'E', 6.96999979019165039, 'E', 6.90000009536743164, 'E', 6.80999994277954102, 'E', 6.30000019073486328, 'E', 5.55999994277954102, NULL, 5.73000001907348633, NULL, 5.78000020980834961, NULL, 5.69999980926513672, NULL, 6.28999996185302734, NULL, 6.57999992370605469, NULL, 6.3899998664855957, NULL, 6.46999979019165039, NULL, 6.73000001907348633, NULL, 6.19999980926513672, NULL, 6.19000005722045898, NULL),
     ('08MG026', 2016, 8, 1, 31, 4.1100001335144043, 127.489997863769517, 23, 3.01999998092651367, 14, 5.53999996185302734, 5.15999984741210938, NULL, 4.40000009536743164, NULL, 3.86999988555908203, NULL, 4.21000003814697266, NULL, 3.97000002861022949, NULL, 3.52999997138977051, NULL, 3.72000002861022949, NULL, 3.93000006675720215, NULL, 3.6099998950958252, NULL, 4.07999992370605469, NULL, 4.28999996185302734, NULL, 5.03000020980834961, NULL, 5.38000011444091797, NULL, 5.53999996185302734, NULL, 5.17000007629394531, NULL, 5.32000017166137695, NULL, 5.1100001335144043, NULL, 4.59000015258789062, NULL, 4.15000009536743164, NULL, 4.36999988555908203, NULL, 4.26000022888183594, NULL, 3.26999998092651367, NULL, 3.01999998092651367, NULL, 3.1099998950958252, NULL, 3.44000005722045898, NULL, 3.51999998092651367, NULL, 3.99000000953674316, NULL, 3.20000004768371582, NULL, 3.36999988555908203, NULL, 3.43000006675720215, NULL, 3.45000004768371582, NULL),
     ('08MG026', 2016, 9, 1, 30, 2.15000009536743208, 64.6200027465820312, 30, 1.34000003337860107, 1, 3.71000003814697266, 3.71000003814697266, NULL, 3.05999994277954102, NULL, 2.68000006675720215, NULL, 2.43000006675720215, NULL, 2.32999992370605469, NULL, 2.34999990463256836, NULL, 2.33999991416931152, NULL, 2.26999998092651367, NULL, 2.05999994277954102, NULL, 2.55999994277954102, NULL, 2.19000005722045898, NULL, 1.88999998569488525, NULL, 1.86000001430511475, NULL, 2.03999996185302779, NULL, 2.13000011444091797, NULL, 2.3599998950958252, NULL, 3.11999988555908203, NULL, 2.50999999046325684, NULL, 2.19000005722045898, NULL, 1.85000002384185791, NULL, 1.66999995708465576, NULL, 1.55999994277954102, NULL, 1.62000000476837158, NULL, 1.50999999046325684, NULL, 1.6799999475479126, NULL, 2.03999996185302779, NULL, 2.13000011444091797, NULL, 1.6799999475479126, NULL, 1.46000003814697288, NULL, 1.34000003337860107, NULL, NULL, NULL),
     ('08MG026', 2016, 10, 1, 31, 2.13000011444091797, 66.05999755859375, 5, 1.10000002384185791, 16, 4.55999994277954102, 1.25999999046325684, NULL, 1.1799999475479126, NULL, 1.14999997615814209, NULL, 1.13999998569488525, NULL, 1.10000002384185791, NULL, 1.25999999046325684, NULL, 1.87000000476837203, NULL, 1.75, NULL, 1.62999999523162842, NULL, 1.37000000476837158, NULL, 1.23000001907348633, NULL, 1.19000005722045898, NULL, 1.90999996662139893, NULL, 3.54999995231628418, NULL, 3.47000002861022905, NULL, 4.55999994277954102, NULL, 3.01999998092651367, NULL, 2.6099998950958252, NULL, 2.34999990463256836, NULL, 2.49000000953674316, NULL, 2.3599998950958252, NULL, 2.06999993324279785, NULL, 1.91999995708465598, NULL, 2.11999988555908203, NULL, 2.5, NULL, 2.30999994277954102, 'A', 3.26999998092651367, NULL, 2.68000006675720215, NULL, 2.3900001049041748, 'A', 2.19000005722045898, NULL, 2.16000008583068848, NULL),
     ('08MG026', 2016, 11, 1, 30, 4.94000005722045898, 148.330001831054688, 1, 2.03999996185302779, 9, 20.6000003814697266, 2.03999996185302779, NULL, 3.07999992370605469, NULL, 4.46000003814697266, NULL, 3.17000007629394531, NULL, 17.7999992370605469, NULL, 5.71000003814697266, NULL, 4.80999994277954102, NULL, 7.26999998092651367, NULL, 20.6000003814697266, NULL, 6.23999977111816406, NULL, 5.30999994277954102, 'A', 9.76000022888183594, NULL, 5.53999996185302734, NULL, 5.1399998664855957, NULL, 4.28000020980834961, NULL, 3.63000011444091797, NULL, 3.55999994277954102, NULL, 3.31999993324279785, NULL, 3.13000011444091797, 'A', 3.06999993324279785, NULL, 2.94000005722045898, NULL, 2.8599998950958252, NULL, 2.80999994277954102, NULL, 2.75999999046325684, NULL, 2.72000002861022905, NULL, 2.70000004768371582, NULL, 2.59999990463256836, NULL, 2.44000005722045898, NULL, 2.31999993324279785, NULL, 2.25999999046325684, 'A', NULL, NULL),
     ('08MG026', 2016, 12, 1, 31, 1.44000005722045898, 44.7900009155273438, 21, 1.19000005722045898, 1, 2.20000004768371582, 2.20000004768371582, NULL, 2.1400001049041748, NULL, 2.07999992370605469, NULL, 1.85000002384185791, NULL, 1.75, NULL, 1.47000002861022949, NULL, 1.35000002384185791, NULL, 1.44000005722045898, NULL, 1.69000005722045898, NULL, 1.75, NULL, 1.62000000476837158, NULL, 1.37999999523162842, NULL, 1.29999995231628418, NULL, 1.33000004291534424, NULL, 1.35000002384185791, NULL, 1.35000002384185791, NULL, 1.38999998569488525, NULL, 1.37999999523162842, NULL, 1.25, NULL, 1.23000001907348633, NULL, 1.19000005722045898, NULL, 1.19000005722045898, NULL, 1.22000002861022949, NULL, 1.21000003814697288, NULL, 1.22000002861022949, NULL, 1.25, NULL, 1.25999999046325684, NULL, 1.24000000953674316, NULL, 1.25999999046325684, NULL, 1.23000001907348633, NULL, 1.22000002861022949, NULL)
     ON CONFLICT (station_number, year, month) DO NOTHING;
    """)
        op.execute("""INSERT INTO dly_levels
        (station_number, year, month, precision_code, full_month, no_days, monthly_mean, monthly_total, first_day_min, min, first_day_max, max, level1, level_symbol1, level2, level_symbol2, level3, level_symbol3, level4, level_symbol4, level5, level_symbol5, level6, level_symbol6, level7, level_symbol7, level8, level_symbol8, level9, level_symbol9, level10, level_symbol10, level11, level_symbol11, level12, level_symbol12, level13, level_symbol13, level14, level_symbol14, level15, level_symbol15, level16, level_symbol16, level17, level_symbol17, level18, level_symbol18, level19, level_symbol19, level20, level_symbol20, level21, level_symbol21, level22, level_symbol22, level23, level_symbol23, level24, level_symbol24, level25, level_symbol25, level26, level_symbol26, level27, level_symbol27, level28, level_symbol28, level29, level_symbol29, level30, level_symbol30, level31, level_symbol31)
    VALUES
    ('08MG026', 2011, 1, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 5.75299978256225586, NULL, 5.74800014495849609, NULL, 5.74800014495849609, NULL, 5.76399993896484375, NULL, 5.77299976348876953, NULL, 5.77099990844726562, NULL, 5.78200006484985352, NULL, 5.76800012588500977, NULL, 5.75500011444091797, NULL, 5.74599981307983398, NULL, 5.76000022888183594, NULL, 5.82800006866455078, NULL, 5.76000022888183594, NULL, 5.7909998893737793, NULL, 5.80200004577636719, NULL, 5.84000015258789062, NULL, 5.85200023651123136, NULL, 5.82800006866455078, NULL, 5.81500005722045898, NULL, 5.80700016021728516, NULL, 5.80100011825561523, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2011, 2, 8, 0, 28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 5.75, 'A', NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2011, 3, 8, 1, 31, 5.73999977111816406, 177.955000000000013, 26, 5.73099994659423828, 31, 5.77600002288818359, 5.74599981307983398, NULL, 5.74900007247924805, NULL, 5.74499988555908203, NULL, 5.74200010299682617, NULL, 5.74100017547607422, NULL, 5.73899984359741211, NULL, 5.73799991607666016, NULL, 5.7369999885559082, NULL, 5.73899984359741211, NULL, 5.74300003051757812, NULL, 5.73600006103515625, NULL, 5.73799991607666016, NULL, 5.73899984359741211, NULL, 5.75, NULL, 5.75099992752075195, NULL, 5.74900007247924805, NULL, 5.74100017547607422, NULL, 5.73899984359741211, NULL, 5.73799991607666016, NULL, 5.7350001335144043, NULL, 5.7369999885559082, NULL, 5.73400020599365234, NULL, 5.73299980163574219, NULL, 5.73299980163574219, NULL, 5.73199987411499023, NULL, 5.73099994659423828, NULL, 5.73099994659423828, NULL, 5.73099994659423828, NULL, 5.73400020599365234, NULL, 5.74800014495849609, NULL, 5.77600002288818359, NULL),
    ('08MG026', 2011, 4, 8, 1, 30, 5.74200010299682617, 172.260999999999996, 20, 5.72800016403198242, 1, 5.76900005340576172, 5.76900005340576172, NULL, 5.7630000114440918, NULL, 5.75600004196166992, NULL, 5.75400018692016602, NULL, 5.75099992752075195, NULL, 5.74700021743774414, NULL, 5.73999977111816406, NULL, 5.73899984359741211, NULL, 5.73799991607666016, NULL, 5.74499988555908203, NULL, 5.74900007247924805, NULL, 5.74100017547607422, NULL, 5.74300003051757812, NULL, 5.73999977111816406, NULL, 5.73600006103515625, NULL, 5.7350001335144043, NULL, 5.73299980163574219, NULL, 5.73400020599365234, NULL, 5.72900009155273438, NULL, 5.72800016403198242, NULL, 5.72900009155273438, NULL, 5.73000001907348633, NULL, 5.7350001335144043, NULL, 5.73400020599365234, NULL, 5.73799991607666016, NULL, 5.74300003051757812, NULL, 5.74599981307983398, NULL, 5.74100017547607422, NULL, 5.74499988555908203, NULL, 5.75, NULL, NULL, NULL),
    ('08MG026', 2011, 5, 8, 1, 31, 5.85799980163574219, 181.599999999999994, 1, 5.75500011444091797, 31, 5.94700002670288086, 5.75500011444091797, NULL, 5.76599979400634766, NULL, 5.76800012588500977, NULL, 5.77099990844726562, NULL, 5.78299999237060547, NULL, 5.79400014877319336, NULL, 5.79699993133544922, NULL, 5.80100011825561523, NULL, 5.80900001525878906, NULL, 5.82200002670288086, NULL, 5.84899997711181641, NULL, 5.84100008010864258, NULL, 5.83099985122680664, NULL, 5.8470001220703125, NULL, 5.90299987792968839, NULL, 5.92100000381469727, NULL, 5.88700008392333984, NULL, 5.8600001335144043, NULL, 5.85799980163574219, NULL, 5.88399982452392578, NULL, 5.91099977493286133, NULL, 5.90700006484985352, NULL, 5.90799999237060547, NULL, 5.90999984741210938, NULL, 5.90799999237060547, NULL, 5.92199993133544922, NULL, 5.90399980545044034, NULL, 5.89499998092651367, NULL, 5.90600013732910156, NULL, 5.93499994277954102, NULL, 5.94700002670288086, NULL),
    ('08MG026', 2011, 6, 8, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 5.96400022506713867, NULL, 5.98000001907348633, NULL, 5.96500015258789062, NULL, 5.97800016403198242, NULL, 5.99300003051757812, NULL, 6.01900005340576172, NULL, 6.05800008773803711, NULL, 6.03999996185302734, NULL, 6.03999996185302734, NULL, 6.03399991989135742, NULL, 6.02799987792968839, NULL, 6.02299976348876953, NULL, 6.00500011444091797, NULL, 6.00699996948242188, NULL, 6.00199985504150391, NULL, 6.00199985504150391, NULL, 6.00799989700317383, NULL, 6.02500009536743164, NULL, 6.02199983596801758, NULL, 6.01900005340576172, NULL, 6.03100013732910156, NULL, 6.04600000381469727, NULL, 6.04699993133544922, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2011, 7, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 6.10699987411499023, 'A', 6.07700014114379883, NULL, 6.05999994277954102, NULL, 6.07399988174438477, NULL, 6.09999990463256836, NULL, 6.10400009155273438, NULL, 6.08699989318847656, NULL, 6.07999992370605469, NULL, 6.09100008010864258, NULL, 6.09100008010864258, NULL, 6.1399998664855957, NULL),
    ('08MG026', 2011, 8, 8, 1, 31, 6.0409998893737793, 187.266999999999996, 18, 5.99300003051757812, 22, 6.10200023651123136, 6.09499979019165039, NULL, 6.07600021362304688, NULL, 6.0689997673034668, NULL, 6.07700014114379883, NULL, 6.09000015258789062, NULL, 6.09399986267089844, NULL, 6.08199977874755859, NULL, 6.07499980926513672, NULL, 6.05700016021728516, NULL, 6.04699993133544922, NULL, 6.05900001525878906, NULL, 6.05200004577636719, NULL, 6.03100013732910156, NULL, 6.02099990844726562, NULL, 6.01200008392333984, NULL, 6, NULL, 5.99599981307983398, NULL, 5.99300003051757812, NULL, 5.99499988555908203, NULL, 6.00500011444091797, NULL, 6.02699995040893644, NULL, 6.10200023651123136, NULL, 6.08799982070922852, NULL, 6.04400014877319336, NULL, 6.02600002288818359, NULL, 6.01900005340576172, NULL, 6.00899982452392578, NULL, 6.01100015640258789, NULL, 6.0130000114440918, NULL, 6.00699996948242188, NULL, 5.99499988555908203, NULL),
    ('08MG026', 2011, 9, 8, 1, 30, 5.97700023651123136, 179.306000000000012, 20, 5.90199995040893644, 23, 6.1100001335144043, 5.97499990463256836, NULL, 5.96000003814697266, NULL, 5.95300006866455078, NULL, 5.95499992370605469, NULL, 5.95699977874755859, NULL, 5.95800018310546875, NULL, 5.95800018310546875, NULL, 5.96400022506713867, NULL, 5.96799993515014648, NULL, 5.97399997711181641, NULL, 5.97599983215332031, NULL, 5.96799993515014648, NULL, 5.96500015258789062, NULL, 5.95300006866455078, NULL, 5.9590001106262207, NULL, 5.95300006866455078, NULL, 5.93400001525878906, NULL, 5.92899990081787109, NULL, 5.91400003433227539, NULL, 5.90199995040893644, NULL, 5.94199991226196289, NULL, 6.08799982070922852, NULL, 6.1100001335144043, NULL, 6.06400012969970703, NULL, 6.06199979782104492, NULL, 6.0130000114440918, 'A', 6.01900005340576172, 'A', 5.99499988555908203, NULL, 5.97100019454956055, NULL, 5.96700000762939453, NULL, NULL, NULL),
    ('08MG026', 2011, 10, 8, 1, 31, 5.90799999237060547, 183.156000000000006, 27, 5.8619999885559082, 3, 5.98099994659423828, 5.94999980926513672, NULL, 5.93599987030029297, NULL, 5.98099994659423828, NULL, 5.98000001907348633, NULL, 5.95699977874755859, NULL, 5.94000005722045898, NULL, 5.93699979782104492, NULL, 5.92299985885620117, NULL, 5.92100000381469727, NULL, 5.92100000381469727, NULL, 5.95200014114379883, NULL, 5.93300008773803711, NULL, 5.9159998893737793, NULL, 5.90700006484985352, NULL, 5.89599990844726562, NULL, 5.88700008392333984, NULL, 5.88299989700317383, NULL, 5.88199996948242188, 'A', 5.88700008392333984, NULL, 5.90700006484985352, NULL, 5.90600013732910156, NULL, 5.90199995040893644, NULL, 5.89200019836425781, NULL, 5.88000011444091797, NULL, 5.87099981307983398, NULL, 5.86700010299682617, NULL, 5.8619999885559082, NULL, 5.87400007247924805, NULL, 5.86600017547607422, NULL, 5.87400007247924805, NULL, 5.86600017547607422, NULL),
    ('08MG026', 2011, 11, 8, 1, 30, 5.84499979019165039, 175.356999999999999, 19, 5.81300020217895508, 27, 5.875, 5.85699987411499023, NULL, 5.85900020599365234, NULL, 5.85900020599365234, NULL, 5.85200023651123136, NULL, 5.84999990463256836, NULL, 5.84200000762939453, NULL, 5.84399986267089844, NULL, 5.83900022506713867, NULL, 5.83799982070922852, NULL, 5.86800003051757812, NULL, 5.86800003051757812, NULL, 5.84999990463256836, NULL, 5.84100008010864258, NULL, 5.8340001106262207, NULL, 5.82700014114379883, NULL, 5.83799982070922852, NULL, 5.84600019454956055, NULL, 5.83799982070922852, NULL, 5.81300020217895508, NULL, 5.82100009918212891, NULL, 5.83099985122680664, NULL, 5.84600019454956055, NULL, 5.84000015258789062, NULL, 5.83900022506713867, NULL, 5.83199977874755859, NULL, 5.84000015258789062, NULL, 5.875, NULL, 5.86299991607666016, NULL, 5.8619999885559082, NULL, 5.84499979019165039, NULL, NULL, NULL),
    ('08MG026', 2011, 12, 8, 1, 31, 5.78399991989135742, 179.313999999999993, 21, 5.75799989700317383, 1, 5.83099985122680664, 5.83099985122680664, NULL, 5.8189997673034668, NULL, 5.81099987030029297, NULL, 5.80900001525878906, NULL, 5.8060002326965332, NULL, 5.80399990081787109, NULL, 5.80100011825561523, NULL, 5.78800010681152344, NULL, 5.79500007629394531, NULL, 5.79500007629394531, NULL, 5.78499984741210938, NULL, 5.76900005340576172, NULL, 5.78200006484985352, NULL, 5.77600002288818359, NULL, 5.77299976348876953, NULL, 5.77199983596801758, NULL, 5.77699995040893644, NULL, 5.77500009536743164, NULL, 5.76800012588500977, NULL, 5.77099990844726562, NULL, 5.75799989700317383, NULL, 5.76100015640258789, NULL, 5.77400016784667969, NULL, 5.77199983596801758, NULL, 5.76599979400634766, NULL, 5.7630000114440918, NULL, 5.76599979400634766, NULL, 5.79199981689453125, NULL, 5.79500007629394531, NULL, 5.78700017929077237, NULL, 5.77299976348876953, NULL),
    ('08MG026', 2012, 1, 8, 1, 31, 5.78599977493286133, 179.366000000000014, 27, 5.74700021743774414, 4, 5.86800003051757812, 5.77400016784667969, NULL, 5.77899980545044034, NULL, 5.78700017929077237, NULL, 5.86800003051757812, NULL, 5.86700010299682617, NULL, 5.83900022506713867, NULL, 5.82499980926513672, NULL, 5.81599998474121094, NULL, 5.83099985122680664, NULL, 5.8060002326965332, NULL, 5.79600000381469727, NULL, 5.80399990081787109, NULL, 5.79500007629394531, NULL, 5.79300022125244141, NULL, 5.77600002288818359, NULL, 5.76900005340576172, NULL, 5.76200008392333984, NULL, 5.75400018692016602, NULL, 5.76999998092651367, NULL, 5.78200006484985352, NULL, 5.78800010681152344, NULL, 5.76700019836425781, NULL, 5.7630000114440918, NULL, 5.76000022888183594, NULL, 5.75699996948242188, NULL, 5.75199985504150391, NULL, 5.74700021743774414, NULL, 5.74700021743774414, NULL, 5.77299976348876953, NULL, 5.75899982452392578, NULL, 5.76000022888183594, NULL),
    ('08MG026', 2012, 2, 8, 1, 29, 5.74499988555908203, 166.592999999999989, 27, 5.72599983215332031, 1, 5.75899982452392578, 5.75899982452392578, NULL, 5.75400018692016602, NULL, 5.75299978256225586, NULL, 5.75400018692016602, NULL, 5.74900007247924805, NULL, 5.75, NULL, 5.75299978256225586, NULL, 5.74900007247924805, NULL, 5.74700021743774414, NULL, 5.74900007247924805, NULL, 5.75099992752075195, NULL, 5.75099992752075195, NULL, 5.74700021743774414, NULL, 5.74399995803833008, NULL, 5.73999977111816406, NULL, 5.74200010299682617, NULL, 5.74100017547607422, NULL, 5.74300003051757812, NULL, 5.74200010299682617, NULL, 5.73799991607666016, NULL, 5.73799991607666016, NULL, 5.74300003051757812, NULL, 5.73799991607666016, NULL, 5.74300003051757812, NULL, 5.74200010299682617, NULL, 5.73400020599365234, NULL, 5.72599983215332031, NULL, 5.7369999885559082, NULL, 5.73600006103515625, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2012, 3, 8, 1, 31, 5.72900009155273438, 177.603000000000009, 19, 5.71600008010864258, 5, 5.74700021743774414, 5.73099994659423828, NULL, 5.72900009155273438, NULL, 5.73199987411499023, NULL, 5.74499988555908203, NULL, 5.74700021743774414, NULL, 5.73099994659423828, NULL, 5.73299980163574219, NULL, 5.73400020599365234, NULL, 5.74200010299682617, NULL, 5.73899984359741211, NULL, 5.7369999885559082, NULL, 5.74200010299682617, NULL, 5.73000001907348633, NULL, 5.71899986267089844, NULL, 5.72900009155273438, NULL, 5.72700023651123136, NULL, 5.72300004959106445, NULL, 5.71999979019165039, NULL, 5.71600008010864258, NULL, 5.71700000762939453, NULL, 5.71700000762939453, NULL, 5.71700000762939453, NULL, 5.71700000762939453, NULL, 5.71700000762939453, NULL, 5.71999979019165039, NULL, 5.71999979019165039, NULL, 5.72100019454956055, NULL, 5.73899984359741211, NULL, 5.74100017547607422, NULL, 5.7369999885559082, NULL, 5.73400020599365234, NULL),
    ('08MG026', 2012, 4, 8, 1, 30, 5.80999994277954102, 174.306999999999988, 2, 5.73000001907348633, 26, 5.99599981307983398, 5.73400020599365234, NULL, 5.73000001907348633, NULL, 5.75299978256225586, NULL, 5.74700021743774414, NULL, 5.74300003051757812, NULL, 5.74100017547607422, NULL, 5.74100017547607422, NULL, 5.74100017547607422, NULL, 5.74599981307983398, NULL, 5.75600004196166992, NULL, 5.76599979400634766, NULL, 5.78399991989135742, NULL, 5.78900003433227539, NULL, 5.79799985885620117, NULL, 5.80100011825561523, NULL, 5.80100011825561523, NULL, 5.79500007629394531, NULL, 5.78999996185302734, NULL, 5.78900003433227539, NULL, 5.79300022125244141, NULL, 5.78999996185302734, NULL, 5.80000019073486328, NULL, 5.87099981307983398, NULL, 5.91099977493286133, NULL, 5.94899988174438477, NULL, 5.99599981307983398, NULL, 5.94099998474121094, NULL, 5.90799999237060547, NULL, 5.90000009536743164, NULL, 5.90299987792968839, NULL, NULL, NULL),
    ('08MG026', 2012, 5, 8, 1, 31, 5.92000007629394531, 183.534999999999997, 5, 5.85099983215332031, 16, 5.98899984359741211, 5.89099979400634766, NULL, 5.87300014495849609, NULL, 5.86299991607666016, NULL, 5.85699987411499023, NULL, 5.85099983215332031, NULL, 5.85099983215332031, NULL, 5.86399984359741211, NULL, 5.88899993896484375, NULL, 5.8899998664855957, NULL, 5.86899995803833008, NULL, 5.8600001335144043, NULL, 5.86700010299682617, NULL, 5.90100002288818359, NULL, 5.94299983978271484, NULL, 5.97599983215332031, NULL, 5.98899984359741211, NULL, 5.97100019454956055, NULL, 5.94899988174438477, NULL, 5.93400001525878906, NULL, 5.93200016021728516, NULL, 5.94899988174438477, NULL, 5.96600008010864258, NULL, 5.94299983978271484, NULL, 5.93300008773803711, NULL, 5.93900012969970703, NULL, 5.96000003814697266, NULL, 5.9720001220703125, NULL, 5.97100019454956055, NULL, 5.96500015258789062, NULL, 5.95100021362304688, NULL, 5.96600008010864258, NULL),
    ('08MG026', 2012, 6, 8, 1, 30, 6.02299976348876953, 180.693999999999988, 9, 5.94500017166137695, 23, 6.125, 6.01000022888183594, NULL, 6.01700019836425781, NULL, 5.97900009155273438, NULL, 5.95800018310546875, NULL, 5.96099996566772461, NULL, 5.96199989318847656, NULL, 5.95399999618530273, NULL, 5.94600009918212891, NULL, 5.94500017166137695, NULL, 5.95800018310546875, NULL, 5.97399997711181641, NULL, 6.01100015640258789, NULL, 6.04300022125244141, NULL, 6.02600002288818359, NULL, 5.99700021743774414, NULL, 6.03399991989135742, NULL, 6.08500003814697266, NULL, 6.07899999618530273, NULL, 6.04400014877319336, NULL, 6.03399991989135742, NULL, 6.06300020217895508, NULL, 6.08900022506713867, NULL, 6.125, NULL, 6.08900022506713867, NULL, 6.05499982833862305, NULL, 6.04799985885620117, NULL, 6.03800010681152344, NULL, 6.02799987792968839, NULL, 6.05100011825561523, NULL, 6.09100008010864258, NULL, NULL, NULL),
    ('08MG026', 2012, 7, 8, 1, 31, 6.08599996566772461, 188.669999999999987, 31, 6.01700019836425781, 17, 6.15100002288818359, 6.09100008010864258, NULL, 6.06400012969970703, NULL, 6.05299997329711914, NULL, 6.03999996185302734, NULL, 6.03700017929077237, NULL, 6.04600000381469727, NULL, 6.05800008773803711, NULL, 6.07700014114379883, NULL, 6.10400009155273438, NULL, 6.13600015640258789, NULL, 6.12900018692016602, NULL, 6.11899995803833008, NULL, 6.12599992752075195, NULL, 6.14499998092651367, NULL, 6.13899993896484375, NULL, 6.14200019836425781, NULL, 6.15100002288818359, NULL, 6.14900016784667969, NULL, 6.11899995803833008, NULL, 6.10400009155273438, NULL, 6.08099985122680664, NULL, 6.07100009918212891, NULL, 6.06599998474121094, NULL, 6.04899978637695312, NULL, 6.07399988174438477, NULL, 6.07899999618530273, NULL, 6.07399988174438477, NULL, 6.05900001525878906, NULL, 6.04400014877319336, NULL, 6.02699995040893644, NULL, 6.01700019836425781, NULL),
    ('08MG026', 2012, 8, 8, 1, 31, 5.99100017547607422, 185.731999999999999, 31, 5.88399982452392578, 6, 6.07999992370605469, 6.01100015640258789, NULL, 6.0130000114440918, NULL, 6.01999998092651367, NULL, 6.04699993133544922, NULL, 6.07299995422363281, NULL, 6.07999992370605469, NULL, 6.07200002670288086, NULL, 6.07200002670288086, NULL, 6.03399991989135742, NULL, 6.00799989700317383, NULL, 6.00699996948242188, NULL, 6.01000022888183594, NULL, 6.00199985504150391, NULL, 6.01900005340576172, NULL, 6.01700019836425781, NULL, 6.00600004196166992, NULL, 6.00899982452392578, NULL, 6.01100015640258789, NULL, 6.01999998092651367, NULL, 6, NULL, 5.97700023651123136, NULL, 5.96299982070922852, NULL, 5.94799995422363281, NULL, 5.92999982833862305, NULL, 5.92399978637695312, NULL, 5.93300008773803711, NULL, 5.93400001525878906, NULL, 5.91300010681152344, NULL, 5.89900016784667969, NULL, 5.89599990844726562, NULL, 5.88399982452392578, NULL),
    ('08MG026', 2012, 9, 8, 1, 30, 5.87799978256225586, 176.325999999999993, 30, 5.84999990463256836, 8, 5.90999984741210938, 5.875, NULL, 5.86899995803833008, NULL, 5.86999988555908203, NULL, 5.87900018692016602, NULL, 5.8880000114440918, NULL, 5.88399982452392578, NULL, 5.89599990844726562, NULL, 5.90999984741210938, NULL, 5.90700006484985352, NULL, 5.90000009536743164, NULL, 5.86700010299682617, NULL, 5.85599994659423828, NULL, 5.86299991607666016, NULL, 5.8600001335144043, NULL, 5.8600001335144043, NULL, 5.86299991607666016, NULL, 5.8619999885559082, NULL, 5.86299991607666016, NULL, 5.86899995803833008, NULL, 5.8880000114440918, NULL, 5.89799976348876953, NULL, 5.89799976348876953, NULL, 5.90500020980834961, NULL, 5.90100002288818359, NULL, 5.88000011444091797, NULL, 5.86600017547607422, NULL, 5.85599994659423828, NULL, 5.87300014495849609, NULL, 5.86999988555908203, NULL, 5.84999990463256836, NULL, NULL, NULL),
    ('08MG026', 2012, 10, 8, 1, 31, 5.86299991607666016, 181.762, 11, 5.80200004577636719, 19, 6.02799987792968839, 5.89499998092651367, NULL, 5.88199996948242188, NULL, 5.84299993515014648, NULL, 5.82999992370605469, NULL, 5.81799983978271484, NULL, 5.81199979782104492, NULL, 5.81500005722045898, NULL, 5.81400012969970703, NULL, 5.81099987030029297, NULL, 5.8060002326965332, NULL, 5.80200004577636719, NULL, 5.80700016021728516, NULL, 5.83500003814697266, NULL, 6.01800012588500977, NULL, 5.93900012969970703, NULL, 5.92000007629394531, NULL, 5.85900020599365234, NULL, 5.92999982833862305, NULL, 6.02799987792968839, NULL, 5.91300010681152344, NULL, 5.87900018692016602, NULL, 5.85799980163574219, NULL, 5.84299993515014648, NULL, 5.82800006866455078, NULL, 5.81599998474121094, NULL, 5.81400012969970703, NULL, 5.81300020217895508, NULL, 5.81599998474121094, NULL, 5.85400009155273438, NULL, 5.88899993896484375, NULL, 5.97499990463256836, NULL),
    ('08MG026', 2012, 11, 8, 1, 30, 5.85599994659423828, 175.673000000000002, 28, 5.80100011825561523, 5, 5.9869999885559082, 5.96500015258789062, NULL, 5.91099977493286133, NULL, 5.94299983978271484, NULL, 5.97800016403198242, NULL, 5.9869999885559082, NULL, 5.93400001525878906, NULL, 5.90700006484985352, NULL, 5.87699985504150391, NULL, 5.85099983215332031, NULL, 5.82999992370605469, NULL, 5.84200000762939453, NULL, 5.84600019454956055, NULL, 5.83900022506713867, NULL, 5.82899999618530273, NULL, 5.82100009918212891, NULL, 5.81099987030029297, NULL, 5.85099983215332031, NULL, 5.83699989318847656, NULL, 5.8340001106262207, NULL, 5.83199977874755859, NULL, 5.82600021362304688, NULL, 5.81799983978271484, NULL, 5.82200002670288086, NULL, 5.81599998474121094, NULL, 5.80299997329711914, NULL, 5.80200004577636719, NULL, 5.80299997329711914, NULL, 5.80100011825561523, NULL, 5.82299995422363281, NULL, 5.8340001106262207, NULL, NULL, NULL),
    ('08MG026', 2012, 12, 8, 1, 31, 5.77799987792968839, 179.125, 30, 5.74399995803833008, 1, 5.84299993515014648, 5.84299993515014648, NULL, 5.83699989318847656, NULL, 5.8340001106262207, NULL, 5.8340001106262207, NULL, 5.82100009918212891, NULL, 5.81199979782104492, NULL, 5.80499982833862305, NULL, 5.79400014877319336, NULL, 5.79199981689453125, NULL, 5.78499984741210938, NULL, 5.78000020980834961, NULL, 5.76700019836425781, NULL, 5.76599979400634766, NULL, 5.75899982452392578, NULL, 5.76100015640258789, NULL, 5.7630000114440918, NULL, 5.7649998664855957, NULL, 5.75600004196166992, NULL, 5.76000022888183594, NULL, 5.77099990844726562, NULL, 5.76399993896484375, NULL, 5.76200008392333984, NULL, 5.76200008392333984, NULL, 5.75799989700317383, NULL, 5.75899982452392578, NULL, 5.75600004196166992, NULL, 5.75400018692016602, NULL, 5.75500011444091797, NULL, 5.75400018692016602, NULL, 5.74399995803833008, NULL, 5.75199985504150391, NULL),
    ('08MG026', 2013, 1, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 5.74700021743774414, NULL, 5.74800014495849609, NULL, 5.74900007247924805, NULL, 5.75, NULL, 5.75099992752075195, NULL, 5.75, NULL, 5.74900007247924805, NULL, 5.74800014495849609, NULL, 5.75, NULL, 5.73199987411499023, NULL, 5.70800018310546875, NULL, 5.69199991226196289, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 5.72599983215332031, 'A', 5.71899986267089844, NULL, 5.71500015258789062, NULL, 5.71199989318847656, NULL, 5.71199989318847656, NULL, 5.71099996566772461, NULL, 5.7220001220703125, NULL, 5.72700023651123136, NULL, 5.72800016403198242, NULL, 5.72599983215332031, NULL, 5.72599983215332031, NULL, 5.72499990463256836, NULL, 5.7220001220703125, NULL, 5.7220001220703125, NULL, 5.72399997711181641, NULL),
    ('08MG026', 2013, 2, 8, 1, 28, 5.71500015258789062, 160.016999999999996, 20, 5.70300006866455078, 5, 5.72599983215332031, 5.72300004959106445, NULL, 5.72100019454956055, NULL, 5.7220001220703125, NULL, 5.72399997711181641, NULL, 5.72599983215332031, NULL, 5.72399997711181641, NULL, 5.72399997711181641, NULL, 5.71799993515014648, NULL, 5.71199989318847656, NULL, 5.70499992370605469, NULL, 5.7090001106262207, NULL, 5.7090001106262207, NULL, 5.70800018310546875, NULL, 5.70599985122680664, NULL, 5.70699977874755859, NULL, 5.71799993515014648, NULL, 5.71199989318847656, NULL, 5.71400022506713867, NULL, 5.70499992370605469, NULL, 5.70300006866455078, NULL, 5.71899986267089844, NULL, 5.72100019454956055, NULL, 5.71500015258789062, NULL, 5.71500015258789062, NULL, 5.71700000762939453, NULL, 5.71299982070922852, NULL, 5.71299982070922852, NULL, 5.71400022506713867, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2013, 3, 8, 1, 31, 5.77500009536743164, 179.013000000000005, 11, 5.73999977111816406, 14, 5.84299993515014648, 5.78000020980834961, NULL, 5.82200002670288086, NULL, 5.78800010681152344, NULL, 5.77099990844726562, NULL, 5.7649998664855957, NULL, 5.75600004196166992, NULL, 5.75, NULL, 5.74599981307983398, NULL, 5.74100017547607422, NULL, 5.74100017547607422, NULL, 5.73999977111816406, NULL, 5.74800014495849609, NULL, 5.79899978637695312, NULL, 5.84299993515014648, NULL, 5.83099985122680664, NULL, 5.82399988174438477, NULL, 5.80800008773803711, NULL, 5.79400014877319336, NULL, 5.78499984741210938, NULL, 5.78499984741210938, NULL, 5.77199983596801758, NULL, 5.7649998664855957, NULL, 5.76000022888183594, NULL, 5.75699996948242188, NULL, 5.75699996948242188, NULL, 5.75400018692016602, NULL, 5.75500011444091797, NULL, 5.75699996948242188, NULL, 5.76200008392333984, NULL, 5.76999998092651367, NULL, 5.78700017929077237, NULL),
    ('08MG026', 2013, 4, 8, 1, 30, 5.82800006866455078, 174.825999999999993, 22, 5.78999996185302734, 6, 5.88399982452392578, 5.82000017166137695, NULL, 5.83900022506713867, NULL, 5.83799982070922852, NULL, 5.84499979019165039, NULL, 5.87699985504150391, NULL, 5.88399982452392578, NULL, 5.86499977111816406, NULL, 5.84600019454956055, NULL, 5.83599996566772461, NULL, 5.85300016403198242, NULL, 5.8470001220703125, NULL, 5.83699989318847656, NULL, 5.82600021362304688, NULL, 5.81699991226196289, NULL, 5.8060002326965332, NULL, 5.80000019073486328, NULL, 5.79400014877319336, NULL, 5.79400014877319336, NULL, 5.79799985885620117, NULL, 5.80200004577636719, NULL, 5.79699993133544922, NULL, 5.78999996185302734, NULL, 5.79199981689453125, NULL, 5.79799985885620117, NULL, 5.81300020217895508, NULL, 5.84299993515014648, NULL, 5.8619999885559082, NULL, 5.84999990463256836, NULL, 5.83500003814697266, NULL, 5.82200002670288086, NULL, NULL, NULL),
    ('08MG026', 2013, 5, 8, 1, 31, 5.84399986267089844, 181.152999999999992, 26, 5.71199989318847656, 12, 6.11499977111816406, 5.81599998474121094, NULL, 5.81500005722045898, NULL, 5.82899999618530273, NULL, 5.87900018692016602, NULL, 5.95499992370605469, NULL, 6.01900005340576172, NULL, 6.05499982833862305, NULL, 6.0560002326965332, NULL, 6.04500007629394531, NULL, 6.04699993133544922, NULL, 6.04400014877319336, NULL, 6.11499977111816406, NULL, 5.96099996566772461, NULL, 5.85500001907348633, NULL, 5.79600000381469727, NULL, 5.77299976348876953, NULL, 5.76900005340576172, NULL, 5.76999998092651367, NULL, 5.75799989700317383, NULL, 5.75099992752075195, NULL, 5.75400018692016602, NULL, 5.74100017547607422, NULL, 5.75099992752075195, NULL, 5.73199987411499023, NULL, 5.71999979019165039, NULL, 5.71199989318847656, NULL, 5.71199989318847656, NULL, 5.72499990463256836, NULL, 5.73299980163574219, NULL, 5.73999977111816406, NULL, 5.72499990463256836, NULL),
    ('08MG026', 2013, 6, 8, 1, 30, 5.83500003814697266, 175.056000000000012, 1, 5.71999979019165039, 30, 5.96600008010864258, 5.71999979019165039, NULL, 5.72800016403198242, NULL, 5.75299978256225586, NULL, 5.78800010681152344, NULL, 5.82299995422363281, NULL, 5.83900022506713867, NULL, 5.85799980163574219, NULL, 5.85200023651123136, NULL, 5.80999994277954102, NULL, 5.78999996185302734, NULL, 5.78200006484985352, NULL, 5.76599979400634766, NULL, 5.76100015640258789, NULL, 5.76000022888183594, NULL, 5.77099990844726562, NULL, 5.81400012969970703, NULL, 5.84800004959106445, NULL, 5.85200023651123136, NULL, 5.84999990463256836, NULL, 5.88000011444091797, NULL, 5.8600001335144043, NULL, 5.85900020599365234, NULL, 5.86899995803833008, NULL, 5.90399980545044034, NULL, 5.89900016784667969, NULL, 5.89200019836425781, NULL, 5.89900016784667969, NULL, 5.90399980545044034, NULL, 5.9590001106262207, NULL, 5.96600008010864258, NULL, NULL, NULL),
    ('08MG026', 2013, 7, 8, 1, 31, 5.80299997329711914, 179.901999999999987, 30, 5.73000001907348633, 1, 6.00299978256225586, 6.00299978256225586, NULL, 6, NULL, 5.94700002670288086, NULL, 5.89400005340576172, NULL, 5.85500001907348633, NULL, 5.82899999618530273, NULL, 5.81799983978271484, NULL, 5.81099987030029297, NULL, 5.8189997673034668, NULL, 5.82100009918212891, NULL, 5.80000019073486328, NULL, 5.76599979400634766, NULL, 5.74499988555908203, NULL, 5.73899984359741211, NULL, 5.7350001335144043, NULL, 5.75099992752075195, NULL, 5.77400016784667969, NULL, 5.78599977493286133, NULL, 5.79799985885620117, NULL, 5.80000019073486328, NULL, 5.79699993133544922, NULL, 5.79500007629394531, NULL, 5.78700017929077237, NULL, 5.77899980545044034, NULL, 5.77099990844726562, NULL, 5.76999998092651367, NULL, 5.76100015640258789, NULL, 5.74499988555908203, NULL, 5.73400020599365234, NULL, 5.73000001907348633, NULL, 5.74200010299682617, NULL),
    ('08MG026', 2013, 8, 8, 1, 31, 5.74399995803833008, 178.075999999999993, 21, 5.67999982833862305, 30, 5.87699985504150391, 5.76800012588500977, NULL, 5.75799989700317383, NULL, 5.76900005340576172, NULL, 5.77600002288818359, NULL, 5.77400016784667969, NULL, 5.77299976348876953, NULL, 5.76100015640258789, NULL, 5.75099992752075195, NULL, 5.75699996948242188, NULL, 5.76000022888183594, NULL, 5.75099992752075195, NULL, 5.73999977111816406, NULL, 5.72800016403198242, NULL, 5.71000003814697266, NULL, 5.7350001335144043, NULL, 5.74499988555908203, NULL, 5.76900005340576172, NULL, 5.72700023651123136, NULL, 5.70499992370605469, NULL, 5.68599987030029297, NULL, 5.67999982833862305, NULL, 5.69000005722045898, NULL, 5.70399999618530273, NULL, 5.71899986267089844, NULL, 5.69000005722045898, NULL, 5.6810002326965332, NULL, 5.70499992370605469, NULL, 5.76900005340576172, NULL, 5.8600001335144043, NULL, 5.87699985504150391, NULL, 5.75799989700317383, NULL),
    ('08MG026', 2013, 9, 8, 0, 30, NULL, NULL, NULL, NULL, NULL, NULL, 5.75400018692016602, NULL, 5.74800014495849609, NULL, 5.74499988555908203, NULL, 5.72100019454956055, NULL, 5.72599983215332031, NULL, 5.72599983215332031, NULL, 5.73199987411499023, NULL, 5.72599983215332031, NULL, 5.71799993515014648, NULL, 5.71600008010864258, NULL, 5.75099992752075195, NULL, 5.75299978256225586, NULL, 5.7369999885559082, NULL, 5.74399995803833008, NULL, 5.75199985504150391, NULL, 5.77299976348876953, NULL, 5.69600009918212891, NULL, 5.6380000114440918, NULL, 5.61899995803833008, NULL, 5.625, NULL, 5.64900016784667969, NULL, 5.63399982452392578, NULL, 5.64599990844726562, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 5.76000022888183594, 'A', 5.64900016784667969, NULL, 5.65299987792968839, NULL, NULL, NULL),
    ('08MG026', 2013, 10, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 5.63399982452392578, 'A', NULL, NULL, NULL, NULL, NULL, NULL, 5.63899993896484375, 'A', 5.67799997329711914, NULL, 5.66499996185302734, NULL, 5.63100004196166992, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2014, 1, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 5.37300014495849609, 'A', 5.37200021743774414, NULL, 5.37699985504150391, NULL, 5.38399982452392578, NULL, 5.37400007247924805, NULL, 5.37900018692016602, NULL, 5.38500022888183594, NULL, 5.38500022888183594, NULL, 5.37900018692016602, NULL, 5.37200021743774414, NULL, 5.36499977111816406, NULL, 5.36100006103515625, NULL, 5.3600001335144043, NULL, 5.3600001335144043, NULL, 5.35900020599365234, NULL, 5.35900020599365234, NULL, 5.36299991607666016, NULL, 5.36700010299682617, NULL, 5.36800003051757812, NULL, 5.36600017547607422, NULL, 5.36899995803833008, NULL, 5.37400007247924805, NULL, 5.36999988555908203, NULL, 5.35200023651123136, NULL),
    ('08MG026', 2014, 2, 8, 1, 28, 5.37599992752075195, 150.527999999999992, 3, 5.35200023651123136, 14, 5.39699983596801758, 5.35300016403198242, NULL, 5.35699987411499023, NULL, 5.35200023651123136, NULL, 5.35200023651123136, NULL, 5.35799980163574219, NULL, 5.36700010299682617, NULL, 5.36800003051757812, NULL, 5.36999988555908203, NULL, 5.37099981307983398, NULL, 5.37900018692016602, NULL, 5.3899998664855957, NULL, 5.39599990844726562, NULL, 5.39599990844726562, NULL, 5.39699983596801758, NULL, 5.39699983596801758, NULL, 5.38899993896484375, NULL, 5.3880000114440918, NULL, 5.38899993896484375, NULL, 5.38199996948242188, NULL, 5.38399982452392578, NULL, 5.37699985504150391, NULL, 5.37200021743774414, NULL, 5.36800003051757812, NULL, 5.3619999885559082, NULL, 5.36600017547607422, NULL, 5.37300014495849609, NULL, 5.38299989700317383, NULL, 5.39200019836425781, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2014, 3, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, 5.375, NULL, 5.36800003051757812, NULL, 5.37099981307983398, NULL, 5.38500022888183594, NULL, 5.39400005340576172, NULL, 5.39200019836425781, NULL, 5.39400005340576172, NULL, 5.40399980545044034, NULL, 5.40299987792968839, NULL, 5.40100002288818359, NULL, 5.39900016784667969, 'A', 5.40199995040893644, NULL, 5.40799999237060547, NULL, 5.4159998893737793, NULL, 5.40899991989135742, NULL, 5.40899991989135742, NULL, 5.40700006484985352, NULL, 5.40299987792968839, NULL, 5.40700006484985352, NULL, 5.40100002288818359, NULL, 5.39400005340576172, NULL, 5.39099979400634766, NULL, 5.39699983596801758, NULL, 5.41200017929077237, NULL, 5.41499996185302734, NULL, 5.40999984741210938, 'A', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('08MG026', 2016, 7, 8, 0, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 5.70599985122680664, 'A', 5.68400001525878906, NULL, 5.69199991226196289, NULL, 5.69500017166137695, NULL, 5.69099998474121094, NULL, 5.71899986267089844, NULL, 5.73199987411499023, NULL, 5.72300004959106445, NULL, 5.72700023651123136, NULL, 5.73799991607666016, NULL, 5.71500015258789062, NULL, 5.71500015258789062, NULL),
    ('08MG026', 2016, 8, 8, 1, 31, 5.60300016403198242, 173.688999999999993, 23, 5.53399991989135742, 14, 5.68300008773803711, 5.66400003433227539, NULL, 5.62200021743774414, NULL, 5.59200000762939453, NULL, 5.61100006103515625, NULL, 5.5970001220703125, NULL, 5.57000017166137695, NULL, 5.58099985122680664, NULL, 5.59499979019165039, NULL, 5.57499980926513672, NULL, 5.60300016403198242, NULL, 5.61499977111816406, NULL, 5.65500020980834961, NULL, 5.67399978637695312, NULL, 5.68300008773803711, NULL, 5.66200017929077237, NULL, 5.67100000381469727, NULL, 5.65999984741210938, NULL, 5.63199996948242188, NULL, 5.60699987411499023, NULL, 5.61800003051757812, NULL, 5.61399984359741211, NULL, 5.55200004577636719, NULL, 5.53399991989135742, NULL, 5.53999996185302734, NULL, 5.56300020217895508, NULL, 5.56799983978271484, NULL, 5.59800004959106445, NULL, 5.54799985885620117, NULL, 5.55900001525878906, NULL, 5.56300020217895508, NULL, 5.56300020217895508, NULL),
    ('08MG026', 2016, 9, 8, 1, 30, 5.46099996566772461, 163.817000000000007, 30, 5.38000011444091797, 1, 5.57899999618530273, 5.57899999618530273, NULL, 5.53800010681152344, NULL, 5.50899982452392578, NULL, 5.48799991607666016, NULL, 5.48000001907348633, NULL, 5.48099994659423828, NULL, 5.48099994659423828, NULL, 5.47499990463256836, NULL, 5.45599985122680664, NULL, 5.49900007247924805, NULL, 5.46700000762939453, NULL, 5.43900012969970703, NULL, 5.43599987030029297, NULL, 5.45200014114379883, NULL, 5.46099996566772461, NULL, 5.48099994659423828, NULL, 5.53999996185302734, NULL, 5.49499988555908203, NULL, 5.46799993515014648, NULL, 5.43599987030029297, NULL, 5.41699981689453125, NULL, 5.40500020980834961, NULL, 5.41200017929077237, NULL, 5.39900016784667969, NULL, 5.41699981689453125, NULL, 5.45300006866455078, NULL, 5.46199989318847656, NULL, 5.41800022125244141, NULL, 5.39300012588500977, NULL, 5.38000011444091797, NULL, NULL, NULL),
    ('08MG026', 2016, 10, 8, 1, 31, 5.45300006866455078, 169.045999999999992, 5, 5.34800004959106445, 16, 5.63000011444091797, 5.36999988555908203, NULL, 5.35900020599365234, NULL, 5.35500001907348633, NULL, 5.35300016403198242, NULL, 5.34800004959106445, NULL, 5.36800003051757812, NULL, 5.43599987030029297, NULL, 5.42500019073486328, NULL, 5.41200017929077237, NULL, 5.38299989700317383, NULL, 5.36499977111816406, NULL, 5.36100006103515625, NULL, 5.44000005722045898, NULL, 5.57100009918212891, NULL, 5.56199979782104492, NULL, 5.63000011444091797, NULL, 5.53499984741210938, NULL, 5.50400018692016602, NULL, 5.48199987411499023, NULL, 5.49300003051757812, NULL, 5.48299980163574219, NULL, 5.45599985122680664, NULL, 5.44199991226196289, NULL, 5.4590001106262207, NULL, 5.49499988555908203, NULL, 5.47800016403198242, 'A', 5.55299997329711914, NULL, 5.50899982452392578, NULL, 5.48600006103515625, 'A', 5.46799993515014648, NULL, 5.46500015258789062, NULL),
    ('08MG026', 2016, 11, 8, 1, 30, 5.57299995422363281, 167.194999999999993, 30, 5.40899991989135742, 9, 6.12900018692016602, 5.45399999618530273, NULL, 5.52899980545044034, NULL, 5.62300014495849609, NULL, 5.54500007629394531, NULL, 6.0560002326965332, NULL, 5.65999984741210938, NULL, 5.60300016403198242, NULL, 5.72300004959106445, NULL, 6.12900018692016602, NULL, 5.69099998474121094, NULL, 5.63700008392333984, 'A', 5.83300018310546875, NULL, 5.65100002288818359, NULL, 5.62599992752075195, NULL, 5.56500005722045898, NULL, 5.5149998664855957, NULL, 5.50899982452392578, NULL, 5.49100017547607422, NULL, 5.47800016403198242, 'A', 5.47300004959106445, NULL, 5.46400022506713867, NULL, 5.45800018310546875, NULL, 5.45399999618530273, NULL, 5.44999980926513672, NULL, 5.44700002670288086, NULL, 5.44600009918212891, NULL, 5.43699979782104492, NULL, 5.42500019073486328, NULL, 5.41400003433227539, NULL, 5.40899991989135742, 'A', NULL, NULL),
    ('08MG026', 2016, 12, 8, 1, 31, 5.32499980926513672, 165.068000000000012, 21, 5.29500007629394531, 1, 5.40399980545044034, 5.40399980545044034, NULL, 5.39900016784667969, NULL, 5.39300012588500977, NULL, 5.36899995803833008, NULL, 5.3600001335144043, NULL, 5.32899999618530273, NULL, 5.31599998474121094, NULL, 5.32600021362304688, NULL, 5.35400009155273438, NULL, 5.3600001335144043, NULL, 5.34600019454956055, NULL, 5.31799983978271484, NULL, 5.30900001525878906, NULL, 5.31300020217895508, NULL, 5.31599998474121094, NULL, 5.31500005722045898, NULL, 5.32000017166137695, NULL, 5.3189997673034668, NULL, 5.30299997329711914, NULL, 5.30100011825561523, NULL, 5.29500007629394531, NULL, 5.29500007629394531, NULL, 5.29899978637695312, NULL, 5.29799985885620117, NULL, 5.29799985885620117, NULL, 5.30299997329711914, NULL, 5.30499982833862305, NULL, 5.30200004577636719, NULL, 5.30399990081787109, NULL, 5.30000019073486328, NULL, 5.29899978637695312, NULL)
    ON CONFLICT (station_number, year, month) DO NOTHING;
    """)
        op.execute('SET search_path TO public')

    # use_pg_trgm
    op.execute("""
    create index if not exists idx_freshwater_atlas_watersheds_fwa_watershed_code
        on freshwater_atlas_watersheds
        using gin ("FWA_WATERSHED_CODE" gin_trgm_ops);
    create index if not exists idx_freshwater_atlas_stream_networks_fwa_watershed_code
        on freshwater_atlas_stream_networks
        using gin ("FWA_WATERSHED_CODE" gin_trgm_ops);
    create index if not exists idx_freshwater_atlas_stream_networks_fwa_watershed_code_btree
        on freshwater_atlas_stream_networks ("FWA_WATERSHED_CODE");
    create index if not exists idx_freshwater_atlas_stream_networks_linear_feature_id
        on freshwater_atlas_stream_networks ("LINEAR_FEATURE_ID");
    """)

    # create prism schema
    op.execute("""
    create schema if not exists prism;
    """)

    # if this is a dev environment, add sample data. This data covers only Whistler.
    # see imports/prism/load_prism.sh and openshift/import-jobs/prism.job.yaml
    # for methods for loading production data.
    if WALLY_ENV == ENV_DEV:
        op.execute("""
        --
        -- Name: prism; Type: TABLE; Schema: prism; Owner: wally
        --

        CREATE TABLE prism.prism (
            rid integer NOT NULL,
            rast public.raster,
            filename text,
            CONSTRAINT enforce_height_rast CHECK ((public.st_height(rast) = 100)),
            CONSTRAINT enforce_nodata_values_rast CHECK ((public._raster_constraint_nodata_values(rast) = '{-9999.0000000000}'::numeric[])),
            CONSTRAINT enforce_num_bands_rast CHECK ((public.st_numbands(rast) = 1)),
            CONSTRAINT enforce_out_db_rast CHECK ((public._raster_constraint_out_db(rast) = '{f}'::boolean[])),
            CONSTRAINT enforce_pixel_types_rast CHECK ((public._raster_constraint_pixel_types(rast) = '{32BF}'::text[])),
            CONSTRAINT enforce_same_alignment_rast CHECK (public.st_samealignment(rast, '010000000077220E111111813F77220E11111181BFBC34222222CA5EC0E41400000020494000000000000000000000000000000000E610000001000100'::public.raster)),
            CONSTRAINT enforce_scalex_rast CHECK ((round((public.st_scalex(rast))::numeric, 10) = round(0.008333333333, 10))),
            CONSTRAINT enforce_scaley_rast CHECK ((round((public.st_scaley(rast))::numeric, 10) = round((- 0.008333333333), 10))),
            CONSTRAINT enforce_srid_rast CHECK ((public.st_srid(rast) = 4326)),
            CONSTRAINT enforce_width_rast CHECK ((public.st_width(rast) = 100))
        );


        --
        -- Name: prism_rid_seq; Type: SEQUENCE; Schema: prism; Owner: wally
        --

        CREATE SEQUENCE prism.prism_rid_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1;


        --
        -- Name: prism_rid_seq; Type: SEQUENCE OWNED BY; Schema: prism; Owner: wally
        --

        ALTER SEQUENCE prism.prism_rid_seq OWNED BY prism.prism.rid;


        --
        -- Name: prism rid; Type: DEFAULT; Schema: prism; Owner: wally
        --

        ALTER TABLE ONLY prism.prism ALTER COLUMN rid SET DEFAULT nextval('prism.prism_rid_seq'::regclass);


        --
        -- Data for Name: prism; Type: TABLE DATA; Schema: prism; Owner: wally
        --

        INSERT INTO prism.prism (rid, rast, filename) VALUES (1, '010000010077220E111111813F77220E11111181BFBC34222222CA5EC0E41400000020494000000000000000000000000000000000E6100000640064004A003C1CC62DDECF446001CE4491A9CD44FD80CD445845CE44023FD044EA29D2444988D2442ED1D24499B1D24448D9D14432FBD044B9CAD044B2EDD044D31DD1448DEBD044494CD044022FCF44AD70CE44C590CE441050CF4437A5D0443721D24442CCD2448F3AD3447F46D2448CC4D044D1A6CD44160DCA44D7F2C4446762BE44B12EB344ACC4A74449A09F44B6279A44EBCD9A448557A344A08EB64408F0CB4446FADD443910EE44C40C0145DF47094544FB0D45A2B50F45817F0F4541520F456C490F45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC68344D444E7B3CF44D1AACD442B7FCD44502DCE448F8ACF444333D0443D1AD044E90ECD445C83C9445F76C84430F5C644B430C5449AF9C3447029C344A111C2444CE7C0443EB2BF440A93BE44775EBE4409A0BE4431B4BF44647BC1444170C2445001C3449005C344DB41C2444E56C144F79FBE4496E7BA44D235B544D7EBAD4433A7A444A2D19C4462B8994408249C44584DA744122FBA4468F1CC449DC3DD44371DEA44C8BAF74447910245AAED0645EFE90B4542D20E45FE141145B4261645003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC606E1D944754BD6442234D4444F35D444E87BD4449230D544EDA8D444A0DAD144F1BACF4482A8CA44BE93C844252EC744A424C544FAD6C1440AE7BE44DAC6BC441A5CBB442B17BA44D5C0B8440A73B744BB3DB644460AB6443928B6440CD2B644A410B844BE4BB944863BBA44CDFCBA44FA5AB944D5ECB544F678B04406DDA8441E86A24411E09B4430B99B44DF0BA1447300AF441160C1442960D04485DFDD443C07EA44070CF1447557FA44A086024527010745E34D0D4524301145DFD71645003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC62F51E6448DC7E2447B9CE2442898E244418CE344BD33E444C365E0442064DC4480F1D7448B08D3444B97D044F5ECCF440F55CE44B394CB440AA7C744F8F3C4441AF8C24465EBC1448746C044B2A9BD4485D7BA44446FB844EF03B744D78BB7442257B944CE7CBC440592BF44F173C144C166C04485CFBC443CF7B5442D32AC4480C2A444041A9F448FCEA0448E1FA94439FCB84454A3C644F123D5445109E0440C3AEA447D2FF144D982FA4456AC02454721074512BB0D45EF091145C4611345003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6816DF8441029F244BAF5F2444F91F744E534F844DC0DF8443D26F144FA5EEE440124E74471E5E34449D4E3443C92E244BD50DE441D56D9444433D5448971D244662AD044C88ACE4403D7CB444E1AC84437D1C44466F2C0445E12BE44DD18BE442034C0449587C344BF83C74410F4CA4462B8CA445E3AC644C832C0443A40B54436D2AA44B454A544D408A8448B04B244F7F4C0440CEACC44BC99D844F475E34406CDEC4458E1F3447111FE44B80A044589570845C0AA0E4558E51045EDF20F45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC674E4FE444E6AF9444CE3F9440F90FC44300DFE44B21300450EEDFE44B6D3F6445E16F64406B1F5445D87F54451E5F54479B5F444523CEB44E535E4448C0CDF44F8AFDC445238DA442E91D644A40CD244B6E3CC44D45DC744139FC3442EBDC24412CBC3446AA4C744D3FDCD443C53D2447B24D3443BC3CE444337C6444940BD44BB0DB244FAEEAB442C52AE44268DB844C96AC544E5D8D1443EF6DC44EEACE644542BF0441ACFF9445E2202451B35064574C10A45F68C104515AE104581E90B45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6A046FD44F296F94469DDF844B06EFA4436A6FC44BA21FF44B339FF44A61D0045A44A0145BE1D0245E2F20245D3E902454ADA0245F8A7FA444497EF44F83FE8444BBBE3444F6DE1441FF5DC44DD40D8441EC5D2444819CD44C508C844C232C544D215C544299CC74414A6CC443CF2D0449D6FD244F7CBCF44DD00C8443E86BF4477C2B544E6E0B044416CB344FAAEBD443CB6C94423A3D644D882E244E8B6EB44FA6AF544D948004595930445A681084556100F45353A1045D8B50D457D3B0745003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC64959FC442EA6F944156EF844CA86F84472E8F944FEB4FD44EA32FF441C500045920905457B24084584110B45B29F0C453A720C457F8207451CA2FE44043EF14420B1EA444C17E544E5C8E1449488DD44C530D6448593D0445D67CB444CA3C744241EC544D296C44484D3C544D315C8446F1AC9448AC9C644082CC244DD94BB4483A8B544D5DCB2444E52B74420BDC044BE53CE4450D5DB44AA29E944DD8CF54491A700457BBC0545B7610945B6010D45E7091045F2EA0F4520F60B450AC30545003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6BCFDFA44DD14F944D6BCF744B8B2F644F0F7F7449BADFB4410BDFE44CDC0004500120545A42A0845D4120B45B6530C45133F0C45AA2309456BAC0245761FF644A992EC44D20DE5448CD7DF44F25EDB44E7DBD444C78FCF445DD6CB440060C7443F71C344026FC0442556BE44FE54BD440CDEBC44E932BB44AAB1B8441671B54474F4B244D2CAB44451C4BB4436AEC5445071D344EA12E244FD64EF44F103FF44FC8F054540CD0A45BAAF0E45F8A11145E17C1145D0610F45C0D20B45EE880645003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC63FC9F9441808F844B95AF644A82EF54437A1F6443AF0F944C9DEFD447BE60045A7100545B4A20745328C084538A70845FD7D0845680707457BF8014579F1F544485DEA4412FBE24448C1DC443019D844135BD0442526C944B016C444E833C04427ADBC44F439BA44C18EB644441BB3446995B144A404B144C102B1444666B2440DD2B4445B80BA44B856C2447141CE44972ADA44DE10E7449DFBF24446D6004521C00645F85F0B45B0740F45B26F1245C9AE124571A51045C5600C45D59C0845003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC69637F844FABEF6444E22F544C418F4445274F5441E99F844E3F5FC445BDA0045562A04456A8A0545ACC4054522850545107C0445FD8201452C42FC44B8EAF34490A6E744A454DE440F69D8440050D24429D4CA440D7AC144ACB0BB449C30B944A1B9B5442D46B0445EF2AC447B94AC44DACAAD449281B044357EB344E8DBB644C743BC448A5DC3440E5DCD44B683D8448527E44435B2EF4499D1FB44C01603450C1C0745F9180A45EE430E45ADEE104554AB12450CCA114572E60D458DED0A45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC61B6EF74405BAF544AEDFF344C64BF3444E46F4444E6AF744B3A1FB4460B3004592A7034544F50445E8130545D57E0445811B0245D00EFC442F29F344E0FAEA447417E2447BB0D944CC94D4443433CE446EEAC5442492BC44B1EAB2447929AC445C33AA4478FEA9444980AB44838CAE44F89BB044A68BB444B255B9447AB5BD444194C444B4A0CC445ACCD5442D56DE448EDFE944F575F4441F0D004583BA05458FE80845EA160C4598720F45CBB71145FA8813458D3913450C00114590420E45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC60E21F744F4C9F4445DFFF244CD98F244905DF344D420F5440CC6F944144A0045021303455A3A0445FD610445231F04457E1D02456772FC44D74BF244AE47E944D072E1449D98D844420CD24491EDC944F5F5BF443BE7B344760AAB44D56CA844D34DA844E9AAA944F9BAAC447FAAB0441F89B5449EAFBC448E4BC144E6F4C64451F4CC440EA1D24494ACD94491DADE44E1A2E8449BCCF144CA25FD4427970345BAD30845E85B0D4528121145A8CC144588E81545B6351545AE531345DF851145003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6AC50F7443E9EF444065DF2446E9AF14411D8F14473D4F344A942F844D056FF445EAC0245C80C0445AC7E044510CC044597EC044528970145CA85FB448D6FF0440DB1E144B101D744CC38CF445CB3C744345FBC4491B1B0442267A944AE23A844C464A84481CDA94415F6AC44D7CBB444043EB9442B2FC3446A24CA440452CF44827DD444CA39D8446208DC4490EADE443F91E0444F7DE8440AEBF14412DBFB44C4A40245A42A054560CF0A4531D60F4589E310457D331045215C0F45AE790F45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC61E69FD44708DF44417C9F0449BECEF440E19F044EEB0F1447A2CF6442E29FC4439D20145E89103458ED10445A0C0054574D7054599E5024520A0FD449F56F144D1C5E044E22DD5449A95CC44B677C644BFF3BB4449E8B044A4B4A9442154A944DA9EA9449420AB442D3EAE44B4B0B6444C37BC4421DCC744366AD044154ED544E023DA440BCFDD4440EDE1441E21E2448CDCE044E926E144C8A3E344DFBBEE447626F644EA8DFF44464A024565750545DF23074563680845711F09459DA10A45003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC69A2D0045439CF7442609F04482F4EB445C27EC44E550EE44D464F3440C82F944CD50004563AC0245DECC034564710445C1A003453EAE00457AD4F5448CA3EB448CC4DD4447A9D2446D03CB44678EC6443536BC44223BB1440649AF44D510AF445EFAAE44A832B0447A18B344E2BEB8445869BF44FD08CB44155ED444BC14DA440CE2DF441631E4445164E844578DE74468D5E54498DEE344F638E244A687E2445DCBE7444CA7EE447B25F3442A68F744580DFE44D2B9004501B00245126F0545003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6107A004580BAF7442F29EF449CF8E84454AFE944E086EB44802AF14402FFF6444403FE44802001454AA601450C920145850FFE4430A0F6445905ED441AD3E44479ADD944DDC8CE4428F0CA44326CC644B301BD448179BC441844BC44B600BC44CDD8BB44CAD6BB44A657BC446AE0BF44447AC6446F7AD2442393DB446AC8E144F87BE94458EDEE440B86F2440900F244F538EE441DB2E94480C6E644816DE3441B43E244BFEFE24403DBE444DBA5E844C276EE44903AF244EEC0F444D23DFC44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC656D4004517D5F744AE77ED44FE74E6440A93E6447075E944041AED441EDDF3442EDAF94411DCFC442EDEFC440B6AF54454ABEB441AD7E244D3ADDB44E58CD644FFB3D1447A9CCC442BA7CA44B4C4C644687DC6441B73C644855FC644DA22C644B4FCC544BCB8C544956BC644EFDFC84450B9CF442F5DDA44A51CE444E0D2E944C09AF1445164F744A1C1FB442248FC44F44DF844BEFFF144397CEB44087CE844BBF9E5443AA0E544E491E44466FAE344BD97E3447E92E3443F09E6448782E944003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC624DEFF44FA86F7440884EC44ACECE34458C1E1443A7CE344062DE6446E16EA44ABC0EB440E91EB4410A8E54439B0DD44901ED8444FF9D344917DD144FBF5CF442729CE44039BCC444831CC44F1B6CB447238CC445E5ACC4429ECCC44B126CD440C16CD44FEA8CC447AADCC447A69CD440B42D24418C8DC44DC80E644681DED440257F5448F5EFB446A280045D9D60045AAD9FC447732F844C2B9F344E296F0447C9CED4430D0EB4451A1E84493A0E6449AD9E44470B9E1443C37DD44D9FEDB44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC64DEAF5447488F3447915EC44BE13E2444091DB44E371DB446D1FDB44300CDB44ECB5DA443845DA44433BD644D00ED3448091D1446BA8D0449E57D04410FCCF44F2B2CF441E39D044CEF4CF4464EBCF44DCD0CF44E479D0445CEFD0449225D1448021D244DE54D044C4DCCE44E2A2CE444427D144B942D7448663DF44ECFDE6449653F044C3DDF84474250045D4900145F2FEFF44D832FB44033FF744EFABF5447016F544E38DF44404D6F2442775EE4427BDE944F28EE6445A78E244B7C3DC44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6955FEE44FABAEA441051E744A77EDF44FCDDD7444562D5442ED9D444123BD444A7CBD344DF4BD344A693D24422C3D1448271D1443D12D1447C4BD144C697D1446188D144F504D2441E66D244BC4CD244A0AED244ADDBD244C176D444CD1CD744F4D1D844EE18D74477FED344547FD24431E0D1442BDBD344C707D844467ADE448E0AE5449CCBED44693DF6444CF7FD4483040045B345FE44473DFB440F89FA44F55CFB44019FFC44DD3CFC443566F944D4A1F4442CC6EF44C7F3E9444646E344003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6168EEC449901E644981EE244C584DF440830D844E9DED544A88ED5440F05D54467A2D44485EBD3445220D444A1C5D3445268D344CF03D344B4A0D2445597D2443D3ED44432D7D5446885D6443B93D644A09AD744D1B6DA4450B9DE44B630E244BF5EE344DE7CE144C18EDC445BA8D744F2E2D444B872D344D823D44439B8D74427E1DC44E787E344D76BEB442851F344F644FA44544BFF44272B0045686B0045521A0145B0CE014595670245183E014542A4FE44F738F944B83AF344EAC6E944003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC63D76EC44DA61E6449875E244723CDE442014D844BFABD644D25ED64448C9D644D9D2D6446855D64416DDD5442207D544BDD8D34460F1D244F58CD2446398D2441914D644CA8DDA449AADDA44A70EDB441BE7DB448059DE44DFBBE1440CE2E444703DE7444393E6446CA7E244321CDD44AED3D8442A28D6440DFAD444209CD5443696D744047EDB449CFCE04498AAE74414B6ED44C49CF244B93EF944BAE1FF4456DE0245887C0445CBC105457FAA05458D2B03457B6C0045414CF844A88AEB44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC67AA9EC4497DAE6448EE3E2447881DC4491E5D744045ED74446B6D744502DD944A14ADB44A64FDB44A826DB4448ADDA44530CD944F6B8D544AEE3D444E1F2D444E0F3D544D9EEDA44E6FCDA44762EDB444E1EDB44CA55DC44ED50DE44FDDCE0443900E344AEE7E4449E97E444C4CCE244E9D6DD443FDDDA446642D9446165D84478C1D844CC54D9446CB7DA4484E0DF4419C4E444C35DE8447CCBED440C8EF3443273FB441B750145A020054529D6064577320545C8BC01452E4EF7441651E644003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6BD0CED44674AE7442831E3448CC8DB445019D8440DD5D7446340D84489A1DB4480F5DD441C77DE444612DE44EE84DD44D202DD445A20DC442536DB445DBBDA440778DA44683DDA44A507DA44587DDA44D92EDA44C4D4D944EB15DA447101DB44BFB3DC44F34ADE449CACDF44F485E044E329E1444F06E1444417E04410F0DE44DD8CDE44DC9DDE447467DE44A64BDF448EFFE0441818E34488FDE6442581EC4419E3F344703DFA4481150145B4300445E13E03459235FF44C84AF54446CAE644003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6607DED443E9AE7444759E344CA5DDB44D524D844D8ABD7446B18D8443D86DB442170DE444632E044A683E244CA65E344024FE3445BF7E24443AFE244D96AE24457EAE144B8E6E0441888DD4429A4DA44BDA0D844E43DD84407CDD7442A8CD744425CD744570ED8447A31D9447FFADA445ED6DC44FBB5DE449533E044471DE34460FDE444EE84E544995DE54402A3E54472E1E544CE5FE7449A21EA44595CEE442785F34458CDF744521CFE449D330145AA710045AC20FB4436C6F344C5B8EB44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6DBF9ED448F06E844A438E2440233DA44583ED8448CC4D7446338D844D570DC44D271E044E0B2E3449F52E944BAA5F0446B64F94492C5FB444692FB44FD80FB44C036FB44C6B8F6440F74EB446E5ADE44A41CD9448D1FD8444656D044965FCB44FFECCA4420D4CA44BF3BCB44D076CC44D341CF44E956D34480A9D744ADACDC44FB6EE144B2E5E7448D2BEB447861EC44F687ED441138EF444029F144FB70F444AA4DF7447D23FB44DF73FD44C520FD44B4D8FA4448E9F544CCA4EF449527EC44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6EA6EEE44C002E844DE7CDF440830DA44D524D9446D3FDB44785DDD4498E2E544804EEB446417F14418DDFB44005005456D0B094506C309459A0D0A457F100A45CEED0945FACE074573EC014562F8F5444E0EE6440287DD446C93D4447EABCE44318CCB44C414C44405B1C044962BC144CECBC244E1BAC6444168CB44791DD044CD78D6449ECBDE445F4EE9442950EF441C03F2445C27F5446DEFF74404FAFE44E8DB004547B50145B4DA0045AA3EFC448816F7445D37F24479A5EC44A51FEA44003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6DCF5ED443EF1E3443795DA447657DA44F09BDE44BDA4E544B4A4EE44E6B7FB44C5460245BDB005459FAF094543AB0D45850311457EBA1345E6121545624E154574331545D56C1345E6620D453AAE0845237F0245326BFA446C07F244EBEAE544E94ED5442089CB447762C544FCE9BD442F89BB446029BE446A30C244BA3DC644E99ECB448E57D34413FAD944C787E1449E2BEA44DE88F0441C7BF544953FFE4411620045373501451B4300459211FB445DAEF3446A38EC443EE2E6443C4FE444003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC61BCBE8447260DD4442C8DA44A6B7DE4484C3EA44A2B9F644FE0CFE44CB01034506650745FED00A45A6AF0E455EA6124500F41545F0AD18456D291A45DB351B4577FE1A45FE821945BBB11445CC5E0F4516030C4520A10A45063B09454ECA0445F0CBF6440FF0DC445051CC44E6ACC54483B8BD44DFFFB9448CACBA44C0B6BE44A03EC3448626C74444DBCD44451AD6442940DC442028E2444A30E944E26DF04437E9FA44865FFE4482C5FE44C2EEF9445CD3EF444859E844D66BE34476C2E044003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6003C1CC6', 'prism_pr.asc');


        --
        -- Name: prism_rid_seq; Type: SEQUENCE SET; Schema: prism; Owner: wally
        --

        SELECT pg_catalog.setval('prism.prism_rid_seq', 1, true);


        --
        -- Name: prism enforce_max_extent_rast; Type: CHECK CONSTRAINT; Schema: prism; Owner: wally
        --

        ALTER TABLE prism.prism
            ADD CONSTRAINT enforce_max_extent_rast CHECK ((public.st_envelope(rast) OPERATOR(public.@) '0103000020E61000000100000005000000BC34222222CA5EC08D7C555555B54840BC34222222CA5EC0E41400000020494090E8CCCCCC945EC0E41400000020494090E8CCCCCC945EC08D7C555555B54840BC34222222CA5EC08D7C555555B54840'::public.geometry)) NOT VALID;


        --
        -- Name: prism prism_pkey; Type: CONSTRAINT; Schema: prism; Owner: wally
        --

        ALTER TABLE ONLY prism.prism
            ADD CONSTRAINT prism_pkey PRIMARY KEY (rid);


        --
        -- Name: prism_st_convexhull_idx; Type: INDEX; Schema: prism; Owner: wally
        --

        CREATE INDEX prism_st_convexhull_idx ON prism.prism USING gist (public.st_convexhull(rast));

        """)

    # add short term licence layer
    op.execute('SET search_path TO metadata')

    # populate water_approval_points info
    op.execute("""
          WITH ds_id AS (
            INSERT INTO data_source (
                data_format_code,
                name,
                description,
                source_url,
                source_object_name,
                data_table_name,
                source_object_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                'json',
                'Water Approval Points',
                'The location (point) where an approval has been requested to conduct works in the vicinity of a water source.',
                'https://catalogue.data.gov.bc.ca/dataset/water-approval-points',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_APPROVALS_SVW',
                'water_approval_points',
                'WATER_APPROVAL_ID',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING data_source_id
        ),
        wms_id AS (
          INSERT INTO wms_catalogue (
                wms_catalogue_id,
                description,
                wms_name,
                wms_style,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES (
                (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                'Water Approval Points',
                'WHSE_WATER_MANAGEMENT.WLS_WATER_APPROVALS_SVW',
                '',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            ) RETURNING wms_catalogue_id
        )
        INSERT INTO display_catalogue (
            display_data_name,
            display_name,
            label_column,
            label,
            highlight_columns,
            data_source_id,
            wms_catalogue_id,
            layer_category_code,
            mapbox_layer_id,
            mapbox_source_id,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) SELECT
            'water_approval_points',
            'Water Approval Points',
            'FCBC_TRACKING_NUMBER',
            'FCBC Tracking Number',
            ARRAY[
                'WSD_REGION', 'APPROVAL_TYPE', 'APPROVAL_FILE_NUMBER', 'FCBC_TRACKING_NUMBER', 'SOURCE', 'WORKS_DESCRIPTION', 'QUANTITY', 'QUANTITY_UNITS', 'QTY_DIVERSION_MAX_RATE', 'QTY_UNITS_DIVERSION_MAX_RATE', 'WATER_DISTRICT', 'PRECINCT', 'APPROVAL_STATUS', 'APPLICATION_DATE', 'FCBC_ACCEPTANCE_DATE', 'APPROVAL_ISSUANCE_DATE', 'APPROVAL_START_DATE', 'APPROVAL_EXPIRY_DATE', 'APPROVAL_REFUSE_ABANDON_DATE'
            ],
            ds_id.data_source_id,
            wms_id.wms_catalogue_id,
            'WATER_ADMINISTRATION',
            'iit-water.448thhpa',
            'iit-water.448thhpa',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        FROM ds_id, wms_id ;
    """)

    op.execute('SET search_path TO public')

    # update mapbox layer references
    op.execute('SET search_path TO metadata')

    op.execute("""
               UPDATE display_catalogue SET required_map_properties = ARRAY['APPROVAL_STATUS'] WHERE display_data_name = 'water_approval_points';
               UPDATE display_catalogue SET required_map_properties = ARRAY['LIFE_STAGE', 'SPECIES_NAME'] WHERE display_data_name = 'fish_observations';
               UPDATE display_catalogue SET required_map_properties = ARRAY['DOWNSTREAM_ROUTE_MEASURE', 'FWA_WATERSHED_CODE', 'LINEAR_FEATURE_ID', 'LOCAL_WATERSHED_CODE', 'STREAM_MAGNITUDE'] WHERE display_data_name = 'freshwater_atlas_stream_networks';
               UPDATE display_catalogue SET required_map_properties = ARRAY['station_number'] WHERE display_data_name = 'hydrometric_stream_flow';
               UPDATE display_catalogue SET required_map_properties = ARRAY['WATERSHED_FEATURE_ID'] WHERE display_data_name = 'freshwater_atlas_watersheds';
               UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.0tsq064k' WHERE display_data_name = 'aquifers';
               UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.31epl7h1' WHERE display_data_name = 'hydrometric_stream_flow';
               UPDATE display_catalogue SET mapbox_layer_id = 'iit-water.56s6dyhu' WHERE display_data_name = 'freshwater_atlas_stream_directions';
               UPDATE data_source SET source_object_id = 'AQUIFER_ID' WHERE data_table_name = 'ground_water_aquifers';
               UPDATE data_source SET source_object_id = 'OBJECTID' WHERE data_table_name = 'bc_major_watersheds';
        """)

    op.execute('SET search_path TO public')

    # wms information updates
    op.execute('SET search_path TO metadata')

    op.execute('alter table display_catalogue add column use_wms boolean default true')

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Freshwater Atlas Stream Networks',
                    'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP',
                    '1853',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'freshwater_atlas_stream_networks';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'ParcelMap BC Parcel Fabric',
                    'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'cadastral';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Ground Water Aquifers',
                    'postgis_ftw.wally_aquifer_view',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'aquifers';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Water Rights Applications - Public',
                    'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_APPLICTNS_SV',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'water_rights_applications';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'First Nation Community Locations',
                    'WHSE_HUMAN_CULTURAL_ECONOMIC.FN_COMMUNITY_LOCATIONS_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'fn_community_locations';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'First Nations Treaty Areas',
                    'WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_AREA_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'fn_treaty_areas';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'First Nations Treaty Lands',
                    'WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_LAND_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'fn_treaty_lands';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Water Rights Licences - Public',
                    'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'water_rights_licences';
        """)

    op.execute("""
            WITH wms_id AS (
                INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Ground Water Wells',
                    'postgis_ftw.wally_well_view',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            UPDATE display_catalogue SET wms_catalogue_id = (SELECT wms_catalogue_id FROM wms_id) WHERE display_data_name = 'groundwater_wells';
        """)

    op.execute("""
            UPDATE display_catalogue set use_wms = false where display_data_name = 'hydrometric_stream_flow';
            UPDATE display_catalogue set use_wms = false where display_data_name = 'normal_annual_runoff_isolines';

            UPDATE wms_catalogue set wms_style = '719' where wms_name = 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY';
            UPDATE wms_catalogue set wms_style = '4883' where wms_name = 'WHSE_WILDLIFE_MANAGEMENT.WCP_CRITICAL_HABITAT_SP';
        """)

    op.execute('SET search_path TO public')

    # update terminology
    # metadata.data_source.name needed to be changed from varchar(50) to varchar(200) to
    # accommodate some of the longer layer names
    op.execute("""

    alter table metadata.data_source
    alter column name type varchar(200);


    update  metadata.wms_catalogue
    set     description = 'ParcelMap BC'
    where   description = 'ParcelMap BC Parcel Fabric';

    update  metadata.wms_catalogue
    set     description = 'Critical Habitat (federally-listed species at risk)'
    where   description = 'Critical Habitat federally-listed species at risk';

    update  metadata.wms_catalogue
    set     description = 'Known BC Fish Observations & Distributions'
    where   description = 'Known BC Fish Observations & BC Fish Distributions';

    update  metadata.layer_category
    set     description = 'Forests, Grasslands, and Wetlands'
    where   description = 'Forests, Grasslands and Wetlands';



    update  metadata.display_catalogue
    set     display_name = 'Critical Habitat (federally-listed species at risk)'
    where   display_name = 'Critical Habitat for federally-listed species at risk (posted)';

    update  metadata.display_catalogue
    set     display_name = 'EcoCat Water-related Reports'
    where   display_name = 'Ecocat - Water related reports';

    update  metadata.display_catalogue
    set     display_name = 'Hydrometric Stream Flow (HYDAT)'
    where   display_name = 'Hydrometric Stream Flow';

    update  metadata.display_catalogue
    set     display_name = 'ParcelMap BC'
    where   display_name = 'Cadastral Parcel Information';


    update  metadata.display_catalogue
    set     display_name = 'Known BC Fish Observations & Distributions'
    where   display_name = 'Known BC Fish Observations and BC Fish Distributions';




    update  metadata.data_source
    set     name = 'Known BC Fish Observations & Distributions'
    where   name = 'Known BC Fish Observations & BC Fish Distributions';

    update  metadata.data_source
    set     name = 'EcoCat Water-related Reports'
    where   name = 'Ecocat - Water related reports';

    update  metadata.data_source
    set     name = 'Critical Habitat (federally-listed species at risk)'
    where   name = 'Critical Habitat federally-listed species at risk';

    update  metadata.data_source
    set     name = 'ParcelMap BC'
    where   name = 'ParcelMap BC Parcel Fabric';


    """)

    # fish obstacle layer
    op.execute('SET search_path TO metadata')

    op.execute("""
              WITH ds_id AS (
                INSERT INTO data_source (
                    data_format_code,
                    name,
                    description,
                    source_url,
                    source_object_name,
                    data_table_name,
                    source_object_id,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    'json',
                    'Provincial Obstacles to Fish Passage',
                    'The Provincial Obstacles to Fish Passage theme presents records of all known obstacles to fish passage from several fisheries datasets. Records from the following datasets have been included: The Fisheries Information Summary System (FISS); the Fish Habitat Inventory and Information Program (FHIIP); the Field Data Information System (FDIS) and the Resource Analysis Branch (RAB) inventory studies. The main intent of this layer is to have a single layer of all known obstacles to fish passage.',
                    'https://catalogue.data.gov.bc.ca/dataset/provincial-obstacles-to-fish-passage',
                    'WHSE_FISH.FISS_OBSTACLES_PNT_SP',
                    'fish_obstacles',
                    'FISH_OBSTACLE_POINT_ID',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING data_source_id
            ),
            wms_id AS (
              INSERT INTO wms_catalogue (
                    wms_catalogue_id,
                    description,
                    wms_name,
                    wms_style,
                    create_user, create_date, update_user, update_date, effective_date, expiry_date
                ) VALUES (
                    (select wms_catalogue_id from wms_catalogue order by wms_catalogue_id desc limit 1) + 1,
                    'Provincial Obstacles to Fish Passage',
                    'WHSE_FISH.FISS_OBSTACLES_PNT_SP',
                    '',
                    'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
                ) RETURNING wms_catalogue_id
            )
            INSERT INTO display_catalogue (
                display_data_name,
                display_name,
                label_column,
                label,
                highlight_columns,
                data_source_id,
                wms_catalogue_id,
                layer_category_code,
                mapbox_layer_id,
                mapbox_source_id,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) SELECT
                'fish_obstacles',
                'Provincial Obstacles to Fish Passage',
                'FISH_OBSTACLE_POINT_ID',
                'Fish Obstacle Point Id',
                ARRAY[
                    'OBSTACLE_NAME', 'SOURCE', 'SURVEY_DATE', 'AGENCY_NAME', 'HEIGHT', 'LENGTH', 'ACAT_REPORT_URL', 'UTM_EASTING', 'UTM_NORTHING', 'WATERBODY_TYPE'
                ],
                ds_id.data_source_id,
                wms_id.wms_catalogue_id,
                'FISH_WILDLIFE_PLANTS',
                'iit-water.448thhpa',
                'iit-water.448thhpa',
                'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
            FROM ds_id, wms_id ;
        """)

    op.execute('SET search_path TO public')

    # add user table
    op.create_table(
        'user',
        Column('uuid', String, primary_key=True),
        Column('default_map_layers', ARRAY(TEXT), nullable=True),
        Column('create_date', DateTime, nullable=False),
        Column('update_date', DateTime, nullable=False)
    )
    #
    # # op.execute('SET search_path TO public')
    # logger.info("what's the current schema? public?")


def downgrade():
    op.execute("""
        drop schema prism;
        """)
