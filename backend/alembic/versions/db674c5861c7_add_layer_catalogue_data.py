"""add layer catalogue data

Revision ID: db674c5861c7
Revises: fc2537bad3fa
Create Date: 2019-09-11 15:34:58.155423

"""
import logging
import os
import json
import datetime
from alembic import op
from sqlalchemy import orm
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, ARRAY, TEXT
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'db674c5861c7'
down_revision = 'fc2537bad3fa'
branch_labels = None
depends_on = None


class DataFormatCode(Base):
    __tablename__ = 'data_format_code'
    data_format_code = Column(String, primary_key=True, comment='source data format, options: '
                                                                'wms, csv, excel, sqlite, text, json')
    description = Column(String, comment='code type description')
    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


class ComponentTypeCode(Base):
    __tablename__ = 'component_type_code'
    component_type_code = Column(String, primary_key=True,
                                 comment='components have many different types, which determines what business '
                                         'logic to use when constructing the component.')
    description = Column(String, comment='explanation of component type and use case')
    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


class ApiCatalogue(Base):
    __tablename__ = 'api_catalogue'
    api_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='api endpoint description')
    url = Column(String, comment='an internal api endpoint that serves all data points for a display layer')
    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


class WmsCatalogue(Base):
    __tablename__ = 'wms_catalogue'
    wms_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='wms layer description')
    wms_name = Column(String, comment='identifying layer name with the data bc wms server')
    wms_style = Column(String, comment='style key to display data in different visualizations for wms layer')
    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


class VectorCatalogue(Base):
    __tablename__ = 'vector_catalogue'
    vector_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='vector layer description')
    vector_name = Column(String, comment='identifying vector layer name')
    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


class DisplayCatalogue(Base):
    __tablename__ = 'display_catalogue'
    display_catalogue_id = Column(Integer, primary_key=True)

    display_name = Column(String, comment='this is the public name of the display layer')
    display_data_name = Column(String(200), unique=True,
                               comment='this is the main business key used throughout the application to '
                                       'identify data layers and connect data to templates.')
    label = Column(String, comment='label for label_column value')
    label_column = Column(String, comment='we use this column value as a list item label in the client')
    highlight_columns = Column(ARRAY(TEXT), comment='the key columns that have business value to the end user. '
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
