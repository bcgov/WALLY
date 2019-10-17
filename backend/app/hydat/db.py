"""
Database tables and data access functions for Water Survey of Canada's
National Water Data Archive Hydrometic Data
"""
import logging
from typing import List
from geojson import FeatureCollection, Feature, Point
from sqlalchemy import Column, Integer, ForeignKey, String, MetaData, func
from sqlalchemy.orm import Session, relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from shapely.geometry import Polygon
import app.hydat.models as streams_v1
from app.hydat.db_models import DlyFlow, Station, DlyLevel

logger = logging.getLogger("api")


def get_stations(db: Session, search_area: Polygon = None):
    """ List all stream monitoring stations in BC as a FeatureCollection.

        Accepts a `bbox` argument (as a list of coordinates) to constrain the search to an area.
    """

    q = db.query(Station).filter(
        Station.prov_terr_state_loc == 'BC')

    if search_area:
        q = q.filter(
            func.ST_Intersects(search_area.wkt, Station.geom)
        )

    return q.all()


def get_monthly_levels_by_station(db: Session, station: str, year: int) -> List[streams_v1.MonthlyLevel]:
    """ fetch monthly stream levels for a specified station_number and year """
    if year:
        return db.query(DlyLevel).filter(
            DlyLevel.station_number == station,
            DlyLevel.year == year
        ).all()

    # year not specified, return an average by month for all years.
    return db.query(
        func.avg(DlyLevel.monthly_mean).label('monthly_mean'),
        func.min(DlyLevel.min).label('min'),
        func.max(DlyLevel.max).label('max'),
        DlyLevel.month
    ) \
        .filter(DlyLevel.station_number == station, DlyLevel.full_month == 1) \
        .group_by(DlyLevel.month) \
        .order_by(DlyLevel.month).all()


def get_monthly_flows_by_station(db: Session, station: str, year: int) -> List[streams_v1.MonthlyFlow]:
    """ fetch monthly stream levels for a specified station_number and year """
    if year:
        return db.query(DlyFlow).filter(
            DlyFlow.station_number == station,
            DlyFlow.year == year
        ).all()

    # year not specified, return average by month for all available years.
    return db.query(
        func.avg(DlyFlow.monthly_mean).label('monthly_mean'),
        func.min(DlyFlow.min).label('min'),
        func.max(DlyFlow.max).label('max'),
        DlyFlow.month) \
        .filter(DlyFlow.station_number == station, DlyFlow.full_month == 1) \
        .group_by(DlyFlow.month) \
        .order_by(DlyFlow.month).all()


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


# Function name needs to match get_as_geojson name in app.db.base_class.py
# this is so the generic aggregate function can call the same function name
# between baselayerclass objects and custom data objects such as Hydat
def get_as_geojson(db: Session, search_area: Polygon) -> FeatureCollection:
    """ calls get_stations and formats the result in geojson """
    stations = get_stations(db, search_area)

    # add properties to geojson Feature objects
    points = [
        Feature(
            geometry=Point((stn.longitude, stn.latitude)),
            id=stn.station_number,
            properties={
                "name": stn.station_name,
                "type": "hydat",
                "url": f"/api/v1/hydat/{stn.station_number}",
                "description": "Stream discharge and water level data",
            }
        ) for stn in stations
    ]

    return FeatureCollection(points)


# def get_create_context(db: Session, bbox: List[float] = []):
