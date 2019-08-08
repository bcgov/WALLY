# coding: utf-8
from sqlalchemy import Integer, String, BigInteger,Column, DateTime, JSON, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Custom Base Class
class Base(object):
    __table_args__ = {'schema': 'meta'}
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class DataMart(Base):
    __tablename__ = 'data_mart'

    name = Column(Text, comment='data mart name')
    description = Column(Text, comment='explanation behind data mart and use case')
    type = Column(Integer, ForeignKey('data_format.id'))
    source_url = Column(Text, comment='root source url of data')
    data_format_id = Column(Integer, ForeignKey('data_format.id'), comment='link to data format type')
    data_format = relationship("DataFormat")
    time_relevance = Column(Integer, comment='how long before this data is invalid, measured in DAYS')
    last_updated = Column(DateTime, comment='last time local data store was update from source')


# Layer Mixin
class Layer(object):
    name = Column(String, comment='layer name we use for headers and descriptions')
    titleColumn = Column(String, comment='column we use as a title identifier in the client')
    titleLabel = Column(String, comment='label we use to identify the titleColumn value')
    highlight_columns = Column(JSON, comment='columns to use from the data source, ignore other columns')
    highlight_descriptions = Column(JSON, comment='explanations of each highlight column and their value')


class WmsLayer(Base, Layer):
    __tablename__ = 'wms_layer'

    layerId = Column(String, comment='wms layer id used in all async requests')
    layerStyle = Column(String, comment='wms style identifier to view layer info with different visualizations')


class ApiLayer(Base, Layer):
    __tablename__ = 'api_layer'

    url = Column(String, comment='api endpoint to get base geojson information')


class LayerType(Base):
    __tablename__ = 'data_format'

    name = Column(String, comment='data format identifiers: csv, excel, wms')
