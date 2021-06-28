import time
import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import DataError
import logging
from fastapi import HTTPException
from shapely import wkb
from shapely.geometry import Point, Polygon
from typing import List
from api.v1.hydat.db_models import Station as StreamStationDB
from api.v1.hydat.schema import FASSTRLongTermSummary, FASSTRMonthlyFlow, FlowStat, StreamStation, FASSTRFlowStatsSummary, NearbyStream
from geoalchemy2.shape import to_shape

logger = logging.getLogger("api")


def get_stations_in_area(db: Session, polygon: Polygon) -> list:
    """ Get hydrometric stations given a polygon area (ie watershed)"""
    logger.debug('Get hydrometric stations in polygon', polygon.wkt)

    # Search for point Lat: 49.250285 Lng: -122.953816
    stn_q = db.query(
        StreamStationDB,
    ).filter(
        func.ST_Intersects(
            func.ST_GeographyFromText(polygon.wkt),
            func.Geography(StreamStationDB.geom)
        )
    )

    rs_stations = stn_q.all()

    stations = [
        StreamStationDB.get_as_feature(x, StreamStationDB.get_geom_column(db))
        for x in rs_stations
    ]

    return stations


def get_fasstr_longterm_summary(db: Session, station_number: str) -> FASSTRLongTermSummary:
    """ gets the FASSTR longterm daily flow summary for a station"""

    q = """
    with flows as (
        select  s.station_number,
                array_agg(f.value) as values,
                array_agg(f.date) as dates
        from    hydat.stations s
        join    fasstr.fasstr_flows f
        on      f.station_number = s.station_number
        where   s.station_number = :station_number
       group by s.station_number

    )
    select * from fasstr.fasstr_calc_longterm_daily_stats(
        (select dates from flows), (select values from flows), TRUE, FALSE);
    """
    try:
        res = db.execute(q, {"station_number": station_number})
    except DataError:
        raise HTTPException(
            status_code=400,
            detail="Not enough data to compute long-term stats for this station."
        )

    if not res:
        raise HTTPException(
            status_code=404, detail="Station not found.")

    monthly_stats: List[FASSTRMonthlyFlow] = []
    summary = None

    for row in res:
        row = dict(row)
        if row['month'] == 'Long-term':
            summary = FASSTRLongTermSummary(
                **row,
                station_number=station_number,
                months=[]
            )
        else:
            # row['month'] = datetime.datetime.strptime(row['month'], '%b').month
            monthly_stats.append(
                FASSTRMonthlyFlow(**row)
            )
    summary.months = monthly_stats
    return summary


def get_fasstr_flow_stats(db: Session, station_number: str, full_years: bool = False) -> FASSTRFlowStatsSummary:
    """
    returns FASSTR flow statistics for a station, based on quantiles for selected return periods.

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
        join    fasstr.fasstr_flows f
        on      f.station_number = s.station_number
        where   s.station_number = :station_number
       group by s.station_number

    )
    select  station_number,
            ROUND(fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 10 ), 2) as "low_30q10",
            ROUND(fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 5 ), 2) as "low_30q5",
            ROUND(fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 10, summer=>true ), 2) as "low_7q10",
            ROUND(fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days => 30, return_period => 5, summer=>true ), 2) as "low_30q10_summer",
            ROUND(fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days => 7, return_period => 10 ), 2) as "low_30q5_summer",
            ROUND(fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days => 7, return_period => 10, summer=>true ), 2) as "low_7q10_summer"
    from    flows
    """

    try:
        res = db.execute(q, {"station_number": station_number}).fetchone()
    except DataError:
        raise HTTPException(
            status_code=400,
            detail="Not enough data to compute quantiles for this station."
        )

    if not res:
        raise HTTPException(
            status_code=404, detail="Station not found.")

    end = time.perf_counter()

    logger.info("calculated stream stats in %s s", end - start)

    flow_stats = []

    hydrostats_display_names = {
        "low_30q10": "30Q10",
        "low_30q5": "30Q5",
        "low_7q10": "7Q10",
        "low_30q10_summer": "30Q10-Summer",
        "low_30q5_summer": "30Q5-Summer",
        "low_7q10_summer": "7Q10-Summer"
    }

    station = res["station_number"]

    for k in hydrostats_display_names.keys():
        flow_stats.append(FlowStat(
            stat=k,
            display_name=hydrostats_display_names[k],
            value=float(res[k])
        ))

    return FASSTRFlowStatsSummary(station_number=station, stats=flow_stats)


def get_station(db: Session, station_number: str) -> StreamStation:
    """ Returns station details (from the HYDAT database) for a given
    station_number. """

    q = db.query(StreamStationDB) \
          .filter(StreamStationDB.station_number == station_number)

    res = q.first()
    stn = dict(res.__dict__)
    stn['geom'] = to_shape(stn['geom'])

    return StreamStation(**stn)


def get_point_on_stream(db: Session, station_number: str) -> Point:
    """
    given a HYDAT station number, return a point on a stream for that station.

    Sometimes the Hydat stream station coordinates are slightly away from the stream,
    or may be located at a confluence point (so we may need to look at the station name
    to determine which stream to snap to). This function helps snap the coordinates to a
    FWA streamline, with a preference for the stream's GNIS name including the first word in the
    station name.
    """

    q = """
      WITH stn AS (
        select station_name, geom
        from hydat.stations
        where station_number = :station_number
      ),
      nearest_streams AS (
          select    *
          from      freshwater_atlas_stream_networks streams
          order by  streams."GEOMETRY" <#>
                        (select geom from stn)
          limit     10
      )
      SELECT 
        (select ST_AsBinary(geom) from stn) as station_point,
        nearest_streams."GNIS_NAME" as gnis_name,
        nearest_streams."LINEAR_FEATURE_ID" as linear_feature_id,
        ST_AsBinary(
          ST_ClosestPoint(
            nearest_streams."GEOMETRY", 
            (select geom from stn)
          )
        ) as stream_point
      FROM      nearest_streams
      ORDER BY  
        coalesce(nearest_streams."GNIS_NAME" ILIKE '%' || (select split_part(station_name, ' ', 1) from stn) || '%', FALSE) DESC,
        ST_Distance(nearest_streams."GEOMETRY", (select geom from stn)) ASC
      LIMIT     1
    """
    res = db.execute(q, {"station_number": station_number})
    stream = res.fetchone()

    stream_point = wkb.loads(stream['stream_point'].tobytes())
    station_point = wkb.loads(stream['station_point'].tobytes())
    stream_feature_id = stream['linear_feature_id']

    logger.info('Station %s - using point on stream: %s', station_number, stream_point.wkt)

    return (stream_point, stream_feature_id, station_point)


def get_nearest_stream_segments(db: Session, station_number: str) -> List[NearbyStream]:
    """ get nearest stream segments returns the 5 stream segments nearest the
        HYDAT station that match the name of the station.

        This helps with inferring the station location (in cases where the location
        is not clear) because we can run a watershed delineation from each segment
        and compare the results with the listed drainage_area_gross to infer which
        segment the station is likely on.
    """

    q = """
      WITH stn AS (
        select station_name, geom
        from hydat.stations
        where station_number = :station_number
      ),
      nearest_streams AS (
          select    *
          from      freshwater_atlas_stream_networks streams
          order by  streams."GEOMETRY" <#>
                        (select geom from stn)
          limit     5
      )
      SELECT 
        (select ST_AsBinary(geom) from stn) as station_point,
        nearest_streams."GNIS_NAME" as gnis_name,
        nearest_streams."LINEAR_FEATURE_ID" as linear_feature_id,
        ST_AsBinary(
          ST_ClosestPoint(
            nearest_streams."GEOMETRY", 
            (select geom from stn)
          )
        ) as stream_point
      FROM      nearest_streams
      ORDER BY  
        coalesce(nearest_streams."GNIS_NAME" ILIKE '%' || (select split_part(station_name, ' ', 1) from stn) || '%', FALSE) DESC,
        ST_Distance(nearest_streams."GEOMETRY", (select geom from stn)) ASC
    """
    res = db.execute(q, {"station_number": station_number})
    streams = []
    for row in res:
        row = dict(row)
        streams.append(NearbyStream(
            stream_point=wkb.loads(row['stream_point'].tobytes()),
            stream_feature_id=row['linear_feature_id']
        ))
    return streams
