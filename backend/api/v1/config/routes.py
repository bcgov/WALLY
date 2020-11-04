from logging import getLogger
from fastapi import APIRouter
from api.config import MAPBOX_ACCESS_TOKEN, MAPBOX_STYLE
from api.config import WALLY_VERSION, WALLY_ENV, API_VERSION
import api.v1.config.schema as schema

from api.config import get_settings

logger = getLogger("config")

router = APIRouter()


@router.get("/map", response_model=schema.MapConfig)
def get_map_config():
    """
    Get config for frontend web map (e.g. access tokens)
    """

    settings = get_settings()

    access_token = settings.w_mapbox_token if settings.w_mapbox_token else MAPBOX_ACCESS_TOKEN
    style = settings.w_mapbox_style if settings.w_mapbox_style else MAPBOX_STYLE

    return schema.MapConfig(mapbox_token=access_token, mapbox_style=style)


# TODO: Debating on this being in config/version or system/info or system/version
@router.get("/version", response_model=schema.VersionConfig)
def get_wally_version():
    return {
        'wally_version': WALLY_VERSION,
        'wally_env': WALLY_ENV,
        'api_version': API_VERSION,
    }


@router.get("/")
def get_config():
    return get_settings()
