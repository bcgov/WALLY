from typing import List
import json
import app.templating.custom_builders as custom_builders
import app.templating.db as db
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger("template_builder")


# This method builds a template object for each layer using default template data
# but also allows overwriting of the defaults by implementing a layer method in
# the app.template_builder.custom_builders file
def build_templates(session: Session, geojson_layers: List):
    # logger.info(geojson_layers)

    layer_names = [l.layer for l in geojson_layers]
    templates = db.get_display_templates(session, layer_names)

    hydrated_templates = []

    # for layer in geojson_layers:
    #     # Get display templates from database for this layer
    #     templates = db.get_display_templates(session, layer.layer)

    for template in templates:
        logger.info(template)
        override_key = template["display_template"].override_key
        # check for custom_builder matching method name to layer name
        if override_key is not None and hasattr(custom_builders, override_key):
            # hydrate our template with custom transformer
            hydrated_templates.append(
                getattr(custom_builders, override_key)(template, geojson_layers)
            )
        else:
            # hydrate our template using the default builder
            # TODO ** Add support for multi-layer templates **
            # use override key in that case and map data from geojson_layers
            geojson_layer = next((x for x in geojson_layers if x.layer ==
                                  template["display_template"].display_data_names[0]), None)

            hydrated_templates.append(
                default_builder(template, geojson_layer.geojson.features)
            )

    return hydrated_templates


def default_builder(template, features):
    logger.info(template)

    hydrated_template = {
        "title": template["display_template"].title,
        "display_order": template["display_template"].display_order,
        "display_data_names": template["display_template"].display_data_names
    }

    charts = []
    for chart in template["charts"]:
        labels = []
        data_sets = [[]] * len(chart.dataset_keys)
        for feature in features:
            logger.info(feature)
            labels.append(feature.properties[chart.labels_key])
            for d in range(len(chart.dataset_keys)):
                data_sets[d].append(feature.properties[chart.dataset_keys[d]])

        chart.chart["data"]["labels"] = labels
        for c in range(len(chart.chart["data"]["datasets"])):
            chart.chart["data"]["datasets"][c]["data"] = data_sets[c]

        result = {
            "title": chart.title,
            "display_order": chart.display_order,
            "chart": chart.chart
        }
        charts.append(result)

    hydrated_template["charts"] = charts

    links = []
    for link_component in template["links"]:
        link_group = {
            "title": link_component.title,
            "display_order": link_component.display_order,
            "links": []
        }
        for feature in features:
            link_group["links"].append(link_component.link_pattern
                         .format(*link_data(link_component.link_pattern_keys, feature.properties)))

        links.append(link_group)

    hydrated_template["links"] = links

    for image in template["images"]:
        pass

    for formula in template["formulas"]:
        pass

    logger.info(hydrated_template)

    return hydrated_template


def link_data(link_columns, props):
    data = []
    for column in link_columns:
        data.append(str(props[column]))

    return data
