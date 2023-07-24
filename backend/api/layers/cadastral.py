# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, Float, BigInteger, Text
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA, UUID
import uuid


class Cadastral(BaseLayerTable):
    __tablename__ = 'cadastral'

    PARCEL_FABRIC_POLY_ID = Column(Integer, primary_key=True, autoincrement=False, comment='PARCEL_FABRIC_POLY_ID is a system generated '
                                                                      'unique identification number.')
    PARCEL_NAME = Column(String, comment='PARCEL_NAME is the same as the PID, if there is one. If there is a '
                                         'PIN but no PID, then PARCEL_NAME is the PIN. If there is no PID nor '
                                         'PIN, then PARCEL_NAME is the parcel class value, e.g., COMMON OWNERSHIP, '
                                         'BUILDING STRATA, AIR SPACE, ROAD, PARK.')
    PLAN_NUMBER = Column(String, comment='PLAN_NUMBER is the Land Act, Land Title Act, or Strata Property Act Plan '
                                         'Number for the land survey plan that corresponds to this parcel, e.g., '
                                         'VIP1632, NO_PLAN.')
    PIN = Column(Integer, comment='PIN is the Crown Land Registry Parcel Identifier, if applicable.')
    PID = Column(String, comment='PID is the Land Title Register parcel identifier, an up-to nine-digit text number '
                                 'with leading zeros that uniquely identifies a parcel in the land title register '
                                 'of in British Columbia. The registrar assigns PID numbers to parcels for which a '
                                 'title is being entered as a registered title. The Land Title Act refers to the '
                                 'PID as the permanent parcel identifier.')
    PID_NUMBER = Column(Integer, comment='PID_NUMBER is the Land Title Register parcel identifier, an up-to nine-digit '
                                         'number without leading zeros that uniquely identifies a parcel in the land '
                                         'title register of in British Columbia. The registrar assigns PID numbers '
                                         'to parcels for which a title is being entered as a registered title. The '
                                         'Land Title Act refers to the PID as the permanent parcel identifier.')
    PARCEL_STATUS = Column(String, comment='PARCEL_STATUS is the status of the parcel, according to the Land Title '
                                           'Register or Crown Land Registry, as appropriate, '
                                           'i.e., ACTIVE, CANCELLED, INACTIVE, PENDING.')
    PARCEL_CLASS = Column(String, comment='PARCEL_CLASS is the Parcel classification for maintenance, mapping, '
                                          'publishing and analysis, i.e., PRIMARY, SUBDIVISION, PART OF PRIMARY, '
                                          'BUILDING STRATA, BARE LAND STRATA, AIR SPACE, ROAD, HIGHWAY, PARK, '
                                          'INTEREST, COMMON OWNERSHIP, ABSOLUTE FEE BOOK, CROWN SUBDIVISION, '
                                          'RETURN TO CROWN.')
    OWNER_TYPE = Column(String, comment='OWNER_TYPE is the general ownership category, e.g., PRIVATE, CROWN '
                                        'PROVINCIAL, MUNICIPAL. For more information, '
                                        'see https://help.ltsa.ca/parcelmap-bc/owner-types-parcelmap-bc')
    PARCEL_START_DATE = Column(DateTime, comment='PARCEL_START_DATE is the date of the legal event that created '
                                                 'the parcel, i.e., the date the plan was filed.')
    MUNICIPALITY = Column(String, comment='MUNICIPALITY is the municipal area within which the parcel is located. '
                                          'The value is either RURAL (for parcels in unincorporated regions) or '
                                          'the name of a BC municipality.')
    REGIONAL_DISTRICT = Column(String, comment='REGIONAL_DISTRICT is the name of the regional district in which '
                                               'the parcel is located, e.g., CAPITAL REGIONAL DISTRICT.')
    WHEN_UPDATED = Column(DateTime, comment='WHEN_UPDATED is the date and time the record was last modified.')
    FEATURE_AREA_SQM = Column(Float, comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional '
                                             'polygon in square meters.')
    FEATURE_LENGTH_M = Column(Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a '
                                             'geometry in meters.')
    SHAPE = Column(Geometry(srid=4326), comment='SHAPE is the column used to reference the spatial coordinates defining '
                   'the feature.')
    OBJECTID = Column(Integer, comment='OBJECTID is a column required by spatial layers that interact with ESRI '
                                       'ArcSDE. It is populated with unique values automatically by SDE.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                                             'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                                             'storage data type.')


class Parcel(BaseLayerTable):
    __tablename__ = "parcel"

    geom = Column(Geometry('MULTIPOLYGON', 4326))
    PARCEL_FABRIC_POLY_ID = Column(BigInteger, unique=True, primary_key=True)
    PIN = Column(BigInteger)
    PID = Column(Text)
    PID_NUMBER = Column(BigInteger)
    PARCEL_NAME = Column(Text)
    PLAN_NUMBER = Column(BigInteger)


class Publisher(BaseLayerTable):
    __tablename__ = "publisher"

    publisher_guid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    name = Column(String, index=True, nullable=False)
    description = Column(String)
