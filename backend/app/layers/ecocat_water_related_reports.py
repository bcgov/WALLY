# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, BLOB
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class EcocatWaterRelatedReports(BaseLayerTable):
    __tablename__ = 'ecocat_water_related_reports'

    REPORT_POINT_ID = Column(Integer, primary_key=True, comment='')
    FEATURE_CODE = Column(String, comment='')
    REPORT_ID = Column(Integer, comment='')
    TITLE = Column(String, comment='')
    SHORT_DESCRIPTION = Column(String, comment='')
    AUTHOR = Column(String, comment='')
    DATE_PUBLISHED = Column(DateTime, comment='')
    WATERSHED_CODE = Column(String, comment='')
    WATERBODY_IDENTIFIER = Column(String, comment='')
    LONG_DESCRIPTION = Column(String, comment='')
    REPORT_AUDIENCE = Column(String, comment='')
    GEOMETRY = Column(Geometry, comment='')
    OBJECTID = Column(Integer, comment='')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='')