"""add data sources

Revision ID: 30d75d8eb63d
Revises: 23a3899db882
Create Date: 2019-10-19 23:59:11.657726

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, ARRAY, TEXT
from sqlalchemy.ext.declarative import declarative_base
import datetime


# revision identifiers, used by Alembic.
revision = '30d75d8eb63d'
down_revision = '23a3899db882'
branch_labels = None
depends_on = None


Base = declarative_base()

class DataSource(Base):
    __tablename__ = 'data_source'

    data_source_id = Column(Integer, primary_key=True)
    name = Column(String, comment='data source detail name', index=True)
    description = Column(
        String, comment='explanation behind data source and use case')
    source_url = Column(String, comment='root source url of data')
    data_format_code = Column(String, ForeignKey('metadata.data_format_code.data_format_code'),
                              comment='format type of the source information')
    data_format = orm.relationship('DataFormatCode')
    data_store_id = Column(Integer, ForeignKey('metadata.data_store.data_store_id'),
                           comment='related data store where this sources data is held after ETL')
    data_store = orm.relationship("DataStore")
    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


def upgrade():
    op.execute('SET search_path TO metadata')

    # add foreign key column relating to data source
    op.add_column('display_catalogue',
                  sa.Column('data_source_id', sa.Integer(), sa.ForeignKey('metadata.data_source.data_source_id'), nullable=True, comment='references a data source'))

    # add data source information
    op.bulk_insert(DataSource, [
        {
            'data_source_id': 1,
            'name': 'Automated Snow Weather Station Locations',
            'description': 'Locations of automated snow weather stations, active and inactive. Automated snow weather stations are components of the BC snow survey network.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/automated-snow-weather-station-locations',
            **get_audit_fields()
        },
        {
            'data_source_id': 2,
            'name': 'BC Major Watersheds',
            'description': 'Major watersheds of BC tagged with the first 3 digits of the Watershed Code (e.g.: 920)',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/bc-major-watersheds',
            **get_audit_fields()
        },
        {
            'data_source_id': 3,
            'name': 'BC Wildfire Active Weather Stations',
            'description': 'This dataset contains point locations for actively reporting BC Wildfire Service (BCWS) weather stations. BCWS operates a network of automated hourly reporting weather stations to support all aspects of fire management. The data are used as input to the Canadian Forest Fire Danger Rating System, as a basis for weather forecasting and for climate monitoring. Sensors at the weather stations monitor temperature, relative humidity, wind speed and direction and rainfall. In a collaborative project with other government agencies and the private sector, select sites are being upgraded for year round operation by the addition of snow measurement gauges.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-active-weather-stations',
            **get_audit_fields()
        },
        {
            'data_source_id': 4,
            'name': 'ParcelMap BC Parcel Fabric',
            'description': 'ParcelMap BC is the single, complete, trusted and sustainable electronic map of active titled parcels and surveyed provincial Crown land parcels in British Columbia. This particular dataset is a subset of the complete ParcelMap BC data and is comprised of the parcel fabric and attributes for over two million parcels published under the Open Government License - British Columbia.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/parcelmap-bc-parcel-fabric',
            **get_audit_fields()
        },
        {
            'data_source_id': 5,
            'name': 'Critical Habitat for federally-listed species at risk (posted)',
            'description': 'This dataset displays the geographic areas within which critical habitat for species at risk listed on Schedule 1 of the federal Species at Risk Act (SARA) occurs in British Columbia. However, not all of the area within these boundaries is necessarily critical habitat. To precisely define what constitutes critical habitat for a particular species it is essential that this geo-spatial information be considered in conjunction with complementary information in a species’ recovery document. Recovery documents are available from the Species at Risk (SAR) Public Registry (http://www.sararegistry.gc.ca). The recovery documents contain important information about the interpretation of the geo-spatial information, especially regarding the biological and environmental features (“biophysical attributes”) that complete the definition of a species’ critical habitat.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/critical-habitat-for-federally-listed-species-at-risk-posted-',
            **get_audit_fields()
        },
        {
            'data_source_id': 6,
            'name': 'Ecological Catalogue (formerly AquaCat)',
            'description': 'A compendium of reports that provide information about aquatic and terrestrial animals and plants, soils, surface water, groundwater and their accompanying data files and maps',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/ecological-catalogue-formerly-aquacat',
            **get_audit_fields()
        },
        {
            'data_source_id': 7,
            'name': 'Freshwater Atlas Stream Directions',
            'description': 'Points with rotations that indicate downstream flow direction. Can be displayed with arrow symbols to show flow direction. There is one point at the upstream end for each stream network feature',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-directions',
            **get_audit_fields()
        },
        {
            'data_source_id': 8,
            'name': 'Freshwater Atlas Watersheds',
            'description': 'All fundamental watershed polygons generated from watershed boundary lines, bank edges, delimiter edges, coastline edges, and administrative boundary edges',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-watersheds',
            **get_audit_fields()
        },
        {
            'data_source_id': 9,
            'name': 'Ground Water Aquifers',
            'description': 'Polygon features represent developed ground water aquifers in BC (that have been mapped). Most aquifer boundaries are delineated based on geology, hydrology and topographic information. Some aquifer boundaries stop at the border of BC mapsheet boundaries due to resource or data constraints at the time of mapping.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/ground-water-aquifers',
            **get_audit_fields()
        },
        {
            'data_source_id': 10,
            'name': 'Ground Water Wells',
            'description': 'Point features showing the location of groundwater wells in BC joined with attributes and information from the WELLS database. NOTE: Artesian wells are flowing wells at the time of drilling.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/ground-water-wells',
            **get_audit_fields()
        },
        {
            'data_source_id': 11,
            'name': 'Streams with Water Allocation Restrictions',
            'description': 'This dataset displays streams that have water allocation restrictions on them.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/streams-with-water-allocation-restrictions',
            **get_audit_fields()
        },
        {
            'data_source_id': 12,
            'name': 'Water Rights Licences - Public',
            'description': 'This is a province-wide SDE spatial layer displaying water rights licence data administrated under the Water Sustainability Act which includes data for both surface water and groundwater Points of Diversions. Point of Diversion types include Surface water Points of Diversion (PDs) Groundwater Points of Well Diversion (PWDs) as well as points of Groundwater diversion (PGs), non-well groundwater diversion points such as dugouts, ditches and quarries. This layer contains a record for each water licence on each POD type that exists in the province (each POD can have multiple licences). For each record, some basic information about the water licence is included.',
            'source_url': 'https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public',
            **get_audit_fields()
        },
        {
            'data_source_id': 13,
            'name': 'National Water Data Archive: HYDAT',
            'description': 'Hydrometric data are collected and compiled by Water Survey of Canada’s eight regional offices. The information is housed in two centrally-managed databases: HYDEX and HYDAT. HYDEX is the relational database that contains inventory information on the various streamflow, water level, and sediment stations (both active and discontinued) in Canada. This database contains information about the stations themselves such as; location, equipment, and type(s) of data collected. HYDAT is a relational database that contains the actual computed data for the stations listed in HYDEX. These data include: daily and monthly means of flow, water levels and sediment concentrations (for sediment sites). For some sites, peaks and extremes are also recorded.WSC now offers hydrometric data and station information in a single downloadable file, either in Microsoft Access Database format or in SQLite format, updated on a quarterly basis.',
            'source_url': 'http://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/',
            **get_audit_fields()
        }
    ])

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


def downgrade():
    pass
