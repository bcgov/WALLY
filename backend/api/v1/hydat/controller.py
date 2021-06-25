from sqlalchemy.orm import Session
from sqlalchemy import func
import logging
from shapely import wkb
from shapely.geometry import Point, Polygon
from typing import List
from api.v1.hydat.db_models import Station as StreamStationDB
from api.v1.hydat.schema import StreamStation, NearbyStream
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
