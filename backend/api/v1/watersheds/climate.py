""" Functions for interacting with climate data to get precipitation and potential
    evapotranspiration means for watershed areas

    Climate WNA/PRISM data source:
    Hamann, A. and Wang, T., Spittlehouse, D.L., and Murdock, T.Q. 2013. A comprehensive,
    high-resolution database of historical and projected climate surfaces for western
    North America. Bulletin of the American Meteorological Society 94: 1307–1309.
    Retrieved from https://sites.ualberta.ca/~ahamann/data/climatewna.html on June 10, 2021
    
    Potential evapotranspiration:
    Trabucco, Antonio; Zomer, Robert (2019): Global Aridity Index and Potential
    Evapotranspiration (ET0) Climate Database v2. figshare. Dataset.
    https://doi.org/10.6084/m9.figshare.7504448.v3 
    Retrieved from https://cgiarcsi.community/data/global-aridity-and-pet-database/ on June 10, 2021


    Raster files must be in the /backend/fixtures/raster directory. See PRECIP_RASTER and PET_RASTER
    constants for the filenames. The files should be packaged as Cloud Optimized GeoTIFFs (COG) in
    the EPSG:4326 lat/lng coordinate system.

    Creating the COG tif files:

    Climate WNA precipitation:
    1.  Download the annual bioclimate variables file
        (http://www.cacpd.org.s3.amazonaws.com/climate_normals/NORM_6190_Bioclim_ASCII.zip)

    2.  Convert the MAP file (mean annual precipitation) to EPSG:4326:
        `gdalwarp -t_srs EPSG:4326 NORM_6190_MAP.tif precip.tif`
    
    3.  Convert the resulting file to a COG:
        `gdal_translate -of COG -co COMPRESS=LZW precip.tif NORM_6190_Precip.tif`
    
    4.  Upload the file to WALLY Staging and Prod Minio

    Potential evapotranspiration:
    1.  Download the database from the Global Aridity and PET link above. Unzip
        the file and then unzip the annual et0 file inside.
    
    2.  Optional, but recommended:  use QGIS to get the extents of the above Climate WNA file,
        and clip the annual_et0.tif file.  The annual_et0.tif file has global coverage that we
        don't need.  Ensure the clipped area includes parts of Washington, Idaho, Alaska etc
        that BC watersheds originate in (e.g. Chilliwack River).

    3.  Follow the instructions 2-4 for ClimateWNA to convert annual_et0.tif to EPSG:4326 and create a
        COG tif file named WNA_et0.tif.

    Fixtures:
    1.  Use the /backend/fixtures/extents file to clip Whistler area rasters for /backend/fixtures/raster.


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
from api.v1.watersheds.schema import MonthlyTemperatureMinMax

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
