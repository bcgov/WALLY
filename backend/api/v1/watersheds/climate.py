""" Functions for interacting with climate data to get precipitation and potential
    evapotranspiration means for watershed areas




    Raster files must be in the /backend/fixtures/raster directory. See PRECIP_RASTER and PET_RASTER
    constants for the filenames. The files should be packaged as Cloud Optimized GeoTIFFs (COG) in
    the EPSG:4326 lat/lng coordinate system.

    See api/v1/watersheds/README.md for instructions on creating the GeoTIFF files.
"""
import logging
from tempfile import TemporaryDirectory
from osgeo import gdal
import fiona
import time
import math
import uuid
from typing import Optional
from shapely.ops import transform
from shapely.geometry import Polygon, Point, mapping
from api.v1.watersheds import PRECIP_RASTER, PET_RASTER
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326

logger = logging.getLogger('climate')


def new_polygon(centroid: Point, size_sqm: float = 5e6):
    """
    Returns a new polygon centered at `centroid` with area `size_sqm` (sq. m)
    centroid should be EPSG:4326
    """

    centroid_3005 = transform(transform_4326_3005, centroid)

    side = math.sqrt(size_sqm)

    poly = Polygon((
        (centroid_3005.x - side/2, centroid_3005.y - side/2),
        (centroid_3005.x + side/2, centroid_3005.y - side/2),
        (centroid_3005.x + side/2, centroid_3005.y + side/2),
        (centroid_3005.x - side/2, centroid_3005.y + side/2),
        (centroid_3005.x - side/2, centroid_3005.y - side/2),
    ))

    return transform(transform_3005_4326, poly)


def get_mean_annual_precipitation(
    area: Polygon,
    raster: str = "/vsis3/"+PRECIP_RASTER,
    retry_min_size: Optional[float] = None
) -> float:
    """
    Reads the precip in `area` from a PRISM raster (located at the path provided by the
    `precip_raster` argument), and returns the mean of all values.

    `raster` can be a file path or a GDAL virtual filesystem path.
    /vsis3/ is pre-configured for WALLY's Minio storage.
    example:  "/vsis3/raster/NORM_6190_Precip.tif"
    """
    start = time.perf_counter()

    with TemporaryDirectory() as rasterdir:
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

        # create a unique file for GDAL's /vsimem/ in-memory file system
        precip_file = "/vsimem/precip" + str(uuid.uuid4()) + ".tif"

        # open the Cloud Optimized GeoTIFF from Minio, returning a dataset
        # clipped to the watershed extents, and convert to numpy array.
        precip_data = gdal.Warp(precip_file, raster,
                                cutlineDSName=extents_file, cropToCutline=True,
                                dstNodata=-9999,
                                )

        if not precip_data and retry_min_size:
            retry_area_sqm = retry_min_size
            logger.warning('Area was too small to sample a pixel.  Retrying with a %s sq km square', retry_area_sqm/1e6)
            retry_area = new_polygon(area.centroid, size_sqm=retry_area_sqm)
            return get_mean_annual_precipitation(retry_area, raster=raster, retry_min_size=2*retry_min_size)

        precip_data = precip_data.ReadAsArray()

        precip = precip_data[precip_data != -9999].mean().item()

        # clean up GDAL datasets
        precip_data = None
        gdal.Unlink(precip_file)

        elapsed = (time.perf_counter() - start)
        logger.info('Average precip %s - calculated in %s',
                    precip, elapsed)

    return precip


def get_potential_evapotranspiration(
    area: Polygon,
    raster: str = "/vsis3/"+PET_RASTER,
    retry_min_size: Optional[float] = None
) -> float:
    """
    Retrieves potential evapotranspiration from the Global Aridity and PET database.
    The data should be a raster file (sourced from the annual_et0 PET dataset).

    `raster` can be a file path or a GDAL virtual filesystem path.
    /vsis3/ is pre-configured for WALLY's Minio storage.
    example:  "/vsis3/raster/WNA_et0.tif"

    Trabucco, Antonio; Zomer, Robert (2019): Global Aridity Index and Potential
    Evapotranspiration (ET0) Climate Database v2. figshare. Dataset.
    https://doi.org/10.6084/m9.figshare.7504448.v3 
    https://cgiarcsi.community/data/global-aridity-and-pet-database/



    """
    start = time.perf_counter()

    with TemporaryDirectory() as rasterdir:
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

        # create a unique file for GDAL's /vsimem/ in-memory file system
        pet_file = "/vsimem/pet" + str(uuid.uuid4()) + ".tif"

        # open the Cloud Optimized GeoTIFF from Minio, returning a dataset
        # clipped to the watershed extents, and convert to numpy array.
        pet_data = gdal.Warp(pet_file, raster,
                             cutlineDSName=extents_file, cropToCutline=True,
                             dstNodata=-32768,
                             )

        if not pet_data and retry_min_size:
            retry_area_sqm = retry_min_size
            logger.warning('Area was too small to sample a pixel.  Retrying with a %s sq km square', retry_area_sqm/1e6)
            retry_area = new_polygon(area.centroid, size_sqm=retry_area_sqm)
            return get_potential_evapotranspiration(retry_area, raster=raster, retry_min_size=2*retry_min_size)

        pet_data = pet_data.ReadAsArray()

        # get mean of all valid cells (-32768 represents NoData)
        pet = pet_data[pet_data != -32768].mean().item()

        # clean up GDAL datasets
        pet_data = None
        gdal.Unlink(pet_file)

        elapsed = (time.perf_counter() - start)
        logger.info('Average pet %s - calculated in %s',
                    pet, elapsed)

    return pet
