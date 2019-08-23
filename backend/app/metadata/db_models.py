# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, JSON, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


# Custom Base Class
class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_user = Column(String(100), comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


Base = declarative_base(cls=Base)


# Data Storage Tables
class DataStore(Base):
    __tablename__ = 'data_store'

    data_store_id = Column(Integer, primary_key=True)

    name = Column(String, comment='data store detail name', index=True)
    description = Column(String, comment='explanation behind data store and use case')
    time_relevance = Column(Integer, comment='how long before this data store becomes stale, measured in DAYS')
    last_updated = Column(DateTime, comment='last time data store was updated from sources')

    data_sources = relationship("DataSource")


class DataFormatCode(Base):
    __tablename__ = 'data_format_code'
    data_format_code = Column(String, primary_key=True, comment='source data format, options: '
                                                                'wms, csv, excel, sqlite, text, json')
    description = Column(String, comment='code type description')


class DataSource(Base):
    __tablename__ = 'data_source'

    data_source_id = Column(Integer, primary_key=True)

    name = Column(String, comment='data source detail name', index=True)
    description = Column(String, comment='explanation behind data source and use case')
    source_url = Column(String, comment='root source url of data')

    data_format_code = Column(String, ForeignKey('metadata.data_format_code.data_format_code'),
                              comment='format type of the source information')
    data_format = relationship('DataFormatCode')

    data_store_id = Column(Integer, ForeignKey('metadata.data_store.data_store_id'), comment='related data store where this '
                                                                                  'sources data is held after ETL')
    data_store = relationship("DataStore")


class ApiCatalogue(Base):
    __tablename__ = 'api_catalogue'
    api_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='api endpoint description')
    url = Column(String, comment='an internal api endpoint that serves all data points for a display layer')


class WmsCatalogue(Base):
    __tablename__ = 'wms_catalogue'
    wms_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='wms layer description')
    wms_name = Column(String, comment='identifying layer name with the data bc wms server')
    wms_style = Column(String, comment='style key to display data in different visualizations for wms layer')


class ComponentTypeCode(Base):
    __tablename__ = 'component_type_code'
    component_type_code = Column(String, primary_key=True, comment='components have many different types, which '
                                                                   'determines what business logic to use when '
                                                                   'constructing the component.')
    description = Column(String, comment='explanation of component type and use case')


class ChartProperty(Base):
    __tablename__ = 'chart_property'
    chart_property_id = Column(Integer, primary_key=True)

    chart_property = Column(JSON, comment='this holds the chart js json schema to use in the client and reporting')
    labels_key = Column(String, comment='the key used to generate the labels array')
    data_keys = Column(ARRAY(String), comment='the keys used to generate the raw data for chart datasets')


class LinkProperty(Base):
    __tablename__ = 'link_property'
    link_property_id = Column(Integer, primary_key=True)

    link_pattern = Column(String, comment='url pattern to source document or webpage')
    link_pattern_keys = Column(ARRAY(String), comment='keys to plug into link pattern')


class ImageProperty(Base):
    __tablename__ = 'image_property'
    image_property_id = Column(Integer, primary_key=True)

    width = Column(Integer, comment='x size of image')
    height = Column(Integer, comment='y size of image')

    url = Column(String, comment='source url to image source')


class FormulaProperty(Base):
    __tablename__ = 'formula_property'
    formula_property_id = Column(Integer, primary_key=True)

    formula_property = Column(JSON, comment='formula layout for calculation')


class DisplayCatalogue(Base):
    __tablename__ = 'display_catalogue'
    display_catalogue_id = Column(Integer, primary_key=True)

    display_data_name = Column(String(200), unique=True,
                               comment='this is the main business key used throughout the application to '
                                       'identify data layers and connect data to templates.')
    title_column = Column(String, comment='we use this column value as a list item title in the client')
    title_label = Column(String, comment='label for title_column value')
    highlight_columns = Column(ARRAY(String), comment='the key columns that have business value to the end user. '
                                              'We primarily will only show these columns in the client and report')

    api_catalogue_id = Column(String, ForeignKey('metadata.api_catalogue.api_catalogue_id'),
                              comment='references api catalogue item')
    api_catalogue = relationship("ApiCatalogue")

    wms_catalogue_id = Column(String, ForeignKey('metadata.wms_catalogue.wms_catalogue_id'),
                              comment='references wms catalogue item')
    wms_catalogue = relationship("WmsCatalogue")

    display_components = relationship("DisplayComponent", secondary="display_templates")


class DisplayComponent(Base):
    __tablename__ = 'display_component'
    display_component_id = Column(Integer, primary_key=True)

    component_type_code = Column(String, ForeignKey('metadata.component_type_code.component_type_code'))
    component_type_code_rel = relationship('ComponentTypeCode')
    component_title = Column(String, comment='title to be used for headers and labels for components')
    display_order = Column(Integer, comment='determines which components are shown first to last in 100s')

    display_catalogues = relationship("DisplayCatalogue", secondary="display_templates")

    link_property_id = Column(Integer, ForeignKey('metadata.link_property.link_property_id'),
                              comment='reference to link component')
    link_property = relationship("LinkProperty")

    chart_property_id = Column(Integer, ForeignKey('metadata.chart_property.chart_property_id'),
                               comment='reference to chart component')
    chart_property = relationship("ChartProperty")

    image_property_id = Column(Integer, ForeignKey('metadata.image_property.image_property_id'),
                               comment='reference to image component')
    image_property = relationship("ImageProperty")

    formula_property_id = Column(Integer, ForeignKey('metadata.formula_property.formula_property_id'),
                                 comment='reference to formula component')
    formula_property = relationship("FormulaProperty")


class DisplayTemplate(Base):
    __tablename__ = 'display_template'
    display_template_id = Column(Integer, primary_key=True)
    display_template_order = Column(Integer, comment='determines which templates are shown first to last in 100s')

    display_component_id = Column(Integer, ForeignKey('metadata.display_component.display_component_id'))
    display_catalogue_id = Column(Integer, ForeignKey('metadata.display_catalogue.display_catalogue_id'))

    display_component = relationship("DisplayComponent", backref=backref("display_templates"))
    display_catalogue = relationship("DisplayCatalogue", backref=backref("display_templates"))




