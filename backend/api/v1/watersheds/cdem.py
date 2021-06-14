""" Functions for interacting with CDEM data to get median elevation for watershed areas
    CDEM data source:
    https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/
"""
import logging
from sqlalchemy.orm import Session
from shapely.geometry import Polygon, mapping
from shapely.ops import transform
import math
import time
import fiona
from osgeo import gdal
from tempfile import TemporaryDirectory
from api.config import RASTER_FILE_DIR, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST_URL
from api.db.utils import get_db_session
from api.v1.aggregator.helpers import transform_4326_4140, transform_4326_3005
from api.v1.watersheds.climate import new_polygon
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
        if not area:
            area = self.area4326
        start = time.perf_counter()

        with TemporaryDirectory() as rasterdir:
            hillshade_in_file = f"/vsis3/{RASTER_FILE_DIR}/BC_Area_Hillshade_3005.tif"
            extents_file = rasterdir + "/extents.shp"

            # Define a Polygon feature geometry with one attribute
            poly_schema = {
                'geometry': 'Polygon',
                'properties': {'id': 'int'},
            }

            # Write a new Shapefile with the envelope.
            with fiona.open(extents_file, 'w', 'ESRI Shapefile', poly_schema, crs=f"EPSG:4326") as c:
                c.write({
                    'geometry': mapping(area),
                    'properties': {'id': 1},
                })

            hillshade_data = gdal.Warp("", hillshade_in_file, format="MEM",
                                       cutlineDSName=extents_file, cropToCutline=True,
                                       dstNodata=-32768,
                                       )
            if not hillshade_data and retry_min_size:
                retry_area_sqm = retry_min_size
                logger.warning(
                    'get_mean_hillshade: Area was too small to sample a pixel.  Retrying with a %s sq km square',
                    retry_area_sqm / 1e6)
                retry_area = new_polygon(area.centroid, size_sqm=retry_area_sqm)
                return self.get_mean_hillshade(area=retry_area, retry_min_size=2*retry_min_size)

            hillshade_data = hillshade_data.ReadAsArray()

            mean_hillshade_int16 = hillshade_data[hillshade_data != -32768].mean()
            mean_hillshade = mean_hillshade_int16 / 32767
            elapsed = (time.perf_counter() - start)
            logger.info('HILLSHADE BY TIF %s - calculated in %s',
                        mean_hillshade, elapsed)
            hillshade_data = None
        return mean_hillshade

    def get_mean_time_in_daylight(self, area=None, retry_min_size=None):
        if not area:
            area = self.area4326
        start = time.perf_counter()

        with TemporaryDirectory() as rasterdir:
            time_in_daylight_in_file = f"/vsis3/{RASTER_FILE_DIR}/BC_Area_TimeInDaylight_3005.tif"
            extents_file = rasterdir + "/extents.shp"

            # Define a Polygon feature geometry with one attribute
            poly_schema = {
                'geometry': 'Polygon',
                'properties': {'id': 'int'},
            }

            # Write a new Shapefile with the envelope.
            with fiona.open(extents_file, 'w', 'ESRI Shapefile', poly_schema, crs=f"EPSG:4326") as c:
                c.write({
                    'geometry': mapping(self.area4326),
                    'properties': {'id': 1},
                })

            time_in_daylight_data = gdal.Warp("", time_in_daylight_in_file, format="MEM",
                                              cutlineDSName=extents_file, cropToCutline=True,
                                              dstNodata=-32768,
                                              )

            if not time_in_daylight_data and retry_min_size:
                retry_area_sqm = retry_min_size
                logger.warning(
                    'get_mean_time_in_daylight: Area was too small to sample a pixel.  Retrying with a %s sq km square',
                    retry_area_sqm / 1e6)
                retry_area = new_polygon(area.centroid, size_sqm=retry_area_sqm)
                return self.get_mean_time_in_daylight(area=retry_area, retry_min_size=2*retry_min_size)

            time_in_daylight_data = time_in_daylight_data.ReadAsArray()

            time_in_daylight = time_in_daylight_data[time_in_daylight_data != -32768].mean(
            ).item()
            elapsed = (time.perf_counter() - start)
            logger.info('TIME IN DAYLIGHT BY TIF %s - calculated in %s',
                        time_in_daylight, elapsed)
            time_in_daylight_data = None
        return time_in_daylight
