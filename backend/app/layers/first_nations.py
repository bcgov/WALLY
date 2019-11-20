from sqlalchemy import Integer, String, Column, Float
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry


class CommunityLocation(BaseLayerTable):
    """
    https://catalogue.data.gov.bc.ca/dataset/first-nation-community-locations
    """
    __tablename__ = 'fn_community_locations'

    ogc_fid = Column(Integer, primary_key=True, autoincrement=True)
    COMMUNITY_LOCATION_ID = Column(Integer)
    FIRST_NATION_BC_NAME = Column(String)
    FIRST_NATION_FEDERAL_NAME = Column(String)
    FIRST_NATION_FEDERAL_ID = Column(Integer)
    URL_TO_BC_WEBSITE = Column(String)
    URL_TO_FEDERAL_WEBSITE = Column(String)
    URL_TO_FIRST_NATION_WEBSITE = Column(String)
    MEMBER_ORGANIZATION_NAMES = Column(String)
    LANGUAGE_GROUP = Column(String)
    BC_REGIONAL_OFFICE = Column(String)
    MAPSHEET_NUMBER = Column(String)
    PREFERRED_NAME = Column(String)
    ALTERNATIVE_NAME_1 = Column(String)
    ALTERNATIVE_NAME_2 = Column(String)
    ADDRESS_LINE1 = Column(String)
    ADDRESS_LINE2 = Column(String)
    OFFICE_CITY = Column(String)
    OFFICE_PROVINCE = Column(String)
    OFFICE_POSTAL_CODE = Column(String)
    LOCATION_DESCRIPTION = Column(String)
    SITE_NAME = Column(String)
    SITE_NUMBER = Column(String)
    COMMENTS = Column(String)
    OBJECTID = Column(Integer)
    SE_ANNO_CAD_DATA = Column(String)
    fme_feature_type = Column(String)
    SHAPE = Column(Geometry('POINT', 4326), index=True)


class TreatyArea(BaseLayerTable):
    """
    https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-areas
    """
    __tablename__ = 'fn_treaty_areas'

    ogc_fid = Column(Integer, primary_key=True, autoincrement=True)
    TREATY_AREA_ID = Column(Integer)
    TREATY = Column(String)
    EFFECTIVE_DATE = Column(String)
    FIRST_NATION_NAME = Column(String)
    AREA_TYPE = Column(String)
    LAND_TYPE = Column(String)
    GEOGRAPHIC_LOCATION = Column(String)
    CHAPTER_REFERENCE = Column(String)
    APPENDIX_REFERENCE = Column(String)
    COMMENTS = Column(String)
    FEATURE_CODE = Column(String)
    SE_ANNO_CAD_DATA = Column(String)
    OBJECTID = Column(Integer)
    FEATURE_AREA_SQM = Column(Float(53))
    FEATURE_LENGTH_M = Column(Float(53))
    fme_feature_type = Column(String)
    SHAPE = Column(Geometry(srid=4326), index=True)


class TreatyLand(BaseLayerTable):
    """
    https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-lands
    """
    __tablename__ = 'fn_treaty_lands'

    ogc_fid = Column(Integer, primary_key=True, autoincrement=True)
    TREATY_LAND_ID = Column(Integer)
    TREATY = Column(String)
    EFFECTIVE_DATE = Column(String)
    FIRST_NATION_NAME = Column(String)
    LAND_TYPE = Column(String)
    CHAPTER_REFERENCE = Column(String)
    APPENDIX_REFERENCE = Column(String)
    COMMENTS = Column(String)
    FEATURE_CODE = Column(String)
    OBJECTID = Column(Integer)
    SE_ANNO_CAD_DATA = Column(String)
    FEATURE_AREA_SQM = Column(Float(53))
    FEATURE_LENGTH_M = Column(Float(53))
    fme_feature_type = Column(String)
    SHAPE = Column(Geometry(srid=4326), index=True)
