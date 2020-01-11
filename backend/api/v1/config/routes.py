from logging import getLogger
from fastapi import APIRouter
from api.config import MAPBOX_ACCESS_TOKEN, MAPBOX_STYLE
import api.v1.catalogue.models as view_model

logger = getLogger("config")

router = APIRouter()


@router.get("/map", response_model=view_model.MapConfig)
def get_map_config():
    """
    Get config for frontend web map (e.g. access tokens)
    """

    return view_model.MapConfig(mapbox_token='pk.eyJ1IjoiaWl0LXdhdGVyIiwiYSI6ImNrMHBrZzczZjBlZ2UzZG54NTZldTRtdmUifQ.70prUCk1zBMUFnqfDSywYg', mapbox_style='mapbox://styles/iit-water/ck22hx0391ch31dk9amwwr67x')
