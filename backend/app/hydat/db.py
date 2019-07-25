"""
Database tables and data access functions for Water Survey of Canada's
National Water Data Archive Hydrometic Data
"""
from typing import List
from geojson import FeatureCollection, Feature, Point
from sqlalchemy import Column, Integer, ForeignKey, String, MetaData
from sqlalchemy.orm import Session, relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import app.hydat.models as streams_v1
from app.hydat.db_models import DlyFlow, Station, DlyLevel


def get_stations(db: Session):
    """ list all stream monitoring stations in BC as a FeatureCollection """
    return db.query(Station).filter(
        Station.prov_terr_state_loc == 'BC').all()


def get_monthly_levels_by_station(db: Session, station: str, year: int) -> List[streams_v1.MonthlyLevel]:
    """ fetch monthly stream levels for a specified station_number and year """
    return db.query(DlyLevel).filter(
        DlyLevel.station_number == station,
        DlyLevel.year == year
    ).all()


def get_monthly_flows_by_station(db: Session, station: str, year: int) -> List[streams_v1.MonthlyFlow]:
    """ fetch monthly stream levels for a specified station_number and year """
    return db.query(DlyFlow).filter(
        DlyFlow.station_number == station,
        DlyFlow.year == year
    ).all()


def get_station_details(db: Session, station: str) -> streams_v1.StreamStation:
    """
    fetch details for a given stream monitoring station, including a list of years
    for which relevant data is available.
    """

    return db.query(Station).get(station)


def get_available_flow_years(db: Session, station: str):
    """ fetch a list of years for which stream flow data is available """
    return db.query(DlyFlow).filter(
        DlyFlow.station_number == station).distinct("year")


def get_available_level_years(db: Session, station: str):
    """ fetch a list of years for which stream level data is available """
    return db.query(DlyLevel).filter(
        DlyLevel.station_number == station).distinct("year")
