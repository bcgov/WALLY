# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class FreshwaterAtlasWatersheds(BaseLayerTable):
    __tablename__ = 'freshwater_atlas_watersheds'

    WATERSHED_FEATURE_ID = Column(
        Integer, primary_key=True, autoincrement=False,
        comment='A unique identifier for each watershed '
        'in the layer.')
    WATERSHED_GROUP_ID = Column(Integer, comment='An automatically generate id that uniquely identifies '
                                                 'the watershed group feature.')
    WATERSHED_TYPE = Column(String, comment='The type of watershed. This has yet to be determined for FWA '
                                            'version 2.0.0, but possible values may include: R - real watershed, '
                                            'F - face unit watershed, W - waterbody watershed, etc.')
    GNIS_ID_1 = Column(Integer, comment='The first BCGNIS (BC Geographical Names Information System) feature id '
                                        'associated with the watershed key of the principal watershed.')
    GNIS_NAME_1 = Column(String, comment='The first BCGNIS (BC Geographical Names Information System) name '
                                         'associated with the watershed key of the principal watershed.')
    GNIS_ID_2 = Column(Integer, comment='The second BCGNIS (BC Geographical Names Information System) feature '
                                        'id associated with the watershed key of the principal watershed.')
    GNIS_NAME_2 = Column(String, comment='The second BCGNIS (BC Geographical Names Information System) name '
                                         'associated with the watershed key of the principal watershed.')
    GNIS_ID_3 = Column(Integer, comment='The third BCGNIS (BC Geographical Names Information System) feature '
                                        'id associated with the watershed key of the principal watershed.')
    GNIS_NAME_3 = Column(String, comment='The third BCGNIS (BC Geographical Names Information System) name '
                                         'associated with the watershed key of the principal watershed.')
    WATERBODY_ID = Column(Integer, comment='If the principal watershed is made up of a lake or river, this '
                                           'field will contain the waterbody id associated with that waterbody, '
                                           'otherwise it will be null.')
    WATERBODY_KEY = Column(Integer, comment='If the principal watershed is made up of a lake or river, this '
                                            'field will contain the waterbody key associated with that waterbody, '
                                            'otherwise it will be null.')
    WATERSHED_KEY = Column(Integer, comment='The watershed key associated with the watershed polygon '
                                            '(and watershed code).')
    FWA_WATERSHED_CODE = Column(String, comment='The 143 character watershed code associated with '
                                                'the watershed polygon.')
    LOCAL_WATERSHED_CODE = Column(String, comment='A 143 character code similar to the fwa watershed code '
                                                  'that further subdivides remnant polygons to provide an '
                                                  'approximate location along the mainstem.')
    WATERSHED_GROUP_CODE = Column(String, comment='The watershed group code associated with the polygon.')
    LEFT_RIGHT_TRIBUTARY = Column(String, comment='A value attributed via the watershed code to all watersheds '
                                                  'indicating on what side of the watershed they drain into.')
    WATERSHED_ORDER = Column(Integer, comment='The maximum order of the watershed key associated with the '
                                              'principal watershed polygon.')
    WATERSHED_MAGNITUDE = Column(Integer, comment='The maximum magnitude of the watershed key associated with '
                                                  'the principal watershed.')
    LOCAL_WATERSHED_ORDER = Column(Integer, comment='The order associated with the local watershed code.')
    LOCAL_WATERSHED_MAGNITUDE = Column(Integer, comment='The magnitude associated with the local watershed code.')
    AREA_HA = Column(Float, comment='Area of the watershed, in hectares.')
    RIVER_AREA = Column(Float, comment='Area of double line rivers within the watershed, in hectares.')
    LAKE_AREA = Column(Float, comment='Area of lakes within the watershed, in hectares.')
    WETLAND_AREA = Column(Float, comment='Area of wetland features within the watershed, in hectares.')
    MANMADE_AREA = Column(Float, comment='Area of manmade features within the watershed, in hectares.')
    GLACIER_AREA = Column(Float, comment='Area of glacier features within the watershed, in hectares.')
    AVERAGE_ELEVATION = Column(Float, comment='The average elevation of the watershed, in meters.')
    AVERAGE_SLOPE = Column(Float, comment='The average slope of the watershed.')
    ASPECT_NORTH = Column(Float, comment='The percentage of the watershed that has an aspect within '
                                         '45 degrees of north, ie. an aspect between 315 and 45 degrees.')
    ASPECT_SOUTH = Column(Float, comment='The percentage of the watershed that has an aspect within '
                                         '45 degrees of south, ie. an aspect between 135 and 225 degrees.')
    ASPECT_WEST = Column(Float, comment='The percentage of the watershed that has an aspect within '
                                        '45 degrees of west, ie. an aspect between 225 and 315 degrees.')
    ASPECT_EAST = Column(Float, comment='The percentage of the watershed that has an aspect within '
                                        '45 degrees of east, ie. an aspect between 45 and 135 degrees.')
    ASPECT_FLAT = Column(Float, comment='The percentage of the watershed with no discernable aspect, '
                                        'ie. the flat land.')
    FEATURE_CODE = Column(String, comment='FEATURE CODE contains a value based on the Canadian Council '
                                          'of Surveys and Mappings (CCSM) system for classification of '
                                          'geographic features.')
    GEOMETRY = Column(
        Geometry(geometry_type='MULTIPOLYGON', srid=4326), comment='')
    OBJECTID = Column(Integer, comment='')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='')
    FEATURE_AREA_SQM = Column(Float, comment='FEATURE_AREA_SQM is the system calculated area of a '
                                             'two-dimensional polygon in square meters')
    FEATURE_LENGTH_M = Column(Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter '
                                             'of a geometry in meters')
