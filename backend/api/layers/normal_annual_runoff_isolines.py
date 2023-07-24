# coding: utf-8
from sqlalchemy import Integer, Column
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry


class NormalAnnualRunoffIsolines(BaseLayerTable):
    __tablename__ = 'normal_annual_runoff_isolines'

    id = Column(Integer, primary_key=True, autoincrement=False, comment='Arbitrary id to differentiate polygons.')
    ANNUAL_RUNOFF_IN_MM = Column(Integer, comment='Annual runoff of precipitation in the area of the associated polygon.')
    GEOMETRY = Column(Geometry(srid=4326), comment='This geometry is the polygon associated with the isoline for this area.')