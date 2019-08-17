from typing import List
import app.context.transformers as t
import app.context.db as db

import logging


logger = logging.getLogger("context")


# CONTEXT_MAP = {
#     "automated_snow_weather_station_locations": streams_repo.get_stations_as_geojson,
#     "bc_wildfire_active_weather_stations":
# }


def build_context(features: List):
    contexts = []
    for feature in features:
        context = db.get_context(feature.layer)
        contexts.append(getattr(t, feature.layer)(context, feature.geojson.features))

    return contexts



