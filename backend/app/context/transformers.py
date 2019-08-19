import logging
import json

logger = logging.getLogger("context")


def ground_water_wells(context, features):
    links = []
    labels = []
    data = []
    for f in features:
        links.append(context.link_pattern.format(*link_data(context.link_columns, f)))
        labels.append(f.properties["LOCATION_NAME"])
        data.append(f.properties["ELEVATION"])


def automated_snow_weather_station_locations(context, features):
    links = []
    labels = []
    data = []

    # loop all features in result to build context data
    for feature in features:
        links.append(context.link_pattern.format(*link_data(context.link_columns, feature.properties)))
        labels.append(feature.properties["LOCATION_NAME"])
        data.append(feature.properties["ELEVATION"])

    # load layer specific context
    context_data = json.loads(context.context)

    # update context values with column values
    context.links = links
    context_data["chart"]["data"]["labels"] = labels
    context_data["chart"]["data"]["datasets"][0]["data"] = data

    # hydrate the db context with the hydrated values
    context.context = context_data

    return context


# def format_links(context, features):


def link_data(link_columns, props):
    data = []
    for c in link_columns:
        data.append(str(props[c]))
    return data
