# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, BLOB, Float
from app.db.base_class import BaseTable
from geoalchemy2 import Geometry


class FreshwaterAtlasStreamDirections(BaseTable):
    __tablename__ = 'freshwater_atlas_stream_directions'

    STREAM_DIRECTION_ID = Column(Integer, comment='STREAM DIRECTION ID is a surrogate key for the'
                                                  ' STREAM DIRECTION SP record. i.e. 1')
    LINEAR_FEATURE_ID = Column(Integer, comment='The LINEAR FEATURE ID is a unique numeric identifier used to '
                                                'identify the STREAM NETWORKS SP spatial line that this '
                                                'STREAM DIRECTION provides direction for. i.e 7209923')
    DOWNSTREAM_DIRECTION = Column(Float, comment='DOWNSTREAM DIRECTION is the direction in decimal degrees, '
                                                 'counterclockwise from east, where east is 0, north is 90, west '
                                                 'is 180, and south is 270, e.g., 179.227053, which indicates '
                                                 'almost due west.')
    FEATURE_CODE = Column(String, comment='FEATURE CODE contains a value based on the Canadian Council of Surveys'
                                          ' and Mappings (CCSM) system for classification of geographic features.')
    GEOMETRY = Column(Geometry, comment='GEOMETRY is the column used to reference the spatial coordinates '
                                        'defining the feature.')
    OBJECTID = Column(Integer, primary_key=True, comment='OBJECTID is a required attribute of feature classes and '
                                                         'object classes in a geodatabase.')
    SE_ANNO_CAD_DATA = Column(BLOB, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools '
                                            'to store annotation, curve features and CAD data when using '
                                            'the SDO_GEOMETRY storage data type.')
