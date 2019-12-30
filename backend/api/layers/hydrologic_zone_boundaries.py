# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class HydrologicZoneBoundaries(BaseLayerTable):
    __tablename__ = 'hydrologic_zone_boundaries'
    
    HYDROLOGICZONE_SP_ID = Column(Integer, primary_key=True, autoincrement=False, comment='Primary unique numeric identifier for a Hydrological Zone Polygon.')
    FEATURE_CODE = Column(String, comment='A standard numeric code to identify the type of feature represented by the spatial data.')
    HYDROLOGICZONE_NO = Column(Integer, comment='A numeric identifier assigned to a zone that represents an area of homogenous hydrologic and geomorphological characteristics')
    HYDROLOGICZONE_NAME = Column(String, comment='A descriptive name, assigned to a zone having a numeric identifier and that represents an area of homogenous hydrologic and geomorphological characteristics.')
    FEATURE_AREA_SQM = Column(Float, comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional polygon in square meters')
    FEATURE_LENGTH_M =	Column(Integer, comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a geometry in meters')
    GEOMETRY = Column(Geometry(srid=4326), index=True, comment='GEOMETRY is the column used to reference the spatial coordinates defining the feature.')
    OBJECTID = Column(Float, comment='')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools'
                              'to store annotation, curve features and CAD data when using'
                              'the SDO_GEOMETRY storage data type.')