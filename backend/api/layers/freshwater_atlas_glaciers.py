# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class FreshwaterAtlasGlaciers(BaseLayerTable):
    __tablename__ = 'freshwater_atlas_glaciers'
    
    WATERBODY_POLY_ID = Column(Integer, primary_key=True, autoincrement=False, comment='The WATERBODY POLY ID is the unique key for the waterbody polygon spatial layer. It is not applied to the warehouse model only, i.e., it originates with the source FWA system.')
    WATERSHED_GROUP_ID = Column(Integer, comment='An automatically generate id that uniquely identifies the watershed group feature.')
    WATERBODY_TYPE = Column(String, comment='The type of waterbody. Possible values include: \'L\' (lake), \'R\' (double lined river), \'W\' (wetland), \'X\' (manmade river or lake), or \'G\' (glacier or icefield).')
    WATERBODY_KEY = Column(Integer, comment='A unique identifier associated with waterbodies in order to group polygons that make up a single waterbody.')
    AREA_HA = Column(Float, comment='Area of polygon (hectares).')
    GNIS_ID_1 =	Column(Integer, comment='A BCGNIS (BC Geographical Names Information System) feature id attached to a waterbody or island, if applicable. In a grouped system the feature id of the BCGNIS group is provided here and any subsequent names provided in gnis_id2 and gnis_id3. Note: For Vancouver Island, Graham Island, and Moresby Island the names are not attached to the label points.')
    GNIS_NAME_1	= Column(String, comment='The name of the first BCGNIS (BC Geographical Names Information System) feature id (an English name was used where available, otherwise another language was selected).')
    GNIS_ID_2 = Column(Integer, comment='A second BCGNIS (BC Geographical Names Information System) feature id attached to a waterbody or island, if applicable.')
    GNIS_NAME_2 = Column(String, comment='The name of the second BCGNIS (BC Geographical Names Information System) feature id (an English name was used where available, otherwise another language was selected).')
    GNIS_ID_3 =	Column(Integer, comment='A third BCGNIS (BC Geographical Names Information System) feature id attached to a waterbody or island, if applicable.')
    GNIS_NAME_3 = Column(String, comment='The name of the third BCGNIS (BC Geographical Names Information System) feature id (an English name was used where available, otherwise another language was selected).')
    BLUE_LINE_KEY =	Column(Integer, comment='The blue line key of the controlling route through the waterbody.')
    WATERSHED_KEY = Column(Integer, comment='The watershed key of the controlling rout through the waterbody.')
    FWA_WATERSHED_CODE = Column(String, comment='The watershed code of the controlling route through the waterbody.')
    LOCAL_WATERSHED_CODE = Column(String, comment='The local watershed code associated with the waterbody.')
    WATERSHED_GROUP_CODE = Column(String, comment='The watershed group codeof the watershed the feature is contained within.')
    LEFT_RIGHT_TRIBUTARY = Column(String, comment='A value attributed via the watershed code to all waterbodies indicating on what side of the watershed they drain into.')
    WATERBODY_KEY_50K =	Column(Integer, comment='The \'best\' matched waterbody from the 1:50K Watershed Atlas. In cases where there are multiple matches to features in the 1:50K watershed atlas the match with the greatest overlapping area was used.')
    WATERSHED_GROUP_CODE_50K = Column(String, comment='The group code from the 1:50K Watershed Atlas associated with the waterbody key 50k.')
    WATERBODY_KEY_GROUP_CODE_50K = Column(String, comment='The waterbody key 50K with the group code 50K concatenated.')
    WATERSHED_CODE_50K = Column(String, comment='The 1:50K Watershed Atlas watershed code associated with the waterbody key 50K.')
    FEATURE_CODE = Column(String, comment='FEATURE CODE contains a value based on the Canadian Council of Surveys and Mapping\'s (CCSM) system for classification of geographic features.')
    OBJECTID = Column(Float, comment='')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools'
                              'to store annotation, curve features and CAD data when using'
                              'the SDO_GEOMETRY storage data type.')
    FEATURE_AREA_SQM = Column(Float, comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional polygon in square meters')
    FEATURE_LENGTH_M = Column(Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a geometry in meters')
    GEOMETRY = Column(Geometry(srid=4326), index=True)
