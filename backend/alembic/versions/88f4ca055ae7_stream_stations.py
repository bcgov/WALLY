"""stream stations

Revision ID: 88f4ca055ae7
Revises: 4375f087337e
Create Date: 2019-07-15 16:27:54.990523

"""
from alembic import op
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Table, Text, PrimaryKeyConstraint, ForeignKey

from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
import logging
# revision identifiers, used by Alembic.
revision = '88f4ca055ae7'
down_revision = '4375f087337e'
branch_labels = None
depends_on = None

logger = logging.getLogger("alembic")


def upgrade():
    op.execute("create schema if not exists hydat")
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
        Index('idx_20802_annual_instant_peaks___uniqueindex', 'station_number', 'data_type', 'year', 'peak_code', unique=True),
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
        Index('idx_20940_annual_statistics_primarykey', 'station_number', 'data_type', 'year', unique=True),
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
        Index('idx_20886_sed_dly_suscon_primarykey', 'station_number', 'year', 'month', unique=True),
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
        Index('idx_20970_sed_samples_primarykey', 'station_number', 'sed_data_type', 'date', unique=True),
    )

    op.create_table(
        'sed_samples_psd',
        Column('station_number', Text, primary_key=True),
        Column('sed_data_type', Text, primary_key=True),
        Column('date', DateTime(True), primary_key=True),
        Column('particle_size', DOUBLE_PRECISION, primary_key=True),
        Column('percent', BigInteger),
        Index('idx_20796_sed_samples_psd_primarykey', 'station_number', 'sed_data_type', 'date', 'particle_size', unique=True),
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
        Index('idx_20826_stn_data_collection___uniqueindex', 'station_number', 'data_type', 'year_from', unique=True),
    )

    op.create_table(
        'stn_data_range',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('sed_data_type', Text, primary_key=True),
        Column('year_from', BigInteger),
        Column('year_to', BigInteger),
        Column('record_length', BigInteger),
        Index('idx_20898_stn_data_range_primarykey', 'station_number', 'data_type', 'sed_data_type', unique=True),
    )

    op.create_table(
        'stn_datum_conversion',
        Column('station_number', Text, primary_key=True),
        Column('datum_id_from', BigInteger, primary_key=True),
        Column('datum_id_to', BigInteger, primary_key=True),
        Column('conversion_factor', DOUBLE_PRECISION),
        Index('idx_20874_stn_datum_conversion_primarykey', 'station_number', 'datum_id_from', 'datum_id_to', unique=True),
    )

    op.create_table(
        'stn_datum_unrelated',
        Column('station_number', Text, primary_key=True),
        Column('datum_id', BigInteger, primary_key=True),
        Column('year_from', DateTime(True)),
        Column('year_to', DateTime(True)),
        Index('idx_20808_stn_datum_unrelated_primarykey', 'station_number', 'datum_id', unique=True),
    )

    op.create_table(
        'stn_operation_schedule',
        Column('station_number', Text, primary_key=True),
        Column('data_type', Text, primary_key=True),
        Column('year', BigInteger, primary_key=True),
        Column('month_from', Text),
        Column('month_to', Text),
        Index('idx_20892_stn_operation_schedule___uniqueindex', 'station_number', 'data_type', 'year', unique=True),
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
        Index('idx_20868_stn_remarks___uniqueindex', 'station_number', 'remark_type_code', 'year', unique=True),
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


def downgrade():
    pass
