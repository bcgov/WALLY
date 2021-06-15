""" Functions for interacting with CDEM data to get median elevation for watershed areas
    CDEM data source:
    https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/
"""
import logging
from shapely.ops import transform
import time
from api.config import RASTER_FILE_DIR
from api.utils import get_raster_dataset
from api.db.utils import get_db_session
from api.v1.aggregator.helpers import transform_4326_4140
logger = logging.getLogger('cdem')


class CDEM:

    def __init__(self, polygon_4326):
        self.area4140 = transform(transform_4326_4140, polygon_4326)
        self.area4326 = polygon_4326
        self.db = get_db_session()

    def get_raster_summary_stats(self):
        """ finds the elevation stats summary from CDEM for a given area
            area should be a polygon with SRID 4140.
        """

        # Use ST_SummaryStats to find a summary of raster stats
        # https://postgis.net/docs/RT_ST_SummaryStats.html
        q = """
            select ST_SummaryStats(ST_Clip(cdem.rast,ST_GeomFromText(:area, 4140))) FROM dem.cdem
        """

        stats = self.db.execute(q, {"area": self.area4140.wkt})
        stats = stats.fetchone()
        if not stats:
            raise Exception(
                "elevation stats could not be found using CDEM")
        logger.info("found CDEM elevation stats: %s", stats)

        return stats

    def get_median_elevation(self):
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

        median_elev = self.db.execute(q, {"area": self.area4140.wkt})
        median_elev = median_elev.fetchone()
        if not median_elev or not median_elev[0]:
            raise Exception(
                "median elevation could not be found using CDEM")
        median_elev = median_elev[0]
        logger.info("found CDEM median elevation: %s", median_elev)

        return median_elev

    def get_average_slope(self):
        """ finds the mean slope in PERCENT from CDEM for a given area
            area should be a polygon with SRID 4140.
        """

        # Use ST_Slope to find the slope of a pixel
        # https://postgis.net/docs/RT_ST_Slope.html
        q = """
          SELECT 
            AVG((vc).value)
          FROM (
            SELECT ST_ValueCount(
              ST_Slope(
                ST_Clip(cdem.rast, ST_GeomFromText(:area, 4140)),
                1,             
                '32BF',        
                'PERCENT',     
                111120,        
                FALSE::boolean 
              )
            ) as vc
            FROM dem.cdem as cdem
          ) as foo
        """

        avg_slope_perc = self.db.execute(q, {"area": self.area4140.wkt})
        avg_slope_perc = avg_slope_perc.fetchone()
        if not avg_slope_perc or not avg_slope_perc[0]:
            raise Exception(
                "mean slope could not be found using CDEM")
        avg_slope_perc = avg_slope_perc[0]
        logger.info("found CDEM mean slope: %s", avg_slope_perc)

        return avg_slope_perc

    def get_mean_hillshade(self, area=None, retry_min_size=None):
        """
        Get the mean hillshade from an int16-based Hillshade raster.
        WALLY's hillshade raster was produced from 12 arcsecond CDEM
        and WhiteboxTools.

        https://github.com/jblindsay/whitebox-tools            
        """
        if not area:
            area = self.area4326
        start = time.perf_counter()

        hillshade_file = f"/vsis3/{RASTER_FILE_DIR}/BC_Area_Hillshade_3005.tif"
        no_data = -32768
        hillshade_data = get_raster_dataset(hillshade_file, area=area, no_data=no_data, retry_min_size=retry_min_size)
        hillshade_data = hillshade_data.ReadAsArray()

        mean_hillshade_int16 = hillshade_data[hillshade_data != no_data].mean()

        # scale down the hillshade value from 0-32767 to a percent value representing how much shade
        # our watershed gets.  32767 is the max possible value for our int16 hillshade raster.
        mean_hillshade = mean_hillshade_int16 / 32767
        elapsed = (time.perf_counter() - start)
        logger.info('HILLSHADE BY TIF %s - calculated in %s',
                    mean_hillshade, elapsed)
        hillshade_data = None
        return mean_hillshade
