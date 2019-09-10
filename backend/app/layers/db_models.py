from sqlalchemy import Column, Text, Table, BigInteger
from geoalchemy2 import Geometry
from app.db.base_class import BaseTable


class Parcel(BaseTable):
    __tablename__ = "parcel"
    PARCEL_FABRIC_POLY_ID = Column(BigInteger, unique=True, primary_key=True)
    geom = Column(Geometry('MULTIPOLYGON', 4326))
    PIN = Column(BigInteger)
    PID = Column(Text)
    PID_NUMBER = Column(BigInteger)
    PARCEL_NAME = Column(Text)
    PLAN_NUMBER = Column(BigInteger)
