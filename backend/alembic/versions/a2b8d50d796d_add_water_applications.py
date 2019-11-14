"""add water applications

Revision ID: a2b8d50d796d
Revises: ab7b5daedfbd
Create Date: 2019-11-13 13:00:45.271757

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA

# revision identifiers, used by Alembic.
revision = 'a2b8d50d796d'
down_revision = '5be35dfffc00'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'water_rights_applications',

        sa.Column('WLS_WRA_SYSID', sa.Integer, comment='WLS WRA SYSID is a system generated unique identification number.'),
        sa.Column('APPLICATION_JOB_NUMBER', sa.String, primary_key=True, comment='APPLICATION JOB NUMBER is a unique identifier for a ground water licence application, e.g. 1003202.'),
        sa.Column('POD_NUMBER', sa.String, comment='POD NUMBER is the unique identifier for a Point of Diversion, e.g., PW189413. Each POD can have multiple licences associated with it.'),
        sa.Column('POD_SUBTYPE', sa.String, comment='POD SUBTYPE distinguishes the different POD types, i.e., POD (a surface water point of diversion), PWD (a point of well diversion that diverts groundwater), or PG (a point of groundwater diversion that diverts grounwater such as a dugout, ditch or quarry).'),
        sa.Column('POD_DIVERSION_TYPE', sa.String, comment='POD_DIVERSION_TYPE is the type of diversion for a point of groundwater diversion (PG subtype), i.e., Dugout, Ditch, Quarry. Since this only applies to PG subtypes, other subypes (POD or PWD) will be left blank (null value).'),
        sa.Column('FILE_NUMBER', sa.String, comment='FILE NUMBER is the water business file number, assigned during the application phase, e.g., 0321048. A file may hold one or more applications.'),
        sa.Column('APPLICATION_STATUS', sa.String, comment='APPLICATION STATUS is the status of the water rights application submitted by the applicant. There are two possible statuses: Active Application, if the application is undergoing adjudication; or Refused, if the application is complete but no licence was granted. When an application is granted as a licence it is removed from the applications dataset and added to the licences dataset.'),
        sa.Column('WELL_TAG_NUMBER', sa.Integer, comment='WELL TAG NUMBER is a unique well identifier for either registered or licensed wells, e.g., 12345.'),
        sa.Column('PURPOSE_USE_CODE', sa.String, comment='PURPOSE USE CODE is the use of water authorized by the licence, identified as a code, e.g., 02I.'),
        sa.Column('PURPOSE_USE', sa.String, comment='PURPOSE USE is the use of water authorized by the licence, e.g., Industrial.'),
        sa.Column('QTY_DIVERSION_MAX_RATE', sa.Float, comment='QTY DIVERSION MAX RATE is the maximum authorized diversion rate of water within a second, minute or day up to the total licensed quantity per year, e.g, 0.006, 2000'),
        sa.Column('QTY_UNITS_DIVERSION_MAX_RATE', sa.String, comment='QTY UNITS DIVERSION MAX RATE are the units of measurement for the maximum diversion rate of water authorized in the licence, e.g., m3/second, m3/minute, m3/day, m3/year.'),
        sa.Column('PRIMARY_APPLICANT_NAME', sa.String, comment='PRIMARY APPLICANT NAME is the primary contact for the application, co-applicants will be displayed as et al.'),
        sa.Column('ADDRESS_LINE_1', sa.String, comment='ADDRESS LINE 1 is the first line of the applicant\'s mailing address.'),
        sa.Column('ADDRESS_LINE_2', sa.String, comment='ADDRESS LINE 2 is the second line of the applicant\'s mailing address.'),
        sa.Column('ADDRESS_LINE_3', sa.String, comment='ADDRESS LINE 3 is the third line of the applicant\'s mailing address.'),
        sa.Column('ADDRESS_LINE_4', sa.String, comment='ADDRESS LINE 4 is the fourth line of the applicant\'s mailing address.'),
        sa.Column('COUNTRY', sa.String, comment='COUNTRY is the applicant\'s country.'),
        sa.Column('POSTAL_CODE', sa.String, comment='POSTAL CODE is the applicant\'s postal code.'),
        sa.Column('LATITUDE', sa.Float, comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.String, comment='	LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), of the location of the feature as measured from the prime meridian, e.g., -123.093544.'),
        sa.Column('DISTRICT_PRECINCT_NAME', sa.String, comment='DISTRICT PRECINCT NAME is a jurisdictional area within a Water District. It is a combination of District and Precinct codes and names, e.g., New Westminster / Coquitlam. Not all Water Districts contain Precincts.'),
        sa.Column('SHAPE', Geometry, comment='SHAPE is the column used to reference the spatial coordinates defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, comment='	OBJECTID is a column required by spatial layers that interact with ESRI ArcSDE. It is populated with unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE ANNO CAD DATA is a binary sa.column used by spatial tools '
                                                    'to store annotation, curve features and CAD data when using the '
                                                    'SDO GEOMETRY storage data type.')
    )

    op.execute('SET search_path TO metadata')

    op.execute("""
        INSERT INTO vector_catalogue (
            description, 
            vector_name,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES (
            'Water Rights Applications', 
            'water_rights_applications',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        );

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
            SELECT CURRVAL(pg_get_serial_sequence('vector_catalogue','vector_catalogue_id'),
            SELECT CURRVAL(pg_get_serial_sequence('data_source','data_source_id'),
            WATER_ADMINISTRATION,
            'iit-water.2svbut5f',
            'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'
        );
    """)

    op.execute('SET search_path TO public')


def downgrade():
    pass
