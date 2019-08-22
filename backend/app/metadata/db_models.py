# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, JSON, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Custom Base Class
class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_user = Column(Text, comment='The user who created this record in the database.')
    create_date = Column(DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(Text, comment='The user who last updated this record in the database.')
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

    id = Column(Integer, primary_key=True)

    name = Column(Text, comment='data store detail name')
    description = Column(Text, comment='explanation behind data store and use case')
    time_relevance = Column(Integer, comment='how long before this data store becomes stale, measured in DAYS')
    last_updated = Column(DateTime, comment='last time data store was updated from sources')

    data_sources = relationship("DataSource")


class DataSource(Base):
    __tablename__ = 'data_source'

    id = Column(Integer, primary_key=True)

    name = Column(Text, comment='data source detail name')
    description = Column(Text, comment='explanation behind data source and use case')
    source_url = Column(Text, comment='root source url of data')

    data_source_code = Column(String, ForeignKey('metadata.data_source_format_code.data_source_format_code'))
    # data_source_code = relationship("DataSourceCode")

    data_store_id = Column(Integer, ForeignKey('metadata.data_store.id'), comment='related data store where this '
                                                                                  'sources data is held after ETL')
    data_store = relationship("DataStore")


class DataSourceFormatCode(Base):
    __tablename__ = 'data_source_format_code'
    data_source_format_code = Column(String, primary_key=True, comment='source data format, '
                                                                'options: wms, csv, excel, sqlite, text, json')
    description = Column(String)


# Display Catalogue Tables
class DisplayCatalogue(Base):
    __tablename__ = 'data_catalogue'
    display_catalogue_id = Column(Integer, primary_key=True)

    display_data_name = Column(String, unique=True)

    api_catalogue_id = Column(String, ForeignKey('metadata.api_catalogue.id'), comment='')
    api_catalogue = relationship("ApiCatalogue")

    wms_catalogue_id = Column(String, ForeignKey('metadata.wms_catalogue.id'), comment='')
    wms_catalogue = relationship("WmsCatalogue")


class ApiCatalogue(Base):
    __tablename__ = 'api_catalogue'
    api_catalogue_id = Column(Integer, primary_key=True)
    url = Column(String, comment='')


class WmsCatalogue(Base):
    __tablename__ = 'wms_catalogue'
    wms_catalogue_id = Column(Integer, primary_key=True)
    wms_name = Column(String, comment='')
    wms_style = Column(String, comment='')


# Display Template Tables
class DisplayTemplate(Base):
    __tablename__ = 'display_template'
    display_template_id = Column(Integer, primary_key=True)

    display_data_id = Column(Integer)


class DisplayComponent(Base):
    __tablename__ = 'display_component'
    display_catalogue_id = Column(Integer, primary_key=True)


class ChartProperty(Base):
    __tablename__ = 'chart_property'
    chart_property_id = Column(Integer, primary_key=True)


class UrlProperty(Base):
    __tablename__ = 'url_property'
    url_property_id = Column(Integer, primary_key=True)


class FormulaProperty(Base):
    __tablename__ = 'formula_property'
    formula_property_id = Column(Integer, primary_key=True)


class ComponentTypeCode(Base):
    __tablename__ = 'component_type_code'
    component_type_code = Column(String, primary_key=True, comment='components have many different types, which '
                                                                   'determines what business logic to use when '
                                                                   'constructing the component.')
    description = Column(String)





class MapLayer(Base):
    __tablename__ = 'map_layer'

    layer_id = Column(String, primary_key=True, comment='id used internally to map contexts')
    layer_name = Column(String, comment='name used to represent layer to users')

    wms_name = Column(String, comment='wms layer id used in all async requests')
    wms_style = Column(String, comment='wms style identifier to view layer info with different visualizations')
    api_url = Column(String, comment='api endpoint to get base geojson information')

    map_layer_type_id = Column(String, ForeignKey('metadata.map_layer_type.type'), comment='this layers source type')
    map_layer_type = relationship("MapLayerType")

    data_mart_id = Column(Integer, ForeignKey('metadata.data_mart.id'), comment='parent data mart')
    data_mart = relationship("DataMart")


class MapLayerType(Base):
    __tablename__ = 'map_layer_type'
    type = Column(String, primary_key=True, comment='type that defines where map layer data comes from '
                                                    '- options: api, wms')


class ContextData(Base):
    __tablename__ = 'context_data'

    context_id = Column(String, primary_key=True, comment='identifies which MapLayer(s) this fixtures belongs to by '
                                                          'layer_name, a ContextData can be the visualization of two '
                                                          'merged MapLayers. ex: MapLayer(layer_id=GWELLS_) '
                                                          'MapLayer(layer_id=HYDAT_) context_name = GWELLS_HYDAT_')

    context = Column(JSON, comment='holds the fixtures schema for this singular or combination of layer(s)')

    title_column = Column(String, comment='we use this column value as a title in the client')
    title_label = Column(String, comment='label for title_column value')

    chart_label_columns = Column(ARRAY(String), comment='column value that represents chart(s) x axis labels')
    chart_data_columns = Column(ARRAY(String), comment='column value that represents chart(s) x axis values')

    link_pattern = Column(String, comment='link pattern to source data')
    link_columns = Column(ARRAY(String), comment='id value(s) to use with link column to reach source data')

    image_url = Column(String, comment='image representing this context')

    highlight_columns = Column(JSON, comment='columns to use from the data source, ignore other columns')
    highlight_descriptions = Column(JSON, comment='explanations of each highlight column and their value')

    data_mart_id = Column(Integer, ForeignKey('metadata.data_mart.id'), comment='parent data mart')
    data_mart = relationship("DataMart")

