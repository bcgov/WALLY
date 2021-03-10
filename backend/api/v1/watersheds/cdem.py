""" Functions for interacting with CDEM data to get median elevation for watershed areas
    CDEM data source:
    https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/
"""
import logging
from sqlalchemy.orm import Session
from shapely.geometry import Polygon

logger = logging.getLogger('cdem')


def mean_elevation(db: Session, area: Polygon):
    """ finds the mean elevation from CDEM for a given area
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
    select  sum(value*tot_pix)/sum(tot_pix) AS avg
    from    elev;
    """

    mean_elev = db.execute(q, {"area": area.wkt})
    mean_elev = mean_elev.fetchone()
    if not mean_elev or not mean_elev[0]:
        raise Exception(
            "mean elevation could not be found using CDEM")
    mean_elev = mean_elev[0]
    logger.info("found CDEM mean elevation: %s", mean_elev)

    return mean_elev
