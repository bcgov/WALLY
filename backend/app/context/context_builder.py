from typing import List
import json
import app.context.transformers as transformers
import app.context.db as db
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger("context")


# This method builds a context object for each layer using default template data
# but also allows overwriting of the defaults by implementing a layer method in
# the app.context.transformers file
def build_context(session: Session, layers: List):
    contexts = {}
    for layer in layers:
        # Get cached context template from database
        context = db.get_context(session, layer.layer)

        # check for existing override transformer by matching method name to layer name
        if hasattr(transformers, layer.layer):
            # hydrate our context with custom transformer
            contexts[layer.layer] = \
                getattr(transformers, layer.layer)(context, layer.geojson.features)
        else:
            # hydrate our context using the default builder
            contexts[layer.layer] = default_builder(context, layer.geojson.features)

    return contexts


def default_builder(context, features):
    # load layer specific context
    context_data = json.loads(context.context)
    logger.info(context_data)
    for i in range(len(context_data)):

        if context_data[i]["type"] == "title":
            continue

        if context_data[i]["type"] == "chart":
            labels = []
            data_sets = [[]] * len(context_data[i]["data_columns"])
            for feature in features:
                labels.append(feature.properties[context_data[i]["label_column"]])

                for d in range(len(context_data[i]["data_columns"])):
                    data_sets[d].append(feature.properties[context_data[i]["data_columns"][d]])

                context_data[i]["chart"]["data"]["labels"] = labels

                for c in range(len(context_data[i]["chart"]["data"]["datasets"])):
                    context_data[i]["chart"]["data"]["datasets"][c]["data"] = data_sets[c]

        if context_data[i]["type"] == "links":
            links = []
            for feature in features:
                links.append(context_data[i]["link_pattern"].\
                    format(*link_data(context_data[i]["link_columns"], feature.properties)))
            context_data[i]["links"] = links

        if context_data[i]["type"] == "card":
            continue

        if context_data[i]["type"] == "table":
            continue

    # hydrate the layer context
    context.context = context_data

    return context


# Default builder currently supports links and multiple charts with single datasets
def default_builder2(context, features):
    links = []
    labels = [[]] * len(context.chart_label_columns)
    data = [[]] * len(context.chart_data_columns)

    # load layer specific context
    context_data = json.loads(context.context)

    # loop all features in result to build context data
    for feature in features:
        # add any external document site links
        links.append(context.link_pattern.format(*link_data(context.link_columns, feature.properties)))
        # add labels from label columns
        for i in range(len(context.chart_label_columns)):
            labels[i].append(feature.properties[context.chart_label_columns[i]])
        # add data from data columns
        for i in range(len(context.chart_data_columns)):
            data[i].append(feature.properties[context.chart_data_columns[i]])

    # update context values with column values
    context.links = links

    # hydrate chart data with created label and data lists
    # currently only one dataset per chart is supported
    for i in range(len(context_data["charts"])):
        if labels[i] is not None:
            context_data["charts"][i]["chart"]["data"]["labels"] = labels[i]
        if data[i] is not None:
            context_data["charts"][i]["chart"]["data"]["datasets"][0]["data"] = data[i]

    # hydrate the layer context
    context.context = context_data

    return context


def link_data(link_columns, props):
    data = []
    for column in link_columns:
        data.append(str(props[column]))

    return data
