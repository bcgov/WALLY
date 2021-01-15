import os
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
BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080"
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
    "GWELLS_API_URL", "https://gwells-prod.pathfinder.gov.bc.ca/gwells")

COMMON_DOCGEN_CLIENT_ID = os.getenv("COMMON_DOCGEN_CLIENT_ID", "")
COMMON_DOCGEN_CLIENT_SECRET = os.getenv("COMMON_DOCGEN_CLIENT_SECRET", "")
COMMON_DOCGEN_SSO_ENDPOINT = os.getenv("COMMON_DOCGEN_SSO_ENDPOINT", "")
COMMON_DOCGEN_ENDPOINT = os.getenv("COMMON_DOCGEN_ENDPOINT", "")

BASE_DIR = '/app/'
CONFIG_DIR = BASE_DIR + '.config/'

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_HOST_URL = os.getenv("MINIO_HOST_URL", "minio:9000")

WATERSHED_DEBUG = os.getenv("WATERSHED_DEBUG", False)

# Use Pydantic's settings management
class Settings(BaseSettings):
    external_import = False
    external_import_types = ""

    wally_model = False
    surface_water_design_v2 = True

    projects = False

    # Wally mapbox settings, to differentiate from constant declaration above
    w_mapbox_token = ""
    w_mapbox_style = ""

    hydraulic_connectivity_custom_stream_points = False

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    env_file = f"{CONFIG_DIR}/{WALLY_ENV.lower()}.env"
    return Settings(_env_file=env_file)
