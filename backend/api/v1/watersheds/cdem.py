""" Functions for interacting with CDEM data to get median elevation for watershed areas
    CDEM data source:
    https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/
"""
import logging
from sqlalchemy.orm import Session
from shapely.geometry import Polygon
import numpy as np

logger = logging.getLogger('cdem')


def raster_summary_stats(db: Session, area: Polygon):
    """ finds the elevation stats summary from CDEM for a given area
        area should be a polygon with SRID 4140.
    """

    # Use ST_SummaryStats to find a summary of raster stats
    # https://postgis.net/docs/RT_ST_SummaryStats.html
    q = """
        select ST_SummaryStats(ST_Clip(cdem.rast,ST_GeomFromText(:area, 4140))) FROM dem.cdem
    """

    stats = db.execute(q, {"area": area.wkt})
    stats = stats.fetchone()
    if not stats:
        raise Exception(
            "elevation stats could not be found using CDEM")
    logger.info("found CDEM elevation stats: %s", stats)

    return stats


def median_elevation(db: Session, area: Polygon):
    """ finds the median elevation in METERS from CDEM for a given area
        area should be a polygon with SRID 4140.
    """

    # Use ST_ValueCount to find values and pixel counts
    # https://postgis.net/2014/09/26/tip_count_of_pixel_values/
    # Using the value counts find the mean elevation.
    q = """
    with elev as
    (
        select distinct
                (vc).value,
                sum ((vc).count) as tot_pix
        from    dem.cdem as cdem
        inner join
                ST_GeomFromText(:area, 4140) as geom
        on      ST_Intersects(cdem.rast, geom),
                ST_ValueCount(ST_Clip(cdem.rast,geom),1)
        as vc
        group by (vc).value
        order by (vc).value
    )
    select percentile_cont(0.5) WITHIN GROUP (ORDER BY value) AS median
    from elev;
    """

    median_elev = db.execute(q, {"area": area.wkt})
    median_elev = median_elev.fetchone()
    if not median_elev or not median_elev[0]:
        raise Exception(
            "median elevation could not be found using CDEM")
    median_elev = median_elev[0]
    logger.info("found CDEM median elevation: %s", median_elev)

    return median_elev


def average_slope(db: Session, area: Polygon):
    """ finds the mean slope in DEGREES from CDEM for a given area
        area should be a polygon with SRID 4140.
    """

    # Use ST_Slope to find the slope of a pixel
    # https://postgis.net/docs/RT_ST_Slope.html
    q = """
    with slope as
    (
        select distinct
                (vc).value,
                sum ((vc).count) as tot_pix
        from    dem.cdem as cdem
        inner join
                ST_GeomFromText(:area, 4140) as geom
        on      ST_Intersects(cdem.rast, geom),
                ST_ValueCount(ST_Slope(ST_Clip(cdem.rast,geom),1,'32BF','DEGREES'))
        as vc
        group by (vc).value
        order by (vc).value
    )
    select  sum(value)/sum(tot_pix) AS avg
    from    slope;
    """

    avg_slope_perc = db.execute(q, {"area": area.wkt})
    avg_slope_perc = avg_slope_perc.fetchone()
    if not avg_slope_perc or not avg_slope_perc[0]:
        raise Exception(
            "mean slope could not be found using CDEM")
    avg_slope_perc = avg_slope_perc[0]
    logger.info("found CDEM mean slope: %s", avg_slope_perc)

    return avg_slope_perc


def mean_aspect(db: Session, area: Polygon):
    """ finds the mean aspect in RADIANS from CDEM for a given area
        area should be a polygon with SRID 4140.
    """

    # Use ST_Aspect to find the slope of a pixel
    # https://postgis.net/docs/RT_ST_Aspect.html
    q = """
    with slope as
    (
        select distinct
                (vc).value,
                sum ((vc).count) as tot_pix
        from    dem.cdem as cdem
        inner join
                ST_GeomFromText(:area, 4140) as geom
        on      ST_Intersects(cdem.rast, geom),
                ST_ValueCount(ST_Aspect(ST_Clip(cdem.rast,geom),1,'32BF','RADIANS'))
        as vc
        group by (vc).value
        order by (vc).value
    )
    select  sum(value)/sum(tot_pix) AS avg
    from    slope;
    """

    aspect = db.execute(q, {"area": area.wkt})
    aspect = aspect.fetchone()
    if not aspect or not aspect[0]:
        raise Exception(
            "mean aspect could not be found using CDEM")
    aspect = aspect[0]
    logger.info("found CDEM mean aspect: %s", aspect)

    return aspect
