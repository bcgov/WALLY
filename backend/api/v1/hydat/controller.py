import time
from sqlalchemy.orm import Session
from sqlalchemy import text, func
import logging
from fastapi import HTTPException
from shapely.geometry import Polygon
from api.v1.hydat.db_models import Station as StreamStation
from api.v1.hydat.schema import FlowStatistics
logger = logging.getLogger("api")


def get_stations_in_area(db: Session, polygon: Polygon) -> list:
    """ Get hydrometric stations given a polygon area (ie watershed)"""
    logger.debug('Get hydrometric stations in polygon', polygon.wkt)

    # Search for point Lat: 49.250285 Lng: -122.953816
    stn_q = db.query(
        StreamStation,
    ).filter(
        func.ST_Intersects(
            func.ST_GeographyFromText(polygon.wkt),
            func.Geography(StreamStation.geom)
        )
    )

    rs_stations = stn_q.all()

    stations = [
        StreamStation.get_as_feature(x, StreamStation.get_geom_column(db))
        for x in rs_stations
    ]

    return stations


def flow_statistics(db: Session, station_number: str, full_years: bool = False):
    """
    returns flow statistics for a station.

    Returns the following low flows:
    30Q10
    30Q5
    7Q10
    30Q10-Summer
    30Q5-Summer
    7Q10-Summer

    full_years: indicates whether to only consider years for which there is full data.
    """

    start = time.perf_counter()

    q = """
    with flows as (
        select  s.station_number,
                array_agg(f.value) as values,
                array_agg(f.date) as dates
        from    hydat.stations s
        join    hydat.fasstr_flows f
        on      f.station_number = s.station_number
        where   s.station_number = :station_number
       group by s.station_number

    )
    select  station_number,
            hydat.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 10 ) as "low_30q10",
            hydat.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 5 ) as "low_30q5",
            hydat.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 10, summer=>true ) as "low_7q10",
            hydat.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 5, summer=>true ) as "low_30q10_summer",
            hydat.fasstr_compute_frequency_quantile(dates, values, roll_days => 7, return_period => 10 ) as "low_30q5_summer",
            hydat.fasstr_compute_frequency_quantile(dates, values, roll_days => 7, return_period => 10, summer=>true ) as "low_7q10_summer"
    from    flows
    """

    """
    select  station_number,
            hydat.fasstr_compute_frequency_quantile(station_number, roll_days => 30, return_period => 10 ) as "low_30q10",
            hydat.fasstr_compute_frequency_quantile(station_number, roll_days => 30, return_period => 5 ) as "low_30q5",
            hydat.fasstr_compute_frequency_quantile(station_number, roll_days => 30, return_period => 10, summer=>true ) as "low_7q10",
            hydat.fasstr_compute_frequency_quantile(station_number, roll_days => 30, return_period => 5, summer=>true ) as "low_30q10_summer",
            hydat.fasstr_compute_frequency_quantile(station_number, roll_days => 7, return_period => 10 ) as "low_30q5_summer",
            hydat.fasstr_compute_frequency_quantile(station_number, roll_days => 7, return_period => 10, summer=>true ) as "low_7q10_summer"
    from    hydat.stations
    where   station_number = :station_number
    """

    res = db.execute(q, {"station_number": station_number}).fetchone()

    if not res:
        raise HTTPException(
            status_code=404, detail="Station not found.")

    end = time.perf_counter()

    logger.info("calculated stream stats in %s s", end - start)

    return FlowStatistics.from_orm(res)
