""" Functions for interacting with climate data to get precipitation and potential
    evapotranspiration means for watershed areas




    Raster files must be in the /backend/fixtures/raster directory. See PRECIP_RASTER and PET_RASTER
    constants for the filenames. The files should be packaged as Cloud Optimized GeoTIFFs (COG) in
    the EPSG:4326 lat/lng coordinate system.

    See api/v1/watersheds/README.md for instructions on creating the GeoTIFF files.
"""
import logging
import time
from typing import Optional
from shapely.geometry import Polygon
from api.utils import get_raster_dataset
from api.v1.watersheds import PRECIP_RASTER, PET_RASTER

logger = logging.getLogger('climate')


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

    no_data = -9999

    # get a clipped raster covering `area` and read into a Numpy array
    precip_data = get_raster_dataset(raster, area=area, no_data=no_data, retry_min_size=retry_min_size).ReadAsArray()

    # find mean using Numpy
    precip = precip_data[precip_data != no_data].mean().item()

    # clean up GDAL datasets
    precip_data = None

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
    no_data = -32768

    # get a clipped raster for `area` and read into a Numpy array
    pet_data = get_raster_dataset(raster, area=area, no_data=no_data, retry_min_size=retry_min_size).ReadAsArray()

    # get mean of all valid cells
    pet = pet_data[pet_data != no_data].mean().item()

    # clean up GDAL datasets
    pet_data = None

    elapsed = (time.perf_counter() - start)
    logger.info('Average pet %s - calculated in %s',
                pet, elapsed)

    return pet
