# coding: utf-8
from pydantic import BaseModel, Schema
from typing import Optional, List
from sqlalchemy import Integer, String, Column, DateTime, Float, func
from sqlalchemy.orm import Session
from geojson import Point, Feature, FeatureCollection
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class WaterRightsLicenses(BaseLayerTable):
    __tablename__ = 'water_rights_licenses'

    WLS_WRL_SYSID = Column(Integer, primary_key=True, comment='WLS WRL SYSID is a system generated unique '
                                                              'identification number.')
    POD_NUMBER = Column(String, comment='POD NUMBER is the unique identifier for a Point of Diversion, e.g., PW189413. '
                                        'Each POD can have multiple licences associated with it.')
    POD_SUBTYPE = Column(String, comment='POD SUBTYPE distinguishes the different POD types, i.e., POD (a surface '
                                         'water point of diversion), PWD (a point of well diversion that diverts '
                                         'groundwater), or PG (a point of groundwater diversion that diverts '
                                         'groundwater such as a dugout, ditch or quarry).')
    POD_DIVERSION_TYPE = Column(String, comment='POD_DIVERSION_TYPE is the type of diversion for a point of '
                                                'groundwater diversion (PG subtype), i.e., Dugout, Ditch, Quarry. '
                                                'Since this only applies to PG subtypes, other subypes (POD or PWD)'
                                                ' will be left blank (null value).')
    POD_STATUS = Column(String, comment='POD STATUS is the status of the Point of Diversion. Each POD can have '
                                        'multiple licences, e.g., Active (one or more active licences associated), '
                                        'Inactive (only historical inactive licences associated).')
    FILE_NUMBER = Column(String, comment='FILE NUMBER is the water business file number, assigned during the '
                                         'application phase, e.g., 0321048. A file may hold one or more licences.')
    WELL_TAG_NUMBER = Column(Integer, comment='WELL TAG NUMBER is a unique well identifier for either registered '
                                              'or licensed wells, e.g., 12345.')
    LICENCE_NUMBER = Column(String, comment='LICENCE NUMBER is the authorization number referenced in the water '
                                            'licence document, e.g., 121173.')
    LICENCE_STATUS = Column(String, comment='LICENCE STATUS represents the existing status of licence, e.g., '
                                            'Current, Cancelled, Pending.')
    LICENCE_STATUS_DATE = Column(DateTime, comment='LICENCE STATUS DATE indicates the last time the '
                                                   'licence status changed.')
    PRIORITY_DATE = Column(DateTime, comment='PRIORITY DATE is the date from which the precedence of the '
                                             'licence is established within the first in time first '
                                             'in right framework.')
    EXPIRY_DATE = Column(
        DateTime, comment='EXPIRY DATE is the date the licence expires.')
    PURPOSE_USE_CODE = Column(String, comment='PURPOSE USE CODE is the use of water authorized by the licence, '
                                              'identified as a code, e.g., 02I.')
    PURPOSE_USE = Column(
        String, comment='PURPOSE USE is the use of water authorized by the licence, e.g. Industrial.')
    SOURCE_NAME = Column(String, comment='SOURCE NAME is the aquifer or body of surface water from which '
                                         'the licence is authorized to extract water. A surface water body '
                                         'can be a lake, river, creek or any other surface water source e.g., '
                                         'Skaha Lake or Kokanee Creek. For a known aquifer that has been mapped, '
                                         'the aquifer name is the BC Governments Aquifer ID number, e.g., 1137. '
                                         'For an unmapped aquifer, the aquifer name is derived from water precincts '
                                         'names in common use, and lithologic or litho-stratigraphic units,'
                                         ' e.g., Nelson Unconsolidated; Nelson Bedrock.')
    REDIVERSION_IND = Column(String, comment='REDIVERSION IND is an indicator of whether the Point of Well '
                                             'Diversion is, for the particular licence, used to divert water '
                                             'from another water source, i.e., Y or N.')
    QUANTITY = Column(Float, comment='QUANTITY is the maximum quantity of water that is authorized to be '
                                     'diverted for the purpose use, e.g., 500.')
    QUANTITY_UNITS = Column(String, comment='QUANTITY UNITS is the units of measurement for the quantity of '
                                            'water authorized in the licence, e.g., m3 / year.')
    QUANTITY_FLAG = Column(String, comment='QUANTITY FLAG is the code used to identify how the total quantity '
                                           'is assigned across multiple Points of Well Diversion (PWD) for a '
                                           'particular licence and purpose use, i.e., T, M, D, or P.')
    QUANTITY_FLAG_DESCRIPTION = Column(String, comment='QUANTITY FLAG DESCRIPTION is a description of the '
                                                       'QUANTITY FLAG code used to identify how the total quantity '
                                                       'is assigned across multiple Points of Well Diversion (PWD) '
                                                       'for a particular licence and purpose use, i.e., T (Total '
                                                       'demand for purpose, one PWD); M (Maximum licensed demand '
                                                       'for purpose, multiple PWDs, quantity at each PWD unknown); '
                                                       'D (Multiple PWDs for purpose, quantities at each are known, '
                                                       'PWDs on different aquifers); P (Multiple PWDs for purpose, '
                                                       'quantities at each are known, PWDs on same aquifer).')
    QTY_DIVERSION_MAX_RATE = Column(Float, comment='QTY DIVERSION MAX RATE is the maximum authorized diversion '
                                                   'rate of water within a second, minute or day up to the total '
                                                   'licensed quantity per year, e.g, 0.006, 2000')
    QTY_UNITS_DIVERSION_MAX_RATE = Column(String, comment='QTY UNITS DIVERSION MAX RATE are the units of '
                                                          'measurement for the maximum diversion rate of water '
                                                          'authorized in the licence, e.g., m3/second, '
                                                          'm3/minute, m3/day, m3/year.')
    HYDRAULIC_CONNECTIVITY = Column(String, comment='HYDRAULIC CONNECTIVITY is an indicator of whether the '
                                                    'licensed aquifer diversion (PWD or PG) may be hydraulically '
                                                    'connected to one or more surface water sources (stream or '
                                                    'lake), i.e., Likely, Unknown.')
    PERMIT_OVER_CROWN_LAND_NUMBER = Column(String, comment='PERMIT OVER CROWN LAND NUMBER is an Internal number'
                                                           ' assigned to a Permit over Crown Land '
                                                           '(PCL), e.g., 12345.')
    PRIMARY_LICENSEE_NAME = Column(String, comment='PRIMARY LICENSEE NAME is the primary contact for the licence, '
                                                   'co-licensees will be displayed as et al.')
    ADDRESS_LINE_1 = Column(
        String, comment='ADDRESS LINE 1 is the first line of the licensees mailing address.')
    ADDRESS_LINE_2 = Column(
        String, comment='ADDRESS LINE 2 is the second line of the licensees mailing address.')
    ADDRESS_LINE_3 = Column(
        String, comment='ADDRESS LINE 3 is the third line of the licensees mailing address.')
    ADDRESS_LINE_4 = Column(
        String, comment='ADDRESS LINE 4 is the fourth line of the licensees mailing address.')
    COUNTRY = Column(String, comment='COUNTRY is the licensees country.')
    POSTAL_CODE = Column(
        String, comment='POSTAL CODE is the licensees postal code.')
    LATITUDE = Column(Float, comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), '
                                     'of the location of the feature as measured from the equator, e.g., 55.323653.')
    LONGITUDE = Column(Float, comment='LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), '
                                      'of the location of the feature as measured from the prime meridian, '
                                      'e.g., -123.093544.')
    DISTRICT_PRECINCT_NAME = Column(String, comment='DISTRICT PRECINCT NAME is a jurisdictional area within a '
                                                    'Water District. It is a combination of District and Precinct '
                                                    'codes and names, e.g., New Westminster / Coquitlam. Not all '
                                                    'Water Districts contain Precincts.')
    SHAPE = Column(Geometry(srid=4326), comment='SHAPE is the column used to reference the spatial coordinates '
                   'defining the feature.')
    OBJECTID = Column(Integer, comment='OBJECTID is a column required by spatial layers that interact with '
                                       'ESRI ArcSDE. It is populated with unique values automatically by SDE.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE ANNO CAD DATA is a binary column used by spatial tools to '
                              'store annotation, curve features and CAD data when using '
                              'the SDO GEOMETRY storage data type.')
