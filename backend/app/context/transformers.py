import logging
import json

logger = logging.getLogger("context")


# def ground_water_wells(context, features):
#     links = []
#     yield_chart_labels = []
#     yield_chart_data = []
#     depth_chart_labels = []
#     depth_chart_data = []
#     for feature in features:
#         links.append(context.link_pattern.format(*link_data(context.link_columns, feature)))
#         yield_chart_labels.append(feature.properties["WELL_TAG_NUMBER"])
#         yield_chart_data.append(feature.properties["YIELD_VALUE"])
#         depth_chart_labels.append(feature.properties["WELL_TAG_NUMBER"])
#         depth_chart_data.append(feature.properties["DEPTH_WELL_DRILLED"])

#     # load layer specific context
#     context_data = json.loads(context.context)

#     # update context values with column values
#     context.links = links
#     context_data["chart"]["data"]["labels"] = labels
#     context_data["chart"]["data"]["datasets"][0]["data"] = data

#     # hydrate the db context with the hydrated values
#     context.context = context_data

#     return context


# def automated_snow_weather_station_locations(context, features):
#     links = []
#     labels = []
#     data = []

#     # loop all features in result to build context data
#     for feature in features:
#         links.append(context.link_pattern.format(*link_data(context.link_columns, feature.properties)))
#         labels.append(feature.properties["LOCATION_NAME"])
#         data.append(feature.properties["ELEVATION"])

#     # load layer specific context
#     context_data = json.loads(context.context)

#     # update context values with column values
#     context.links = links
#     context_data["chart"]["data"]["labels"] = labels
#     context_data["chart"]["data"]["datasets"][0]["data"] = data

#     # hydrate the db context with the hydrated values
#     context.context = context_data

#     return context


# def link_data(link_columns, props):
#     data = []
#     for c in link_columns:
#         data.append(str(props[c]))
#     return data
