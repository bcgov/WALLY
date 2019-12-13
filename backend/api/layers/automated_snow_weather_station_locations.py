# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class AutomatedSnowWeatherStationLocations(BaseLayerTable):
    __tablename__ = 'automated_snow_weather_station_locations'

    SNOW_ASWS_STN_ID = Column(Integer, primary_key=True, autoincrement=False, comment='SNOW_ASWS_STN_ID is a system generated unique '
                                                                 'identification number.')
    LOCATION_ID = Column(String, comment='LOCATION_ID is the unique identifier of the snow weather station, '
                                         'e.g. 1C41P.')
    LOCATION_NAME = Column(String, comment='LOCATION_NAME is the name of the snow weather station, e.g. Yanks Peak.')
    ELEVATION = Column(Float, comment='ELEVATION the elevation of the snow weather station in metres, e.g. 1670.')
    STATUS = Column(String, comment='STATUS is the operational status of the snow station, e.g. Active, Inactive.')
    LATITUDE = Column(Float, comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the '
                                     'location of the feature as measured from the equator, e.g., 55.323653.')
    LONGITUDE = Column(Float, comment='	LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), of '
                                      'the location of the feature as measured from the prime meridian, '
                                      'e.g., -123.093544.')
    SHAPE = Column(Geometry(geometry_type='POINT', srid=4326), comment='SHAPE is the column used to reference the spatial coordinates defining '
                   'the feature.')
    OBJECTID = Column(Integer, comment='OBJECTID is a column required by spatial layers that '
                                       'interact with ESRI ArcSDE. It is populated with unique '
                                       'values automatically by SDE.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                              'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                              'storage data type.')
