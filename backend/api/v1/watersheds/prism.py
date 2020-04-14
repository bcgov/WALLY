""" Functions for interacting with PRISM data to get precipitation and temperature
    means for watershed areas

    PRISM data source:
    Pacific Climate Impacts Consortium, University of Victoria, and PRISM Climate Group,
    Oregon State University, (Jan. 2014). High Resolution Climatology. Downloaded from
    https://www.pacificclimate.org/data/prism-climatology-and-monthly-timeseries-portal
    on April 8, 2020
"""
import logging
from sqlalchemy.orm import Session
from shapely.geometry import Polygon

from api.v1.watersheds.controller import get_annual_precipitation

logger = logging.getLogger('prism')


def mean_annual_precipitation(db: Session, area: Polygon):
    """ finds the mean annual precipitation from PRISM for a given area
        area should be a polygon with SRID 4326.
    """

    # Use ST_ValueCount to find values and pixel counts from the PRISM raster
    # https://postgis.net/2014/09/26/tip_count_of_pixel_values/
    # Using the value counts find the mean precipitation.
    q = """
    with precip as
    (
        select distinct
                (vc).value,
                sum ((vc).count) as tot_pix
        from    prism.prism as prism
        inner join
                ST_GeomFromText(:area, 4326) as geom
        on      ST_Intersects(prism.rast, geom),
                ST_ValueCount(ST_Clip(prism.rast,geom),1)
        as vc
        group by (vc).value
        order by (vc).value
    )
    select  sum(value*tot_pix)/sum(tot_pix) AS avg
    from    precip;
    """

    try:
        mean_precip = db.execute(q, {"area": area.wkt})
        mean_precip = mean_precip.fetchone()
        if not mean_precip or not mean_precip[0]:
            raise Exception(
                "mean precipitation could not be found using PRISM")
        mean_precip = mean_precip[0]
    except:
        # fall back on PCIC data
        mean_precip = get_annual_precipitation(area)
        logger.info("found PCIC annual precipitation: %s", mean_precip)
    else:
        logger.info("found PRISM annual precipitation: %s", mean_precip)

    return mean_precip
