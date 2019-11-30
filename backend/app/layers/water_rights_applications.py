# coding: utf-8
from pydantic import BaseModel, Schema
from typing import Optional, List
from sqlalchemy import Integer, String, Column, DateTime, Float, func
from sqlalchemy.orm import Session
from geojson import Point, Feature, FeatureCollection
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class WaterRightsApplications(BaseLayerTable):
    __tablename__ = 'water_rights_applications'

    WLS_WRA_SYSID = Column(Integer, comment='WLS WRA SYSID is a system generated unique identification number.')
    APPLICATION_JOB_NUMBER = Column(String, primary_key=True, autoincrement=False,
                                    comment='APPLICATION JOB NUMBER is a unique identifier for a ground water licence application, e.g. 1003202.')
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
    FILE_NUMBER = Column(String, comment='FILE NUMBER is the water business file number, assigned during the '
                                         'application phase, e.g., 0321048. A file may hold one or more licences.')
    APPLICATION_STATUS = Column(String, comment='APPLICATION STATUS is the status of the water rights application submitted '
                                                'by the applicant. There are two possible statuses: Active Application, if '
                                                'the application is undergoing adjudication; or Refused, if the application '
                                                'is complete but no licence was granted. When an application is granted as a '
                                                'licence it is removed from the applications dataset '
                                                'and added to the licences dataset.')
    WELL_TAG_NUMBER = Column(Integer, comment='WELL TAG NUMBER is a unique well identifier for either registered '
                                              'or licensed wells, e.g., 12345.')
    PURPOSE_USE_CODE = Column(String, comment='PURPOSE USE CODE is the use of water authorized by the licence, '
                                              'identified as a code, e.g., 02I.')
    PURPOSE_USE = Column(
        String, comment='PURPOSE USE is the use of water authorized by the licence, e.g. Industrial.')
    QTY_DIVERSION_MAX_RATE = Column(Float, comment='QTY DIVERSION MAX RATE is the maximum authorized diversion '
                                                   'rate of water within a second, minute or day up to the total '
                                                   'licensed quantity per year, e.g, 0.006, 2000')
    QTY_UNITS_DIVERSION_MAX_RATE = Column(String, comment='QTY UNITS DIVERSION MAX RATE are the units of '
                                                          'measurement for the maximum diversion rate of water '
                                                          'authorized in the licence, e.g., m3/second, '
                                                          'm3/minute, m3/day, m3/year.')
    PRIMARY_APPLICANT_NAME = Column(String, comment='PRIMARY APPLICANT NAME is the primary contact for the application, '
                                                    'co-applicants will be displayed as et al.')
    ADDRESS_LINE_1 = Column(
        String, comment='ADDRESS LINE 1 is the first line of the applicant\'s mailing address.')
    ADDRESS_LINE_2 = Column(
        String, comment='ADDRESS LINE 2 is the second line of the applicant\'s mailing address.')
    ADDRESS_LINE_3 = Column(
        String, comment='ADDRESS LINE 3 is the third line of the applicant\'s mailing address.')
    ADDRESS_LINE_4 = Column(
        String, comment='ADDRESS LINE 4 is the fourth line of the applicant\'s mailing address.')
    COUNTRY = Column(String, comment='COUNTRY is the applicant\'s country.')
    POSTAL_CODE = Column(
        String, comment='POSTAL CODE is the applicant\'s postal code.')
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
