# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class WaterAllocationRestrictions(BaseLayerTable):
    __tablename__ = 'water_allocation_restrictions'

    LINEAR_FEATURE_ID = Column(Integer, comment='LINEAR FEATURE ID is a primary Key to link to stream segments in '
                                                'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP as a one to one join. This '
                                                'is maintained by business users. E.g., 831792750')
    RESTRICTION_ID_LIST = Column(String, comment='RESTRICTION ID LIST is a list of one or more restriction IDs of '
                                                 'stream restriction points downstream from the stream segment. The '
                                                 'RESTRICTION_IDs correspond with RESTRICTION_IDs in '
                                                 'WHSE_WATER_MANAGEMENT.WLS_WATER_RESTRICTION_LOC_SVW. E.g., RS34144')
    PRIMARY_RESTRICTION_CODE = Column(String, comment='PRIMARY RESTRICTION CODE indicates the type of restriction '
                                                      'point downstream from the stream segment. E.g., FR - '
                                                      'Fully Recorded; FR_EXC - Fully Recorded Except; PWS - '
                                                      'Possible Water Shortage; RNW - Refused No Water; OR - '
                                                      'Office Reserve; UNSPECIFIED - type of '
                                                      'restriction not specified.')
    SECONDARY_RESTRICTION_CODES = Column(String, comment='SECONDARY RESTRICTION CODES is a list of additional '
                                                         'types of water restrictions downstream from the stream'
                                                         ' segment. E.g., FR - Fully Recorded; FR_EXC - '
                                                         'Fully Recorded Except; PWS - Possible Water Shortage; '
                                                         'RNW - Refused No Water; OR - Office Reserve; '
                                                         'UNSPECIFIED - type of restriction not specified.')
    FWA_WATERSHED_CODE = Column(String, comment='FWA WATERSHED CODE is a 143 character code derived using a '
                                                'hierarchy coding scheme. Approximately identifies where a '
                                                'particular stream is located within the province.')
    WATERSHED_GROUP_CODE = Column(String, comment='WATERSHED GROUP CODE is the watershed group code '
                                                  'associated with the polygon.')
    GNIS_NAME = Column(String, comment='GNIS NAME is the BCGNIS (BC Geographical Names Information System) '
                                       'name associated with the GNIS feature id (an English name was used '
                                       'where available, otherwise another language was selected).')
    STREAM_ORDER = Column(Float, comment='STREAM ORDER is the calculated modified Strahler order.')
    STREAM_MAGNITUDE = Column(Float, comment='STREAM MAGNITUDE is the calculated magnitude.')
    FEATURE_CODE = Column(String, comment='FEATURE CODE contains a value based on the Canadian Council of'
                                          ' Surveys and Mappings (CCSM) system for classification of '
                                          'geographic features.')
    GEOMETRY = Column(Geometry(srid=4326), comment='GEOMETRY is the column used to reference the spatial coordinates '
                                        'defining the feature.')
    OBJECTID = Column(Integer, primary_key=True, autoincrement=False, comment='OBJECTID is a required attribute of feature classes and '
                                                         'object classes in a geodatabase.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to '
                              'store annotation, curve features and CAD data when using the '
                              'SDO_GEOMETRY storage data type.')
    FEATURE_LENGTH_M = Column(Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter '
                                             'of a geometry in meters')
