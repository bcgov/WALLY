# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class FreshwaterAtlasWatersheds(BaseLayerTable):
    __tablename__ = 'fwa_watersheds_poly'

    WATERSHED_FEATURE_ID = Column('watershed_feature_id', Integer, primary_key=True, autoincrement=False, comment='A unique identifier for each watershed '
                                  'in the layer.')
    WATERSHED_GROUP_ID = Column('watershed_group_id', Integer, comment='An automatically generate id that uniquely identifies '
                                'the watershed group feature.')
    WATERSHED_TYPE = Column('watershed_type', String, comment='The type of watershed. This has yet to be determined for FWA '
                            'version 2.0.0, but possible values may include: R - real watershed, '
                            'F - face unit watershed, W - waterbody watershed, etc.')
    GNIS_ID_1 = Column('gnis_id_1', Integer, comment='The first BCGNIS (BC Geographical Names Information System) feature id '
                       'associated with the watershed key of the principal watershed.')
    GNIS_NAME_1 = Column('gnis_name_1', String, comment='The first BCGNIS (BC Geographical Names Information System) name '
                         'associated with the watershed key of the principal watershed.')
    GNIS_ID_2 = Column('gnis_id_2', Integer, comment='The second BCGNIS (BC Geographical Names Information System) feature '
                       'id associated with the watershed key of the principal watershed.')
    GNIS_NAME_2 = Column('gnis_name_2', String, comment='The second BCGNIS (BC Geographical Names Information System) name '
                         'associated with the watershed key of the principal watershed.')
    GNIS_ID_3 = Column('gnis_id_3', Integer, comment='The third BCGNIS (BC Geographical Names Information System) feature '
                       'id associated with the watershed key of the principal watershed.')
    GNIS_NAME_3 = Column('gnis_name_3', String, comment='The third BCGNIS (BC Geographical Names Information System) name '
                         'associated with the watershed key of the principal watershed.')
    WATERBODY_ID = Column('waterbody_id', Integer, comment='If the principal watershed is made up of a lake or river, this '
                          'field will contain the waterbody id associated with that waterbody, '
                          'otherwise it will be null.')
    WATERBODY_KEY = Column('waterbody_key', Integer, comment='If the principal watershed is made up of a lake or river, this '
                           'field will contain the waterbody key associated with that waterbody, '
                           'otherwise it will be null.')
    WATERSHED_KEY = Column('watershed_key', Integer, comment='The watershed key associated with the watershed polygon '
                           '(and watershed code).')
    FWA_WATERSHED_CODE = Column('fwa_watershed_code', String, comment='The 143 character watershed code associated with '
                                'the watershed polygon.')
    LOCAL_WATERSHED_CODE = Column('local_watershed_code', String, comment='A 143 character code similar to the fwa watershed code '
                                  'that further subdivides remnant polygons to provide an '
                                  'approximate location along the mainstem.')
    WATERSHED_GROUP_CODE = Column('watershed_group_code', String,
                                  comment='The watershed group code associated with the polygon.')
    LEFT_RIGHT_TRIBUTARY = Column('left_right_tributary', String, comment='A value attributed via the watershed code to all watersheds '
                                  'indicating on what side of the watershed they drain into.')
    WATERSHED_ORDER = Column('watershed_order', Integer, comment='The maximum order of the watershed key associated with the '
                             'principal watershed polygon.')
    WATERSHED_MAGNITUDE = Column('watershed_magnitude', Integer, comment='The maximum magnitude of the watershed key associated with '
                                 'the principal watershed.')
    LOCAL_WATERSHED_ORDER = Column('local_watershed_order', Integer,
                                   comment='The order associated with the local watershed code.')
    LOCAL_WATERSHED_MAGNITUDE = Column(
        'local_watershed_magnitude', Integer, comment='The magnitude associated with the local watershed code.')
    AREA_HA = Column('area_ha', Float,
                     comment='Area of the watershed, in hectares.')
    RIVER_AREA = Column(
        'river_area', Float, comment='Area of double line rivers within the watershed, in hectares.')
    LAKE_AREA = Column(
        'lake_area', Float, comment='Area of lakes within the watershed, in hectares.')
    WETLAND_AREA = Column(
        'wetland_area', Float, comment='Area of wetland features within the watershed, in hectares.')
    MANMADE_AREA = Column(
        'manmade_area', Float, comment='Area of manmade features within the watershed, in hectares.')
    GLACIER_AREA = Column(
        'glacier_area', Float, comment='Area of glacier features within the watershed, in hectares.')
    AVERAGE_ELEVATION = Column(
        'average_elevation', Float, comment='The average elevation of the watershed, in meters.')
    AVERAGE_SLOPE = Column('average_slope', Float,
                           comment='The average slope of the watershed.')
    ASPECT_NORTH = Column('aspect_north', Float, comment='The percentage of the watershed that has an aspect within '
                          '45 degrees of north, ie. an aspect between 315 and 45 degrees.')
    ASPECT_SOUTH = Column('aspect_south', Float, comment='The percentage of the watershed that has an aspect within '
                          '45 degrees of south, ie. an aspect between 135 and 225 degrees.')
    ASPECT_WEST = Column('aspect_west', Float, comment='The percentage of the watershed that has an aspect within '
                         '45 degrees of west, ie. an aspect between 225 and 315 degrees.')
    ASPECT_EAST = Column('aspect_east', Float, comment='The percentage of the watershed that has an aspect within '
                         '45 degrees of east, ie. an aspect between 45 and 135 degrees.')
    ASPECT_FLAT = Column('aspect_flat', Float, comment='The percentage of the watershed with no discernable aspect, '
                         'ie. the flat land.')
    FEATURE_CODE = Column('feature_code', String, comment='FEATURE CODE contains a value based on the Canadian Council '
                          'of Surveys and Mappings (CCSM) system for classification of '
                          'geographic features.')
    GEOMETRY = Column('geom', Geometry(srid=4326), comment='')

    __table_args__ = {'schema': 'whse_basemapping'}
