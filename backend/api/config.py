import os
from osgeo import gdal
from pydantic import BaseSettings
from functools import lru_cache


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


# Environments
ENV_DEV = "DEV"
ENV_STAGING = "STAGING"
ENV_PROD = "PRODUCTION"

API_V1_STR = "/api/v1"

API_VERSION = os.getenv("API_VERSION", "1")
WALLY_VERSION = os.getenv("WALLY_VERSION", "0.0.0")
WALLY_ENV = os.getenv("WALLY_ENV", ENV_DEV)

SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")

# a string of origins separated by commas
# e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080"
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")
PROJECT_NAME = "Wally"
SENTRY_DSN = os.getenv("SENTRY_DSN")

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN", "")
MAPBOX_STYLE = os.getenv("MAPBOX_STYLE", "")

GWELLS_API_URL = os.getenv(
    "GWELLS_API_URL", "https://apps.nrs.gov.bc.ca/gwells")

COMMON_DOCGEN_CLIENT_ID = os.getenv("COMMON_DOCGEN_CLIENT_ID", "")
COMMON_DOCGEN_CLIENT_SECRET = os.getenv("COMMON_DOCGEN_CLIENT_SECRET", "")
COMMON_DOCGEN_SSO_ENDPOINT = os.getenv("COMMON_DOCGEN_SSO_ENDPOINT", "")
COMMON_DOCGEN_ENDPOINT = os.getenv("COMMON_DOCGEN_ENDPOINT", "")

BASE_DIR = '/app/'
CONFIG_DIR = BASE_DIR + '.config/'

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")
MINIO_HOST_URL = os.getenv("MINIO_HOST_URL", "127.0.0.1:9000")

WATERSHED_DEBUG = os.getenv("WATERSHED_DEBUG", True)
RASTER_FILE_DIR = 'raster'

AUTH_WELL_KNOWN_ENDPOINT = os.getenv("AUTH_WELL_KNOWN_ENDPOINT", "https://dev.loginproxy.gov.bc.ca/auth/realms/standard/.well-known/openid-configuration")
AUTH_CLIENT=os.getenv("AUTH_CLIENT", "wally-4389")
AUTH_CLIENT_APITEST=os.getenv("AUTH_CLIENT_APITEST", "wally-api-4845")
gdal.SetConfigOption('AWS_ACCESS_KEY_ID', MINIO_ACCESS_KEY)
gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', MINIO_SECRET_KEY)
gdal.SetConfigOption('AWS_S3_ENDPOINT', MINIO_HOST_URL)
gdal.SetConfigOption('AWS_HTTPS', 'FALSE')
gdal.SetConfigOption('AWS_VIRTUAL_HOSTING', 'FALSE')


class Settings(BaseSettings):
    """
    Use Pydantic's settings management
    """
    # Wally mapbox settings, to differentiate from constant declaration above
    w_mapbox_token = ""
    w_mapbox_style = ""

    # Feature flags
    # These are overridden by config file, so don't change these unless absolutely necessary
    external_import = False
    wally_model = False
    projects = False
    saved_analysis = False
    hydraulic_connectivity_custom_stream_points = False
    efn_analysis = False

    # allow users to select upstream catchment area delineation method.
    # default is False; WALLY will default to DEM+FWA which should be the best
    # estimate in all cases.  Other options are mostly for debugging intermediate steps.
    # see api/v1/watersheds/delineate_watershed.py for more info.
    surface_water_debug_upstream_method = False

    # Keep this set to true, we need to retire the old design
    surface_water_design_v2 = True

    # Other app settings
    sql_alchemy_debug = False
    local_development = False

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    env_file = f"{CONFIG_DIR}/{WALLY_ENV.lower()}.env"
    return Settings(_env_file=env_file)
