"""
Functions for aggregating data from web requests and database records
"""
import logging
import asyncio
import json
import logging
import requests
from typing import List
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from aiohttp import ClientSession, ClientResponse
from shapely.geometry import Polygon, MultiPolygon, shape, box
from shapely.ops import transform
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload
from fastapi import HTTPException

from api.v1.catalogue.db_models import DisplayCatalogue
from api.v1.hydat.db_models import Station as StreamStation
from api.v1.aggregator.helpers import gwells_api_request, transform_4326_3005, transform_3005_4326
from api.v1.aggregator.schema import ExternalAPIRequest, LayerResponse, WMSGetFeatureQuery
from api.layers.freshwater_atlas_stream_networks import FreshwaterAtlasStreamNetworks
from api.layers.normal_annual_runoff_isolines import NormalAnnualRunoffIsolines

logger = logging.getLogger("aggregator")

# returns a module or class that has `get_as_geojson` and `get_details` functions for looking up data from a layer
# NOTE: this dict used to have a line for all layers. Removing (or commenting) will cause the aggregator function to
# fall back fetching data on the fly from DataBC, as long as DATABC_LAYER_IDS or a wms_catalogue database entry
# exists for that layer.
API_DATASOURCES = {
    "HYDAT": StreamStation,
    "hydrometric_stream_flow": StreamStation,
    "freshwater_atlas_stream_networks": FreshwaterAtlasStreamNetworks,
    "normal_annual_runoff_isolines": NormalAnnualRunoffIsolines
}

# For external APIs that may require different parameters (e.g. not a WMS/GeoServer with
# relatively consistent request params), add a helper function that returns an ExternalAPIRequest
# object.
EXTERNAL_API_REQUESTS = {
    "groundwater_wells": gwells_api_request
}


# DATABC_LAYER_IDS maps layer names to DataBC API Catalogue layers.
# This information can also be kept on the database table metadata.wms_catalogue,
# and the lookup_feature function will also check there. However, there are issues
# with having a wms_catalogue record for layers we intend to use as vector layers.
# DATABC_LAYER_IDS provides an alternative for the purpose of DataBC WFS lookups in
# this file.
DATABC_LAYER_IDS = {
    "cadastral": "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW",
    "aquifers": "WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW",
    "water_rights_licences": "WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV",
    "water_rights_applications": "WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_APPLICTNS_SV",
    "fn_treaty_areas": "WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_AREA_SP",
    "fn_community_locations": "WHSE_HUMAN_CULTURAL_ECONOMIC.FN_COMMUNITY_LOCATIONS_SP",
    "fn_treaty_lands": "WHSE_LEGAL_ADMIN_BOUNDARIES.FNT_TREATY_LAND_SP",
    "bc_major_watersheds": "WHSE_BASEMAPPING.BC_MAJOR_WATERSHEDS",
    "freshwater_atlas_glaciers": "WHSE_BASEMAPPING.FWA_GLACIERS_POLY",
    "runoff_isolines": "WHSE_WATER_MANAGEMENT.HYDZ_ANNUAL_RUNOFF_LINE"
}


# DataBC names geometry fields either GEOMETRY or SHAPE
# We will assume GEOMETRY, except for layers listed here.
DATABC_GEOMETRY_FIELD = {
    "water_rights_licences": "SHAPE",
    "water_rights_applications": "SHAPE",
    "automated_snow_weather_station_locations": "SHAPE",
    "bc_wildfire_active_weather_stations": "SHAPE",
    "critical_habitat_species_at_risk": "SHAPE",
    "cadastral": "SHAPE",
    "fn_treaty_areas": "GEOMETRY",
    "fn_community_locations": "SHAPE",
    "fn_treaty_lands": "GEOMETRY",
}


def build_api_query(req: ExternalAPIRequest) -> str:
    """ build_api_query takes a ExternalAPIRequest object and returns a URL with query params """

    # if the query options weren't specified, return the url without
    # adding to it.
    if not req.q:
        return req.url

    base_url = req.url

    if not base_url.endswith('?'):
        base_url += '?'

    return base_url + urlencode(dict(req.q))


async def parse_result(res: ClientResponse, req: ExternalAPIRequest):
    """ parse_result takes an API response and returns features """
    body = await res.read()
    features = []
    data = {}
    fc = {}
    next_url = None

    # try to load the response body.
    # if it's not JSON (e.g. xml, an html error page, etc.), it will fail
    # with a TypeError. In this case, we just continue with the defaults
    # set above.
    try:
        data = json.loads(body)
    except TypeError as e:
        logger.error(e)
    except json.JSONDecodeError as e:
        logger.error(e)

    crs = None

    # check if data looks like a geojson FeatureCollection, and if so,
    # make proper Features out of all the objects
    if (res.status == 200 and
        hasattr(data, "get") and
        "type" in data and
        data.get("type") == "FeatureCollection" and
            "features" in data):
        for feat in data["features"]:
            features.append(Feature(id=feat.pop('id', None), geometry=feat.pop(
                'geometry'), properties=feat.pop('properties', {})))

        # CRS for this set of results. DataBC results have a crs specified in the FeatureCollection
        # that indicates the projection of geometry in the collection.
        if data.get("crs"):
            crs = data.get("crs")

    # if we didn't recognize a geojson response, check if a formatter was supplied to create geojson.
    elif res.status == 200 and req.formatter and len(data) > 0:
        features = req.formatter(data)['features']

    if data.get('next', None) and data.get('results', None):
        next_url = data['next']

    return features, res.status, next_url, crs


async def fetch_results(req: ExternalAPIRequest, session: ClientSession) -> LayerResponse:
    """ asyncronously fetch results.
        note: follows "next" urls for paginated responses and combines the results.
    """
    url = build_api_query(req)

    next_url = url

    layer_resp = LayerResponse(
        status=0,
        layer=req.layer,
        geojson=FeatureCollection(features=[])
    )

    i = 0
    MAX_PAGES = 20
    features = []

    # CRS for this set of results. DataBC results have a crs specified in the FeatureCollection.
    # there is no assertion that in any given set of paginated results that the CRS is
    # identical for each page. Currently the last page sets the CRS.
    crs = None

    # make request, and follow URLs for the next page if the response is paginated
    # and "next" is provided in the response.
    # continue to make requests until there is no "next" url.
    while next_url:
        i += 1

        # stop request here if MAX_PAGES was exceeded. User should be notified immediately
        # so that it's clear that there were more results available but we didn't retrieve them.
        # note: MAX_PAGES is meant to be a safety to prevent looping indefinitely; it could be
        # increased based on user needs.
        if i > MAX_PAGES:
            raise HTTPException(
                status_code=400, detail=f"Too many results in search area ({req.layer}). Please try again using a smaller area.")

        logger.info('external request: %s', next_url)
        async with session.get(next_url) as response:
            results, status, next_url, crs = await asyncio.ensure_future(parse_result(response, req))
            features.extend(results)
            # preserve error statuses even if a later request returns 200 OK
            if layer_resp.status < status:
                layer_resp.status = status

        # if pagination is disabled, stop here.
        if not req.paginate:
            break

    layer_resp.geojson = FeatureCollection(features=features, crs=crs)
    return layer_resp


async def batch_fetch(
        semaphore: asyncio.Semaphore,
        req: ExternalAPIRequest,
        session: ClientSession) -> asyncio.Future:
    """
    batch_fetch uses a semaphore to make batched requests in parallel
    (up a limit equal to the size of the semaphore).
    """

    # The semaphore will block at the limit, and not make any more requests until
    # the first requests return, keeping the number of active requests bounded.
    async with semaphore:
        return await fetch_results(req, session)


async def fetch_all(requests: List[ExternalAPIRequest]) -> asyncio.Future:
    """
    fetch_all collects features from multiple sources, provided in a list
    of ExternalAPIRequest objects. It returns a "future" iterable. This function can
    be run with asyncio.run(fetch_all(requests)), which will block until
    all the requests are complete.
    """
    tasks = []
    semaphore = asyncio.Semaphore(10)
    headers = {'accept': 'application/json'}

    async with ClientSession(headers=headers) as session:
        for req in requests:
            # use the list of ExternalAPIRequests to form URLs and start adding the requests to the
            # request queue.
            task = asyncio.ensure_future(
                batch_fetch(semaphore, req, session))
            tasks.append(task)

        # return the gathered tasks, which will be a list of JSON responses when all requests return.
        return await asyncio.gather(*tasks)


def fetch_geojson_features(requests: List[ExternalAPIRequest]) -> List[LayerResponse]:
    """ fetch_geojson_features collects features from one or more sources and aggregates
    them into a list of LayerResponse results, each containing the geojson response
    body and a status code """
    return asyncio.run(fetch_all(requests))


def get_display_catalogue(db: Session, display_data_names: List[str]):
    q = db.query(DisplayCatalogue).options(joinedload(DisplayCatalogue.wms_catalogue),
                                           joinedload(
                                               DisplayCatalogue.api_catalogue),
                                           joinedload(DisplayCatalogue.vector_catalogue))\
        .filter(DisplayCatalogue.display_data_name.in_(display_data_names))\
        .all()
    # [logger.info(vars(x)) for x in q]
    return q


def get_layer_feature(db: Session, layer_class, feature_id):

    q = db.query(layer_class).filter(
        layer_class.primary_key() == feature_id).one_or_none()
    geom = layer_class.get_geom_column(db)
    if q is None:
        raise HTTPException(
            status_code=404, detail="Feature information not found.")

    return layer_class.get_as_feature(q, geom)


def feature_search(db: Session, layers, search_area):
    """ finds features in a given search area """

    albers_search_area = transform(transform_4326_3005, search_area)

    # Compare requested layers against layers we keep track of.  The valid WMS layers and their
    # respective WMS endpoints will come from our metadata.
    catalogue = get_display_catalogue(db, layers)

    wms_requests = []

    # keep track of layers that are processed.
    # this enables us to use internal data, marking it as done, but fall
    # back on making a WMS request if needed.
    processed_layers = {}

    # Internal datasets:
    # Gather valid internal sources that were included in the request's `layers` param
    internal_data = []
    # logger.info([c.display_data_name for c in catalogue])
    for item in catalogue:
        if item.display_data_name in API_DATASOURCES:
            internal_data.append(item)
            processed_layers[item.display_data_name] = True

    # Create a ExternalAPIRequest object with all the values we need to make WMS requests for each of the
    # WMS layers that we have metadata for.
    for item in catalogue:
        if item.display_data_name in processed_layers:
            continue

        if item.display_data_name in EXTERNAL_API_REQUESTS:

            # use the helper function in EXTERNAL_API_REQUESTS (if available)
            # to return an ExternalAPIRequest directly.
            wms_requests.append(
                EXTERNAL_API_REQUESTS[item.display_data_name](search_area)
            )
            logger.info('added external API request!')
            continue

        # if we don't have a direct API to access, fall back on WMS.
        if item.display_data_name in DATABC_LAYER_IDS or item.wms_catalogue_id is not None:
            query = WMSGetFeatureQuery(
                typeName=DATABC_LAYER_IDS.get(
                    item.display_data_name, None) or item.wms_catalogue.wms_name,
                cql_filter=f"""
                    INTERSECTS({DATABC_GEOMETRY_FIELD.get(item.display_data_name, 'GEOMETRY')}, {
                               albers_search_area.wkt})
                """
            )
            req = ExternalAPIRequest(
                url=f"https://openmaps.gov.bc.ca/geo/pub/wfs?",
                layer=item.display_data_name,
                q=query
            )
            wms_requests.append(req)

    # Go and fetch features for each of the WMS endpoints we need, and make a FeatureCollection
    # out of all the aggregated features.
    feature_list = fetch_geojson_features(wms_requests)

    # Loop through all datasets that are available internally.
    # We will make use of the data access function registered in API_DATASOURCES
    # to avoid making api calls to our own web server.
    for dataset in internal_data:
        display_data_name = dataset.display_data_name

        # use function registered for this source
        # API_DATASOURCES is a map of layer names to a module or class;
        # Use it here to look up a module/class that has a `get_as_geojson`
        # function for looking up data in a layer. This function will return geojson
        # features in the bounding box for each layer, which we will package up
        # into a response.
        objects = API_DATASOURCES[display_data_name].get_as_geojson(
            db, search_area)

        feat_layer = LayerResponse(
            layer=display_data_name,
            status=200,
            geojson=objects
        )

        feature_list.append(feat_layer)

    return feature_list


def databc_feature_search(layer, search_area=None, cql_filter=None) -> FeatureCollection:
    """ looks up features from `layer` in `search_area`.
        Layer should be in DATABC_LAYER_IDS.
        Search area should be SRID 4326.
    """
    if not search_area and not cql_filter:
        raise HTTPException(
            status_code=400, detail="Must provide either search_area or cql_filter")

    if search_area and cql_filter:
        raise HTTPException(
            status_code=400, detail="Must provide either search_area or cql_filter, not both")

    if search_area:
        search_area = transform(transform_4326_3005, search_area)
        cql_filter = f"""
                INTERSECTS({DATABC_GEOMETRY_FIELD.get(
                    layer, 'GEOMETRY')}, {search_area.wkt})
            """

    query = WMSGetFeatureQuery(
        typeName=DATABC_LAYER_IDS.get(
            layer, layer),
        cql_filter=cql_filter
    )

    req = ExternalAPIRequest(
        url=f"https://openmaps.gov.bc.ca/geo/pub/wfs?",
        layer=layer,
        q=query
    )
    feature_list = fetch_geojson_features([req])

    if not len(feature_list):
        raise HTTPException(status_code=404, detail="Dataset not found")

    return feature_list[0].geojson
