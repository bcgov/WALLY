# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, BLOB, Float
from app.db.base_class import BaseTable
from geoalchemy2 import Geometry


class GroundWaterWells(BaseTable):
    __tablename__ = 'ground_water_wells'


