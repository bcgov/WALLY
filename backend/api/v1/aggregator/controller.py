"""
Functions for aggregating data from web requests and database records
"""
import logging
import asyncio
import json
from typing import List
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from aiohttp import ClientSession, ClientResponse
from sqlalchemy.orm import Session
from typing import List
import logging
from api.v1.catalogue.db_models import DisplayCatalogue
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from api.v1.aggregator.schema import ExternalAPIRequest, LayerResponse

logger = logging.getLogger("aggregator")


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

    # check if data looks like a geojson FeatureCollection, and if so,
    # make proper Features out of all the objects
    if (res.status == 200 and
        hasattr(data, "get") and
        "type" in data and
        data.get("type") == "FeatureCollection" and
            "features" in data):
        for feat in data["features"]:
            features.append(Feature(**feat))

    # if we didn't recognize a geojson response, check if a formatter was supplied to create geojson.
    elif res.status == 200 and req.formatter and len(data) > 0:
        features = req.formatter(data)['features']

    if data.get('next', None) and data.get('results', None):
        next_url = data['next']

    return features, res.status, next_url


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
            results, status, next_url = await asyncio.ensure_future(parse_result(response, req))
            features.extend(results)
            # preserve error statuses even if a later request returns 200 OK
            if layer_resp.status < status:
                layer_resp.status = status

        # if pagination is disabled, stop here.
        if not req.paginate:
            break

    layer_resp.geojson = FeatureCollection(features=features)
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
