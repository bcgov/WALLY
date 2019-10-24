# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, Float
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class BcWildfireActiveWeatherStations(BaseLayerTable):
    __tablename__ = 'bc_wildfire_active_weather_stations'

    WEATHER_STATIONS_ID	= Column(Integer, primary_key=True, autoincrement=False, comment='WEATHER STATION ID is a system generated '
                                                                       'unique identifier number.')
    STATION_CODE = Column(Integer, comment='STATION_CODE is the internal unique number assigned to this weather '
                                           'station, e.g., 67 .')
    STATION_NAME = Column(String, comment='STATION_NAME is a derived name of a weather station based on geographic '
                                          'significance, e.g. HAIG CAMP.')
    STATION_ACRONYM = Column(String, comment='STATION_ACRONYM is a 4 character airport code for the closest airport to '
                                             'the station. This is used for weather forecasting software. This is not '
                                             'populated for all weather stations. The leading "C" may be dropped from '
                                             'most of the values, e.g.,CYYJ, YVR.')
    LATITUDE = Column(Float, comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the '
                                     'location of the feature as measured from the equator, e.g., 55.323653.')
    LONGITUDE = Column(Float, comment='LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), '
                                      'of the location of the feature as measured from the prime meridian, '
                                      'e.g., -123.093544.')
    ELEVATION = Column(Float, comment='ELEVATION is the elevation of the weather station in metres above sea level as '
                                      'derived from the TRIM DEM.')
    INSTALL_DATE = Column(DateTime, comment='INSTALL_DATE is the date when the weather station was '
                                            'physically installed.')
    SHAPE = Column(Geometry(srid=4326), comment='SHAPE is the column used to reference the spatial coordinates '
                   'defining the feature.')
    OBJECTID = Column(Integer, comment='OBJECTID is a column required by spatial layers that interact with '
                                       'ESRI ArcSDE. It is populated with unique values automatically by SDE.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                              'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                              'storage data type.')
