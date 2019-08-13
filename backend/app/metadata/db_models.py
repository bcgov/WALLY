# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Custom Base Class
class Base(object):
    __table_args__ = {'schema': 'metadata'}
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class DataMart(Base):
    __tablename__ = 'data_mart'

    map_layers = relationship("MapLayer")
    data_stores = relationship("DataStore")
    data_sources = relationship("DataSource")
    context_data = relationship("ContextData")


class DataStore(Base):
    __tablename__ = 'data_store'

    name = Column(Text, comment='data store detail name')
    description = Column(Text, comment='explanation behind data store and use case')
    time_relevance = Column(Integer, comment='how long before this data store becomes stale, measured in DAYS')
    last_updated = Column(DateTime, comment='last time data store was updated from sources')
    data_mart_id = Column(Integer, ForeignKey('data_mart.id'), comment='parent data mart')
    data_mart = relationship("DataMart")

    data_sources = relationship("DataSource")


class DataFormat(Base):
    __tablename__ = 'data_format'

    name = Column(String, comment='source data format - options: wms, csv, excel, sqlite, text, json')


class DataSource(Base):
    __tablename__ = 'data_source'

    name = Column(Text, comment='data source detail name')
    description = Column(Text, comment='explanation behind data source and use case')
    source_url = Column(Text, comment='root source url of data')

    data_format_id = Column(Integer, ForeignKey('data_format.id'), comment='data format type')
    data_format = relationship("DataFormat")

    data_store_id = Column(Integer, ForeignKey('data_store.id'), comment='related data store')
    data_store = relationship("DataStore")

    data_mart_id = Column(Integer, ForeignKey('data_mart.id'), comment='parent data mart')
    data_mart = relationship("DataMart")


class MapLayer(Base):
    __tablename__ = 'map_layer'

    layer_name = Column(String, comment='wms layer id used in all async requests', unique=True)

    wms_name = Column(String, comment='wms layer id used in all async requests')
    wms_style = Column(String, comment='wms style identifier to view layer info with different visualizations')
    api_url = Column(String, comment='api endpoint to get base geojson information')

    map_layer_type_id = Column(Integer, ForeignKey('map_layer_type.id'), comment='this layers source type')
    map_layer_type = relationship("MapLayerType")

    data_mart_id = Column(Integer, ForeignKey('data_mart.id'), comment='parent data mart')
    data_mart = relationship("DataMart")


class MapLayerType(Base):
    __tablename__ = 'map_layer_type'
    name = Column(String, comment='type that defines where map layer data comes from - options: api, wms')


class ContextData(Base):
    __tablename__ = 'context_data'

    context_name = Column(String, comment='identifies which MapLayer(s) this fixtures belongs to by layer_name, '
                                          'a ContextData can be the visualization of two merged MapLayers. '
                                          'ex: MapLayer(layer_name=gwells) MapLayer(layer_name=hydat) '
                                          'context_name = gwellshydat')

    context = Column(JSON, comment='holds the fixtures schema for this singular or combination of layer(s)')

    title_column = Column(String, comment='we use this column value as a title in the client')
    title_label = Column(String, comment='label for title_column value')

    chart_labels = Column(JSON, comment='array(s) of chart axis labels')
    chart_data = Column(JSON, comment='columns and format of data to use for chart(s)')

    link = Column(String, comment='link pattern to source data')
    link_column = Column(String, comment='id value(s) to use with link column to reach source data')

    image_url = Column(String, comment='image representing this context')

    highlight_columns = Column(JSON, comment='columns to use from the data source, ignore other columns')
    highlight_descriptions = Column(JSON, comment='explanations of each highlight column and their value')

    data_mart_id = Column(Integer, ForeignKey('data_mart.id'), comment='parent data mart')
    data_mart = relationship("DataMart")

