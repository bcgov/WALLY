# coding: utf-8
from sqlalchemy import Integer, String, BigInteger,Column, DateTime, JSON, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Custom Base Class
class Base(object):
    __table_args__ = {'schema': 'data'}
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class DataMart(Base):
    time_relevance = Column(Integer, comment='how long before this data is invalid, measured in DAYS')
    last_updated = Column(DateTime, comment='last time data store was updated from source')

    data_source_id = Column(Integer, ForeignKey('data_source.id'), comment='data source information')
    data_source = relationship("DataSource")
    map_layer_id = Column(Integer, ForeignKey('layer.id'), comment='map layer information')
    map_layer = relationship("MapLayer")
    context_data_id = Column(Integer, ForeignKey('context_data.id'), comment='context data for display bar and reports')
    context_data = relationship("ContextData")


class DataSource(Base):
    __tablename__ = 'data_source'

    name = Column(Text, comment='data source detail name')
    description = Column(Text, comment='explanation behind data source and use case')
    source_url = Column(Text, comment='root source url of data')
    data_format_id = Column(Integer, ForeignKey('data_format.id'), comment='data format type')
    data_format = relationship("DataFormat")


class DataFormat(Base):
    __tablename__ = 'data_Format'
    name = Column(String, comment='source data format - options: wms, csv, excel, sqlite, text, json')


class MapLayer(Base):
    __tablename__ = 'map_layer'

    name = Column(String, comment='layer name we use for headers and descriptions')
    map_layer_type_id = Column(Integer, ForeignKey('map_layer_type.id'), comment='this layers source type')
    map_layer_type = relationship("MapLayerType")
    wms_id = Column(String, comment='wms layer id used in all async requests')
    wms_style = Column(String, comment='wms style identifier to view layer info with different visualizations')
    api_url = Column(String, comment='api endpoint to get base geojson information')


class MapLayerType(Base):
    __tablename__ = 'map_layer_type'
    name = Column(String, comment='type that defines where map layer data comes from - options: api, wms')


class ContextData(Base):
    __tablename__ = 'context_data'

    context = Column(JSON)

    title_column = Column(String, comment='we use this column value as a title in the client')
    title_label = Column(String, comment='label for title_column value')

    chart_labels = Column(JSON)
    chart_data = Column(JSON)

    link = Column(String)
    link_column = Column(String)

    image_url = Column(String)

    highlight_columns = Column(JSON, comment='columns to use from the data source, ignore other columns')
    highlight_descriptions = Column(JSON, comment='explanations of each highlight column and their value')
