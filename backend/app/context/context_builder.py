from typing import List
import app.context.transformers as t
import app.context.db as db
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger("context")


# CONTEXT_MAP = {
#     "automated_snow_weather_station_locations": streams_repo.get_stations_as_geojson,
#     "bc_wildfire_active_weather_stations":
# }

# This method builds a context object for each layer using default template data
# but also allows overwriting of the defaults by implementing a layer method in
# the app.context.transformers file
def build_context(session: Session, layers: List):
    contexts = {}
    for layer in layers:
        # Get cached context template from database
        context = db.get_context(session, layer.layer)
        # Create hydrated context object using the layer transformer method
        contexts[layer.layer] = getattr(t, layer.layer)(context, layer.geojson.features)

    return contexts
