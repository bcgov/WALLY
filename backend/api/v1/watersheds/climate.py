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
import uuid
from sqlalchemy.orm import Session
from shapely.geometry import Polygon, mapping
from api.config import RASTER_FILE_DIR

logger = logging.getLogger('prism')

PRECIP_RASTER = f"{RASTER_FILE_DIR}/NORM_6190_Precip.tif"
PET_RASTER = f"{RASTER_FILE_DIR}/WNA_et0.tif"


def mean_annual_precipitation(area: Polygon) -> float:
    """
    Reads the precip in `area` from a PRISM raster (located at the S3 file
    location referenced by PRECIP_RASTER), and returns the mean of all values.
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
        precip_data = gdal.Warp(precip_file, '/vsis3/'+PRECIP_RASTER,
                                cutlineDSName=extents_file, cropToCutline=True,
                                dstNodata=-9999,
                                ).ReadAsArray()

        precip = precip_data[precip_data != -9999].mean().item()

        # clean up GDAL datasets
        precip_data = None
        gdal.Unlink(precip_file)

        elapsed = (time.perf_counter() - start)
        logger.info('Average precip %s - calculated in %s',
                    precip, elapsed)

    return precip


def get_evapotranspiration_trabucco(area: Polygon):
    """
    Retrieves potential evapotranspiration from the Global Aridity and PET database.

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
        pet_data = gdal.Warp(pet_file, '/vsis3/'+PET_RASTER,
                             cutlineDSName=extents_file, cropToCutline=True,
                             dstNodata=-32768,
                             ).ReadAsArray()

        # get mean of all valid cells (-32768 represents NoData)
        pet = pet_data[pet_data != -32768].mean().item()

        # clean up GDAL datasets
        pet_data = None
        gdal.Unlink(pet_file)

        elapsed = (time.perf_counter() - start)
        logger.info('Average pet %s - calculated in %s',
                    pet, elapsed)

    return pet
