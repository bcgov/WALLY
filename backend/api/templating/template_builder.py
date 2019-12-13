from typing import List
import json
import api.templating.custom_builders as custom_builders
import api.templating.db as db
from sqlalchemy.orm import Session
import logging


logger = logging.getLogger("template_builder")


# This method builds a template object for each layer using default template data
# but also allows overwriting of the defaults by implementing a layer method in
# the api.template_builder.custom_builders file
def build_templates(session: Session, geojson_layers: List):

    layer_names = [l.layer for l in geojson_layers]
    templates = db.get_display_templates(session, layer_names)

    hydrated_templates = []

    # for layer in geojson_layers:
    #     # Get display templates from database for this layer
    #     templates = db.get_display_templates(session, layer.layer)

    for template in templates:
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
            hydrated_templates = sorted(hydrated_templates, key=lambda i: i['display_order'])

    return hydrated_templates


def default_builder(template, features):
    # logger.info(template)

    hydrated_template = {
        "title": template["display_template"].title,
        "display_order": template["display_template"].display_order,
        "display_data_names": template["display_template"].display_data_names,
        "display_components": []
    }

    charts = []
    for chart in template["charts"]:
        labels = []
        data_sets = [[]] * len(chart.dataset_keys)

        for feature in features:
            # logger.info(features)
            if chart.labels_key in feature.properties:
                labels.append(feature.properties[chart.labels_key])
                for d in range(len(chart.dataset_keys)):
                    if chart.dataset_keys[d] in feature.properties:
                        data_sets[d].append(feature.properties[chart.dataset_keys[d]])
                    else:
                        # if label_key exists but dataset_key does not, we want to add an empty
                        # data point so the labels don't go out of sync with the data points
                        data_sets[d].append(0)

        chart.chart["data"]["labels"] = labels
        for c in range(len(chart.chart["data"]["datasets"])):
            chart.chart["data"]["datasets"][c]["data"] = data_sets[c]

        if len(chart.chart["data"]["labels"]) > 0:
            result = {
                "title": chart.chart_title,
                "type": chart.component_type_code,
                "display_order": chart.display_order,
                "chart": chart.chart
            }
            # logger.info(result)
            charts.append(result)

    [hydrated_template["display_components"].append(c) for c in charts]

    links = []
    for link_component in template["links"]:
        link_group = {
            "title": link_component.link_title,
            "type": link_component.component_type_code,
            "display_order": link_component.display_order,
            "links": []
        }
        for feature in features:
            data = link_data(link_component.link_pattern_keys, feature.properties)
            if data is not None:
                link_group["links"].append({
                    "label": feature.properties[link_component.link_label_key],
                    "link": link_component.link_pattern.format(*data)
                })

        links.append(link_group)

    [hydrated_template["display_components"].append(l) for l in links]

    for image in template["images"]:
        pass

    for formula in template["formulas"]:
        pass

    hydrated_template["display_components"] = \
        sorted(hydrated_template["display_components"], key=lambda i: i['display_order'])

    return hydrated_template


def link_data(link_columns, properties):
    data = []
    for column in link_columns:
        # Check that both columns exist in props,
        # otherwise return None so no link is generated
        if column in properties:
            data.append(str(properties[column]))
        else:
            return None

    return data
