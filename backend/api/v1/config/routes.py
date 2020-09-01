from logging import getLogger
from fastapi import APIRouter
from api.config import MAPBOX_ACCESS_TOKEN, MAPBOX_STYLE
from api.config import WALLY_VERSION, WALLY_ENV, API_VERSION
import api.v1.catalogue.models as view_model
import api.v1.config.schema as config_schema

from api.config import get_settings

logger = getLogger("config")

router = APIRouter()


@router.get("/map", response_model=view_model.MapConfig)
def get_map_config():
    """
    Get config for frontend web map (e.g. access tokens)
    """

    return view_model.MapConfig(mapbox_token=MAPBOX_ACCESS_TOKEN, mapbox_style=MAPBOX_STYLE)


# TODO: Debating on this being in config/version or system/info or system/version
@router.get("/version", response_model=config_schema.VersionConfig)
def get_wally_version():
    return {
        'wally_version': WALLY_VERSION,
        'wally_env': WALLY_ENV,
        'api_version': API_VERSION,
    }


@router.get("/")
def get_config():
    return get_settings()
