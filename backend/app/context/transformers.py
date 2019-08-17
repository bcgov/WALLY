

def ground_water_wells(context, features):
    links = []
    labels = []
    data = []
    for f in features:
        links.append(context.link.format(link_data(context.link_columns, f)))
        labels.append(f.properties["LOCATION_NAME"])
        data.append(f.properties["ELEVATION"])


def automated_snow_weather_station_locations(context, features):
    links = []
    labels = []
    data = []
    for f in features:
        links.append(context.link.format(link_data(context.link_columns, f)))
        labels.append(f.properties["LOCATION_NAME"])
        data.append(f.properties["ELEVATION"])

    context.links = links
    context.chart.data.labels = labels
    context.chart.data.datasets[0].data = data

    return context


def link_data(link_columns, feature):
    data = {}
    for c in link_columns:
        data[c] = feature[c]
    return data
