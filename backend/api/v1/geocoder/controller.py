import re
import requests
from urllib.parse import urlencode
from fastapi import HTTPException
from sqlalchemy.orm import Session
from geojson import Feature, FeatureCollection
from logging import getLogger
from shapely.geometry import shape, mapping
from shapely.ops import transform

from api.config import GWELLS_API_URL
import api.v1.aggregator.controller as agr_repo
from api.v1.aggregator.controller import fetch_geojson_features, DATABC_LAYER_IDS as WFS_LAYER_IDS
from api.v1.aggregator.schema import WMSGetFeatureQuery, ExternalAPIRequest
from api.v1.aggregator.helpers import transform_3005_4326

logger = getLogger("geocoder")
search_symbols = re.compile(r'[^\w ]', re.UNICODE)
search_spaces = re.compile(r'[ ]+')

# Search strings will match against any of the fields provided in SEARCH_FIELDS.
WFS_SEARCH_FIELDS = {
    "cadastral": ["PARCEL_NAME"],
    "water_rights_licences": ["LICENCE_NUMBER", "FILE_NUMBER"],
    "water_rights_applications": ["FILE_NUMBER"],
    "aquifers": ["AQNAME", "AQUIFER_NAME"],
    "ecocat_water_related_reports": ["REPORT_ID", "TITLE"],
    "hydrometric_stations_databc": ["STATION_NAME", "STATION_NUMBER"]
}

# searches will make a request to these external URLs, if available for the layer type
EXTERNAL_API_SEARCH_URLS = {
    "groundwater_wells": f"{GWELLS_API_URL}/api/v2/wells/locations?limit=5&search="
}


def external_search(query, feature_type, url):
    """ Makes an external search request to a specified URL.  The url will have the search
        text appended to it. Returns geojson matches with extra data for the geocoder.
    """

    logger.info("using external API for feature lookup: %s", url + query)

    req = ExternalAPIRequest(
        url=url + query,
        layer=feature_type,
        q={},
        paginate=False
    )
    # Fetch features.
    feature_collection = fetch_geojson_features([req])

    features = feature_collection[0].geojson['features']
    geocoder_features = []

    for feature in features:
        feature['layer'] = feature_type
        feature['center'] = (feature.geometry.coordinates[0],
                             feature.geometry.coordinates[1])
        feature['place_name'] = str(feature.properties['well_tag_number'])
        geocoder_features.append(feature)

    return geocoder_features


def wfs_search(db, query, feature_type):
    """
        Get feature info and coordinates for features that match `query` for
        a given feature type. Returns geojson with extra metadata used by
        the geocoder.
    """

    logger.info("using WFS for feature lookup: %s", feature_type)

    # look up the DataBC layer ID.
    # first check in the WFS_LAYER_IDS constant defined above
    layer = WFS_LAYER_IDS.get(feature_type, None)

    # fall back on WMS metadata, if available
    if not layer:
        catalogue = agr_repo.get_display_catalogue(db, [feature_type])
        if not catalogue or not catalogue[0].wms_catalogue_id:
            raise HTTPException(status_code=400, detail="Feature type invalid")
        layer = catalogue[0].wms_catalogue.wms_name

    search_fields = WFS_SEARCH_FIELDS.get(feature_type, None)
    if not search_fields or not layer:
        raise HTTPException(status_code=400, detail="Feature type invalid")

    # form CQL filter.
    # note: this is not SQL, and this string will be sent over HTTP to a public server.
    # this doesn't automatically carry the same risks as forming a SQL string.
    cql_filter = f"{search_fields[0]} ILIKE '%{query}%'"

    # append additional filter statements if multiple search fields available.
    if len(search_fields) > 1:
        cql_filter = cql_filter + ' '.join([
            f"OR {field} ILIKE '%{query}%'" for field in search_fields[1:]
        ])

    query = WMSGetFeatureQuery(
        typeName=layer,
        count=5,
        cql_filter=cql_filter
    )
    req = ExternalAPIRequest(
        url=f"https://openmaps.gov.bc.ca/geo/pub/wfs?",
        layer=feature_type,
        q=query
    )

    # Fetch features.
    feature_collection = fetch_geojson_features([req])
    features = feature_collection[0].geojson['features']

    # create a collection to add processed features to.
    # this list will eventually be returned as geocoder results.
    geocoder_features = []

    for feature in features:

        # skip null geometries (e.g. a result with no coordinates)
        # todo: in the future we should ideally ask DataBC only for features
        # that can be placed on the map, but filtering on valid geom
        # does not work the same for all layers so it's harder to push
        # that requirement up to the API request.
        if not feature.geometry:
            continue

        # Some datasets in the DataBC API only output BC Albers (3005). Project
        # to SRID 4326 so we can get a representative point in lat/long degrees.
        geom = transform(transform_3005_4326, shape(feature.geometry))
        new_feature = Feature(geometry=mapping(geom.centroid))

        # add metadata to the feature. This info is required
        # for displaying and zooming to search results.
        new_feature['layer'] = feature_type
        new_feature['center'] = [geom.centroid.x, geom.centroid.y]
        new_feature['place_name'] = ' '.join([str(feature.properties.get(field, ''))
                                              for field in WFS_SEARCH_FIELDS[feature_type]])
        new_feature['id'] = feature['id']
        geocoder_features.append(new_feature)

    return geocoder_features


def lookup_feature(db: Session, query: str, feature_type: str) -> FeatureCollection:
    """ searches for feature locations using external APIs or internal data.
        will make use of DataBC, using layer names from the Wally metadata catalogue,
        unless another provider function is specified (e.g. for searching on GWELLS)
    """

    geocoder_features = []

    if feature_type in EXTERNAL_API_SEARCH_URLS.keys():
        geocoder_features = external_search(
            query, feature_type, EXTERNAL_API_SEARCH_URLS.get(feature_type))
    else:
        geocoder_features = wfs_search(db, query, feature_type)

    logger.info(geocoder_features)

    return FeatureCollection(geocoder_features)


def address_lookup(query: str) -> FeatureCollection:
    """ Looks up address using DataBC's geocoder """

    q = {
        "addressString": query,
        "autoComplete": "true",
        "maxResults": 5,
        "brief": "true"
    }

    search_url = "https://geocoder.api.gov.bc.ca/addresses.json?" + \
        urlencode(q)

    logger.info("using DataBC geocoder for feature lookup: %s", search_url)

    try:
        resp = requests.get(search_url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    features = resp.json().get('features')

    geocoder_features = []

    # add metadata to features
    for feat in features:
        new_geom = shape(feat['geometry'])
        new_feature = Feature(geometry=new_geom)

        # add mapbox-gl-js geocoder specific data
        # (used for populating search box)
        new_feature['layer'] = 'street_address'
        new_feature['center'] = new_geom.coords[0]
        new_feature['place_name'] = feat.get(
            'properties', {}).get('fullAddress')

        geocoder_features.append(new_feature)

    return FeatureCollection(geocoder_features)


def place_name_lookup(query: str) -> FeatureCollection:
    """ Looks up a place name using the DataBC GNIS name geocoder"""
    q = {
        "name": query,
        "exactSpelling": 0,
        "maxResults": 5,
        "sortBy": "relevance",
        "outputStyle": "summary",
        "outputSRS": 4326,
        "outputFormat": "json"
    }

    search_url = "https://apps.gov.bc.ca/pub/bcgnws/names/search?" + \
        urlencode(q)

    logger.info("using DataBC GNIS geocoder for feature lookup: %s", search_url)

    try:
        resp = requests.get(search_url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    features = resp.json().get('features')

    geocoder_features = []

    # add metadata to features
    for feat in features:
        new_geom = shape(feat['geometry'])
        new_feature = Feature(geometry=new_geom)

        # add mapbox-gl-js geocoder specific data
        # (used for populating search box)
        new_feature['layer'] = 'place_name'
        new_feature['center'] = new_geom.coords[0]
        new_feature['place_name'] = feat.get(
            'properties', {}).get('name')

        geocoder_features.append(new_feature)

    return FeatureCollection(geocoder_features)
